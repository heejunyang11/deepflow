# -*- coding: utf-8 -*-
"""
元素 #7 ナトリウム / 図3 : 水に囲まれたナトリウムイオン（と塩化物イオン）。

塩が水に溶けると、Na⁺ と Cl⁻ はそれぞれ水分子に取り囲まれて離れていく。
  ・Na⁺ のまわり : 水は「酸素の側」を内側に向ける（酸素の側が少しマイナス）
  ・Cl⁻ のまわり : 水は「水素の側」を内側に向ける（水素の側が少しプラス）
向きが逆になることを、2つの立体を並べて見せる。

配置は、もっとも近い水 6 個を八面体の頂点に置いた模式。実際の水は絶えず
入れ替わっていて、数も 6 前後でゆらぐ（図の出典行にそう書く）。
距離は Ohtaki & Radnai (1993) の総説の代表値:
  Na–O 2.43 Å、Cl–O 3.16 Å。水の形は O–H 0.958 Å、H–O–H 104.48°（#2 図1 と同じ）。
Na⁺・Cl⁻ の玉はイオン半径（Shannon 1976）、水の玉は共有結合半径（emol の約束）。

出力: _fig3_hydration.qmd
"""
import math

import efig
import emol

P, CID = 'nahyd', 'nahyd1'

G = emol.Group(P, scale=23.0, spin_sec=24.0)

R_NAO, R_CLO = 2.43, 3.16
OH, HOH = 0.958, 104.48

def _rot(v, ax, ay):
    """x 軸まわり ax 度、つづいて y 軸まわり ay 度。"""
    x, y, z = v
    a, b = math.radians(ax), math.radians(ay)
    y, z = y * math.cos(a) - z * math.sin(a), y * math.sin(a) + z * math.cos(a)
    x, z = x * math.cos(b) + z * math.sin(b), -x * math.sin(b) + z * math.cos(b)
    return (x, y, z)


# 八面体の頂点。そのままだと水が1個まっすぐ手前に来て、中心のイオンを隠す
# （動かない環境ではそれが唯一の絵になる）。軸を斜めに倒しておく。
DIRS = [_rot(d, 35.0, 40.0) for d in
        [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]]


def _perp(d, k):
    """d に垂直な単位ベクトル。水ごとに向きを変えて、整列しすぎた絵にしない。"""
    a = (0.0, 0.0, 1.0) if abs(d[2]) < 0.9 else (1.0, 0.0, 0.0)
    u = [d[1] * a[2] - d[2] * a[1], d[2] * a[0] - d[0] * a[2], d[0] * a[1] - d[1] * a[0]]
    n = math.sqrt(sum(c * c for c in u))
    u = [c / n for c in u]
    v = [d[1] * u[2] - d[2] * u[1], d[2] * u[0] - d[0] * u[2], d[0] * u[1] - d[1] * u[0]]
    t = math.radians(37 * k + 20)
    return [math.cos(t) * a_ + math.sin(t) * b_ for a_, b_ in zip(u, v)]


def add(p, s, c):
    return tuple(a + s * b for a, b in zip(p, c))


def shell(ion):
    atoms = [((0.0, 0.0, 0.0), ion)]
    bonds = []
    half = math.radians(HOH / 2.0)
    for k, d in enumerate(DIRS):
        u = _perp(d, k)
        if ion == 'Na':
            o = add((0, 0, 0), R_NAO, d)
            # 二等分線を外向き（+d）に。水素は外側、酸素が内側を向く
            h1 = add(o, OH, [math.cos(half) * a + math.sin(half) * b for a, b in zip(d, u)])
            h2 = add(o, OH, [math.cos(half) * a - math.sin(half) * b for a, b in zip(d, u)])
        else:
            o = add((0, 0, 0), R_CLO, d)
            # 片方の O–H をまっすぐ Cl⁻ へ向ける
            h1 = add(o, -OH, d)
            th = math.radians(HOH)
            w = [math.cos(th) * (-a) + math.sin(th) * b for a, b in zip(d, u)]
            h2 = add(o, OH, w)
        i = len(atoms)
        atoms += [(o, 'O'), (h1, 'H'), (h2, 'H')]
        bonds += [(i, i + 1), (i, i + 2)]
    return atoms, bonds


NA = G.add(emol.Mol('na', *shell('Na'), label='水分子6個に囲まれたナトリウムイオンの立体模型'))
CL = G.add(emol.Mol('cl', *shell('Cl'), label='水分子6個に囲まれた塩化物イオンの立体模型'))

CELLS = [
    ('na', 'Na⁺', 'ナトリウムイオン', '酸素の側を内側に',
     '<b>ナトリウムイオン（Na⁺）</b>はプラスを帯びています。'
     'まわりの水は、少しマイナスを帯びた<b>酸素の側</b>を内側に向けて集まり、'
     'ぐるりと取り囲みます。囲まれたナトリウムは、水の中で居心地よく落ち着きます。'),
    ('cl', 'Cl⁻', '塩化物イオン', '水素の側を内側に',
     '<b>塩化物イオン（Cl⁻）</b>はマイナスを帯びています。'
     'こちらでは水の向きが逆で、少しプラスを帯びた<b>水素の側</b>を内側に向けます。'
     '塩の結晶がほどけるのは、2種類のイオンがそれぞれこうして水に囲まれていくからです。'),
]

