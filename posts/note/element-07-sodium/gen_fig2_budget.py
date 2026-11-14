# -*- coding: utf-8 -*-
"""
元素 #7 ナトリウム / 図2 : ナトリウムは、海からなかなか出ていけない。

海は定常状態にある（入る量と出る量が釣り合っている）。違いは出口の太さで、
Ca は太い出口（殻）ですぐ出ていき、Na は細い出口のため高い濃さで釣り合う。
（2026-11-14 の第三者検証で「たまり続ける」を誤りとして直した）

岩 →（雨・川）→ 海 の断面に、カルシウムとナトリウムの粒を流す。
  ・カルシウム（橙）: 海に入ると、貝殻・サンゴに取りこまれて海底へ沈む
  ・ナトリウム（紫）: 海に入ると、長く海にとどまる。出口は細い（点線の矢印）
  ・塩化物イオン（緑）: 火山のガスから海へ入る（大昔の話。点線で描く）
下に、滞留時間の帯を同じ物差しで並べる。ナトリウムの帯は、資料による幅
（約5000万〜8000万年）をぼかしで描く。値を1つに決めないため。

動きは CSS だけ。動かない環境では、粒が途中の位置で止まった絵になる。

出力: _fig2_budget.qmd
"""
import efig

P, CID = 'nabud', 'nabud1'

W, H = 680, 380

# 滞留時間（万年）。Ca は Broecker & Peng (1982)。Na は資料によって幅がある。
RES_CA = 100
RES_NA_LO, RES_NA_HI = 5000, 8000
SCALE_MAX = 9000          # 物差しの右端（万年）
RX0, RW = 150, 500        # 帯の左端と全長（px）


def px(v):
    return RW * v / float(SCALE_MAX)


