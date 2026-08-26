# -*- coding: utf-8 -*-
"""
元素 #1 水素 / 図6 : 朝の寝癖は、水素結合がズレた位置で結び直された跡である。

旧図（ビッグバンからの年表）を差し替えたもの。
「今日、目の前で観測できるもので書く」という方針に合わせ、
毎朝だれでも確かめられる現象に置き換えた。

髪の主成分はケラチン（タンパク質）で、その形は 4 種類の結びつきで保たれている。
  水素結合    濡らすと切れ、乾かすとつながる      ← 水で切れるのはこれだけ
  塩（イオン）結合  水そのものより pH で外れる（安定は pH 4.5-5.5）
  シスチン結合  1 剤（還元剤）で切れ、2 剤（酸化剤）でつながる = パーマ
  ペプチド結合  切れると二度と戻らない（枝毛）
        → 寝癖は水で直り、パーマは水では落ちない。
出典はデミ コスメティクス「髪の4つの結合」と花王「髪が形づくメカニズム」。
初稿では塩結合も「水で切れる」と書いていたが、出典に当たると pH の話なので分けた。

寝癖ができる順序:
  ① ふだんの髪      結び目が本来の位置にある
  ② 寝ているあいだ  汗と湿気で水素結合がほどけ、枕の力で曲がる
  ③ そのまま乾く    ズレた位置で結び直される  = 寝癖
  ④ 朝、水をかける  もう一度ほどいて、整えて乾かす = 元に戻る

図3（結合エネルギーの数直線）と同じ「ちょうどいい弱さ」の話を、
朝の鏡の前で回収するのがこの図の役目。

出力: _fig6_bedhair.qmd
"""
import math
import efig

P, CID = 'ehair', 'ehair6'

# パネルの SVG 座標系
VW, VH = 158.0, 92.0
X0, X1 = 12.0, 146.0          # 毛の左右端
YC = 46.0                     # 中心線
HALF = 8.6                    # リボンの半幅
NRUNG = 7                     # 結び目（横棒）の本数


def edge(bend, off, n=44):
    """毛の輪郭を一本ぶん。bend は曲がりの深さ（px）、off は中心線からのずれ。"""
    pts = []
    for i in range(n + 1):
        t = i / float(n)
        x = X0 + (X1 - X0) * t
        y = YC + off + bend * math.sin(math.pi * t) * math.sin(math.pi * t * 1.6)
        pts.append('%.2f %.2f' % (x, y))
    return 'M' + ' L'.join(pts)


def ribbon(bend):
    """上下の輪郭を閉じたリボンにする。"""
    up = edge(bend, -HALF)
    dn = edge(bend, HALF)
    dn = dn[1:]                      # 先頭の M を落として逆順につなぐ
    pts = dn.split(' L')
    pts.reverse()
    return up + ' L' + ' L'.join(pts) + ' Z'


def rungs(bend, state, shift=0.0):
    """結び目の横棒。state は 'on'（結ばれている）か 'off'（ほどけている）。

    shift はズレた位置で結び直されたことを表す。寝癖のパネルだけ 0 でない。
    """
    o = []
    for i in range(NRUNG):
        t = (i + 0.5) / float(NRUNG)
        x = X0 + (X1 - X0) * t
        y = YC + bend * math.sin(math.pi * t) * math.sin(math.pi * t * 1.6)
        if state == 'off':
            # ほどけている：上下に離れた短い突起として描く
            o.append('<path d="M%.2f %.2f v3.1" class="%s-rg off"/>'
                     % (x, y - HALF + 1.0, P))
            o.append('<path d="M%.2f %.2f v-3.1" class="%s-rg off"/>'
                     % (x, y + HALF - 1.0, P))
        else:
            xx = x + shift * (1 if i % 2 else -1)
            o.append('<path d="M%.2f %.2f V%.2f" class="%s-rg on"/>'
                     % (xx, y - HALF + 1.0, y + HALF - 1.0, P))
    return ''.join(o)