CSS = """
.@@P@@-row{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:18px 8px 6px;}
.@@P@@-cell{display:flex;flex-direction:column;align-items:center;gap:2px;
  padding:10px 6px 12px;border-radius:14px;cursor:default;
  background:rgba(122,96,52,.035);border:1px solid rgba(122,96,52,.13);
  transition:background .18s ease,border-color .18s ease;}
.@@P@@-cell:hover{background:rgba(190,100,10,.07);border-color:rgba(190,100,10,.42);}
.@@P@@-cell svg{display:block;width:100%;max-width:300px;height:auto;
  -webkit-user-select:none;user-select:none;}
.@@P@@-n{font-size:1.5rem;font-weight:800;color:var(--ink);}
.@@P@@-na .@@P@@-n{color:#7B4FA0;} .@@P@@-cl .@@P@@-n{color:#2E8B7A;}
.@@P@@-f{font-size:.95rem;font-weight:700;color:var(--dim);}
.@@P@@-nm{font-size:.82rem;color:var(--faint);}
.@@P@@-lg{display:flex;flex-wrap:wrap;gap:14px;justify-content:center;
  font-size:.8rem;color:var(--dim);margin:2px 8px 0;}
.@@P@@-lg i{display:inline-block;width:11px;height:11px;border-radius:50%;
  margin-right:5px;vertical-align:-1px;}
.@@P@@-defs{position:absolute;width:0;height:0;overflow:hidden;}
@media (max-width:820px){
  .@@P@@-row{gap:7px;margin:14px 0 4px;}
  .@@P@@-n{font-size:1.2rem;} .@@P@@-f{font-size:.85rem;} .@@P@@-nm{font-size:.74rem;}
}
""".replace('@@P@@', P)


def check():
    emol.check_contrast(['Na', 'Cl', 'O', 'H'])
    print('枠 %.1f' % G.vb)
    for m in (NA, CL):
        for i, j in m.bonds:
            assert abs(emol.dist(m.atoms[i][0], m.atoms[j][0]) - OH) < 1e-9
        for i in range(1, len(m.atoms), 3):
            got = emol.angle(m.atoms[i + 1][0], m.atoms[i][0], m.atoms[i + 2][0])
            assert abs(got - HOH) < 1e-6, got
        # 向きの検査: Na⁺ では酸素が水素より内側、Cl⁻ では水素（1個）が酸素より内側
        o_r = [emol.dist((0, 0, 0), m.atoms[i][0]) for i in range(1, len(m.atoms), 3)]
        h_r = [min(emol.dist((0, 0, 0), m.atoms[i + 1][0]),
                   emol.dist((0, 0, 0), m.atoms[i + 2][0])) for i in range(1, len(m.atoms), 3)]
        inward_o = all(o < h for o, h in zip(o_r, h_r))
        print('  %s: イオン–O %.2f Å、最寄りの H %.2f Å、酸素が内側=%s'
              % (m.key, o_r[0], h_r[0], inward_o))
        assert inward_o == (m.key == 'na')


def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, '水に囲まれると、イオンは落ち着きます',
                        '塩が水に溶けたあとの、ナトリウムイオンと塩化物イオンのまわりです。'
                        'どちらもゆっくり回っています。つかんで動かせば自分で回せます。'
                        'カーソルを合わせる（スマホはタップ）と説明が出ます。'),
         G.defs(),
         '<div class="%s-row">' % P]
    for key, sym, name, how, det in CELLS:
        o.append('<div class="%s-cell %s-%s" data-detail="%s">'
                 % (P, P, key, efig.attr(det)))
        o.append(G.svg(key))
        o.append('<span class="%s-n">%s</span>' % (P, sym))
        o.append('<span class="%s-f">%s</span>' % (P, how))
        o.append('<span class="%s-nm">%s</span>' % (P, name))
        o.append('</div>')
    o.append('</div>')
    o.append('<div class="%s-lg">'
             '<span><i style="background:#7B4FA0"></i>ナトリウムイオン</span>'
             '<span><i style="background:#2E8B7A"></i>塩化物イオン</span>'
             '<span><i style="background:#B8401B"></i>酸素</span>'
             '<span><i style="background:#E6DCC8;border:1px solid #8A785A"></i>水素</span>'
             '</div>' % P)
    o.append(efig.close_card(
        P,
        'プラスのナトリウムには水の<b>酸素の側</b>が、マイナスの塩化物イオンには'
        '<b>水素の側</b>が向きます。こうして水に囲まれたイオンは、なかなか水から離れません。'
        '<b>ナトリウムが「いつも溶けている」のは、このためです。</b>',
        'もっとも近い水 6 個を八面体の頂点に置いた模式です。実際の水は絶えず入れ替わり、'
        '数も 6 前後でゆらぎます。距離はナトリウム–酸素 2.43 Å、塩素–酸素 3.16 Å'
        '（Ohtaki &amp; Radnai 1993, <i>Chemical Reviews</i> 93, 1157 の代表値）、'
        '水の形は O–H 0.958 Å・104.48°。イオンの玉はイオン半径（Shannon 1976）、'
        '水の玉は共有結合半径で描いたので、大きさの比べ方は目安です。'
        'イオンと水のあいだに棒が無いのは、手をつないで（共有結合して）いるのではなく、'
        '電気で引き合っているだけだからです。1 Å＝1億分の1センチ。',
        CID))
    o.append(G.spin_js(CID, '.%s-cell svg[viewBox]' % P))
    return '\n'.join(o)


if __name__ == '__main__':
    check()
    efig.save('_fig3_hydration.qmd', build())
