# -*- coding: utf-8 -*-
"""
元素 #5 ケイ素 / 図4 : 1000億分の1まで汚れを落としてから、わざと汚す。

この記事でいちばん面白いところを図にする。

  半導体用のケイ素は 11N（99.999999999%）まで精製される。
  残る汚れは 1000 億分の 1 以下。
  ところが、そこへ<b>狙った不純物を混ぜる</b>。その量が
  だいたい 10 億分の 1 〜 10 万分の 1 で、
  <b>落としきった汚れよりも桁違いに多い。</b>

  -> 「純度を極めてから、狙って汚す」という逆説が、絵として立つ。

数値（いずれも本文・出典行に明記する）:
  冶金級シリコン   Si 98〜99%     -> 汚れ 1e-2 くらい
  太陽電池級  6N   99.9999%       -> 汚れ 1e-6
  半導体級   11N   99.999999999%  -> 汚れ 1e-11
  ドーピング量     1e14〜1e18 cm^-3 を、ケイ素 5e22 cm^-3 で割ると
                   2e-9 〜 2e-5（10 億分の 2 〜 10 万分の 2）

出力: _fig4_purity.qmd
"""
import math

import efig

P, CID = 'sipur', 'sipur1'

# 対数目盛（汚れの割合）。上ほど汚い。
TOP, BOT = -1.0, -12.0          # 10^-1 〜 10^-12
W, H = 660, 330
X0, X1 = 132, 596               # 目盛帯の左右
Y0, Y1 = 46, 250                # 上端 / 下端

SI_DENS = 5.0e22                # ケイ素の原子密度 cm^-3
DOPE_LO, DOPE_HI = 1.0e14, 1.0e18


def y(ex):
    """10^ex の位置を返す。"""
    return Y0 + (TOP - ex) / (TOP - BOT) * (Y1 - Y0)


RUNGS = [
    (-2.0, '冶金級シリコン', 'Si 98〜99%',
     '砂（石英）を炭素と一緒に電気炉で還元して作る、いちばん粗いケイ素です。'
     '<b>汚れが 1〜2%</b> 残っています。'
     '鉄やアルミの材料としてはこれで十分ですが、'
     'このままでは電気の流れを制御できません。'),
    (-6.0, '太陽電池級（6N）', '99.9999%',
     '<b>汚れは 100 万分の 1</b>。太陽光パネルはこの純度で作られます。'
     '半導体ほどの精度は要らないぶん、安く大量に作れます。'),
    (-11.0, '半導体級（11N）', '99.999999999%',
     '<b>汚れは 1000 億分の 1 以下。</b>'
     '人が日常的に大量生産しているものの中で、'
     'もっともきれいな物質のひとつです。'
     '（12N と書かれることがありますが、'
     '実際の生産で確かめられているのは 11N までとされています。）'),
]


