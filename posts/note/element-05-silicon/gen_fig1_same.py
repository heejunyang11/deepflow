# -*- coding: utf-8 -*-
"""
元素 #5 ケイ素 / 図1 : ガラス・砂粒・水晶は、中身が同じ SiO2 である。

第2回（炭素）で「ケイ素は酸素と手を組むと、どこまでも繋がって岩と砂になる」
と書いた。その「どこまでも繋がった網」を、実際に描いて見せる図。

読み取らせたいこと（2 軸で整理する）:
  (1) 並び方の軸 : ガラス＝乱れた網 / 石英＝規則正しい網
  (2) 大きさの軸 : 砂粒＝小さな石英 / 水晶＝大きく育った石英
  -> 「窓ガラスと砂浜は同じ成分。違うのは並び方」
     「砂粒と水晶は同じ並び方。違うのは大きさ」

正確さのための但し書き:
  実際の SiO2 では、ケイ素 1 個に酸素 4 個がついた四面体が頂点を共有して
  三次元に繋がっている。ここで描く 3 配位の平面網は、
  Zachariasen (1932) 以来ガラス構造の説明に使われてきた 2 次元の模式図で、
  結晶とガラスの違いだけを取り出したもの。図の出典行に明記する。

軽さの方針:
  辺は 1 本ずつ <line> を置くとタグが増えて重くなるので、
  まとめて 1 本の <path> にする。既刊の図が 10〜13 KB なので、
  そこに収まる大きさを目安にする。

出力: _fig1_same.qmd
"""
import math
import random

import efig

P, CID = 'sisame', 'sisame1'
W, H = 300, 250          # 各パネルの viewBox


# ---------------------------------------------------------------- 網を作る

def honeycomb(cols, rows, a=1.0):
    """六角形の網（3 配位）。六角形を敷き詰め、頂点を重複除去して作る。

    格子を式で組むより、六角形の頂点を並べて丸めて重ねるほうが確実に
    「全部の辺の長さが等しい 3 配位の網」になる。
    """
    pts, idx, edges = [], {}, set()

    def node(x, y):
        k = (round(x, 4), round(y, 4))
        if k not in idx:
            idx[k] = len(pts)
            pts.append([k[0], k[1]])
        return idx[k]

    for c in range(cols):
        for r in range(rows):
            cx = c * 1.5 * a
            cy = r * math.sqrt(3) * a + (math.sqrt(3) / 2 * a if c % 2 else 0)
            v = [node(cx + a * math.cos(math.radians(60 * k)),
                      cy + a * math.sin(math.radians(60 * k)))
                 for k in range(6)]
            for k in range(6):
                edges.add(tuple(sorted((v[k], v[(k + 1) % 6]))))
    return pts, sorted(edges)


def jitter(pts, amp, seed):
    """点をずらす。ガラスの『乱れた網』を作る。"""
    rnd = random.Random(seed)
    out = []
    for x, y in pts:
        t = rnd.uniform(0, 2 * math.pi)
        d = rnd.uniform(0, amp)
        out.append([x + d * math.cos(t), y + d * math.sin(t)])
    return out


def rewire(pts, edges, n, seed):
    """辺をいくつか繋ぎ替え、5 員環・7 員環を混ぜる。

    ずらすだけでは 6 員環が歪むだけで、
    『環の大きさが揃っていない』というガラスの特徴が出ない。
    """
    rnd = random.Random(seed)
    edges = list(edges)
    have = set(edges)
    for _ in range(n):
        i = rnd.randrange(len(edges))
        a, b = edges[i]
        near = sorted(range(len(pts)),
                      key=lambda k: (pts[k][0] - pts[b][0]) ** 2
                      + (pts[k][1] - pts[b][1]) ** 2)
        for k in near[1:7]:
            e = tuple(sorted((a, k)))
            if k != a and e not in have:
                have.discard(edges[i])
                edges[i] = e
                have.add(e)
                break
    return sorted(set(edges))


