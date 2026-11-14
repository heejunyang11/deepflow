# -*- coding: utf-8 -*-
"""
分子を立体で描いて回すための共通部品。

元素シリーズでは分子の図が何度も出てくる（#2 炭素の図1・図2・図3、
このあとの #3 酸素、#4 窒素……）。同じ描き方を毎回書き直すと必ずずれるので、
ここに一本化する。

方針は efig.py と同じ。
  ・位置は Python が実測値から計算して HTML に焼き込む
    → JavaScript が動かなくても、静止画として図が成立する
  ・見た目は SVG のグラデーションだけで作る（外部依存ゼロ）
  ・JavaScript は「毎コマ回して投影し直す」ためだけに使う

使い方:
    g = emol.Group('efoo', scale=42)
    g.add(emol.Mol('co2', atoms, bonds))
    html = g.defs() + g.svg('co2') + ... + g.spin_js('efoo1')

大事な約束:
  ・枠（viewBox）は Group が持つ全分子の「一周ぶんの外接矩形」から決める。
    したがって同じ Group に入れた分子は、すべて同じ縮尺で描かれる。
    縮尺をそろえたくない分子は、別の Group に入れること。
  ・玉の大きさは共有結合半径そのまま。Cordero et al. (2008) Dalton Trans.
    2832-2838 による（炭素は sp3 の値）。
"""
import json
import math

# 共有結合半径（Å）。Cordero et al. (2008)。
RAD = {
    'H': 0.31, 'He': 0.28, 'C': 0.76, 'N': 0.71, 'O': 0.66, 'Si': 1.11,
    'Al': 1.21,
    # #7 で追加。イオンとして描くので、Na⁺ と Cl⁻ だけはイオン半径（Shannon 1976、
    # 6 配位）を使う。共有結合半径（Na 1.66、Cl 1.02）ではない。図の出典行にそう書くこと。
    'Na': 1.02, 'Cl': 1.81,
}

# CPK 配色（H 白・C 黒・N 青・O 赤・Si 砂色）を、紙色の地に載せても
# 浮かないよう暖色寄りに振り、明度を落としたもの。
# 地（#FDFAF3）に対するコントラストは check_contrast() で検算する。
COLOR = {
    'H':  '#E6DCC8',
    'He': '#A8730F',
    'C':  '#3A342E',
    'N':  '#2A5E9E',
    'O':  '#B8401B',
    'Si': '#8A6B36',
    'Al': '#5B6F80',   # 金属の銀灰。冷たい色で、Si の砂色と見分ける
    'Na': '#7B4FA0',   # CPK の紫を暗く。#7 の図すべてでナトリウムの色
    'Cl': '#2E8B7A',   # CPK の緑を青緑寄りに
}
# 淡い玉は塗りではコントラストが足りないので、輪郭線で受け持たせる
EDGE_FOR_CONTRAST = {'H': '#8A785A'}

SHADOW = '#1A140C'      # 影に混ぜる暖かい黒。純黒だと紙の上で沈む


# ---------------------------------------------------------------- 色

def _hex(t):
    return '#%02X%02X%02X' % tuple(max(0, min(255, int(round(v)))) for v in t)


def mix(a, b, t):
    pa = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    pb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return _hex([x + (y - x) * t for x, y in zip(pa, pb)])


def lighten(c, t):
    return mix(c, '#FFFFFF', t)


def darken(c, t):
    return mix(c, SHADOW, t)


def _lum(h):
    def ch(c):
        c /= 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (int(h[i:i + 2], 16) for i in (1, 3, 5))
    return .2126 * ch(r) + .7152 * ch(g) + .0722 * ch(b)


def contrast(a, b='#FDFAF3'):
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + .05) / (lo + .05)


def check_contrast(elems, floor=3.0, quiet=False):
    """図形なので下限は 3.0（WCAG の非テキスト要素の基準）。"""
    for e in sorted(set(elems)):
        c = contrast(EDGE_FOR_CONTRAST.get(e, COLOR[e]))
        if not quiet:
            print('  %-3s %.2f:1 %s' % (e, c, 'OK' if c >= floor else '*** 低い ***'))
        assert c >= floor, '%s のコントラストが %.1f を下回っている' % (e, floor)


