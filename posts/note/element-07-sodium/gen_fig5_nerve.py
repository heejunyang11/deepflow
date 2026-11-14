# -*- coding: utf-8 -*-
"""
元素 #7 ナトリウム / 図5 : 神経を走る電気は、ナトリウムが運ぶ。

左: 神経の細胞膜の断面。外にナトリウム（紫）が多く、内にカリウム（薄紫）が多い。
    膜にはポンプ（差を作る）とチャネル（一気に流す）がある。チャネルが開くと、
    ナトリウムが内へ流れこむ（CSS アニメーション）。
右: そのとき膜の内側の電位がどう動くか（活動電位）。−70 mV から一瞬 +30 mV へ。

濃さと電位は生理学の教科書の代表値（細胞の種類で違う）:
  外 Na 145 / K 4、内 Na 12 / K 140（mmol/L）、静止 −70 mV、頂点 +30 mV。
粒の数は、その濃さの比をおおまかに写しただけ（数そのものに意味は無い）。

出力: _fig5_nerve.qmd
"""
import random

import efig

P, CID = 'nanrv', 'nanrv1'

W, H = 680, 300
OUT = dict(Na=145, K=4)
IN = dict(Na=12, K=140)

# 膜（左の箱）
BX0, BX1 = 20, 330
MY0, MY1 = 132, 150            # 膜の上端・下端
CH_X = 150                     # チャネルの位置
PUMP_X = 270                   # ポンプの位置

# 電位のグラフ（右の箱）
GX0, GX1, GY0, GY1 = 400, 660, 40, 240
T_MAX = 5.0
V_MIN, V_MAX = -90.0, 40.0
TRACE = [(0, -70), (1.0, -70), (1.25, -60), (1.45, -10), (1.6, 30), (1.75, 10),
         (2.1, -60), (2.4, -78), (2.8, -80), (3.6, -72), (4.2, -70), (5.0, -70)]


def gx(t):
    return GX0 + (GX1 - GX0) * t / T_MAX


def gy(v):
    return GY1 - (GY1 - GY0) * (v - V_MIN) / (V_MAX - V_MIN)


def dots(o, rnd, n, cls, y0, y1, avoid=None):
    for _ in range(n):
        while True:
            x = rnd.uniform(BX0 + 12, BX1 - 12)
            y = rnd.uniform(y0, y1)
            if abs(x - CH_X) > 26 and abs(x - PUMP_X) > 34:
                break
        o.append('<circle class="%s-%s" cx="%.1f" cy="%.1f" r="5"/>' % (P, cls, x, y))


def smooth(points):
    """Catmull-Rom を 3 次ベジエに直した、なめらかな折れ線。"""
    pts = [(gx(t), gy(v)) for t, v in points]
    d = 'M%.1f %.1f' % pts[0]
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += ' C%.1f %.1f %.1f %.1f %.1f %.1f' % (c1 + c2 + p2)
    return d