def build_svg():
    o = ['<svg viewBox="0 0 %d %d" role="img" '
         'aria-label="ケイ素の純度と、混ぜる不純物の量を対数目盛で比べた図">' % (W, H)]

    # 目盛の横線と数字
    for e in range(-1, -13, -1):
        yy = y(e)
        o.append('<line class="%s-gl" x1="%d" y1="%.1f" x2="%d" y2="%.1f"/>'
                 % (P, X0, yy, X1, yy))
        o.append('<text class="%s-tk" x="%d" y="%.1f">10<tspan class="%s-sup" '
                 'dy="-5">−%d</tspan></text>' % (P, X0 - 10, yy + 4, P, -e))
    o.append('<text class="%s-ax" x="%d" y="%.1f">残っている汚れの割合</text>'
             % (P, X0 - 10, Y0 - 18))

    # 純度の段
    for ex, name, val, _d in RUNGS:
        yy = y(ex)
        o.append('<circle class="%s-dot" cx="%d" cy="%.1f" r="7"/>'
                 % (P, X0 + 34, yy))
        o.append('<text class="%s-rn" x="%d" y="%.1f">%s</text>'
                 % (P, X0 + 50, yy - 2, name))
        o.append('<text class="%s-rv" x="%d" y="%.1f">%s</text>'
                 % (P, X0 + 50, yy + 15, val))
    # 精製の矢印
    o.append('<path class="%s-arw" d="M%d %.1f V%.1f"/>'
             % (P, X0 + 34, y(-2.0) + 14, y(-11.0) - 14))
    o.append('<text class="%s-arl" x="%d" y="%.1f" text-anchor="middle" '
             'transform="rotate(-90 %d %.1f)">精製</text>'
             % (P, X0 + 18, (y(-2.0) + y(-11.0)) / 2, X0 + 18,
                (y(-2.0) + y(-11.0)) / 2))

    # 混ぜる不純物の帯
    ylo, yhi = y(math.log10(DOPE_HI / SI_DENS)), y(math.log10(DOPE_LO / SI_DENS))
    o.append('<rect class="%s-band" x="%d" y="%.1f" width="%d" height="%.1f" '
             'rx="6"/>' % (P, X1 - 176, ylo, 172, yhi - ylo))
    o.append('<text class="%s-bl" x="%d" y="%.1f">狙って入れる不純物</text>'
             % (P, X1 - 168, ylo + 20))
    o.append('<text class="%s-bs" x="%d" y="%.1f">リン や ホウ素</text>'
             % (P, X1 - 168, ylo + 38))
    o.append('<text class="%s-bs" x="%d" y="%.1f">10 億分の 2 〜 10 万分の 2</text>'
             % (P, X1 - 168, ylo + 56))

    # 比較の縦棒
    o.append('<path class="%s-cmp" d="M%d %.1f V%.1f"/>'
             % (P, X1 - 196, ylo, y(-11.0)))
    o.append('<text class="%s-cl" x="%d" y="%.1f" text-anchor="end">'
             'この差が 200 倍以上</text>'
             % (P, X1 - 204, (ylo + y(-11.0)) / 2))

    o.append('</svg>')
    return '\n'.join(o)


CSS = """
.%(p)s{--pu:#0F6C8A;--dp:#BE640A;--gl:#E0D7C6;}
.%(p)s-wrap{margin:20px 8px 0;}
.%(p)s-wrap svg{display:block;width:100%%;height:auto;}
.%(p)s-gl{stroke:var(--gl);stroke-width:1;}
.%(p)s-tk{font-size:12px;fill:var(--faint);text-anchor:end;
  font-variant-numeric:tabular-nums;}
.%(p)s-sup{font-size:9px;}
.%(p)s-ax{font-size:12px;fill:var(--dim);text-anchor:end;}
.%(p)s-dot{fill:var(--pu);}
.%(p)s-rn{font-size:15px;font-weight:800;fill:var(--ink);}
.%(p)s-rv{font-size:12px;fill:var(--dim);font-variant-numeric:tabular-nums;}
.%(p)s-arw{stroke:var(--pu);stroke-width:2;fill:none;opacity:.45;
  stroke-dasharray:5 5;}
.%(p)s-arl{font-size:11px;fill:var(--pu);opacity:.8;}
.%(p)s-band{fill:rgba(190,100,10,.16);stroke:var(--dp);stroke-width:2;}
.%(p)s-bl{font-size:14px;font-weight:800;fill:var(--dp);}
.%(p)s-bs{font-size:11.5px;fill:var(--dim);}
.%(p)s-cmp{stroke:var(--dp);stroke-width:2;fill:none;}
.%(p)s-cl{font-size:12px;font-weight:700;fill:var(--dp);}
.%(p)s-wrap text{font-family:"Hiragino Sans","Yu Gothic","Noto Sans JP",sans-serif;}

.%(p)s-rw{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;
  margin:16px 8px 0;}
.%(p)s-r{padding:12px 14px;border-radius:11px;cursor:default;
  background:rgba(15,108,138,.07);border:1px solid rgba(15,108,138,.22);
  transition:background .18s ease;}
.%(p)s-r:hover{background:rgba(15,108,138,.15);}
.%(p)s-r b{display:block;font-size:.92rem;font-weight:800;color:var(--pu);}
.%(p)s-r s{text-decoration:none;font-size:.8rem;color:var(--dim);
  font-variant-numeric:tabular-nums;}

.%(p)s-hit{margin:18px 8px 0;padding:15px 17px;border-radius:12px;
  background:rgba(190,100,10,.09);border:1px solid rgba(190,100,10,.26);}
.%(p)s-hit .a{font-size:1.3rem;font-weight:800;color:var(--dp);
  line-height:1.45;}
.%(p)s-hit .b{font-size:.88rem;color:var(--dim);margin-top:4px;line-height:1.7;}

@media (max-width:820px){
  .%(p)s-wrap{margin:14px 2px 0;}
  .%(p)s-rw{grid-template-columns:1fr;margin:12px 2px 0;gap:8px;}
  .%(p)s-hit{margin:14px 2px 0;padding:13px 14px;}
  .%(p)s-hit .a{font-size:1.02rem;}
}
""" % {'p': P}