def fit(pts, w, h, pad):
    """点群を w×h の枠へ収める。返すのは新しい点群。"""
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    sx = (w - 2 * pad) / max(1e-9, max(xs) - min(xs))
    sy = (h - 2 * pad) / max(1e-9, max(ys) - min(ys))
    s = min(sx, sy)
    ox = pad + (w - 2 * pad - (max(xs) - min(xs)) * s) / 2 - min(xs) * s
    oy = pad + (h - 2 * pad - (max(ys) - min(ys)) * s) / 2 - min(ys) * s
    return [[x * s + ox, y * s + oy] for x, y in pts], s


# ---------------------------------------------------------------- 描く

def net_svg(pts, edges, r_si=4.4, r_o=2.5, oxygen=True, extra=''):
    """網を SVG の断片に。辺はまとめて 1 本の path にする。"""
    d = ''.join('M%.1f %.1fL%.1f %.1f'
                % (pts[a][0], pts[a][1], pts[b][0], pts[b][1])
                for a, b in edges)
    g = ['<path class="%s-bd" d="%s"/>' % (P, d)]
    if oxygen:
        g += ['<circle cx="%.1f" cy="%.1f" r="%.1f" class="%s-o"/>'
              % ((pts[a][0] + pts[b][0]) / 2, (pts[a][1] + pts[b][1]) / 2,
                 r_o, P) for a, b in edges]
    used = sorted({i for e in edges for i in e})
    g += ['<circle cx="%.1f" cy="%.1f" r="%.1f" class="%s-si"/>'
          % (pts[i][0], pts[i][1], r_si, P) for i in used]
    return extra + '\n'.join(g)


def trim(pts, edges, w, h, m=6):
    """枠の外へはみ出した点と、それに繋がる辺を落とす。"""
    keep = {i for i, (x, y) in enumerate(pts)
            if -m <= x <= w + m and -m <= y <= h + m}
    return [(a, b) for a, b in edges if a in keep and b in keep]


def panel_glass():
    pts, edges = honeycomb(4, 3)
    pts = jitter(pts, 0.30, seed=7)
    edges = rewire(pts, edges, 10, seed=11)
    pts, _ = fit(pts, W, H, 20)
    return net_svg(pts, trim(pts, edges, W, H))


def panel_sand():
    """小さな結晶の粒が、向きばらばらに集まっている図。

    粒の中は小さくて酸素まで見えないので、酸素の点は描かない。
    """
    out = []
    grains = [(78, 80, 0.60, -18), (206, 74, 0.50, 26),
              (108, 176, 0.54, 13), (222, 178, 0.42, -33)]
    for gx, gy, s, rot in grains:
        pts, edges = honeycomb(2, 2)
        pts, _ = fit(pts, 120, 120, 6)
        pts = [[(x - 60) * s, (y - 60) * s] for x, y in pts]
        body = net_svg(pts, edges, r_si=3.2, oxygen=False)
        out.append('<g transform="translate(%d,%d) rotate(%d)">%s'
                   '<circle r="%.0f" class="%s-grain"/></g>'
                   % (gx, gy, rot, body, 58 * s, P))
    return '\n'.join(out)


def panel_crystal():
    """大きく育った結晶。網の上に六角柱の外形を重ねる。"""
    pts, edges = honeycomb(4, 3)
    pts, _ = fit(pts, W, H, 22)
    net = net_svg(pts, trim(pts, edges, W, H))
    hexa = ('<path class="%(p)s-hex" d="M150 22 L212 60 L212 182 L150 220 '
            'L88 182 L88 60 Z"/>'
            '<path class="%(p)s-hexl" d="M88 60 L150 92 L212 60 M150 92 '
            'L150 220"/>' % {'p': P})
    return ('<g clip-path="url(#%s-cl)">%s</g>' % (CID, net)) + hexa


CLIP = ('<defs><clipPath id="%s-cl">'
        '<path d="M150 22 L212 60 L212 182 L150 220 L88 182 L88 60 Z"/>'
        '</clipPath></defs>' % CID)


