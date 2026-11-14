# -*- coding: utf-8 -*-
"""
元素 #7 ナトリウム / 図4 : ナトリウムは、589 nm の光で名乗る。

上段: 目に見える光の帯（約380〜750 nm）に、ナトリウムの光の位置を立てる。
      589.0 nm と 589.6 nm の 2 本（D 線）は、この縮尺ではほぼ重なるので、
      右に拡大窓を置いて 2 本に分かれて見えるようにする。
下段: 炎の色の札（ナトリウム・カリウム・銅）。本文で挙げた3つ。

波長は NIST Atomic Spectra Database の値（空気中）: 588.995 nm、589.592 nm。
帯の色は目安（モニターで正確な単色光は出せない）。

出力: _fig4_light.qmd
"""
import efig

P, CID = 'nalit', 'nalit1'

W, H = 680, 210
L0, L1 = 380.0, 750.0
X0, XW = 30, 470
D1, D2 = 588.995, 589.592

# 波長 → おおよその色（目安）
STOPS = [(380, '#4B0B6E'), (420, '#5B2BC4'), (450, '#2E4BE0'), (485, '#0094D0'),
         (510, '#22B04B'), (550, '#9BCB1E'), (575, '#E9D417'), (589, '#FFB10A'),
         (610, '#F46A14'), (650, '#E0261E'), (700, '#A8121B'), (750, '#4E0A0E')]


def x(l):
    return X0 + XW * (l - L0) / (L1 - L0)


# 拡大窓（588〜591 nm）
ZX0, ZW, ZL0, ZL1 = 520, 150, 588.6, 590.0


def zx(l):
    return ZX0 + ZW * (l - ZL0) / (ZL1 - ZL0)


def build_svg():
    o = ['<svg viewBox="0 0 %d %d" role="img" aria-label="目に見える光の帯の上で、'
         'ナトリウムの光が589ナノメートルの黄橙色にあることを示した図。拡大すると2本の線に分かれる">'
         % (W, H)]
    o.append('<defs><linearGradient id="%s-sp" x1="0" x2="1">' % P)
    for l, c in STOPS:
        o.append('<stop offset="%.4f" stop-color="%s"/>' % ((l - L0) / (L1 - L0), c))
    o.append('</linearGradient></defs>')
    o.append('<rect x="%d" y="40" width="%d" height="46" rx="6" fill="url(#%s-sp)"/>'
             % (X0, XW, P))
    for l in (400, 500, 600, 700):
        o.append('<line class="%s-tk" x1="%.1f" y1="86" x2="%.1f" y2="92"/>' % (P, x(l), x(l)))
        o.append('<text class="%s-tl" x="%.1f" y="106">%d</text>' % (P, x(l), l))
    o.append('<text class="%s-ax" x="%d" y="124">波長（ナノメートル）</text>' % (P, X0 + XW / 2))
    o.append('<text class="%s-end" x="%d" y="30">紫</text>' % (P, X0))
    o.append('<text class="%s-end" x="%d" y="30" text-anchor="end">赤</text>' % (P, X0 + XW))
    # ナトリウムの位置
    xd = x((D1 + D2) / 2)
    o.append('<g data-detail="%s">' % efig.attr(
        '<b>ナトリウムの光：589 nm</b>。炎に入れても、ランプの中で光らせても、'
        'ナトリウムなら必ずこの位置に出ます。電子が決まった段から決まった段へ落ちるとき、'
        'その段差のぶんのエネルギーだけを光にするためです。'))
    o.append('<line class="%s-na" x1="%.1f" y1="34" x2="%.1f" y2="92"/>' % (P, xd, xd))
    o.append('<circle class="%s-nadot" cx="%.1f" cy="34" r="5"/>' % (P, xd))
    o.append('<text class="%s-nat" x="%.1f" y="20">ナトリウム 589</text>' % (P, xd))
    o.append('</g>')
    # 拡大窓
    o.append('<path class="%s-zoom" d="M%.1f 40 L%d 40 M%.1f 86 L%d 86"/>'
             % (P, xd + 4, ZX0, xd + 4, ZX0))
    o.append('<rect class="%s-zbox" x="%d" y="40" width="%d" height="46" rx="4"/>' % (P, ZX0, ZW))
    for l, nm in ((D1, '589.0'), (D2, '589.6')):
        o.append('<line class="%s-zl" x1="%.1f" y1="44" x2="%.1f" y2="82"/>' % (P, zx(l), zx(l)))
        o.append('<text class="%s-zt" x="%.1f" y="104">%s</text>' % (P, zx(l), nm))
    o.append('<text class="%s-ax" x="%d" y="124">拡大すると2本</text>' % (P, ZX0 + ZW / 2))

    # 炎の色の札
    chips = [('ナトリウム', '黄橙', '#F2A20F',
              '<b>ナトリウム</b>：黄橙。味噌汁の吹きこぼれ、塩を振った炎、黄色い花火。'),
             ('カリウム', '薄い紫', '#B7A0D8',
              '<b>カリウム</b>：薄い紫。ナトリウムと同じ列のすぐ下の元素ですが、色はまったく違います。'
              'ナトリウムが混じると黄色に隠れてしまうほど淡い色です。'),
             ('銅', '青緑', '#2FA39A',
              '<b>銅</b>：青緑。緑色の花火に使われます。')]
    for i, (nm, col, c, det) in enumerate(chips):
        cx = 120 + i * 200
        o.append('<g class="%s-chip" data-detail="%s">' % (P, efig.attr(det)))
        o.append('<rect class="%s-cbg" x="%d" y="148" width="180" height="46" rx="10"/>'
                 % (P, cx - 90))
        o.append('<path d="M%d 186 c-12 -6 -10 -20 0 -32 c10 12 12 26 0 32 z" fill="%s"/>'
                 % (cx - 60, c))
        o.append('<text class="%s-cn" x="%d" y="168">%s</text>' % (P, cx - 40, nm))
        o.append('<text class="%s-cc" x="%d" y="186">%s</text>' % (P, cx - 40, col))
        o.append('</g>')
    o.append('<text class="%s-ch" x="16" y="140">炎の色（炎色反応）</text>' % P)
    o.append('</svg>')
    return '\n'.join(o)