def drop(x, y, s=1.0):
    """水のしずく。"""
    return ('<path d="M%.2f %.2f c%.2f %.2f %.2f %.2f 0 %.2f '
            'c%.2f %.2f %.2f %.2f 0 %.2f Z" class="%s-drop"/>'
            % (x, y, 2.6 * s, 2.4 * s, 4.0 * s, 4.6 * s, 7.4 * s,
               -4.0 * s, -2.8 * s, -2.6 * s, -2.2 * s, -7.4 * s, P))


def panel(bend, state, shift, wet, tag):
    o = ['<svg viewBox="0 0 %.0f %.0f" aria-hidden="true">' % (VW, VH)]
    # 枕。②③のパネルだけ、毛を押している面として下に敷く
    if tag in ('b', 'c'):
        o.append('<path d="M0 %.0f H%.0f V%.0f H0 Z" class="%s-pil"/>'
                 % (VH - 13, VW, VH, P))
        o.append('<path d="M0 %.0f H%.0f" class="%s-pill"/>' % (VH - 13, VW, P))
    o.append('<path d="%s" class="%s-hair%s"/>'
             % (ribbon(bend), P, ' wet' if wet else ''))
    o.append('<g>%s</g>' % rungs(bend, state, shift))
    if wet:
        for i, (dx, dy, s) in enumerate([(26, 8, .9), (74, 5, 1.1), (118, 9, .8)]):
            o.append('<g class="%s-dg" style="--d:%.1fs">%s</g>'
                     % (P, i * .55, drop(dx, dy, s)))
    o.append('</svg>')
    return ''.join(o)


#  tag, 見出し, 説明, bend, 結び目, ズレ, 濡れているか, 読み取り帯の文
STEPS = [
    ('a', 'ふだんの髪',
     '結び目が、本来の位置にある', 0.0, 'on', 0.0, False,
     'ケラチンという長いタンパク質の鎖が、<b>水素結合</b>で留め合わされています。'
     'この留め金が、髪の形そのものです。'),
    ('b', '寝ているあいだ',
     '汗と湿気で、結び目がほどける', 13.0, 'off', 0.0, True,
     '髪が湿ると、<b>水素結合はあっさりほどけます</b>。'
     '留め金が外れた髪は、枕に押されるまま自由に曲がります。'),
    ('c', 'そのまま乾く',
     'ズレた位置で、結び直される', 13.0, 'on', 2.4, False,
     '乾くと結び目は戻ります。ただし<b>曲がったままの位置で</b>。'
     'これが寝癖です。髪が傷んだのではなく、留め金が掛け違っただけです。'),
    ('d', '朝、水をかける',
     'もう一度ほどいて、結び直す', 0.0, 'on', 0.0, False,
     'もう一度濡らせば、また外れます。整えて乾かせば、'
     '<b>今度は正しい位置で結ばれます</b>。それで直る。'),
]

#  名前, 英字, 何で外れるか（タグの文言と色分け）, 色トークン, 一言, 読み取り帯の文
#    デミ コスメティクス「髪の4つの結合」の記述に合わせてある。
#    塩結合は「水で切れる」ではなく pH で外れるので、水素結合とは分けて書く。
BONDS = [
    ('水素結合', 'hydrogen bond', 'w', 'hb', '髪の形をつくる',
     '<b>この記事の主役です。</b>濡らすと簡単に切れ、乾かすとまたつながる。'
     '寝癖も、ブローで髪型が決まるのも、すべてこの結合のしわざです。'),
    ('塩結合', 'ionic bond', 'p', 'e', 'シャンプーが触る場所',
     'プラスとマイナスの引き合いです。水そのものより<b>液性（pH）で外れます</b>。'
     '髪が落ち着いているのは pH 4.5〜5.5 のあたりで、'
     'シャンプーの液性が手ざわりを変えるのはこのためです。'),
    ('シスチン結合', 'disulfide bond', 'n', 'other', 'パーマが触る場所',
     '硫黄どうしの結びつきで、<b>水ではまったく切れません</b>。'
     'パーマは1剤（還元剤）でこれを切り、2剤（酸化剤）でつなぎ直します。'
     'そのため<b>パーマは洗っても落ちない</b>のです。'),
    ('ペプチド結合', 'peptide bond', 'n', 'cov', 'タンパク質の背骨',
     'アミノ酸をつないで鎖そのものを作っている結合です。'
     '<b>これが切れると、二度と戻りません。</b>枝毛は、この結合が切れた跡です。'),
]

