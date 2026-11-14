# -*- coding: utf-8 -*-
"""
元素 #6 アルミニウム / 図5 : 粘土のシートと、足りない「1」。

粘土（2:1 型）の層を横から見た模式図。
  ケイ素の板（四面体シート）── アルミの板（八面体シート）── ケイ素の板
の3枚重ねが1つの層で、層と層のあいだ（層間）に水と陽イオンが入る。

下側のケイ素の板で、ケイ素（+4）の席を1か所だけアルミ（+3）が占める。
そこだけプラスが1つ足りず、層がマイナスを帯びる。層間の陽イオンが
そこへ引き寄せられる——を、アニメーションで見せる。

正確さについての但し書き（出典行とホバーに書く）:
  - 図は模式図。原子の大きさ・間隔・角度は正確ではない
  - 四面体シートで Si の席に Al が入る置換は、イライトやバーミキュライト、
    ベイデライトで起きる。モンモリロナイトでは主に八面体シートで
    Al の席に Mg が入る。どちらでもプラスが1つ足りなくなる
  - カオリナイト（1:1 型）では置換がほとんど無く、陽イオンを抱える力は
    主に結晶の縁（割れた端）による

陽イオン交換容量（Appelo & Postma 2005, 6章）:
  カオリナイト 3〜15、モンモリロナイト（スメクタイト）80〜120 meq/100 g

出力: _fig5_clay.qmd
"""
import efig

P, CID = 'alclay', 'alclay1'

W, H = 680, 330
N = 8
X0, DX = 110, 70        # 左に板の名前を書く余白を空ける
Y0 = 34                 # 1 層目の上端
TH = 104                # 層の厚さ
GAP = 64                # 層間
SUB = 4                 # 置換する四面体（下側の板、0 始まり）


def tetra(x, yb, down, cls, detail=None):
    """四面体を三角形で。down=True なら頂点が下向き。"""
    if down:
        pts = '%d,%d %d,%d %d,%d' % (x - 24, yb, x + 24, yb, x, yb + 34)
        cy = yb + 13
    else:
        pts = '%d,%d %d,%d %d,%d' % (x - 24, yb, x + 24, yb, x, yb - 34)
        cy = yb - 13
    o = []
    if detail:
        o.append('<g class="%s-hv" data-detail="%s">' % (P, efig.attr(detail)))
    o.append('<polygon class="%s-tet" points="%s"/>' % (P, pts))
    o.append('<circle class="%s-%s" cx="%d" cy="%d" r="%d"/>'
             % (P, cls, x, cy, 8 if cls == 'si' else 9))
    if detail:
        o.append('</g>')
    return '\n'.join(o)