PANELS = [
    ('ガラス', '乱れた網', panel_glass, '',
     '窓ガラスやコップです。<b>網の目の大きさが揃っていません。</b>'
     'どろどろに溶けた状態から急に冷やすと、原子が整列する暇のないまま'
     '固まります。これを<b>アモルファス</b>（非晶質）と呼びます。'
     'ただし窓ガラスは SiO₂ だけではありません。'
     '<b>ソーダと石灰を加えて、約1700℃の融点を1000℃前後まで下げて</b>'
     'あります（SiO₂ は約70%）。加えたナトリウムやカルシウムが、'
     'この網をところどころ切っています。'),
    ('砂粒', '小さな結晶の集まり', panel_sand, '',
     '砂浜の砂です。<b>一粒一粒は、規則正しく並んだ小さな結晶</b>で、'
     'それが向きばらばらに集まっています。'
     '「砂＝ガラスのように乱れたもの」ではありません。'
     '<b>砂粒と水晶を分けているのは、並び方ではなく大きさです。</b>'),
    ('水晶', '大きく育った結晶', panel_crystal, CLIP,
     '同じ並び方のまま、大きく育ったものです。'
     '<b>外から見える六角形は、中の原子の並びがそのまま外に出た形</b>で、'
     '人が削ったものではありません。'
     '透明で不純物の少ないものを、とくに水晶と呼びます。'),
]

CSS = """
.%(p)s{--si:#8A6B36;--ox:#B8401B;--net:#8C8271;--hex:#0F6C8A;}
.%(p)s-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;
  margin:20px 8px 0;}
.%(p)s-p{padding:12px 12px 10px;border-radius:12px;
  background:rgba(122,96,52,.05);border:1px solid rgba(122,96,52,.14);
  cursor:default;transition:background .18s ease,border-color .18s ease;}
.%(p)s-p:hover{background:rgba(122,96,52,.13);
  border-color:rgba(190,100,10,.45);}
.%(p)s-p svg{display:block;width:100%%;height:auto;}
p.%(p)s-t{font-size:1.02rem;font-weight:800;color:var(--ink);margin:0 0 1px;}
p.%(p)s-u{font-size:.8rem;color:var(--faint);margin:0 0 6px;}

.%(p)s-bd{stroke:var(--net);stroke-width:1.7;stroke-linecap:round;fill:none;}
.%(p)s-si{fill:var(--si);}
.%(p)s-o{fill:var(--ox);}
.%(p)s-grain{fill:none;stroke:var(--net);stroke-width:1.1;
  stroke-dasharray:3 3;opacity:.5;}
.%(p)s-hex{fill:rgba(15,108,138,.05);stroke:var(--hex);stroke-width:2;
  stroke-linejoin:round;}
.%(p)s-hexl{fill:none;stroke:var(--hex);stroke-width:1.2;opacity:.5;}

.%(p)s-lg{display:flex;flex-wrap:wrap;gap:16px;margin:16px 8px 0;
  font-size:.85rem;color:var(--dim);align-items:center;}
.%(p)s-lg i{font-style:normal;display:inline-flex;align-items:center;gap:6px;}
.%(p)s-dot{width:11px;height:11px;border-radius:50%%;display:inline-block;}

.%(p)s-ax{display:grid;grid-template-columns:1fr 1fr;gap:10px;
  margin:16px 8px 0;}
.%(p)s-a{padding:13px 15px;border-radius:11px;cursor:default;
  background:rgba(138,107,54,.09);border:1px solid rgba(138,107,54,.26);}
.%(p)s-a b{display:block;font-size:.95rem;font-weight:800;color:var(--si);
  margin-bottom:3px;}
.%(p)s-a s{text-decoration:none;font-size:.86rem;color:var(--dim);
  line-height:1.7;}

@media (max-width:820px){
  .%(p)s-grid{grid-template-columns:1fr;gap:10px;margin:14px 2px 0;}
  p.%(p)s-t{font-size:.95rem;}
  .%(p)s-lg{margin:12px 2px 0;font-size:.78rem;gap:10px;}
  .%(p)s-ax{grid-template-columns:1fr;margin:12px 2px 0;}
}
""" % {'p': P}