# ---------------------------------------------------------------- 幾何

def tetra_axis_angle(inter_deg):
    """3 本が等価なとき、対称軸から測った 1 本の傾き（度）。

    軸から角 a で 3 本を 120 度おきに開くと、2 本のなす角 b は
      cos b = sin^2 a * cos120 + cos^2 a = 1.5 cos^2 a - 0.5
    これを b について解く。アンモニアの 106.67 度から 67.85 度が出る。
    """
    c = (math.cos(math.radians(inter_deg)) + 0.5) / 1.5
    return math.degrees(math.acos(math.sqrt(c)))


def bent(inter_deg):
    """折れ曲がり 2 本。回転前は画面の面内に置く。"""
    h = math.radians(inter_deg / 2.0)
    return [(math.sin(h), math.cos(h), 0.0), (-math.sin(h), math.cos(h), 0.0)]


def linear():
    """直線 2 本。"""
    return [(1.0, 0.0, 0.0), (-1.0, 0.0, 0.0)]


def pyramid(inter_deg, phis=(90, 210, 330)):
    """三角錐 3 本。非共有電子対を上に向け、まわりの原子を下へ開く。"""
    a = math.radians(tetra_axis_angle(inter_deg))
    return [(math.sin(a) * math.cos(math.radians(f)), -math.cos(a),
             math.sin(a) * math.sin(math.radians(f))) for f in phis]


def tetra(phis=(90, 210, 330)):
    """正四面体 4 本。1 本を真上に、残り 3 本を 109.471 度で下へ。"""
    y = -1.0 / 3.0
    r = math.sqrt(1.0 - y * y)
    return [(0.0, 1.0, 0.0)] + [
        (r * math.cos(math.radians(f)), y, r * math.sin(math.radians(f)))
        for f in phis]


def dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def angle(a, b, c):
    """a-b-c のなす角（度）。b が頂点。"""
    u = [x - y for x, y in zip(a, b)]
    v = [x - y for x, y in zip(c, b)]
    nu = math.sqrt(sum(x * x for x in u)) or 1.0
    nv = math.sqrt(sum(x * x for x in v)) or 1.0
    d = sum(x * y for x, y in zip(u, v)) / (nu * nv)
    return math.degrees(math.acos(max(-1.0, min(1.0, d))))


# ---------------------------------------------------------------- 分子

class Mol(object):
    """原子と結合の集まり。座標は Å、原点は回転の軸が通る点。

    atoms: [(位置3つ, 元素記号)] または [(位置, 元素記号, ghost)]
           ghost=True の原子は「この先も続く」ことを示す薄い玉になる。
    bonds: [(i, j)] 原子の番号の組。
    """

    def __init__(self, key, atoms, bonds, label='', vib=None, vib_sec=1.7):
        """vib を渡すと、その向きへ原子が行き来する（基準振動）。

        vib は原子ごとの変位ベクトル（Å）。実際の振動は毎秒 10^13 回なので
        速さは再現しようがない。ここで見せたいのは「どう動くか」であって
        「どれだけ速いか」ではないので、目で追える速さまで落としてある。
        振れ幅も実際よりずっと大きい（そう書き添えること）。
        """
        self.key = key
        self.label = label or key
        self.vib_sec = float(vib_sec)
        self.atoms = [(tuple(float(c) for c in a[0]), a[1],
                       bool(a[2]) if len(a) > 2 else False) for a in atoms]
        self.vib = ([tuple(float(c) for c in v) for v in vib] if vib
                    else [(0.0, 0.0, 0.0)] * len(self.atoms))
        assert len(self.vib) == len(self.atoms), '%s: 変位の数が原子と合わない' % key
        self.bonds = [(int(i), int(j)) for i, j in bonds]
        for i, j in self.bonds:
            assert 0 <= i < len(self.atoms) and 0 <= j < len(self.atoms), \
                '%s: 結合が存在しない原子を指している' % key

    def elems(self):
        return [e for _p, e, _g in self.atoms]

    def recenter(self):
        """全原子の重心を原点へ移す。回転の軸をここに通す。"""
        n = float(len(self.atoms))
        c = [sum(p[k] for p, _e, _g in self.atoms) / n for k in range(3)]
        self.atoms = [(tuple(p[k] - c[k] for k in range(3)), e, g)
                      for p, e, g in self.atoms]
        return self

    def at(self, phase=0.0):
        """位相 phase（-1〜+1）での原子の位置。振動なしならそのまま返す。"""
        return [tuple(p[k] + v[k] * phase for k in range(3))
                for (p, _e, _g), v in zip(self.atoms, self.vib)]


