# -*- coding: utf-8 -*-
"""
元素 #6 アルミニウム / 図6 : アルミが溶け出す pH。

水酸化アルミと釣り合った水に、アルミがどれだけ溶けているかを pH ごとに計算し、
U 字の曲線で描く。その上に、アジサイが青くなる土・ピンクになる土の pH の帯と、
雨水・海水の pH を置く。

計算（25 ℃、活量＝濃度とみなす希薄な水）:
  Al(OH)3 + 3H+ = Al3+ + 3H2O          log K = 8.11（ギブサイト）/ 10.8（非晶質）
  Al3+ + H2O  = AlOH2+   + H+          log K = −5.0
  Al3+ + 2H2O = Al(OH)2+ + 2H+         log K = −10.1
  Al3+ + 3H2O = Al(OH)3  + 3H+         log K = −16.9
  Al3+ + 4H2O = Al(OH)4− + 4H+         log K = −22.7
  いずれも PHREEQC 3.8 付属の phreeqc.dat（非晶質は wateq4f.dat の Al(OH)3(a)）

  溶けているアルミの合計 = Al3+ + AlOH2+ + Al(OH)2+ + Al(OH)3 + Al(OH)4−

pH の帯は園芸の目安（青 5.0〜5.5、ピンク 6.0〜6.5）。花の色は品種・リン酸・水分にもよる。

出力: _fig6_ph.qmd
"""
import math

import efig

P, CID = 'alph', 'alph1'

MW_AL = 26.982
LOGK_SP = {'gibbsite': 8.11, 'amorph': 10.8}
LOGK_HYD = [(1, -5.0), (2, -10.1), (3, -16.9), (4, -22.7)]


def total_al(ph, logk_sp):
    """ギブサイト（または非晶質）と釣り合った水の、溶存アルミ合計 mol/L。"""
    la = logk_sp - 3 * ph               # log[Al3+]
    tot = 10 ** la
    for n, lk in LOGK_HYD:
        tot += 10 ** (la + lk + n * ph)
    return tot


def mgL(ph, key):
    return total_al(ph, LOGK_SP[key]) * MW_AL * 1000.0


def minimum(key):
    best = None
    ph = 4.0
    while ph <= 9.0:
        v = mgL(ph, key)
        if best is None or v < best[1]:
            best = (ph, v)
        ph += 0.01
    return best


W, H = 680, 370
PX0, PX1 = 70, 650            # pH 3.5 〜 10
PH0, PH1 = 3.5, 10.0
YTOP, YBOT = 70, 310          # 10^2 〜 10^-4 mg/L
LTOP, LBOT = 2.0, -4.0


def px(ph):
    return PX0 + (ph - PH0) / (PH1 - PH0) * (PX1 - PX0)


def py(lg, clamp=True):
    if clamp:
        lg = max(LBOT, min(LTOP, lg))
    return YTOP + (LTOP - lg) / (LTOP - LBOT) * (YBOT - YTOP)


def curve(key):
    pts = []
    ph = PH0
    while ph <= PH1 + 1e-9:
        pts.append('%.1f,%.1f' % (px(ph), py(math.log10(mgL(ph, key)), clamp=False)))
        ph += 0.05
    return ' '.join(pts)