def build():
    o = [efig.css(P, CSS),
         efig.open_card(
             P, CID,
             'ガラスも、砂も、水晶も、骨組みは同じ SiO₂ の網です',
             'ケイ素（緑）と酸素（橙）が繋がった網を、模式的に描きました。'
             '3 枚にカーソルを合わせる（スマホはタップ）と説明が出ます。')]

    o.append('<div class="%s-grid">' % P)
    for name, sub, fn, defs, detail in PANELS:
        o.append('<div class="%s-p" data-detail="%s">' % (P, efig.attr(detail)))
        o.append('<p class="%s-t">%s</p><p class="%s-u">%s</p>'
                 % (P, name, P, sub))
        o.append('<svg viewBox="0 0 %d %d" role="img" aria-label="%s">%s%s</svg>'
                 % (W, H, name, defs, fn()))
        o.append('</div>')
    o.append('</div>')

    o.append('<div class="%s-lg">'
             '<i><span class="%s-dot" style="background:var(--si)"></span>'
             'ケイ素 Si</i>'
             '<i><span class="%s-dot" style="background:var(--ox)"></span>'
             '酸素 O</i>'
             '<i>線＝結びつき（Si–O–Si）</i>'
             '<i style="color:var(--hex)">青い枠＝結晶の外形</i></div>'
             % (P, P, P))

    o.append('<div class="%s-ax">' % P)
    o.append('<div class="%s-a" data-detail="%s"><b>並び方の違い</b>'
             '<s>ガラス と 石英。同じ材料でも、<b>整列しているかどうか</b>で'
             '別のものになります。</s></div>'
             % (P, efig.attr(
                 '<b>窓ガラスと砂浜は、成分が同じです。</b>'
                 '違うのは、原子が整列しているかどうかだけ。'
                 '砂を溶かして急に冷やせばガラスになります。')))
    o.append('<div class="%s-a" data-detail="%s"><b>大きさの違い</b>'
             '<s>砂粒 と 水晶。並び方は同じで、<b>結晶がどこまで育ったか</b>'
             'だけが違います。</s></div>'
             % (P, efig.attr(
                 '<b>砂粒は、小さな水晶です。</b>'
                 '同じ規則正しい網でできていて、'
                 '大きく育つ時間と場所があったものが水晶と呼ばれます。')))
    o.append('</div>')

    o.append(efig.close_card(
        P,
        'ガラス・砂・水晶は、いずれも <b>SiO₂ の網</b>を骨組みにしています。'
        '違いは 2 つ。<b>原子が整列しているか（ガラスか、結晶か）</b>と、'
        '<b>結晶がどこまで育ったか（砂粒か、水晶か）</b>。'
        '（窓ガラスはこの網にソーダと石灰を混ぜたもので、SiO₂ は約70%です。）'
        '<a href="/posts/note/element-02-carbon/">第2回</a>で、'
        '炭素は二酸化炭素という小さな粒で終われるのに、'
        'ケイ素は酸素と繋がるとどこまでも続いてしまう、と書きました。'
        '<b>その「どこまでも」が、この網です。</b>',
        'ここに描いたのは、ケイ素 1 個が 3 方向へ手を伸ばす<b>平面の模式図</b>です。'
        '実際の SiO₂ では、ケイ素 1 個を酸素 4 個が囲む四面体が、'
        '頂点を共有しながら<b>立体的に</b>繋がっています。'
        '結晶とガラスの違いだけを取り出して見せるこの描き方は、'
        'W. H. Zachariasen (1932) 以来、ガラスの構造の説明に使われてきたものです。'
        '網の形そのものは、この図のために計算で作りました'
        '（規則正しい網に乱れを与え、環の大きさを揃わなくしています）。'
        'なお岩を作る鉱物の多くは純粋な SiO₂ ではなく、'
        'この網にアルミニウムやナトリウムが入った<b>ケイ酸塩</b>'
        '（長石など）です。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    efig.save('_fig1_same.qmd', build())