def build_svg():
    o = ['<svg viewBox="0 0 %d %d" role="img" aria-label="岩から川を経て海へ、'
         'カルシウムとナトリウムが運ばれる様子。カルシウムは貝殻やサンゴに取りこまれて'
         '海底へ沈み、ナトリウムは海にとどまる。下に、海にとどまる平均の時間を比べた帯">'
         % (W, H)]
    # 空と海
    o.append('<rect class="%s-sea" x="330" y="120" width="350" height="140"/>' % P)
    o.append('<path class="%s-floor" d="M330 260 L680 260 L680 276 L330 276 Z"/>' % P)
    # 山（岩）と川
    o.append('<path class="%s-rock" d="M0 260 L0 150 L60 70 L110 120 L160 60 '
             'L230 140 L330 150 L330 260 Z"/>' % P)
    o.append('<path class="%s-river" d="M150 92 C170 130 200 140 240 150 '
             'C280 158 310 150 336 140"/>' % P)
    # 雨
    for i in range(10):
        x = 30 + i * 26
        o.append('<path class="%s-rain" style="animation-delay:%.2fs" d="M%d 18 l-4 12"/>'
                 % (P, (i * 0.31) % 1.4, x))
    o.append('<text class="%s-lb" x="70" y="200">岩</text>' % P)
    o.append('<text class="%s-lbs" x="70" y="218">雨が溶かし出す</text>' % P)
    o.append('<text class="%s-lb" x="250" y="132">川</text>' % P)
    o.append('<text class="%s-lb" x="610" y="146">海</text>' % P)
    # 火山（右上）と塩化水素
    o.append('<path class="%s-volc" d="M560 120 L600 58 L616 58 L656 120 Z"/>' % P)
    o.append('<path class="%s-gas" d="M608 54 C598 40 618 30 606 16"/>' % P)
    o.append('<text class="%s-lbs" x="608" y="10">大昔の火山</text>' % P)
    o.append('<path class="%s-clarr" d="M584 92 C560 102 548 112 540 128"/>' % P)
    o.append('<text class="%s-clt" x="520" y="98">塩化水素 → Cl⁻</text>' % P)
    # 貝殻・サンゴ（海底）
    o.append('<g class="%s-shell" data-detail="%s">' % (P, efig.attr(
        '<b>カルシウムの出口</b>：貝・サンゴ・小さなプランクトンが、海水のカルシウムと'
        '炭酸水素イオンから<b>炭酸カルシウム</b>の殻や骨を作ります。死ぬと海底に積もり、'
        'やがて石灰岩になります（深い海の底まで沈んだものは溶けて戻ります）。')))
    for i, x in enumerate((390, 430, 470, 510)):
        o.append('<path class="%s-sh" d="M%d 258 q10 -16 20 0 z"/>' % (P, x))
    o.append('<text class="%s-sht" x="450" y="294">貝殻・サンゴ → 海底へ</text>' % P)
    o.append('</g>')
    # ナトリウムの細い出口（海底の岩・塩の層）
    o.append('<g class="%s-shell" data-detail="%s">' % (P, efig.attr(
        '<b>ナトリウムの出口</b>：海底の岩や泥にわずかに取りこまれる、干上がった入り江で'
        '塩の層として残る、など。どれも<b>細い出口</b>です。細いぶん、海のナトリウムは'
        'うんと濃くなったところで、入る量と出る量が釣り合っています。')))
    o.append('<path class="%s-naout" d="M610 236 L610 268"/>' % P)
    o.append('<path class="%s-naouth" d="M604 262 L610 270 L616 262"/>' % P)
    o.append('<text class="%s-naoutt" x="610" y="294">細い出口</text>' % P)
    o.append('</g>')

    # 粒：川を下って海へ。Ca は海底へ沈み、Na は海に残る
    for i in range(4):
        d = i * 1.6
        o.append('<circle class="%s-p %s-ca" r="6" style="animation-delay:%.1fs"/>'
                 % (P, P, d))
        o.append('<circle class="%s-p %s-na" r="6" style="animation-delay:%.1fs"/>'
                 % (P, P, d + 0.8))
    # 海にたまっているナトリウム（動かない粒）
    import random
    rnd = random.Random(7)
    for i in range(26):
        x = rnd.uniform(350, 665)
        y = rnd.uniform(150, 240)
        o.append('<circle class="%s-stay" cx="%.1f" cy="%.1f" r="4.2"/>' % (P, x, y))
    for i in range(9):
        x = rnd.uniform(360, 660)
        y = rnd.uniform(150, 240)
        o.append('<circle class="%s-clst" cx="%.1f" cy="%.1f" r="3.6"/>' % (P, x, y))

    # 凡例
    o.append('<circle class="%s-ca" cx="350" cy="20" r="6"/>' % P)
    o.append('<text class="%s-lg" x="362" y="25">カルシウム</text>' % P)
    o.append('<circle class="%s-na" cx="440" cy="20" r="6"/>' % P)
    o.append('<text class="%s-lg" x="452" y="25">ナトリウム</text>' % P)
    o.append('<circle class="%s-clst" cx="350" cy="44" r="5"/>' % P)
    o.append('<text class="%s-lg" x="362" y="49">塩化物イオン</text>' % P)

    # 滞留時間の帯
    y = 318
    o.append('<text class="%s-rh" x="16" y="%d">海にとどまる平均の時間</text>' % (P, y - 14))
    o.append('<g data-detail="%s">' % efig.attr(
        '<b>カルシウム：約100万年</b>。川から入っても、生き物の殻としてすぐに取り出されるので、'
        '海の中で入れ替わるのが速いのです。'))
    o.append('<text class="%s-rl" x="%d" y="%d">カルシウム</text>' % (P, RX0 - 10, y + 6))
    o.append('<rect class="%s-ca" x="%d" y="%d" width="%.1f" height="12" rx="2"/>'
             % (P, RX0, y - 4, max(px(RES_CA), 3)))
    o.append('<text class="%s-rv" x="%.1f" y="%d">約100万年</text>'
             % (P, RX0 + max(px(RES_CA), 3) + 8, y + 6))
    o.append('</g>')
    y2 = y + 26
    o.append('<g data-detail="%s">' % efig.attr(
        '<b>ナトリウム：数千万年</b>。出口が細いので、ひとつの原子は'
        '何千万年も海にとどまります。見積もりは資料によって約5000万〜8000万年と幅があるので、'
        '帯の先をぼかしました。'))
    o.append('<text class="%s-rl" x="%d" y="%d">ナトリウム</text>' % (P, RX0 - 10, y2 + 6))
    o.append('<defs><linearGradient id="%s-fade" x1="0" x2="1">'
             '<stop offset="0" stop-color="#7B4FA0"/>'
             '<stop offset="%.3f" stop-color="#7B4FA0"/>'
             '<stop offset="1" stop-color="#7B4FA0" stop-opacity="0"/>'
             '</linearGradient></defs>' % (P, px(RES_NA_LO) / px(RES_NA_HI)))
    o.append('<rect x="%d" y="%d" width="%.1f" height="12" rx="2" fill="url(#%s-fade)"/>'
             % (RX0, y2 - 4, px(RES_NA_HI), P))
    o.append('<text class="%s-rv" x="%.1f" y="%d">数千万年</text>'
             % (P, RX0 + px(RES_NA_HI) + 8, y2 + 6))
    o.append('</g>')
    o.append('</svg>')
    return '\n'.join(o)


