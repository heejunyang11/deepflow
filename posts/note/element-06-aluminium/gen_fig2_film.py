# -*- coding: utf-8 -*-
"""
元素 #6 アルミニウム / 図2 : 錆びないのではなく、先に錆びている。

3 コマで見せる。
  1. 空気に触れたとたん、表面が薄い酸化被膜で覆われる
  2. 傷がつくと、むき出しの金属が現れる
  3. むき出しの面がすぐにまた錆びて、被膜がふさがる

下段で鉄のさびと並べ、「なぜアルミのさびは中まで進まないのか」の理由を置く。
  アルミの被膜：すき間がなく、金属にぴったり張りつく → 表面で止まる
  鉄のさび　　：すき間だらけで、はがれ落ちる　　　 → 中まで進む

被膜の厚さは、ふつうの空気中で数ナノメートル（1〜10 nm の報告）。
髪の毛（約 0.08 mm ＝ 8 万 nm）と比べると、およそ 1 万分の 1。

図の中の厚さは誇張してある（実寸で描くと線にもならない）。凡例に明記する。

出力: _fig2_film.qmd
"""
import efig

P, CID = 'alfilm', 'alfilm1'

PW, PH = 200, 150            # 1 コマの大きさ
GAP = 26
W = PW * 3 + GAP * 2 + 20
H = PH + 56


