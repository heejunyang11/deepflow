# -*- coding: utf-8 -*-
"""
元素 #5 ケイ素 / 図5 : 大地になったケイ素も、少しだけ溶けて旅をしている。

第2回（炭素）は「炭素は生き物になり、ケイ素は大地になった。
二酸化ケイ素はいちど岩になったらそこから動きません」で終えた。
その但し書きを、ここで付ける。まったく動かないわけではない。

  石英の溶解度（25℃）        6.8 mg/L
  川や地下水の実際            おおむね 1〜30 mg/L
  非晶質シリカの溶解度（25℃） 約 115 mg/L
  地熱の貯留水（200〜350℃）   300〜700 mg/L

温度が上がると溶解度が跳ね上がる -> 地下深くで溶け込む
地表で急に冷える -> 溶けきれずに析出する（温泉のスケール、珪華）
この筋道が、DeepFlows の地下水・地球化学の記事へそのまま繋がる。

出力: _fig5_dissolved.qmd
"""
import math

import efig

P, CID = 'sidis', 'sidis1'

W, H = 660, 250
X0, X1 = 74, 604
YAX = 176                        # 目盛線の高さ
LO, HI = 1.0, 1000.0             # mg/L（対数）


def x(v):
    return X0 + (math.log10(v) - math.log10(LO)) / \
        (math.log10(HI) - math.log10(LO)) * (X1 - X0)


# (値または範囲, 見出し, 副題, 段, 色キー, 説明)
MARKS = [
    ((6.8, None), '石英の溶解度', '25℃ で 6.8 mg/L', 0, 'qz',
     '水晶や砂の石英が、常温の水にどこまで溶けるかの上限です。'
     '<b>ごくわずかですが、ゼロではありません。</b>'
     '砂の主成分が「まったく動かないもの」ではないことが、この数字に出ています。'),
    ((1.0, 30.0), '川や地下水', 'おおむね 1〜30 mg/L', 1, 'nat',
     '実際の自然の水に溶けているシリカの量です。'
     '花崗岩の地域では高く、石灰岩の地域では低くなります。'
     '<b>水がどんな岩の中を通ってきたかが、この数字に残ります。</b>'
     '地下水の履歴を読む手がかりのひとつです。'),
    ((115.0, None), '非晶質シリカの溶解度', '25℃ で約 115 mg/L', 0, 'am',
     '同じ SiO₂ でも、<b>乱れた並び方（ガラス状）のほうがよく溶けます</b>。'
     '整列した石英より 17 倍ほど多く溶けます。'
     '図1で見た「並び方の違い」が、溶けやすさにも効いています。'),
    ((300.0, 700.0), '地熱の貯留水', '200〜350℃ で 300〜700 mg/L', 1, 'geo',
     '地下深くの熱い水です。<b>温度が上がると、石英ははるかによく溶けます。</b>'
     'この水が地表へ上がって急に冷えると、溶けきれなくなった分が'
     '<b>非晶質シリカとして析出</b>します。'
     '温泉の配管に付くスケールや<b>珪華</b>がこれです。'
     '（「湯の花」は硫黄や炭酸カルシウムのことも多く、'
     'シリカとは限りません。）'),
]

COLORS = {'qz': '#2E6E4E', 'nat': '#5E96C4', 'am': '#BE640A', 'geo': '#B02A37'}

JOURNEY = [
    ('岩', '花崗岩や砂岩の中の石英・長石',
     '雨水が地面にしみ込み、岩と触れ合いながらゆっくり流れます。'
     'このあいだに、石英や長石がわずかずつ溶けます。'
     '<a href="/posts/phreeqc/phreeqc-part11/">PHREEQC #11</a> で'
     '扱った花崗岩の風化が、まさにこの過程です。'),
    ('水', '溶けたケイ酸として運ばれる',
     'ケイ素は <b>ケイ酸（H₄SiO₄）</b> という形で水に溶けます。'
     '電気を帯びていないため、陽イオンに比べれば土に留まりにくく、'
     '水と一緒に長く旅をします（鉄・アルミの酸化物には吸着します）。'
     '<a href="/posts/groundwater/groundwater-sci15/">地下水科学入門 #15</a> では、'
     'この溶けたシリカから地下水の滞留時間を読みました。'),
    ('また固まる', '殻になる／沈殿する',
     '海では<b>珪藻</b>が、この溶けたシリカを取り込んでガラスの殻を作ります。'
     '温泉では、冷えた水から<b>シリカが析出して珪華</b>になります。'
     '大地から溶け出したケイ素が、また固まるところです。'),
]