def build():
    o = [efig.css(P, CSS),
         efig.open_card(
             P, CID,
             '1000 億分の 1 まできれいにしてから、わざと汚します',
             '縦軸は「残っている汚れの割合」で、下へ行くほどきれいです。'
             '目盛は 1 つ下がるごとに 10 分の 1 になります。'
             '下の 3 枚にカーソルを合わせる（スマホはタップ）と説明が出ます。')]

    o.append('<div class="%s-wrap">%s</div>' % (P, build_svg()))

    o.append('<div class="%s-rw">' % P)
    for _ex, name, val, detail in RUNGS:
        o.append('<div class="%s-r" data-detail="%s"><b>%s</b><s>%s</s></div>'
                 % (P, efig.attr(detail), name, val))
    o.append('</div>')

    o.append('<div class="%s-hit" data-detail="%s">'
             '<div class="a">落としきった汚れより、入れる量のほうが多い</div>'
             '<div class="b">残った汚れは 1000 億分の 1 以下。'
             'そこへ混ぜるリンやホウ素は、少ないときでも 10 億分の 2 ほど。'
             '<b>200 倍以上あります。</b>'
             'ここまできれいにするのは、'
             '<b>入れた分だけがきっちり効くようにするため</b>です。</div></div>'
             % (P, efig.attr(
                 '汚れが残っていると、それも電気の流れを変えてしまいます。'
                 '<b>狙って入れた分と、たまたま残った分の区別がつかなくなる。</b>'
                 'だからいったん徹底的に落とし、'
                 'それから必要な量だけを、狙って入れます。')))

    o.append(efig.close_card(
        P,
        '砂から取り出したばかりのケイ素は、<b>1〜2% が汚れ</b>です。'
        'そこから汚れを 1000 億分の 1 以下まで落としたものが、'
        '半導体用のケイ素になります。'
        '<b>ところが、そのあとで不純物を混ぜます。</b>'
        'リンやホウ素を、<b>10 億分の 2 から 10 万分の 2 ほど</b>。'
        '落としきった汚れの 200 倍以上の量です。'
        '<b>きれいにするのは、汚し方を思いどおりにするためでした。</b>',
        '純度の表記は、9 の個数で数える慣習によります'
        '（6N ＝ 99.9999%、11N ＝ 99.999999999%）。'
        '半導体用の多結晶シリコンは 9N〜11N とされ、'
        '12N をうたう例もありますが、実生産で確かめられているのは 11N までです'
        '（<a href="https://www.bernreuter.com/newsroom/polysilicon-news/article/a-silicon-purity-of-12n-only-exists-in-the-world-of-marketers/">Bernreuter Research</a>）。'
        '混ぜる量は、ケイ素の原子密度 5×10²² 個/cm³ に対し、'
        'ドーピング濃度 10¹⁴〜10¹⁸ 個/cm³ を割ったものです'
        '（＝2×10⁻⁹〜2×10⁻⁵）。用途によってこの幅の中で使い分けます。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    print('ドーピング割合  下限 %.1e  上限 %.1e'
          % (DOPE_LO / SI_DENS, DOPE_HI / SI_DENS))
    print('11N の汚れ 1e-11 に対する倍率  下限 %.0f 倍  上限 %.0f 倍'
          % (DOPE_LO / SI_DENS / 1e-11, DOPE_HI / SI_DENS / 1e-11))
    efig.save('_fig4_purity.qmd', build())