TAG = {'w': ('y', '水で切れる'), 'p': ('p', 'pH で外れる'),
       'n': ('n', '水では切れない')}

CSS = """
.%(p)s-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:11px;
  margin:20px 8px 0;}
.%(p)s-st{position:relative;padding:11px 10px 12px;border-radius:13px;
  background:rgba(122,96,52,.055);border:1px solid rgba(122,96,52,.15);
  cursor:default;transition:background .18s ease,border-color .18s ease;}
.%(p)s-st:hover{background:rgba(122,96,52,.13);
  border-color:rgba(122,96,52,.36);}
.%(p)s-st[data-t="c"]{background:rgba(190,100,10,.085);
  border-color:rgba(190,100,10,.30);}
.%(p)s-st[data-t="c"]:hover{background:rgba(190,100,10,.15);}
.%(p)s-st svg{display:block;width:100%%;height:auto;margin:0 0 8px;}
.%(p)s-num{position:absolute;top:9px;left:11px;font-size:.72rem;
  font-weight:800;color:var(--faint);letter-spacing:.06em;}
.%(p)s-st b{display:block;font-size:.94rem;font-weight:800;color:var(--ink);
  line-height:1.45;}
.%(p)s-st s{display:block;text-decoration:none;font-size:.79rem;
  color:var(--dim);line-height:1.6;margin-top:3px;}
.%(p)s-st[data-t="c"] b{color:var(--hb);}

.%(p)s-hair{fill:#E8D6BC;stroke:#C9AE8B;stroke-width:1.1;}
.%(p)s-hair.wet{fill:#DCCFC0;stroke:#B49E86;}
.%(p)s-pil{fill:rgba(94,150,196,.10);}
.%(p)s-pill{fill:none;stroke:rgba(94,150,196,.42);stroke-width:1;
  stroke-dasharray:3 3;}
.%(p)s-rg{fill:none;stroke-linecap:round;}
.%(p)s-rg.on{stroke:#BE640A;stroke-width:2.2;}
.%(p)s-rg.off{stroke:#B7A88F;stroke-width:2.0;opacity:.7;}
.%(p)s-drop{fill:#5E96C4;opacity:.55;}
.%(p)s-dg{animation:%(p)s-fall 2.6s ease-in infinite;
  animation-delay:var(--d);transform-origin:center;}
@keyframes %(p)s-fall{0%%{opacity:0;transform:translateY(-6px)}
  22%%{opacity:.9}70%%{opacity:.55}100%%{opacity:0;transform:translateY(9px)}}

.%(p)s-blab{margin:22px 8px 8px;font-size:.92rem;color:var(--dim);}
.%(p)s-bl{display:grid;gap:8px;margin:0 8px;}
.%(p)s-b{display:grid;grid-template-columns:1fr auto;align-items:center;
  gap:12px;padding:12px 15px;border-radius:12px;cursor:default;
  background:rgba(122,96,52,.055);border:1px solid rgba(122,96,52,.15);
  border-left:4px solid var(--c);
  transition:background .18s ease;}
.%(p)s-b:hover{background:rgba(122,96,52,.14);}
.%(p)s-b i{font-style:normal;}
.%(p)s-b .nm{font-size:1rem;font-weight:800;color:var(--c);line-height:1.4;}
.%(p)s-b .en{font-size:.74rem;color:var(--faint);letter-spacing:.04em;
  margin-left:7px;font-weight:600;}
.%(p)s-b .sb{display:block;font-size:.81rem;color:var(--dim);
  line-height:1.55;margin-top:2px;}
.%(p)s-tag{font-size:.82rem;font-weight:800;white-space:nowrap;
  padding:4px 11px;border-radius:20px;line-height:1.5;}
.%(p)s-tag.y{color:#0F6C8A;background:rgba(15,108,138,.11);
  border:1px solid rgba(15,108,138,.30);}
.%(p)s-tag.p{color:#7A6AA0;background:rgba(122,106,160,.11);
  border:1px solid rgba(122,106,160,.32);}
.%(p)s-tag.n{color:#8C8271;background:rgba(140,130,113,.10);
  border:1px solid rgba(140,130,113,.30);}

@media (max-width:820px){
  .%(p)s-strip{grid-template-columns:repeat(2,1fr);gap:8px;margin:16px 2px 0;}
  .%(p)s-st{padding:9px 8px 10px;}
  .%(p)s-num{top:7px;left:9px;font-size:.66rem;}
  .%(p)s-st b{font-size:.83rem;}
  .%(p)s-st s{font-size:.72rem;}
  .%(p)s-blab{font-size:.84rem;margin:18px 2px 7px;}
  .%(p)s-bl{margin:0 2px;}
  .%(p)s-b{padding:10px 12px;gap:8px;}
  .%(p)s-b .nm{font-size:.88rem;}
  .%(p)s-b .en{display:none;}
  .%(p)s-b .sb{font-size:.74rem;}
  .%(p)s-tag{font-size:.73rem;padding:3px 9px;}
}
""" % {'p': P}