def panel(ix, title, kind):
    ox = 10 + ix * (PW + GAP)
    o = ['<g transform="translate(%d,0)">' % ox]
    o.append('<text class="%s-pt" x="%d" y="18">%d. %s</text>' % (P, PW // 2, ix + 1, title))
    top = 60
    # 金属のかたまり
    if kind == 'scratch' or kind == 'heal':
        # 表面に V 字の傷
        o.append('<path class="%s-metal" d="M0 %d H78 L100 %d L122 %d H%d V%d H0 Z"/>'
                 % (P, top, top + 38, top, PW, PH))
    else:
        o.append('<rect class="%s-metal" x="0" y="%d" width="%d" height="%d"/>'
                 % (P, top, PW, PH - top))
    # 金属の中の原子の並び（点）
    for r in range(4):
        for c in range(10):
            cx, cy = 10 + c * 20, top + 22 + r * 20
            if (kind in ('scratch', 'heal')) and 72 < cx < 128 and cy < top + 40 - abs(cx - 100) * 0:
                if cy < top + 38 - abs(cx - 100) * 38 / 22 + 4:
                    continue
            o.append('<circle class="%s-at" cx="%d" cy="%d" r="3.2"/>' % (P, cx, cy))

    # 被膜
    if kind == 'form':
        o.append('<path class="%s-film %s-grow" d="M0 %d H%d"/>' % (P, P, top, PW))
        # 飛んでくる酸素
        for i, xx in enumerate((30, 80, 130, 170)):
            o.append('<circle class="%s-o %s-o%d" cx="%d" cy="%d" r="4"/>'
                     % (P, P, i, xx, top - 26))
    elif kind == 'scratch':
        o.append('<path class="%s-film" d="M0 %d H78"/>' % (P, top))
        o.append('<path class="%s-film" d="M122 %d H%d"/>' % (P, top, PW))
        o.append('<path class="%s-bare" d="M78 %d L100 %d L122 %d"/>' % (P, top, top + 38, top))
        o.append('<text class="%s-lb %s-lbr" x="100" y="%d">むき出し</text>'
                 % (P, P, top + 58))
        # 釘
        o.append('<path class="%s-nail" d="M112 %d L100 %d L106 %d Z"/>'
                 % (P, top - 34, top + 30, top - 34))
    else:  # heal
        o.append('<path class="%s-film" d="M0 %d H78"/>' % (P, top))
        o.append('<path class="%s-film" d="M122 %d H%d"/>' % (P, top, PW))
        o.append('<path class="%s-film %s-new" d="M78 %d L100 %d L122 %d"/>'
                 % (P, P, top, top + 38, top))
        o.append('<text class="%s-lb %s-lbn" x="100" y="%d">ふさがった</text>'
                 % (P, P, top + 58))
    o.append('</g>')
    return '\n'.join(o)


def build_svg():
    o = ['<svg viewBox="0 0 %d %d" role="img" aria-label="アルミの表面に酸化被膜ができ、'
         '傷ついてもすぐにふさがる様子を3コマで示した図">' % (W, H)]
    o.append(panel(0, '空気に触れる', 'form'))
    o.append(panel(1, '傷がつく', 'scratch'))
    o.append(panel(2, 'すぐにふさがる', 'heal'))
    # 矢印
    for i in range(2):
        xx = 10 + PW + GAP * i + PW * i + 4
        o.append('<text class="%s-arr" x="%d" y="116">→</text>' % (P, xx + (GAP - 8) // 2))
    # 凡例
    o.append('<g transform="translate(10,%d)">' % (PH + 30))
    o.append('<path class="%s-film" d="M0 0 H26"/>' % P)
    o.append('<text class="%s-lg" x="34" y="4">酸化被膜（さび）。'
             '実際は数ナノメートルで、図では何万倍にも太く描いています</text>' % P)
    o.append('</g>')
    o.append('</svg>')
    return '\n'.join(o)


CSS = """
.%(p)s{--al:#5B6F80;--metal:#C9D2DA;--at:#8D9CA9;--film:#0F6C8A;--bare:#E8A33C;
  --ox:#B8401B;--rust:#9A4A1E;}
.%(p)s-wrap{margin:18px 8px 0;}
.%(p)s-wrap svg{display:block;width:100%%;height:auto;}
.%(p)s-wrap text{font-family:"Hiragino Sans","Yu Gothic","Noto Sans JP",sans-serif;}
.%(p)s-pt{font-size:13.5px;font-weight:800;fill:var(--ink);text-anchor:middle;}
.%(p)s-metal{fill:var(--metal);}
.%(p)s-at{fill:var(--at);}
.%(p)s-film{stroke:var(--film);stroke-width:6;fill:none;stroke-linecap:round;
  stroke-linejoin:round;}
.%(p)s-bare{stroke:var(--bare);stroke-width:4;fill:none;stroke-linejoin:round;}
.%(p)s-nail{fill:#7A6E5C;}
.%(p)s-lb{font-size:11.5px;font-weight:700;text-anchor:middle;}
.%(p)s-lbr{fill:#B0660E;}
.%(p)s-lbn{fill:var(--film);}
.%(p)s-o{fill:var(--ox);}
.%(p)s-arr{font-size:18px;fill:var(--faint);text-anchor:middle;}
.%(p)s-lg{font-size:11.5px;fill:var(--dim);}
/* 被膜が左から伸びる。酸素が降ってくる。3 コマ目の新しい被膜が脈打つ。 */
.%(p)s-grow{stroke-dasharray:200;stroke-dashoffset:200;
  animation:%(p)s-draw 1.6s ease-out .3s forwards;}
@keyframes %(p)s-draw{to{stroke-dashoffset:0;}}
.%(p)s-o{animation:%(p)s-fall 1.6s ease-in infinite;}
.%(p)s-o1{animation-delay:.4s;}.%(p)s-o2{animation-delay:.8s;}.%(p)s-o3{animation-delay:1.2s;}
@keyframes %(p)s-fall{0%%{transform:translateY(-10px);opacity:0;}
  30%%{opacity:1;}100%%{transform:translateY(22px);opacity:0;}}
.%(p)s-new{animation:%(p)s-pulse 2.4s ease-in-out infinite;}
@keyframes %(p)s-pulse{0%%,100%%{stroke-width:6;}50%%{stroke-width:9;}}

.%(p)s-cmp{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:16px 8px 0;}
.%(p)s-c{padding:13px 15px;border-radius:11px;cursor:default;line-height:1.7;
  font-size:.9rem;color:var(--dim);transition:background .18s ease;}
.%(p)s-c b{display:block;font-size:1rem;font-weight:800;margin-bottom:3px;}
.%(p)s-ca{background:rgba(15,108,138,.07);border:1px solid rgba(15,108,138,.24);}
.%(p)s-ca b{color:var(--film);}
.%(p)s-cf{background:rgba(154,74,30,.07);border:1px solid rgba(154,74,30,.24);}
.%(p)s-cf b{color:var(--rust);}
.%(p)s-c:hover{filter:brightness(.97);}
@media (max-width:820px){
  .%(p)s-wrap{margin:12px 0 0;}
  .%(p)s-cmp{grid-template-columns:1fr;margin:12px 2px 0;gap:8px;}
}
""" % {'p': P}


def build():
    o = [efig.css(P, CSS),
         efig.open_card(
             P, CID,
             'アルミは、錆びないのではなく、先に錆びています',
             'アルミの表面を横から見た断面です。青い線が酸化被膜（さび）で、'
             '点が金属のアルミの原子です。下の2枚にカーソルを合わせる（スマホはタップ）と'
             '説明が出ます。')]
    o.append('<div class="%s-wrap">%s</div>' % (P, build_svg()))
    o.append('<div class="%s-cmp">' % P)
    o.append('<div class="%s-c %s-ca" data-detail="%s"><b>アルミのさび</b>'
             'すき間がなく、金属にぴったり張りつく。<br>→ 酸素が中まで届かず、表面で止まる</div>'
             % (P, P, efig.attr(
                 'アルミの酸化被膜は、<b>すき間のない緻密な膜</b>で、下の金属にしっかり'
                 '張りついています。酸素も水も、この膜を通り抜けられません。'
                 'そのため、<b>さびが表面の数ナノメートルで止まります。</b>')))
    o.append('<div class="%s-c %s-cf" data-detail="%s"><b>鉄のさび</b>'
             'すき間だらけで、ふくらんではがれ落ちる。<br>→ 新しい面が出て、中まで進む</div>'
             % (P, P, efig.attr(
                 '鉄の赤さびは、<b>水を含んでふくらんだ、すき間の多いかたまり</b>です。'
                 '酸素と水がすき間から入りこみ、しかも表面がはがれ落ちて、'
                 'また新しい鉄が顔を出します。<b>さびが、さびを呼びます。</b>')))
    o.append('</div>')
    o.append(efig.close_card(
        P,
        'アルミは空気に触れたとたん、表面が<b>数ナノメートルの酸化被膜</b>で覆われます。'
        '髪の毛の太さの<b>1万分の1ほど</b>の膜ですが、すき間がないので、'
        '酸素はそれより中へ入れません。傷がついても、むき出しになった面が'
        'すぐにまた錆びて、<b>膜がひとりでにふさがります。</b>',
        '被膜の厚さは、ふつうの空気中でおよそ 1〜10 nm と報告されています'
        '（1 nm は 100 万分の 1 mm）。髪の毛の太さを約 0.08 mm として比べました。'
        '図の被膜は実寸では描けないので、何万倍にも太くしてあります。'
        '酸性やアルカリ性の液に長く触れると、この被膜は溶けてしまいます。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    efig.save('_fig2_film.qmd', build())
