# -*- coding: utf-8 -*-
"""
元素 #6 アルミニウム / 図4 : 雨に打たれるほど、アルミが濃くなる。

岩（長石）→ 粘土（カオリナイト）→ ボーキサイト（ギブサイト）の3段で、
アルミとケイ素が重さの何%を占めるかを棒で並べる。段のあいだには、
雨が運び去るものを書く。

  カリ長石   KAlSi3O8        Al  9.7 %  Si 30.3 %
  カオリナイト Al2Si2O5(OH)4   Al 20.9 %  Si 21.8 %
  ギブサイト  Al(OH)3         Al 34.6 %  Si  0   %

割合は化学式と原子量（IUPAC 2021 の慣用値）から、この場で計算する。
写さない。

反応（釣り合いは確認済み）:
  2 KAlSi3O8 + 2 H+ + 9 H2O → Al2Si2O5(OH)4 + 2 K+ + 4 H4SiO4
  Al2Si2O5(OH)4 + 5 H2O → 2 Al(OH)3 + 2 H4SiO4

#5 の図5（溶存シリカ）の続きになる図。流れ去る H4SiO4 が、#5 で
「水と一緒に長く旅をする」と書いたケイ酸である。

出力: _fig4_weathering.qmd
"""
import efig

P, CID = 'alwea', 'alwea1'

AW = dict(H=1.008, O=15.999, K=39.098, Al=26.982, Si=28.085)


def frac(f, el):
    m = sum(AW[e] * n for e, n in f.items())
    return 100.0 * AW[el] * f.get(el, 0) / m


STAGES = [
    ('岩', '長石', 'カリ長石 KAlSi₃O₈', dict(K=1, Al=1, Si=3, O=8),
     '花崗岩の主成分です。<b>地殻でいちばん多い鉱物</b>が、この長石の仲間です。'
     'アルミは重さの約10%しかなく、<b>ケイ素のほうが3倍多い</b>。'),
    ('粘土', 'カオリナイト', 'Al₂Si₂O₅(OH)₄', dict(Al=2, Si=2, O=9, H=4),
     '雨が長石からカリウムとケイ素の一部を運び去ると、<b>粘土</b>が残ります。'
     'アルミは約21%に<b>倍増</b>。瀬戸物の茶碗の原料になる粘土（カオリン）の主成分が、'
     'このカオリナイトです。'),
    ('ボーキサイト', 'ギブサイト', 'Al(OH)₃', dict(Al=1, O=3, H=3),
     'さらに何百万年も雨に打たれ続けると、<b>ケイ素まで抜けきって</b>、'
     'アルミの水酸化物だけが残ります。これが<b>アルミの鉱石、ボーキサイト</b>の主成分です。'
     'この鉱物だけで見れば、アルミは約35%、ケイ素は<b>ゼロ</b>です。'),
]

GONE = [
    ('カリウム', 'ケイ素の一部'),
    ('残りのケイ素', ''),
]

W, H = 680, 330
COLW = 170
CX = [110, 340, 570]         # 各段の中心
BASE = 262                   # 棒の下端
SCALE = 5.2                  # 1 % あたりの px（35 % で 182 px）
BW = 30