def build_svg():
    rnd = random.Random(11)
    o = ['<svg viewBox="0 0 %d %d" role="img" aria-label="神経の細胞膜の断面と、'
         '信号が通るときの膜の電位の変化。外に多いナトリウムがチャネルを通って流れこみ、'
         '電位がマイナス70ミリボルトから一瞬プラス30ミリボルトへ振れる">' % (W, H)]
    # 外と内
    o.append('<rect class="%s-out" x="%d" y="30" width="%d" height="%d" rx="8"/>'
             % (P, BX0, BX1 - BX0, MY0 - 30))
    o.append('<rect class="%s-in" x="%d" y="%d" width="%d" height="%d" rx="8"/>'
             % (P, BX0, MY1, BX1 - BX0, 262 - MY1))
    o.append('<g data-detail="%s">' % efig.attr(
        '<b>細胞の外</b>：ナトリウムが多く（1 L あたり約145ミリモル）、カリウムは少ない（約4）。'))
    o.append('<text class="%s-rg" x="%d" y="48">細胞の外</text>' % (P, BX0 + 10))
    o.append('<text class="%s-cn" x="%d" y="48">Na⁺ 約%d　K⁺ 約%d</text>'
             % (P, BX1 - 10, OUT['Na'], OUT['K']))
    dots(o, rnd, 16, 'na', 60, MY0 - 10, avoid=CH_X)
    dots(o, rnd, 2, 'k', 60, MY0 - 10, avoid=CH_X)
    o.append('</g>')
    o.append('<g data-detail="%s">' % efig.attr(
        '<b>細胞の内</b>：カリウムが多く（約140ミリモル）、ナトリウムは少ない（約12）。'
        'ふだん、内側は外側より<b>約70ミリボルト、マイナス</b>です。'))
    o.append('<text class="%s-rg" x="%d" y="252">細胞の内</text>' % (P, BX0 + 10))
    o.append('<text class="%s-cn" x="%d" y="252">Na⁺ 約%d　K⁺ 約%d</text>'
             % (P, BX1 - 10, IN['Na'], IN['K']))
    dots(o, rnd, 2, 'na', MY1 + 14, 234, avoid=CH_X)
    dots(o, rnd, 15, 'k', MY1 + 14, 234, avoid=CH_X)
    o.append('</g>')
    # 膜
    o.append('<rect class="%s-mem" x="%d" y="%d" width="%d" height="%d"/>'
             % (P, BX0, MY0, BX1 - BX0, MY1 - MY0))
    # チャネル（開閉する門）
    o.append('<g class="%s-chg" data-detail="%s">' % (P, efig.attr(
        '<b>ナトリウムの通り道（チャネル）</b>：信号が来ると一瞬だけ開き、'
        '外に多いナトリウムが<b>どっと内へ流れこみます</b>。プラスが入ってくるので、'
        '内側の電位がマイナスからプラスへひっくり返ります。')))
    o.append('<rect class="%s-chw" x="%d" y="%d" width="10" height="%d"/>'
             % (P, CH_X - 17, MY0 - 4, MY1 - MY0 + 8))
    o.append('<rect class="%s-chw" x="%d" y="%d" width="10" height="%d"/>'
             % (P, CH_X + 7, MY0 - 4, MY1 - MY0 + 8))
    o.append('<rect class="%s-gate" x="%d" y="%d" width="14" height="6"/>'
             % (P, CH_X - 7, MY0 - 2))
    o.append('<text class="%s-lb" x="%d" y="%d">チャネル</text>' % (P, CH_X, MY0 - 10))
    for i in range(3):
        o.append('<circle class="%s-na %s-flow" cx="%d" cy="%d" r="5" '
                 'style="animation-delay:%.2fs"/>' % (P, P, CH_X, MY0 - 22, i * 0.18))
    o.append('</g>')
    # ポンプ
    o.append('<g class="%s-pg" data-detail="%s">' % (P, efig.attr(
        '<b>ポンプ（ナトリウム–カリウムポンプ）</b>：エネルギーを使って、ナトリウムを外へ'
        'くみ出し、カリウムを内へくみ入れます。<b>濃さの差を作るのはこちら</b>、'
        'その差を一気に流して信号にするのがチャネルです。')))
    o.append('<circle class="%s-pump" cx="%d" cy="%d" r="15"/>' % (P, PUMP_X, (MY0 + MY1) // 2))
    o.append('<path class="%s-parr" d="M%d %d l0 -26 m-4 6 l4 -6 l4 6"/>'
             % (P, PUMP_X - 5, MY0 - 2))
    o.append('<path class="%s-parr" d="M%d %d l0 26 m-4 -6 l4 6 l4 -6"/>'
             % (P, PUMP_X + 5, MY1 + 2))
    o.append('<text class="%s-lb" x="%d" y="%d">ポンプ</text>' % (P, PUMP_X, MY0 - 30))
    o.append('<text class="%s-pl" x="%d" y="%d">Na⁺ を外へ</text>' % (P, PUMP_X - 10, MY0 - 12))
    o.append('<text class="%s-pl" x="%d" y="%d">K⁺ を内へ</text>' % (P, PUMP_X - 10, MY1 + 22))
    o.append('</g>')

    # 電位のグラフ
    o.append('<g data-detail="%s">' % efig.attr(
        '<b>活動電位</b>：チャネルが開いてナトリウムが流れこむと、膜の内側は'
        '約−70 mV から一瞬 <b>+30 mV</b> ほどへ振れます。すぐにカリウムが外へ出て元に戻ります。'
        '全体で数ミリ秒（1ミリ秒は1000分の1秒）の出来事です。'))
    o.append('<rect class="%s-gbg" x="%d" y="%d" width="%d" height="%d" rx="6"/>'
             % (P, GX0, GY0, GX1 - GX0, GY1 - GY0))
    for v in (-70, 0, 30):
        o.append('<line class="%s-gl%s" x1="%d" y1="%.1f" x2="%d" y2="%.1f"/>'
                 % (P, ' %s-zero' % P if v == 0 else '', GX0, gy(v), GX1, gy(v)))
        o.append('<text class="%s-gv" x="%d" y="%.1f">%+d</text>' % (P, GX0 - 6, gy(v) + 4, v)
                 if v else '<text class="%s-gv" x="%d" y="%.1f">0</text>' % (P, GX0 - 6, gy(v) + 4))
    o.append('<text class="%s-gax" x="%d" y="%d">膜の内側の電位（ミリボルト）</text>'
             % (P, GX0, GY0 - 10))
    o.append('<text class="%s-gax2" x="%d" y="%d">時間 → （全体で約5ミリ秒）</text>'
             % (P, GX1, GY1 + 18))
    d = smooth(TRACE)
    o.append('<path class="%s-tr0" d="%s"/>' % (P, d))
    o.append('<path class="%s-tr" d="%s" pathLength="100"/>' % (P, d))
    o.append('<text class="%s-ann" x="%.1f" y="%.1f">← Na⁺ が流れこむ</text>'
             % (P, gx(1.6) + 12, gy(30) + 4))
    o.append('<text class="%s-ann2" x="%.1f" y="%.1f">← K⁺ が出て戻る</text>'
             % (P, gx(2.15) + 8, gy(-35)))
    o.append('</g>')
    o.append('</svg>')
    return '\n'.join(o)


CSS = """
.%(p)s{--na:#7B4FA0;--k:#B9A7C9;}
.%(p)s-wrap{margin:14px 8px 0;}
.%(p)s-wrap svg{display:block;width:100%%;height:auto;}
.%(p)s-wrap text{font-family:"Hiragino Sans","Yu Gothic","Noto Sans JP",sans-serif;}
.%(p)s-out{fill:#EEF3F6;}
.%(p)s-in{fill:#F6F0E4;}
.%(p)s-mem{fill:#D9C9A8;}
.%(p)s-rg{font-size:13px;font-weight:800;fill:var(--ink);}
.%(p)s-cn{font-size:11.5px;fill:var(--dim);text-anchor:end;font-variant-numeric:tabular-nums;}
.%(p)s-na{fill:var(--na);}
.%(p)s-k{fill:var(--k);}
.%(p)s-chw{fill:#8A6B36;}
.%(p)s-gate{fill:#8A6B36;transform-box:fill-box;transform-origin:left center;
  animation:%(p)s-gate 4s ease-in-out infinite;}
@keyframes %(p)s-gate{0%%,22%%{transform:rotate(0deg);}28%%,42%%{transform:rotate(-80deg);}
  50%%,100%%{transform:rotate(0deg);}}
.%(p)s-flow{opacity:0;animation:%(p)s-flow 4s ease-in infinite;}
@keyframes %(p)s-flow{0%%,24%%{transform:translateY(0);opacity:0;}
  27%%{opacity:1;}44%%{transform:translateY(58px);opacity:1;}50%%,100%%{transform:translateY(58px);opacity:0;}}
.%(p)s-lb{font-size:11.5px;font-weight:700;fill:var(--ink);text-anchor:middle;}
.%(p)s-pump{fill:#F2E6CF;stroke:#8A6B36;stroke-width:2;}
.%(p)s-parr{fill:none;stroke:#8A6B36;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;}
.%(p)s-chg,.%(p)s-pg{cursor:default;}
.%(p)s-gbg{fill:rgba(122,96,52,.04);stroke:var(--line2);}
.%(p)s-gl{stroke:var(--line);stroke-width:1;}
.%(p)s-zero{stroke-dasharray:4 4;stroke:var(--faint);}
.%(p)s-gv{font-size:11px;fill:var(--dim);text-anchor:end;font-variant-numeric:tabular-nums;}
.%(p)s-gax{font-size:11.5px;font-weight:700;fill:var(--dim);}
.%(p)s-gax2{font-size:11px;fill:var(--faint);text-anchor:end;}
.%(p)s-tr0{fill:none;stroke:var(--line);stroke-width:3;}
.%(p)s-tr{fill:none;stroke:var(--na);stroke-width:3.2;stroke-linecap:round;
  stroke-dasharray:100;stroke-dashoffset:0;animation:%(p)s-draw 4s linear infinite;}
@keyframes %(p)s-draw{0%%,10%%{stroke-dashoffset:100;}70%%,100%%{stroke-dashoffset:0;}}
.%(p)s-ann{font-size:11.5px;font-weight:800;fill:var(--na);}
.%(p)s-pl{font-size:10px;fill:#8A6B36;text-anchor:end;}
.%(p)s-ann2{font-size:11.5px;font-weight:700;fill:var(--dim);}
@media (max-width:820px){.%(p)s-wrap{margin:10px 0 0;}}
""" % {'p': P}


def build():
    o = [efig.css(P, CSS),
         efig.open_card(
             P, CID,
             '神経の信号は、ナトリウムが流れこむ一瞬です',
             '左は神経の細胞の膜の断面、右はそのとき膜の内側の電位がどう動くかです。'
             '膜の門（チャネル）が開くと、外に多いナトリウムが中へ流れこみます。'
             'カーソルを合わせる（スマホはタップ）と説明が出ます。')]
    o.append('<div class="%s-wrap">%s</div>' % (P, build_svg()))
    o.append(efig.close_card(
        P,
        '<b>ポンプ</b>がエネルギーを使ってナトリウムを外へくみ出し、濃さの差を作っておきます。'
        '信号が来ると<b>チャネル</b>が開き、ナトリウムがどっと流れこんで、'
        '電位が一瞬<b>マイナスからプラスへ</b>ひっくり返ります。'
        'ダムに水をためておいて、水門を開けるのに似ています。',
        '模式図です。粒の数は濃さの比をおおまかに写しただけです。濃さ（1 L あたりのミリモル）は'
        '外 Na 約145・K 約4、内 Na 約12・K 約140、電位は静止時約 −70 mV・頂点約 +30 mV で、'
        'いずれも生理学の教科書に載る代表値です。細胞の種類によって違います。'
        'ポンプは Na⁺/K⁺-ATPase、通り道は電位依存性ナトリウムチャネルと呼ばれる、別々のタンパク質です。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    print('外/内の Na の比 %.1f、K の比 %.1f' % (OUT['Na'] / IN['Na'], IN['K'] / OUT['K']))
    efig.save('_fig5_nerve.qmd', build())