def build_svg():
    o = ['<svg viewBox="0 0 %d %d" role="img" aria-label="pHと、水に溶けるアルミの量の関係。'
         '中性付近で最も少なく、酸性側とアルカリ性側で増えるU字の曲線">' % (W, H)]

    o.append('<clipPath id="%s-clip"><rect x="%d" y="%d" width="%d" height="%d"/></clipPath>'
             % (P, PX0, YTOP, PX1 - PX0, YBOT - YTOP))
    # アジサイの帯
    bands = [(5.0, 5.5, 'blue', 'アジサイが青',
              '土が <b>pH 5.0〜5.5</b> ほどの酸性だと、土の中のアルミが溶け出し、'
              '根から吸われて花の色素と組み、<b>アジサイは青</b>になります。'),
             (6.0, 6.5, 'pink', 'アジサイがピンク',
              '<b>pH 6.0〜6.5</b> ほどになると、アルミはほとんど溶けません。'
              '花にアルミが届かず、色素そのものの赤みが出て<b>ピンク</b>になります。')]
    for a, b, cls, lab, det in bands:
        o.append('<g class="%s-hv" data-detail="%s">' % (P, efig.attr(det)))
        o.append('<rect class="%s-%s" x="%.1f" y="%d" width="%.1f" height="%d"/>'
                 % (P, cls, px(a), YTOP, px(b) - px(a), YBOT - YTOP))
        o.append('<text class="%s-bt %s-bt%s" x="%.1f" y="%d">%s</text>'
                 % (P, P, cls, (px(a) + px(b)) / 2, YTOP - (24 if cls == 'blue' else 8), lab))
        o.append('</g>')

    # 目盛
    for lg in range(int(LBOT), int(LTOP) + 1):
        yy = py(lg)
        o.append('<line class="%s-gl" x1="%d" y1="%.1f" x2="%d" y2="%.1f"/>' % (P, PX0, yy, PX1, yy))
        lab = {2: '100', 1: '10', 0: '1', -1: '0.1', -2: '0.01', -3: '0.001', -4: '0.0001'}[lg]
        o.append('<text class="%s-tky" x="%d" y="%.1f">%s</text>' % (P, PX0 - 6, yy + 4, lab))
    for ph in range(4, 11):
        xx = px(ph)
        o.append('<line class="%s-glx" x1="%.1f" y1="%d" x2="%.1f" y2="%d"/>' % (P, xx, YTOP, xx, YBOT))
        o.append('<text class="%s-tkx" x="%.1f" y="%d">%d</text>' % (P, xx, YBOT + 16, ph))
    o.append('<text class="%s-ax" x="%.1f" y="%d">pH（小さいほど酸性、7 が中性）</text>'
             % (P, (PX0 + PX1) / 2, YBOT + 34))
    o.append('<text class="%s-axy" x="%d" y="%d">溶けているアルミ（mg/L）</text>' % (P, PX0 - 6, YTOP - 48))

    # 曲線
    o.append('<g class="%s-hv" data-detail="%s">' % (P, efig.attr(
        '点線は、<b>できたての、ふわふわした水酸化アルミ</b>（非晶質）と釣り合った場合です。'
        '結晶よりずっと溶けやすく、同じ pH で数百倍になります。'
        '実際の土の水は、おおむね2本の線のあいだにあります。')))
    o.append('<polyline class="%s-am" points="%s" clip-path="url(#%s-clip)"/>' % (P, curve('amorph'), P))
    o.append('</g>')
    o.append('<g class="%s-hv" data-detail="%s">' % (P, efig.attr(
        '実線は、<b>よく結晶した水酸化アルミ（ギブサイト）</b>と釣り合った水です。'
        '<b>pH 6 前後でいちばん溶けにくく</b>、そこから酸性側でもアルカリ性側でも溶ける量が'
        '増えます。酸にもアルカリにも溶ける——<b>両性</b>と呼ばれる性質です。')))
    o.append('<polyline class="%s-gb" points="%s" clip-path="url(#%s-clip)"/>' % (P, curve('gibbsite'), P))
    o.append('</g>')
    pm, vm = minimum('gibbsite')
    o.append('<circle class="%s-min" cx="%.1f" cy="%.1f" r="4.5"/>' % (P, px(pm), py(math.log10(vm))))
    o.append('<text class="%s-mint" x="%.1f" y="%.1f">いちばん溶けにくい（pH %.1f）</text>'
             % (P, px(pm) + 10, py(math.log10(vm)) - 8, pm))

    # 雨と海
    for ph, lab, det in [
        (5.6, '雨', '雨は、空気中の二酸化炭素が溶けこむので、何も汚れていなくても '
                    '<b>pH 5.6 ほど</b>の弱い酸性です。'),
        (8.1, '海', '海水は <b>pH 8.1 ほど</b>の弱いアルカリ性です。')]:
        xx = px(ph)
        o.append('<g class="%s-hv" data-detail="%s">' % (P, efig.attr(det)))
        o.append('<path class="%s-mk" d="M%.1f %d v-10"/>' % (P, xx, YBOT))
        o.append('<text class="%s-mkt" x="%.1f" y="%d">%s %.1f</text>' % (P, xx, YBOT - 14, lab, ph))
        o.append('</g>')

    # 曲線の名前
    o.append('<text class="%s-cl %s-clg" x="%.1f" y="%.1f">結晶（ギブサイト）</text>'
             % (P, P, px(8.9), py(math.log10(mgL(8.9, 'gibbsite'))) + 16))
    o.append('<text class="%s-cl %s-cla" x="%.1f" y="%.1f">非晶質</text>'
             % (P, P, px(8.6), py(math.log10(mgL(8.6, 'amorph'))) - 8))
    o.append('</svg>')
    return '\n'.join(o)