def hub(center, length, dirs, outer='H'):
    """中心 1 個＋そのまわり。原点は中心の原子。"""
    atoms = [((0.0, 0.0, 0.0), center)]
    atoms += [(tuple(c * length for c in v), outer) for v in dirs]
    return atoms, [(0, i + 1) for i in range(len(dirs))]


def pair(elem, length):
    """同じ原子 2 個。原点はその中点。"""
    h = length / 2.0
    return ([((-h, 0.0, 0.0), elem), ((h, 0.0, 0.0), elem)], [(0, 1)])


# ---------------------------------------------------------------- 描画

class Group(object):
    """同じ縮尺・同じ枠で描く分子のまとまり。"""

    def __init__(self, prefix, scale=42.0, ball=0.72, pad=3.0,
                 tilt=-13.0, bond_w=7.6, spin_sec=19.0, sweep=3,
                 ghost_op=0.42, ghost_r=0.72, auto_spin=True):
        # ghost_op / ghost_r は「この先も続く」を示す薄い玉の濃さと大きさ。
        # 縁の原子が多い図（黒鉛など）では 0.42 だと figure 全体が
        # 薄く見えてしまうので、図ごとに上げられるようにしてある。
        self.ghost_op = float(ghost_op)
        self.ghost_r = float(ghost_r)
        # 振動を見せる図では、回しながら震わせると何が起きているか読めない。
        # そういう図は auto_spin=False にして、回すのは読者の手にゆだねる。
        self.auto_spin = bool(auto_spin)
        self.p = prefix
        self.scale = float(scale)
        self.ball = float(ball)
        self.pad = float(pad)
        self.tilt = float(tilt)
        self.bond_w = float(bond_w)
        self.spin_sec = float(spin_sec)
        self.sweep = range(0, 360, sweep)
        self.mols = []
        self._vb = None
        self._box = {}

    # -------- 座標

    def add(self, mol):
        self.mols.append(mol)
        self._vb = None
        return mol

    def spun(self, p, deg):
        """縦軸まわりに deg 回してから、見下ろす角度で傾ける。"""
        ay, ax = math.radians(deg), math.radians(self.tilt)
        x, y, z = p
        x, z = (x * math.cos(ay) + z * math.sin(ay),
                -x * math.sin(ay) + z * math.cos(ay))
        y, z = (y * math.cos(ax) - z * math.sin(ax),
                y * math.sin(ax) + z * math.cos(ax))
        return x, y, z

    def proj(self, p, deg):
        """3 次元の位置（Å）→ 画面のずれ（px）と奥行き（Å）。"""
        x, y, z = self.spun(p, deg)
        return x * self.scale, -y * self.scale, z

    def radius(self, elem, z, ghost=False):
        r = RAD[elem] * self.scale * self.ball * (1.0 + 0.11 * z)
        return r * (self.ghost_r if ghost else 1.0)

    @staticmethod
    def fade(z, k):
        """手前は沈ませず、奥へ下がったぶんだけ薄くする。"""
        return 1.0 - k * min(1.0, max(0.0, -z))

    def _measure(self):
        """一周のあいだに一度でも占める範囲から、全分子共通の枠を決める。

        回転の途中でだけはみ出す、という事故を防ぐため一周ぶん試す。
        """
        need = 0.0
        box = {}
        for m in self.mols:
            x0 = y0 = 1e9
            x1 = y1 = -1e9
            for deg in self.sweep:
                # 振動の両端（位相 -1 と +1）も含めて測る。
                # 振れた瞬間だけ枠からはみ出す、という事故を防ぐため。
                for phase in (-1.0, 0.0, 1.0):
                    for (p, (_p0, e, g)) in zip(m.at(phase), m.atoms):
                        x, y, z = self.proj(p, deg)
                        r = self.radius(e, z, g)
                        x0, x1 = min(x0, x - r), max(x1, x + r)
                        y0, y1 = min(y0, y - r), max(y1, y + r)
            box[m.key] = (x0, x1, y0, y1)
            need = max(need, x1 - x0, y1 - y0)
        self._vb = need + 2 * self.pad
        self._box = box

    @property
    def vb(self):
        if self._vb is None:
            self._measure()
        return self._vb

    def center(self, key):
        """分子ごとの平行移動。回転しても動かない固定値（揺れを防ぐ）。"""
        if self._vb is None:
            self._measure()
        x0, x1, y0, y1 = self._box[key]
        c = self.vb / 2.0
        return c - (x0 + x1) / 2.0, c - (y0 + y1) / 2.0

    # -------- SVG

    def defs(self):
        """使う元素ぶんのグラデーション。ページに一度だけ置く。

        球は「左上から光が当たった玉」を放射グラデーションで作る。
        中心を左上へずらし、明→素の色→暗の順に落とすと球に見える。
        棒は長方形に「縁が暗く中央が明るい」直線グラデーションを掛けて
        円柱に見せる（本物の円柱の陰影も、断面方向に同じ形をしている）。
        """
        used = sorted(set(e for m in self.mols for e in m.elems()))
        o = ['<svg class="%s-defs" width="0" height="0" aria-hidden="true">'
             '<defs>' % self.p]
        for e in used:
            b = COLOR[e]
            o.append(
                '<radialGradient id="%s-b-%s" cx="34%%" cy="26%%" r="76%%">'
                '<stop offset="0%%" stop-color="%s"/>'
                '<stop offset="32%%" stop-color="%s"/>'
                '<stop offset="72%%" stop-color="%s"/>'
                '<stop offset="100%%" stop-color="%s"/></radialGradient>'
                % (self.p, e, lighten(b, .60), lighten(b, .21), b,
                   darken(b, .46)))
        o.append('<radialGradient id="%s-hl" cx="50%%" cy="50%%" r="50%%">'
                 '<stop offset="0%%" stop-color="#FFFFFF" stop-opacity=".95"/>'
                 '<stop offset="55%%" stop-color="#FFFFFF" stop-opacity=".38"/>'
                 '<stop offset="100%%" stop-color="#FFFFFF" stop-opacity="0"/>'
                 '</radialGradient>' % self.p)
        o.append('<linearGradient id="%s-cyl" x1="0" y1="0" x2="0" y2="1">'
                 '<stop offset="0%%" stop-color="#8B7F6B"/>'
                 '<stop offset="16%%" stop-color="#C6BAA3"/>'
                 '<stop offset="38%%" stop-color="#E4DBC9"/>'
                 '<stop offset="62%%" stop-color="#C2B49B"/>'
                 '<stop offset="100%%" stop-color="#7E7259"/></linearGradient>'
                 % self.p)
        o.append('</defs></svg>')
        return ''.join(o)

    def _ball(self, i, e, x, y, r, op):
        hx, hy = x - r * .33, y - r * .38
        return ('<g data-a="%d">'
                '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="url(#%s-b-%s)" '
                'stroke="%s" stroke-opacity=".38" stroke-width="%.2f" '
                'opacity="%.3f"/>'
                '<ellipse cx="%.2f" cy="%.2f" rx="%.2f" ry="%.2f" '
                'fill="url(#%s-hl)" opacity="%.3f" '
                'transform="rotate(-24 %.2f %.2f)"/></g>'
                % (i, x, y, r, self.p, e, darken(COLOR[e], .58),
                   max(.6, r * .045), op,
                   hx, hy, r * .34, r * .24, self.p, .92 * op, hx, hy))

    def _stick(self, k, x1, y1, x2, y2, w, op):
        L = math.hypot(x2 - x1, y2 - y1)
        a = math.degrees(math.atan2(y2 - y1, x2 - x1))
        return ('<g data-s="%d" transform="translate(%.2f %.2f) rotate(%.2f)">'
                '<rect x="0" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" '
                'fill="url(#%s-cyl)" opacity="%.3f"/>'
                '<rect x="0" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" '
                'fill="none" stroke="#6F6450" stroke-opacity=".26" '
                'stroke-width=".7"/></g>'
                % (k, x1, y1, a, -w / 2.0, L, w, w * .34, self.p, op,
                   -w / 2.0, L, w, w * .34))

    def _bond_ends(self, m, i, j, deg):
        """玉の表面から玉の表面へ。手前を向いた棒は短く写るが、それが正しい。"""
        pi, pj = m.atoms[i][0], m.atoms[j][0]
        d = [b - a for a, b in zip(pi, pj)]
        n = math.sqrt(sum(c * c for c in d)) or 1.0
        u = [c / n for c in d]
        ri = RAD[m.atoms[i][1]] * self.ball * (self.ghost_r if m.atoms[i][2] else 1.0)
        rj = RAD[m.atoms[j][1]] * self.ball * (self.ghost_r if m.atoms[j][2] else 1.0)
        s = self.proj([a + c * ri for a, c in zip(pi, u)], deg)
        e = self.proj([a - c * rj for a, c in zip(pj, u)], deg)
        return s, e

    def svg(self, key, deg=0.0, extra_class=''):
        """回転角 deg での 1 分子ぶん。奥のものから順に並べる。"""
        m = [x for x in self.mols if x.key == key][0]
        items = []
        for i, (p, (_p0, e, g)) in enumerate(zip(m.at(0.0), m.atoms)):
            x, y, z = self.proj(p, deg)
            op = self.fade(z, .18) * (self.ghost_op if g else 1.0)
            items.append((z, self._ball(i, e, x, y, self.radius(e, z, g), op)))
        for k, (i, j) in enumerate(m.bonds):
            s, e = self._bond_ends(m, i, j, deg)
            z = (s[2] + e[2]) / 2.0
            gh = m.atoms[i][2] or m.atoms[j][2]
            items.append((z, self._stick(k, s[0], s[1], e[0], e[1],
                                         self.bond_w * (1.0 + 0.10 * z),
                                         self.fade(z, .22)
                                         * (self.ghost_op if gh else 1.0))))
        items.sort(key=lambda t: t[0])
        dx, dy = self.center(key)
        return ('<svg viewBox="0 0 %.1f %.1f" class="%s" role="img" '
                'aria-label="%s">'
                '<g data-scene="1" transform="translate(%.2f %.2f)">%s</g>'
                '</svg>'
                % (self.vb, self.vb, extra_class, m.label, dx, dy,
                   ''.join(n for _z, n in items)))

    # -------- 動き

    def data(self):
        """JavaScript に渡す寸法と座標。Python と同じ式を使わせる。"""
        return {
            'scale': self.scale, 'tilt': self.tilt, 'ball': self.ball,
            'bw': self.bond_w, 'sec': self.spin_sec, 'rad': RAD,
            'gop': self.ghost_op, 'gr': self.ghost_r,
            'spin': 1 if self.auto_spin else 0,
            'mol': [{'k': m.key, 'vs': m.vib_sec,
                     'a': [{'p': [round(c, 5) for c in p], 'e': e,
                            'g': 1 if g else 0,
                            'v': [round(c, 5) for c in v]}
                           for (p, e, g), v in zip(m.atoms, m.vib)],
                     'b': [list(t) for t in m.bonds]} for m in self.mols],
        }

    def spin_js(self, cid, svg_selector=None):
        sel = svg_selector or ('#%s svg[viewBox]' % cid)
        return (_SPIN_JS
                .replace('@@DATA@@', json.dumps(self.data(), separators=(',', ':')))
                .replace('@@CID@@', cid)
                .replace('@@SEL@@', sel))