CSS = """
.%(p)s{--na:#7B4FA0;--ca:#C9822A;--cl:#2E8B7A;--water:#CFE3EE;--rock:#D9CDB6;}
.%(p)s-wrap{margin:14px 8px 0;}
.%(p)s-wrap svg{display:block;width:100%%;height:auto;}
.%(p)s-wrap text{font-family:"Hiragino Sans","Yu Gothic","Noto Sans JP",sans-serif;}
.%(p)s-sea{fill:var(--water);}
.%(p)s-floor{fill:#CDBF9F;}
.%(p)s-rock{fill:var(--rock);}
.%(p)s-river{fill:none;stroke:#8CB8D3;stroke-width:9;stroke-linecap:round;}
.%(p)s-volc{fill:#B9A58A;}
.%(p)s-gas{fill:none;stroke:#A99C88;stroke-width:3;stroke-linecap:round;opacity:.7;}
.%(p)s-clarr{fill:none;stroke:var(--cl);stroke-width:2;stroke-dasharray:4 4;}
.%(p)s-clt{font-size:11px;font-weight:700;fill:var(--cl);text-anchor:end;}
.%(p)s-sh{fill:#F2E6CF;stroke:#B79E77;stroke-width:1.2;}
.%(p)s-sht{font-size:11.5px;font-weight:700;fill:#8A5518;text-anchor:middle;}
.%(p)s-shell{cursor:default;}
.%(p)s-lb{font-size:15px;font-weight:800;fill:var(--ink);text-anchor:middle;}
.%(p)s-lbs{font-size:11px;fill:var(--dim);text-anchor:middle;}
.%(p)s-lg{font-size:11.5px;fill:var(--dim);}
.%(p)s-ca{fill:var(--ca);}
.%(p)s-na{fill:var(--na);}
.%(p)s-stay{fill:var(--na);opacity:.55;}
.%(p)s-clst{fill:var(--cl);opacity:.5;}
.%(p)s-rain{stroke:#7FA7C4;stroke-width:1.6;stroke-linecap:round;opacity:0;
  animation:%(p)s-rain 1.4s linear infinite;}
@keyframes %(p)s-rain{0%%{transform:translateY(0);opacity:0;}
  15%%{opacity:.55;}100%%{transform:translateY(40px);opacity:0;}}
/* 粒の通り道。川の源流（150,92）→ 河口（336,140）→ 海の中 */
.%(p)s-p{transform:translate(150px,92px);}
.%(p)s-p.%(p)s-ca{animation:%(p)s-goca 6.4s linear infinite;}
.%(p)s-p.%(p)s-na{animation:%(p)s-gona 6.4s linear infinite;}
@keyframes %(p)s-goca{
  0%%{transform:translate(150px,92px);opacity:0;}
  5%%{opacity:1;}
  25%%{transform:translate(240px,150px);}
  40%%{transform:translate(336px,140px);}
  60%%{transform:translate(420px,170px);}
  85%%{transform:translate(450px,250px);opacity:1;}
  100%%{transform:translate(450px,256px);opacity:0;}}
@keyframes %(p)s-gona{
  0%%{transform:translate(150px,92px);opacity:0;}
  5%%{opacity:1;}
  25%%{transform:translate(240px,150px);}
  40%%{transform:translate(336px,140px);}
  65%%{transform:translate(470px,175px);}
  85%%{transform:translate(560px,200px);opacity:1;}
  100%%{transform:translate(600px,190px);opacity:0;}}
.%(p)s-naout{fill:none;stroke:var(--na);stroke-width:1.6;stroke-dasharray:3 3;}
.%(p)s-naouth{fill:none;stroke:var(--na);stroke-width:1.6;stroke-linejoin:round;}
.%(p)s-naoutt{font-size:11.5px;font-weight:700;fill:var(--na);text-anchor:middle;}
.%(p)s-rh{font-size:13px;font-weight:800;fill:var(--ink);}
.%(p)s-rl{font-size:12px;fill:var(--dim);text-anchor:end;}
.%(p)s-rv{font-size:12.5px;font-weight:800;fill:var(--ink);}
@media (max-width:820px){.%(p)s-wrap{margin:10px 0 0;}}
""" % {'p': P}


def build():
    o = [efig.css(P, CSS),
         efig.open_card(
             P, CID,
             'カルシウムの出口は太く、ナトリウムの出口は細い',
             '雨が岩から溶かし出したカルシウム（橙）とナトリウム（紫）が、川を下って海へ入るところを'
             '描きました。下の帯は、海に入ってから出ていくまでの平均の時間（滞留時間）です。'
             '貝殻や帯にカーソルを合わせる（スマホはタップ）と説明が出ます。')]
    o.append('<div class="%s-wrap">%s</div>' % (P, build_svg()))
    o.append(efig.close_card(
        P,
        'カルシウムは、貝やサンゴに取りこまれて<b>海底へ出ていきます</b>。'
        'ナトリウムの出口は細く、<b>入る量と釣り合うところまで、海はうんと濃くなりました。</b>'
        '塩のもう半分の塩化物イオンは、岩ではなく<b>大昔の火山のガス</b>から来たと考えられています。',
        '模式図です。粒の数や位置は量を表していません。海は、入る量と出る量が釣り合った状態にあり、塩分は少なくとも数億年、大きくは変わっていなかったと考えられています。滞留時間は、カルシウムが約100万年'
        '（Broecker &amp; Peng 1982）。ナトリウムは出ていく道の見積もり方によって資料ごとに'
        '約5000万〜8000万年と幅があるため、帯の先をぼかしました。帯の長さは同じ物差しです。'
        '塩化物イオンの起源は Rubey (1951) 以来の定説によります。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    print('Na/Ca の滞留時間の比: %d〜%d 倍' % (RES_NA_LO / RES_CA, RES_NA_HI / RES_CA))
    efig.save('_fig2_budget.qmd', build())