def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, '寝癖は、留め金の掛け違いです',
                        '髪の形を留めているのは水素結合です。'
                        'パネルにカーソルを合わせる（スマホはタップ）と説明が出ます。')]

    o.append('<div class="%s-strip">' % P)
    for i, (tag, head, sub, bend, state, shift, wet, detail) in enumerate(STEPS):
        o.append('<div class="%s-st" data-t="%s" data-detail="%s">'
                 '<span class="%s-num">%d</span>%s<b>%s</b><s>%s</s></div>'
                 % (P, tag, efig.attr(detail), P, i + 1,
                    panel(bend, state, shift, wet, tag), head, sub))
    o.append('</div>')

    o.append('<p class="%s-blab">髪の形は 4 種類の結びつきで保たれています。'
             'そのうち<b>水で切れるのは、いちばん上の 1 つだけ</b>です。</p>' % P)
    o.append('<div class="%s-bl">' % P)
    for name, en, kind, tok, note, detail in BONDS:
        cls, txt = TAG[kind]
        o.append('<div class="%s-b" data-detail="%s" style="--c:var(--%s)">'
                 '<i><span class="nm">%s<span class="en">%s</span></span>'
                 '<s class="sb">%s</s></i>'
                 '<span class="%s-tag %s">%s</span></div>'
                 % (P, efig.attr(detail), tok, name, en, note, P, cls, txt))
    o.append('</div>')

    o.append(efig.close_card(
        P,
        '寝癖は、髪が傷んだ跡ではありません。'
        '<b>水素結合が、曲がったままの位置で結び直された跡</b>です。'
        'もう一度濡らせばまた外れるので、整えて乾かせば直ります。'
        '一方でパーマが落ちないのは、あちらが<b>水では切れない結合</b>を'
        '薬剤で切って組み替えているからです。'
        '——図3で見た「ちょうどいい弱さ」を、'
        '私たちは毎朝、鏡の前で確かめていることになります。',
        'ケラチンの 4 つの結合と、それぞれが何で外れるかは'
        '<a href="https://www.demi.nicca.co.jp/salonsupport/beauty1_detail_16.html">'
        'デミ コスメティクス「髪の 4 つの結合」</a>、'
        '水素結合が濡らすと切れ乾くとつながることは'
        '<a href="https://www.kao.com/jp/haircare/scalp-care/9-1/">'
        '花王「髪が形づくメカニズム」</a>による。'
        '図の毛は仕組みを示すための模式で、実際の太さの比ではありません。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    efig.save('_fig6_bedhair.qmd', build())