_SPIN_JS = """
<script>
(function(){
  var D = @@DATA@@;
  var root = document.getElementById('@@CID@@');
  if(!root || !window.requestAnimationFrame) return;
  var svgs = root.querySelectorAll('@@SEL@@');
  if(!svgs.length) return;

  var T = D.tilt * Math.PI / 180, cosT = Math.cos(T), sinT = Math.sin(T);
  function spun(p, a){
    var ca = Math.cos(a), sa = Math.sin(a);
    var x = p[0]*ca + p[2]*sa, z = -p[0]*sa + p[2]*ca, y = p[1];
    return [x*D.scale, -(y*cosT - z*sinT)*D.scale, y*sinT + z*cosT];
  }
  function clamp01(v){ return v < 0 ? 0 : (v > 1 ? 1 : v); }
  // 手前のものは沈ませない。奥へ下がったぶんだけ薄くする
  function fade(z, k){ return 1 - k*clamp01(-z); }
  function rad(e, z, g){
    return D.rad[e]*D.scale*D.ball*(1 + 0.11*z)*(g ? D.gr : 1);
  }
  // 節点は data-a / data-s の番号で拾う。並び順は奥行きで毎回入れ替わるので、
  // 文書に現れる順を当てにしてはいけない。
  function byIndex(g, attr){
    var out = [], ns = g.querySelectorAll('['+attr+']');
    for(var k=0;k<ns.length;k++) out[+ns[k].getAttribute(attr)] = ns[k];
    return out;
  }

  // 速さを分子ごとに少しずらす。全部そろって真横を向くと、
  // 一瞬だけ全部が平たく見えてしまうため。
  var SPEED = [1.00, 1.07, 0.93, 1.12, 0.88, 1.04];
  var mols = [];
  for(var i=0;i<svgs.length && i<D.mol.length;i++){
    var g = svgs[i].querySelector('[data-scene]');
    if(!g) continue;
    mols.push({def: D.mol[i], g: g, svg: svgs[i],
      speed: SPEED[i % SPEED.length], spin: 0, ph: 0, drag: null, order: '',
      atoms: byIndex(g, 'data-a'), sticks: byIndex(g, 'data-s')});
  }
  if(!mols.length) return;

  function draw(m){
    var pos = [], k, kids = [];
    // 振動の位相。sin で行って戻る。ph=0 なら焼き込んだ静止画と同じ姿になる
    var ph = m.def.vs ? Math.sin(m.ph) : 0;
    function at(a){
      return [a.p[0] + a.v[0]*ph, a.p[1] + a.v[1]*ph, a.p[2] + a.v[2]*ph];
    }
    for(k=0;k<m.def.a.length;k++) pos.push(spun(at(m.def.a[k]), m.spin));

    for(k=0;k<m.atoms.length;k++){
      var A = m.def.a[k], P0 = pos[k], r = rad(A.e, P0[2], A.g);
      var op = fade(P0[2], 0.18) * (A.g ? D.gop : 1);
      var c = m.atoms[k].firstChild, h = c.nextSibling;
      c.setAttribute('cx', P0[0].toFixed(2));
      c.setAttribute('cy', P0[1].toFixed(2));
      c.setAttribute('r',  r.toFixed(2));
      c.setAttribute('stroke-width', Math.max(0.6, r*0.045).toFixed(2));
      c.setAttribute('opacity', op.toFixed(3));
      var hx = P0[0] - r*0.33, hy = P0[1] - r*0.38;
      h.setAttribute('cx', hx.toFixed(2));
      h.setAttribute('cy', hy.toFixed(2));
      h.setAttribute('rx', (r*0.34).toFixed(2));
      h.setAttribute('ry', (r*0.24).toFixed(2));
      h.setAttribute('opacity', (0.92*op).toFixed(3));
      h.setAttribute('transform','rotate(-24 '+hx.toFixed(2)+' '+hy.toFixed(2)+')');
      kids.push([P0[2], m.atoms[k]]);
    }

    for(k=0;k<m.sticks.length;k++){
      var b = m.def.b[k], ai = m.def.a[b[0]], aj = m.def.a[b[1]];
      var pi = at(ai), pj = at(aj);
      var d = [pj[0]-pi[0], pj[1]-pi[1], pj[2]-pi[2]];
      var n = Math.sqrt(d[0]*d[0]+d[1]*d[1]+d[2]*d[2]) || 1;
      var ri = D.rad[ai.e]*D.ball*(ai.g ? D.gr : 1);
      var rj = D.rad[aj.e]*D.ball*(aj.g ? D.gr : 1);
      var s = spun([pi[0]+d[0]/n*ri, pi[1]+d[1]/n*ri, pi[2]+d[2]/n*ri], m.spin);
      var t = spun([pj[0]-d[0]/n*rj, pj[1]-d[1]/n*rj, pj[2]-d[2]/n*rj], m.spin);
      var z = (s[2]+t[2])/2, w = D.bw*(1 + 0.10*z);
      var L = Math.sqrt((t[0]-s[0])*(t[0]-s[0]) + (t[1]-s[1])*(t[1]-s[1]));
      var a = Math.atan2(t[1]-s[1], t[0]-s[0])*180/Math.PI;
      m.sticks[k].setAttribute('transform',
        'translate('+s[0].toFixed(2)+' '+s[1].toFixed(2)+') rotate('+a.toFixed(2)+')');
      var r1 = m.sticks[k].firstChild, r2 = r1.nextSibling;
      [r1, r2].forEach(function(rc){
        rc.setAttribute('y', (-w/2).toFixed(2));
        rc.setAttribute('width',  L.toFixed(2));
        rc.setAttribute('height', w.toFixed(2));
        rc.setAttribute('rx', (w*0.34).toFixed(2));
      });
      r1.setAttribute('opacity',
        (fade(z, 0.22) * ((ai.g || aj.g) ? D.gop : 1)).toFixed(3));
      kids.push([z, m.sticks[k]]);
    }

    // 奥のものから並べ直す。順番が変わったときだけ触る
    kids.sort(function(p, q){ return p[0] - q[0]; });
    var key = kids.map(function(p){
      return p[1].getAttribute('data-a') !== null
        ? 'a'+p[1].getAttribute('data-a') : 's'+p[1].getAttribute('data-s');
    }).join(',');
    if(key !== m.order){
      m.order = key;
      for(k=0;k<kids.length;k++) m.g.appendChild(kids[k][1]);
    }
  }

  // つかんで回せるようにする。指でも動くが、縦のスクロールは邪魔しない
  mols.forEach(function(m){
    m.svg.style.touchAction = 'pan-y';
    m.svg.style.cursor = 'grab';
    m.svg.addEventListener('pointerdown', function(ev){
      m.drag = {x: ev.clientX, spin: m.spin};
      m.svg.style.cursor = 'grabbing';
      if(m.svg.setPointerCapture) m.svg.setPointerCapture(ev.pointerId);
    });
    m.svg.addEventListener('pointermove', function(ev){
      if(!m.drag) return;
      m.spin = m.drag.spin + (ev.clientX - m.drag.x) * 0.014;
      draw(m);
    });
    function release(){
      if(m.drag){ m.drag = null; m.svg.style.cursor = 'grab'; }
    }
    m.svg.addEventListener('pointerup', release);
    m.svg.addEventListener('pointercancel', release);
    window.addEventListener('pointerup', release);   // 捕捉に失敗したとき用
  });

  // 動きを減らす設定なら、自分で回す以外は動かさない
  if(window.matchMedia &&
     window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var visible = true;
  if(window.IntersectionObserver){
    new IntersectionObserver(function(es){ visible = es[0].isIntersecting; },
      {rootMargin: '80px'}).observe(root);
  }
  var last = 0, prev = 0;
  function tick(now){
    requestAnimationFrame(tick);
    if(now - last < 33) return;              // 毎秒 30 コマで足りる
    var dt = prev ? Math.min(0.1, (now - prev)/1000) : 0;
    last = now; prev = now;
    if(!visible) return;
    var step = 2*Math.PI * dt / D.sec;
    for(var i=0;i<mols.length;i++){
      var m = mols[i];
      if(D.spin && !m.drag) m.spin += step * m.speed;
      if(m.def.vs) m.ph += 2*Math.PI * dt / m.def.vs;
      if(D.spin || m.def.vs) draw(m);
    }
  }
  requestAnimationFrame(tick);
})();
</script>
"""