def build_svg():
    o = ['<svg viewBox="0 0 %d %d" role="img" aria-label="長石から粘土、'
         'ボーキサイトへと風化が進むにつれ、アルミの割合が増えケイ素が減る様子を示した図">'
         % (W, H)]
    # 雨
    for i in range(18):
        x = 18 + i * 37
        o.append('<path class="%s-rain" style="animation-delay:%.2fs" d="M%d 0 l-4 12"/>'
                 % (P, (i * 0.37) % 1.4, x))
    # 地殻平均の線
    y8 = BASE - 8.2 * SCALE
    o.append('<line class="%s-avg" x1="20" y1="%.1f" x2="%d" y2="%.1f"/>' % (P, y8, W - 20, y8))
    o.append('<text class="%s-avgt" x="24" y="%.1f">地殻の平均（アルミ 約8%%）</text>'
             % (P, y8 - 5))

    for i, (stage, name, formula, f, detail) in enumerate(STAGES):
        cx = CX[i]
        al, si = frac(f, 'Al'), frac(f, 'Si')
        o.append('<g class="%s-st" data-detail="%s">' % (P, efig.attr(detail)))
        o.append('<rect class="%s-hit" x="%d" y="30" width="%d" height="%d"/>'
                 % (P, cx - COLW // 2, COLW, H - 30))
        # アルミの棒
        ha = al * SCALE
        o.append('<rect class="%s-al" x="%d" y="%.1f" width="%d" height="%.1f" rx="4"/>'
                 % (P, cx - BW - 4, BASE - ha, BW, ha))
        o.append('<text class="%s-va" x="%d" y="%.1f">%d%%</text>'
                 % (P, cx - BW // 2 - 4, BASE - ha - 7, round(al)))
        # ケイ素の棒
        hs = si * SCALE
        if hs > 0:
            o.append('<rect class="%s-si" x="%d" y="%.1f" width="%d" height="%.1f" rx="4"/>'
                     % (P, cx + 4, BASE - hs, BW, hs))
        o.append('<text class="%s-vs" x="%d" y="%.1f">%d%%</text>'
                 % (P, cx + BW // 2 + 4, BASE - hs - 7, round(si)))
        o.append('<line class="%s-bl" x1="%d" y1="%d" x2="%d" y2="%d"/>'
                 % (P, cx - 50, BASE, cx + 50, BASE))
        o.append('<text class="%s-sn" x="%d" y="%d">%s</text>' % (P, cx, BASE + 22, stage))
        o.append('<text class="%s-mn" x="%d" y="%d">%s</text>' % (P, cx, BASE + 40, name))
        o.append('<text class="%s-fm" x="%d" y="%d">%s</text>' % (P, cx, BASE + 56, formula))
        o.append('</g>')

    # 段のあいだ：雨が運び去るもの
    for i, (a, b) in enumerate(GONE):
        mx = (CX[i] + CX[i + 1]) / 2
        o.append('<text class="%s-gh" x="%.1f" y="112">雨が運び去る</text>' % (P, mx))
        o.append('<text class="%s-g" x="%.1f" y="130">%s</text>' % (P, mx, a))
        if b:
            o.append('<text class="%s-g" x="%.1f" y="147">%s</text>' % (P, mx, b))
        o.append('<text class="%s-arr" x="%.1f" y="%d">⟶</text>' % (P, mx, 176 if b else 160))

    # 凡例
    o.append('<rect class="%s-al" x="24" y="40" width="14" height="14" rx="3"/>' % P)
    o.append('<text class="%s-lg" x="44" y="52">アルミ</text>' % P)
    o.append('<rect class="%s-si" x="96" y="40" width="14" height="14" rx="3"/>' % P)
    o.append('<text class="%s-lg" x="116" y="52">ケイ素</text>' % P)
    o.append('<text class="%s-lg2" x="24" y="72">（重さに占める割合）</text>' % P)
    o.append('</svg>')
    return '\n'.join(o)


CSS = """
.%(p)s{--al:#5B6F80;--si:#8A6B36;--rain:#7FA7C4;}
.%(p)s-wrap{margin:14px 8px 0;}
.%(p)s-wrap svg{display:block;width:100%%;height:auto;}
.%(p)s-wrap text{font-family:"Hiragino Sans","Yu Gothic","Noto Sans JP",sans-serif;}
.%(p)s-hit{fill:transparent;}
.%(p)s-st{cursor:default;}
.%(p)s-st:hover .%(p)s-hit{fill:rgba(122,96,52,.06);}
.%(p)s-al{fill:var(--al);}
.%(p)s-si{fill:var(--si);}
.%(p)s-va{font-size:14px;font-weight:800;fill:var(--al);text-anchor:middle;
  font-variant-numeric:tabular-nums;}
.%(p)s-vs{font-size:12.5px;font-weight:700;fill:var(--si);text-anchor:middle;
  font-variant-numeric:tabular-nums;}
.%(p)s-bl{stroke:var(--line);stroke-width:1.5;}
.%(p)s-sn{font-size:15px;font-weight:800;fill:var(--ink);text-anchor:middle;}
.%(p)s-mn{font-size:12px;fill:var(--dim);text-anchor:middle;}
.%(p)s-fm{font-size:11px;fill:var(--faint);text-anchor:middle;}
.%(p)s-arr{font-size:26px;fill:var(--rain);text-anchor:middle;}
.%(p)s-gh{font-size:11px;fill:var(--faint);text-anchor:middle;}
.%(p)s-g{font-size:12.5px;font-weight:700;fill:#2F6D9E;text-anchor:middle;}
.%(p)s-avg{stroke:var(--al);stroke-width:1;stroke-dasharray:4 4;opacity:.55;}
.%(p)s-avgt{font-size:10.5px;fill:var(--al);text-anchor:start;opacity:.9;}
.%(p)s-lg{font-size:12px;fill:var(--dim);}
.%(p)s-lg2{font-size:10.5px;fill:var(--faint);}
.%(p)s-rain{stroke:var(--rain);stroke-width:1.6;stroke-linecap:round;opacity:0;
  animation:%(p)s-rain 1.4s linear infinite;}
@keyframes %(p)s-rain{0%%{transform:translateY(0);opacity:0;}
  15%%{opacity:.55;}100%%{transform:translateY(34px);opacity:0;}}
@media (max-width:820px){.%(p)s-wrap{margin:10px 0 0;}}
""" % {'p': P}


def build():
    o = [efig.css(P, CSS),
         efig.open_card(
             P, CID,
             '雨に打たれるほど、アルミが濃くなります',
             '岩が雨に打たれて粘土になり、さらに打たれてボーキサイトになるまでを、'
             '左から順に並べました。棒は、アルミとケイ素が重さの何%を占めるか。'
             '段にカーソルを合わせる（スマホはタップ）と説明が出ます。')]
    o.append('<div class="%s-wrap">%s</div>' % (P, build_svg()))
    o.append(efig.close_card(
        P,
        '雨が運び去るのは、<b>水に溶けるもの</b>です。まずカリウムとケイ素の一部、'
        '最後には残りのケイ素まで。<b>アルミは水に溶けにくいので、動かずに残ります。</b>'
        'そのたびにアルミの割合は上がり、10% → 21% → 35%。'
        '<b>アルミの鉱石は、雨が作ったもの</b>です。',
        '割合は化学式と原子量から計算しました（端数は四捨五入）。反応はそれぞれ '
        '2KAlSi₃O₈ ＋ 2H⁺ ＋ 9H₂O → Al₂Si₂O₅(OH)₄ ＋ 2K⁺ ＋ 4H₄SiO₄、'
        'Al₂Si₂O₅(OH)₄ ＋ 5H₂O → 2Al(OH)₃ ＋ 2H₄SiO₄。'
        '流れ去る H₄SiO₄ が、前回の「水に溶けたケイ素（ケイ酸）」です。'
        '実際のボーキサイトは、ギブサイトのほかベーマイトなどの水酸化アルミの鉱物と、'
        '鉄の酸化物を含むので、掘り出したもののアルミは重さの 2〜3 割ほどです。長石はナトリウムやカルシウムを含む種類もあり、'
        '流れ去る陽イオンはそれに応じて変わります。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    for stage, name, formula, f, _ in STAGES:
        print('%-8s %-10s Al %5.1f %%  Si %5.1f %%' % (stage, name, frac(f, 'Al'), frac(f, 'Si')))
    efig.save('_fig4_weathering.qmd', build())