CSS = """
.%(p)s{--gb:#5B6F80;--am:#8C9DAD;--blue:#3F74C6;--pink:#D0679A;--gl:#ECE3D2;}
.%(p)s-wrap{margin:16px 8px 0;}
.%(p)s-wrap svg{display:block;width:100%%;height:auto;}
.%(p)s-wrap text{font-family:"Hiragino Sans","Yu Gothic","Noto Sans JP",sans-serif;}
.%(p)s-blue{fill:rgba(63,116,198,.13);}
.%(p)s-pink{fill:rgba(208,103,154,.13);}
.%(p)s-bt{font-size:12px;font-weight:800;text-anchor:middle;}
.%(p)s-btblue{fill:var(--blue);}
.%(p)s-btpink{fill:#B34C80;}
.%(p)s-gl{stroke:var(--gl);stroke-width:1;}
.%(p)s-glx{stroke:var(--gl);stroke-width:1;opacity:.6;}
.%(p)s-tky{font-size:10.5px;fill:var(--faint);text-anchor:end;font-variant-numeric:tabular-nums;}
.%(p)s-tkx{font-size:11px;fill:var(--faint);text-anchor:middle;}
.%(p)s-ax{font-size:11.5px;fill:var(--dim);text-anchor:middle;}
.%(p)s-axy{font-size:11.5px;fill:var(--dim);text-anchor:start;}
.%(p)s-gb{fill:none;stroke:var(--gb);stroke-width:3.2;stroke-linejoin:round;
  stroke-dasharray:1200;stroke-dashoffset:1200;animation:%(p)s-draw 2s ease-out .2s forwards;}
.%(p)s-am{fill:none;stroke:var(--am);stroke-width:2;stroke-dasharray:6 5;}
@keyframes %(p)s-draw{to{stroke-dashoffset:0;}}
.%(p)s-min{fill:var(--gb);}
.%(p)s-mint{font-size:11px;fill:var(--gb);text-anchor:start;font-weight:700;}
.%(p)s-mk{stroke:var(--dim);stroke-width:2;}
.%(p)s-mkt{font-size:11.5px;fill:var(--dim);text-anchor:middle;font-weight:700;}
.%(p)s-cl{font-size:11.5px;font-weight:700;text-anchor:middle;}
.%(p)s-clg{fill:var(--gb);}
.%(p)s-cla{fill:var(--am);}
.%(p)s-hv{cursor:default;}
@media (max-width:820px){.%(p)s-wrap{margin:10px 0 0;}}
@media (prefers-reduced-motion:reduce){.%(p)s-gb{stroke-dashoffset:0;}}
""" % {'p': P}


def build():
    pm, vm = minimum('gibbsite')
    r64 = mgL(4.0, 'gibbsite') / mgL(6.0, 'gibbsite')
    o = [efig.css(P, CSS),
         efig.open_card(
             P, CID,
             'アルミは、酸性の水に溶け出します',
             '横軸の pH は、酸性・アルカリ性の目盛りです。7 が中性で、1 小さくなるごとに'
             '水素イオンの濃さは 10 倍になります。縦軸は、水 1 L に溶けているアルミの量（目盛は '
             '1 つ上がるごとに 10 倍）。帯や線にカーソルを合わせる（スマホはタップ）と'
             '説明が出ます。')]
    o.append('<div class="%s-wrap">%s</div>' % (P, build_svg()))
    o.append(efig.close_card(
        P,
        'アルミは <b>pH 6 前後でいちばん溶けにくく</b>、そこから外れると溶けはじめます。'
        '<b>pH が 6 から 4 に下がるだけで、溶ける量はおよそ %s 倍</b>。'
        'アジサイが酸性の土で青くなるのは、溶け出したアルミが花まで届くからです。'
        '中性の土では、アルミはほとんど溶けません。' % ('{:,}'.format(int(round(r64, -3)))),
        '25 ℃、ごく薄い水として計算しました。水酸化アルミが溶ける反応と、溶けたアルミが'
        '水と組む4つの反応の定数は、PHREEQC 3.8 に付属する phreeqc.dat（非晶質は '
        'wateq4f.dat の Al(OH)₃(a)）によります。実際の土の水では、有機物や硫酸・フッ化物と'
        '組んだアルミも加わります。アジサイの帯は園芸でよく示される目安で、花の色は'
        '品種や土のリン酸・水分によっても変わります（アルミと色素の組み方は、'
        '名古屋大学・吉田久美らの研究による）。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    for key in ('gibbsite', 'amorph'):
        pm, vm = minimum(key)
        print('%-9s 最小 pH %.2f  %.2e mg/L' % (key, pm, vm))
    for ph in (4.0, 5.0, 5.6, 6.0, 7.0, 8.1, 9.0):
        print('pH %.1f  gibbsite %.2e mg/L   amorph %.2e mg/L'
              % (ph, mgL(ph, 'gibbsite'), mgL(ph, 'amorph')))
    print('pH4/pH6 比 = %.0f' % (mgL(4.0, 'gibbsite') / mgL(6.0, 'gibbsite')))
    efig.save('_fig6_ph.qmd', build())