def layer(y, first, fade=False):
    o = ['<g class="%s-layer%s">' % (P, ' %s-fade' % P if fade else '')]
    # 上のケイ素の板（頂点が下＝アルミの板のほうを向く）
    for i in range(N):
        o.append(tetra(X0 + i * DX, y, True, 'si'))
    # アルミの板
    o.append('<g class="%s-hv" data-detail="%s">' % (P, efig.attr(
        '<b>アルミの板</b>です。アルミ1個を酸素（と水酸基）6個が囲んだ八面体が、'
        '縁を共有して平らに並んでいます。ケイ素の板2枚が、この板を上下から挟みます。')))
    o.append('<rect class="%s-oct" x="%d" y="%d" width="%d" height="26" rx="6"/>'
             % (P, X0 - 30, y + 38, DX * (N - 1) + 60))
    for i in range(N - 1):
        o.append('<circle class="%s-al" cx="%d" cy="%d" r="9"/>' % (P, X0 + DX // 2 + i * DX, y + 51))
    o.append('</g>')
    # 下のケイ素の板（頂点が上）
    for i in range(N):
        x = X0 + i * DX
        if first and i == SUB:
            o.append(tetra(x, y + TH, False, 'sub',
                     'ここでは、<b>ケイ素（＋4）が座るはずの席に、アルミ（＋3）が座っています。</b>'
                     'プラスが1つ足りないので、<b>この場所がマイナスを帯びます。</b>'
                     '粘土の種類によっては、アルミの板のほうで、アルミの席にマグネシウム（＋2）が'
                     '座ることで同じことが起きます（モンモリロナイト）。'))
        else:
            o.append(tetra(x, y + TH, False, 'si'))
    o.append('</g>')
    return '\n'.join(o)


def build_svg():
    o = ['<svg viewBox="0 0 %d %d" role="img" aria-label="粘土の層を横から見た模式図。'
         'ケイ素の席の1つにアルミが座り、そこへ層のあいだの陽イオンが引き寄せられる">'
         % (W, H)]
    # 層の名前（左）
    o.append('<text class="%s-side" x="8" y="%d">ケイ素の板</text>' % (P, Y0 + 16))
    o.append('<text class="%s-side %s-sidea" x="8" y="%d">アルミの板</text>' % (P, P, Y0 + 56))
    o.append('<text class="%s-side" x="8" y="%d">ケイ素の板</text>' % (P, Y0 + 96))

    o.append(layer(Y0, True))

    # 層間：水と陽イオン
    ymid = Y0 + TH + GAP // 2
    o.append('<g class="%s-hv" data-detail="%s">' % (P, efig.attr(
        '層と層のあいだには<b>水</b>が入りこみ、プラスのイオン（陽イオン）が漂っています。'
        'カリウム、カルシウム、ナトリウム、アンモニウム——<b>どれも肥料や、地下水に溶けている'
        'ものです。</b>')))
    o.append('<rect class="%s-ilr" x="%d" y="%d" width="%d" height="%d" rx="8"/>'
             % (P, X0 - 34, Y0 + TH + 6, DX * (N - 1) + 68, GAP - 12))
    for i, (xx, dy) in enumerate([(128, -8), (170, 10), (250, -6), (318, 12), (452, -10),
                                  (548, 8), (612, -4), (150, 6), (470, 12)]):
        o.append('<circle class="%s-w" cx="%d" cy="%d" r="3"/>' % (P, xx, ymid + dy))
    for xx, lab, cls in [(206, 'K⁺', 'cat'), (505, 'Na⁺', 'cat'), (590, 'K⁺', 'cat')]:
        o.append('<g class="%s-%s"><circle cx="%d" cy="%d" r="11"/>'
                 '<text x="%d" y="%d">%s</text></g>' % (P, cls, xx, ymid, xx, ymid + 4, lab))
    o.append('</g>')

    # 引き寄せられる陽イオン（アニメーション）
    xs = X0 + SUB * DX
    o.append('<g class="%s-hv" data-detail="%s">' % (P, efig.attr(
        'マイナスを帯びた場所に、<b>カルシウムのイオンが引き寄せられて、くっつきます。</b>'
        'くっついたイオンは、雨でもなかなか流されません。'
        'ただし、別の陽イオンがたくさん来ると、<b>入れ替わります</b>（陽イオン交換）。')))
    o.append('<g class="%s-pull"><circle class="%s-ca" cx="%d" cy="%d" r="13"/>'
             '<text class="%s-cat2" x="%d" y="%d">Ca²⁺</text></g>'
             % (P, P, xs, ymid - 4, P, xs, ymid))
    o.append('</g>')
    # マイナスの札
    o.append('<g class="%s-neg"><circle cx="%d" cy="%d" r="10"/>'
             '<text x="%d" y="%d">−</text></g>' % (P, xs + 30, Y0 + TH - 18, xs + 30, Y0 + TH - 13))

    # 2 層目（薄く）
    o.append(layer(Y0 + TH + GAP, False, fade=True))

    # 凡例
    lx, ly = 404, H - 12
    items = [('si', 'ケイ素'), ('al', 'アルミ'), ('sub', 'ケイ素の席のアルミ')]
    for j, (c, t) in enumerate(items):
        o.append('<circle class="%s-%s" cx="%d" cy="%d" r="6"/>' % (P, c, lx + j * 88 - 200, ly - 4, ))
        o.append('<text class="%s-lg" x="%d" y="%d">%s</text>' % (P, lx + j * 88 - 190, ly, t))
    o.append('<circle class="%s-w" cx="%d" cy="%d" r="3"/>' % (P, lx + 106, ly - 4))
    o.append('<text class="%s-lg" x="%d" y="%d">水</text>' % (P, lx + 114, ly))
    o.append('<circle class="%s-lgc" cx="%d" cy="%d" r="6"/>' % (P, lx + 148, ly - 4))
    o.append('<text class="%s-lg" x="%d" y="%d">陽イオン</text>' % (P, lx + 158, ly))
    o.append('</svg>')
    return '\n'.join(o)


CSS = """
.%(p)s{--si:#8A6B36;--al:#5B6F80;--sub:#BE640A;--cat:#C9822A;--w:#6FA3C8;--neg:#B02A37;}
.%(p)s-wrap{margin:16px 8px 0;}
.%(p)s-wrap svg{display:block;width:100%%;height:auto;}
.%(p)s-wrap text{font-family:"Hiragino Sans","Yu Gothic","Noto Sans JP",sans-serif;}
.%(p)s-tet{fill:rgba(138,107,54,.10);stroke:rgba(138,107,54,.55);stroke-width:1.3;}
.%(p)s-oct{fill:rgba(91,111,128,.12);stroke:rgba(91,111,128,.35);stroke-width:1;}
.%(p)s-si{fill:var(--si);}
.%(p)s-al{fill:var(--al);}
.%(p)s-sub{fill:var(--sub);stroke:#fff;stroke-width:2;}
.%(p)s-fade{opacity:.35;}
.%(p)s-side{font-size:11px;fill:var(--si);font-weight:700;}
.%(p)s-sidea{fill:var(--al);}
.%(p)s-ilr{fill:rgba(111,163,200,.10);}
.%(p)s-w{fill:var(--w);opacity:.8;}
.%(p)s-cat circle{fill:rgba(201,130,42,.18);stroke:var(--cat);stroke-width:1.5;}
.%(p)s-cat text{font-size:10px;font-weight:800;fill:#8A5518;text-anchor:middle;}
.%(p)s-ca{fill:var(--cat);}
.%(p)s-cat2{font-size:10px;font-weight:800;fill:#fff;text-anchor:middle;}
.%(p)s-neg circle{fill:var(--neg);}
.%(p)s-neg text{font-size:17px;font-weight:800;fill:#fff;text-anchor:middle;}
.%(p)s-lg{font-size:11px;fill:var(--dim);}
.%(p)s-lgc{fill:rgba(201,130,42,.25);stroke:var(--cat);stroke-width:1.5;}
.%(p)s-hv{cursor:default;}
.%(p)s-hv:hover{filter:brightness(1.06);}
/* カルシウムが、マイナスの場所へ寄っていく */
/* 一度だけ寄ってきて、そこに留まる。動かない環境では最初から留まった位置に描かれる */
.%(p)s-pull{animation:%(p)s-pull 2.4s cubic-bezier(.3,.7,.3,1) .8s both;}
@keyframes %(p)s-pull{from{transform:translate(-150px,16px);}to{transform:translate(0,0);}}
.%(p)s-neg{animation:%(p)s-blink 4.2s ease-in-out infinite;transform-box:fill-box;transform-origin:center;}
@keyframes %(p)s-blink{0%%,40%%{transform:scale(1);}50%%{transform:scale(1.25);}60%%,100%%{transform:scale(1);}}

.%(p)s-cmp{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:14px 8px 0;}
.%(p)s-c{padding:12px 15px;border-radius:11px;cursor:default;line-height:1.65;
  font-size:.88rem;color:var(--dim);}
.%(p)s-c b{display:block;font-size:.98rem;font-weight:800;color:var(--ink);margin-bottom:2px;}
.%(p)s-c .n{font-size:1.35rem;font-weight:800;color:var(--sub);font-variant-numeric:tabular-nums;}
.%(p)s-c .u{font-size:.78rem;color:var(--faint);}
.%(p)s-c1{background:rgba(122,96,52,.06);border:1px solid var(--line2);}
.%(p)s-c2{background:rgba(190,100,10,.07);border:1px solid rgba(190,100,10,.25);}
@media (max-width:820px){
  .%(p)s-wrap{margin:10px 0 0;}
  .%(p)s-cmp{grid-template-columns:1fr;margin:12px 2px 0;gap:8px;}
}
""" % {'p': P}


def build():
    o = [efig.css(P, CSS),
         efig.open_card(
             P, CID,
             '粘土のマイナスは、アルミの「足りない 1」から生まれます',
             '粘土の層を横から見た模式図です。ケイ素の板・アルミの板・ケイ素の板の3枚重ねが'
             '1つの層で、層と層のあいだに水と陽イオン（プラスのイオン）が入ります。'
             '各部にカーソルを合わせる（スマホはタップ）と説明が出ます。')]
    o.append('<div class="%s-wrap">%s</div>' % (P, build_svg()))
    o.append('<div class="%s-cmp">' % P)
    o.append('<div class="%s-c %s-c1" data-detail="%s"><b>カオリナイト（茶碗の粘土）</b>'
             '<span class="n">3〜15</span> <span class="u">meq／100 g</span><br>'
             '席の入れ替わりがほとんど無い → 抱える量は少ない</div>'
             % (P, P, efig.attr(
                 'カオリナイトは、ケイ素の板とアルミの板が1枚ずつの<b>2枚重ね</b>で、'
                 '席の入れ替わりがほとんどありません。わずかに抱える陽イオンは、'
                 '主に結晶の<b>割れた縁</b>にくっついたものです。')))
    o.append('<div class="%s-c %s-c2" data-detail="%s"><b>スメクタイト（よく抱える粘土）</b>'
             '<span class="n">80〜120</span> <span class="u">meq／100 g</span><br>'
             '席の入れ替わりが多い → カオリナイトの10倍ほど抱える</div>'
             % (P, P, efig.attr(
                 'スメクタイトの仲間は、図のような<b>3枚重ね</b>で、席の入れ替わりが多く、'
                 '層のあいだに水をたっぷり吸いこんでふくらみます。'
                 '猫砂や、井戸を掘るときの泥水（ベントナイト）に使われる粘土です。')))
    o.append('</div>')
    o.append(efig.close_card(
        P,
        '粘土の層の中で、<b>ケイ素（＋4）の席にアルミ（＋3）が座る</b>と、'
        'そこだけプラスが1つ足りなくなり、層がマイナスを帯びます。'
        'マイナスには、水の中のプラスのイオン——カリウム、カルシウム、アンモニウム——が'
        '<b>引き寄せられて、くっつきます。</b>粘土が肥料を抱え、'
        '地下水の成分を入れ替えるのは、この仕組みによります。',
        '模式図です。原子の大きさ・間隔・角度は正確ではありません。'
        'ケイ素の席にアルミが入る置換は、イライト・バーミキュライト・ベイデライトなどで起き、'
        'モンモリロナイトでは主にアルミの板の側で、アルミの席にマグネシウムが入ります'
        '（どちらもプラスが1つ足りなくなります）。'
        '数値は陽イオン交換容量で、粘土 100 g が抱えられるプラスの電気の量'
        '（meq はミリ当量）。抱える量は席の入れ替わりの数だけでは決まらず、'
        'イライトは入れ替わりが多いのに 10〜40 meq にとどまります。'
        '層のあいだのカリウムが固く挟まれていて、交換されないためです。'
        'Appelo, C. A. J. & Postma, D. (2005) '
        '<i>Geochemistry, Groundwater and Pollution</i>, 2nd ed., 6章による。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    efig.save('_fig5_clay.qmd', build())