CSS = """
.%(p)s{--qz:#2E6E4E;--nat:#5E96C4;--am:#BE640A;--geo:#B02A37;--gl:#E0D7C6;}
.%(p)s-wrap{margin:20px 8px 0;}
.%(p)s-wrap svg{display:block;width:100%%;height:auto;}
.%(p)s-wrap text{font-family:"Hiragino Sans","Yu Gothic","Noto Sans JP",sans-serif;}
.%(p)s-ax{stroke:#B9AE99;stroke-width:1.5;}
.%(p)s-gl{stroke:var(--gl);stroke-width:1;}
.%(p)s-tk{font-size:11.5px;fill:var(--faint);text-anchor:middle;
  font-variant-numeric:tabular-nums;}
.%(p)s-un{font-size:11.5px;fill:var(--dim);}
.%(p)s-pin{stroke-width:2;}
.%(p)s-dot{stroke:#FFFDF9;stroke-width:1.6;}
.%(p)s-bar{opacity:.30;}
.%(p)s-nm{font-size:13.5px;font-weight:800;}
.%(p)s-sb{font-size:11px;fill:var(--dim);}

.%(p)s-key{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;
  margin:14px 8px 0;}
.%(p)s-k{padding:11px 13px;border-radius:11px;cursor:default;
  background:rgba(122,96,52,.05);border:1px solid rgba(122,96,52,.14);
  border-left:4px solid var(--c);transition:background .18s ease;}
.%(p)s-k:hover{background:rgba(122,96,52,.14);}
.%(p)s-k b{display:block;font-size:.88rem;font-weight:800;color:var(--c);}
.%(p)s-k s{text-decoration:none;font-size:.76rem;color:var(--dim);
  font-variant-numeric:tabular-nums;}

.%(p)s-jr{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;
  margin:18px 8px 0;}
.%(p)s-j{padding:13px 15px;border-radius:11px;cursor:default;
  background:rgba(94,150,196,.09);border:1px solid rgba(94,150,196,.26);
  transition:background .18s ease;}
.%(p)s-j:hover{background:rgba(94,150,196,.19);}
.%(p)s-j b{display:block;font-size:.98rem;font-weight:800;color:#2E5F86;
  margin-bottom:2px;}
.%(p)s-j s{text-decoration:none;font-size:.8rem;color:var(--dim);
  line-height:1.65;}

@media (max-width:820px){
  .%(p)s-wrap{margin:14px 2px 0;}
  .%(p)s-key{grid-template-columns:1fr 1fr;margin:12px 2px 0;gap:7px;}
  .%(p)s-jr{grid-template-columns:1fr;margin:14px 2px 0;}
}
""" % {'p': P}