CSS = """
.%(p)s-wrap{margin:14px 8px 0;}
.%(p)s-wrap svg{display:block;width:100%%;height:auto;}
.%(p)s-wrap text{font-family:"Hiragino Sans","Yu Gothic","Noto Sans JP",sans-serif;}
.%(p)s-tk{stroke:var(--faint);stroke-width:1;}
.%(p)s-tl{font-size:11px;fill:var(--dim);text-anchor:middle;font-variant-numeric:tabular-nums;}
.%(p)s-ax{font-size:11px;fill:var(--faint);text-anchor:middle;}
.%(p)s-end{font-size:11px;fill:var(--faint);}
.%(p)s-na{stroke:var(--ink);stroke-width:2;}
.%(p)s-nadot{fill:#FFB10A;stroke:var(--ink);stroke-width:1.5;
  animation:%(p)s-glow 2.2s ease-in-out infinite;transform-box:fill-box;transform-origin:center;}
@keyframes %(p)s-glow{0%%,100%%{transform:scale(1);}50%%{transform:scale(1.5);}}
.%(p)s-nat{font-size:13px;font-weight:800;fill:var(--ink);text-anchor:middle;}
.%(p)s-zoom{stroke:var(--faint);stroke-width:1;stroke-dasharray:3 3;fill:none;}
.%(p)s-zbox{fill:#FFB10A;stroke:var(--ink);stroke-width:1;}
.%(p)s-zl{stroke:var(--ink);stroke-width:3;}
.%(p)s-zt{font-size:11px;font-weight:700;fill:var(--ink);text-anchor:middle;font-variant-numeric:tabular-nums;}
.%(p)s-ch{font-size:12.5px;font-weight:800;fill:var(--ink);}
.%(p)s-chip{cursor:default;}
.%(p)s-cbg{fill:rgba(122,96,52,.05);stroke:var(--line2);}
.%(p)s-chip:hover .%(p)s-cbg{fill:rgba(190,100,10,.08);}
.%(p)s-cn{font-size:13px;font-weight:800;fill:var(--ink);}
.%(p)s-cc{font-size:11.5px;fill:var(--dim);}
@media (max-width:820px){.%(p)s-wrap{margin:10px 0 0;}}
""" % {'p': P}


def build():
    o = [efig.css(P, CSS),
         efig.open_card(
             P, CID,
             'ナトリウムは、589 ナノメートルの光で名乗ります',
             '目に見える光の帯の上に、ナトリウムが出す光の位置を立てました。'
             '下は、炎に入れたときの色です。カーソルを合わせる（スマホはタップ）と説明が出ます。')]
    o.append('<div class="%s-wrap">%s</div>' % (P, build_svg()))
    o.append(efig.close_card(
        P,
        'ナトリウムの光は<b>589ナノメートル</b>、黄色からオレンジにかかる色です'
        '（1ナノメートルは1ミリの100万分の1）。'
        '元素ごとに出す光の位置が決まっているので、<b>炎の色を見れば、何が入っているか分かります</b>。',
        '波長は NIST Atomic Spectra Database による（空気中の値で 588.995 nm と 589.592 nm。'
        'ナトリウムの D 線と呼ばれます）。光の帯と炎の色は目安で、画面では正確な色を出せません。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    print('D 線の間隔 %.3f nm、帯の上で %.2f px、拡大窓で %.1f px'
          % (D2 - D1, x(D2) - x(D1), zx(D2) - zx(D1)))
    efig.save('_fig4_light.qmd', build())