def build_svg():
    o = ['<svg viewBox="0 0 %d %d" role="img" '
         'aria-label="水に溶けているケイ素の量を、対数目盛で並べた図">' % (W, H)]

    for e in range(0, 4):
        v = 10 ** e
        xx = x(v)
        o.append('<line class="%s-gl" x1="%.1f" y1="40" x2="%.1f" y2="%d"/>'
                 % (P, xx, xx, YAX))
        o.append('<text class="%s-tk" x="%.1f" y="%d">%s</text>'
                 % (P, xx, YAX + 20, format(v, ',')))
    o.append('<line class="%s-ax" x1="%d" y1="%d" x2="%d" y2="%d"/>'
             % (P, X0, YAX, X1, YAX))
    o.append('<text class="%s-un" x="%d" y="%d">溶けているシリカ（mg/L, SiO₂ として）'
             '　目盛は 1 つで 10 倍</text>' % (P, X0, YAX + 40))

    for (a, b), name, sub, tier, ck, _d in MARKS:
        c = COLORS[ck]
        yy = 96 if tier == 0 else 138
        if b is None:
            xx = x(a)
            o.append('<line class="%s-pin" x1="%.1f" y1="%.1f" x2="%.1f" '
                     'y2="%d" stroke="%s"/>' % (P, xx, yy + 6, xx, YAX, c))
            o.append('<circle class="%s-dot" cx="%.1f" cy="%d" r="6" '
                     'fill="%s"/>' % (P, xx, YAX, c))
            tx, anc = xx, 'middle'
        else:
            xa, xb = x(a), x(b)
            o.append('<rect class="%s-bar" x="%.1f" y="%d" width="%.1f" '
                     'height="14" rx="7" fill="%s"/>'
                     % (P, xa, YAX - 7, xb - xa, c))
            o.append('<line class="%s-pin" x1="%.1f" y1="%.1f" x2="%.1f" '
                     'y2="%d" stroke="%s" opacity=".7"/>'
                     % (P, (xa + xb) / 2, yy + 6, (xa + xb) / 2, YAX - 7, c))
            tx, anc = (xa + xb) / 2, 'middle'
        o.append('<text class="%s-nm" x="%.1f" y="%d" text-anchor="%s" '
                 'fill="%s">%s</text>' % (P, tx, yy - 8, anc, c, name))
        o.append('<text class="%s-sb" x="%.1f" y="%d" text-anchor="%s">%s</text>'
                 % (P, tx, yy + 6, anc, sub))
    o.append('</svg>')
    return '\n'.join(o)


def build():
    o = [efig.css(P, CSS),
         efig.open_card(
             P, CID,
             '大地になったケイ素も、少しずつ溶けて旅をしています',
             '水に溶けているシリカの量を並べました。'
             '目盛は 1 つ進むごとに 10 倍です。'
             '下の札にカーソルを合わせる（スマホはタップ）と説明が出ます。')]

    o.append('<div class="%s-wrap">%s</div>' % (P, build_svg()))

    o.append('<div class="%s-key">' % P)
    for (a, b), name, sub, _t, ck, detail in MARKS:
        o.append('<div class="%s-k" data-detail="%s" style="--c:%s">'
                 '<b>%s</b><s>%s</s></div>'
                 % (P, efig.attr(detail), COLORS[ck], name, sub))
    o.append('</div>')

    o.append('<div class="%s-jr">' % P)
    for name, sub, detail in JOURNEY:
        o.append('<div class="%s-j" data-detail="%s"><b>%s</b><s>%s</s></div>'
                 % (P, efig.attr(detail), name, sub))
    o.append('</div>')

    o.append(efig.close_card(
        P,
        '<a href="/posts/note/element-02-carbon/">第2回</a>で、'
        '「二酸化ケイ素はいちど岩になったら動かない」と書きました。'
        '<b>正確には、とてもゆっくり動きます。</b>'
        '常温の水に溶ける石英はせいぜい 6.8 mg/L ですが、'
        '<b>地下深くの熱い水では 300〜700 mg/L にもなります。</b>'
        'その水が地表で冷えると、溶けきれない分が析出する——'
        '温泉地の珪華や、配管に付くスケールがそれです。'
        '海では珪藻がこれを取り込んで、ガラスの殻を作ります。',
        '石英の溶解度 25℃ 約 6.8 mg/L'
        '（Morey, Fournier &amp; Rowe, 1962, <i>Geochim. Cosmochim. Acta</i> <b>26</b>；'
        '報告値には 6〜11 mg/L の幅があります）、'
        '非晶質シリカ 約 115 mg/L'
        '（<a href="https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/JZ069i010p01995">'
        'Morey et al., 1964, J. Geophys. Res.</a>）。'
        '自然の水の実測はおおむね 1〜30 mg/L。'
        '地熱の貯留水は 200〜350℃ で 300〜700 mg/kg 程度とされ、'
        'この値は石英の溶解度が温度とともに上がることで決まります。'
        '珪藻の殻は含水の非晶質シリカ（オパール A）です。'
        '地下水と水質の詳しい話は、'
        '<a href="/posts/groundwater/groundwater-sci15/">地下水科学入門 #15</a> と'
        '<a href="/posts/phreeqc/phreeqc-part11/">PHREEQC #11</a> で扱っています。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    print('非晶質 / 石英 = %.1f 倍' % (115.0 / 6.8))
    efig.save('_fig5_dissolved.qmd', build())
