# -*- coding: utf-8 -*-
"""
元素 #4 窒素 / 図4 : インドール。同じ分子が、濃さだけで別のにおいになる。

  1 % より濃い     はっきりと糞便様
  0.01〜0.1 %      ジャスミンなど白い花の香り（高級香水に不可欠）
  ジャスミンアブソリュートでは、揮発成分の 2〜5 % がインドール

理由として説明されているのは、**濃いとより広い範囲の嗅覚受容体が反応する**こと。
薄いときは一部の受容体だけ、濃くなると別の受容体まで巻きこまれる。
つまり分子ではなく、受け取る側の反応が変わっている。

読み取らせたいこと:
  N2 は「何もしない」。ところが窒素は組むと強烈な個性を出す。
  そして「最悪の悪臭」と「最高の芳香」を分けているのは、物質ではなく量。

出力: _fig4_indole.qmd
"""
import math
import efig

P, CID = 'nind', 'nind4'

LO, HI = 0.003, 10.0          # 対数軸（濃度 %）
PAD = 4.0


def pos(v):
    f = (math.log10(v) - math.log10(LO)) / (math.log10(HI) - math.log10(LO))
    return PAD + f * (100.0 - 2 * PAD)


BANDS = [
    ('flower', 0.01, 0.1, '白い花の香り', '#C77BA8'),
    ('fecal', 1.0, 10.0, '大便のにおい', '#8C7A4A'),
]

MARKS = [
    (0.03, 'flower', 'ジャスミン', '香水に使われる濃さ',
     'この濃さでは、<b>ジャスミンやチューベローズ</b>のような、'
     '濃厚で甘い白い花の香りに感じられます。'
     '<b>高級香水に欠かせない成分</b>です。'),
    (3.5, 'fecal', 'ジャスミン精油の中身', '揮発成分の 2〜5%',
     'ジャスミンの精油（アブソリュート）では、'
     '揮発する成分の <b>2〜5% がインドール</b>です。'
     '花の香りの「濃さ」や「animalな」深みは、'
     '<b>この悪臭成分が支えています</b>。'),
    (2.0, 'fecal', 'トイレのにおい', '1% を超えると',
     '<b>1% を超えると、はっきりと糞便様</b>になります。'
     '実際、大便の強い臭気の主役のひとつがこれです。'),
]

CSS = """
.%(p)s{--fl:#C77BA8;--fe:#8C7A4A;--n:#2E6E4E;}
.%(p)s-stage{position:relative;height:250px;margin:22px 8px 0;}
.%(p)s-track{position:absolute;left:0;right:0;top:150px;height:16px;
  border-radius:8px;overflow:hidden;
  background:linear-gradient(90deg,#F2E3EC 0%%,#EFDCE8 22%%,
    #EDE4D6 52%%,#DED0AE 78%%,#CFBE93 100%%);
  border:1px solid rgba(122,96,52,.20);}
.%(p)s-b{position:absolute;top:146px;height:24px;border-radius:9px;
  border:1.5px solid var(--c);background:transparent;}
.%(p)s-bl{position:absolute;top:176px;transform:translateX(-50%%);
  font-size:.88rem;font-weight:700;color:var(--c);white-space:nowrap;}

.%(p)s-tick{position:absolute;top:196px;transform:translateX(-50%%);
  text-align:center;color:var(--faint);font-size:.84rem;}
.%(p)s-tick i{display:block;width:1px;height:8px;margin:0 auto 5px;
  background:#D2C6AF;}
.%(p)s-unit{position:absolute;top:228px;right:0;color:var(--faint);
  font-size:.84rem;}

.%(p)s-m{position:absolute;top:0;width:0;cursor:default;}
.%(p)s-m .lab{position:absolute;transform:translateX(-50%%);text-align:center;}
.%(p)s-m .nm{font-size:.98rem;font-weight:800;color:var(--c);
  white-space:nowrap;line-height:1.4;}
.%(p)s-m .sb{font-size:.8rem;color:var(--dim);white-space:nowrap;
  line-height:1.4;margin-top:1px;}
.%(p)s-m .stem{position:absolute;left:0;width:1px;background:var(--c);
  opacity:.45;}
.%(p)s-m .dot{position:absolute;top:151px;left:-6px;width:12px;height:12px;
  border-radius:50%%;background:var(--c);
  box-shadow:0 0 0 3px #FFFDF9;}

.%(p)s-mol{display:flex;justify-content:center;margin:4px 8px 0;}
.%(p)s-mol svg{width:100%%;max-width:220px;height:auto;}

.%(p)s-punch{margin:18px 8px 6px;padding:16px 18px;border-radius:12px;
  background:rgba(46,110,78,.08);border:1px solid rgba(46,110,78,.24);}
.%(p)s-punch .a{font-size:1.35rem;font-weight:800;color:var(--n);
  line-height:1.5;}
.%(p)s-punch .b{font-size:.9rem;color:var(--dim);margin-top:5px;
  line-height:1.75;}

@media (max-width:820px){
  .%(p)s-stage{margin:18px 2px 0;height:232px;}
  .%(p)s-m .sb{display:none;}
  .%(p)s-m .nm{font-size:.8rem;}
  .%(p)s-bl{font-size:.76rem;}
  .%(p)s-tick{font-size:.74rem;}
  .%(p)s-unit{font-size:.74rem;}
  .%(p)s-punch{margin:14px 2px 4px;padding:13px 14px;}
  .%(p)s-punch .a{font-size:1.05rem;}
  .%(p)s-punch .b{font-size:.8rem;}
}
""" % {'p': P}


def molecule():
    """インドールの骨格。六員環と五員環が縮環し、N が 1 個だけ入る。"""
    o = ['<svg viewBox="0 0 200 110" role="img" '
         'aria-label="インドールの分子骨格">']
    # 六員環
    hx = [(52, 30), (28, 45), (28, 73), (52, 88), (76, 73), (76, 45)]
    # 五員環（六員環の右辺 (76,45)-(76,73) を共有）
    pt = [(76, 45), (103, 36), (120, 59), (103, 82), (76, 73)]

    def poly(ps, close=True):
        d = 'M%d %d ' % ps[0] + ' '.join('L%d %d' % p for p in ps[1:])
        return d + (' Z' if close else '')
    o.append('<path d="%s" fill="none" stroke="#5F5546" stroke-width="2.2" '
             'stroke-linejoin="round"/>' % poly(hx))
    o.append('<path d="%s" fill="none" stroke="#5F5546" stroke-width="2.2" '
             'stroke-linejoin="round"/>' % poly(pt))
    # 芳香環らしさを出す内側の線
    for a, b in [((34, 48), (34, 70)), ((55, 34), (72, 46)), ((55, 84), (72, 72))]:
        o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#5F5546" '
                 'stroke-width="1.6" opacity=".8"/>' % (a[0], a[1], b[0], b[1]))
    o.append('<line x1="102" y1="42" x2="114" y2="58" stroke="#5F5546" '
             'stroke-width="1.6" opacity=".8"/>')
    # 窒素だけ色をつける
    o.append('<circle cx="120" cy="59" r="11" fill="#FFFDF9"/>')
    o.append('<text x="120" y="65" font-size="17" font-weight="800" '
             'fill="#2E6E4E" text-anchor="middle">N</text>')
    o.append('<text x="120" y="95" font-size="12.5" fill="#7A6E5C" '
             'text-anchor="middle">窒素は、たった 1 個</text>')
    o.append('</svg>')
    return ''.join(o)


def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, '同じ分子が、濃さだけで別のにおいになります',
                        'インドールという窒素化合物。'
                        '印にカーソルを合わせる（スマホはタップ）と説明が出ます。')]

    o.append('<div class="%s-mol">%s</div>' % (P, molecule()))

    o.append('<div class="%s-stage">' % P)
    o.append('<div class="%s-track"></div>' % P)
    for key, lo, hi, name, col in BANDS:
        o.append('<div class="%s-b" style="left:%.2f%%;width:%.2f%%;--c:%s">'
                 '</div>' % (P, pos(lo), pos(hi) - pos(lo), col))
        o.append('<div class="%s-bl" style="left:%.2f%%;--c:%s">%s</div>'
                 % (P, (pos(lo) + pos(hi)) / 2, col, name))

    for v, lab in [(0.01, '0.01'), (0.1, '0.1'), (1, '1'), (10, '10')]:
        o.append('<div class="%s-tick" style="left:%.2f%%"><i></i>%s</div>'
                 % (P, pos(v), lab))
    o.append('<div class="%s-unit">インドールの濃さ（%%・対数目盛）</div>' % P)

    for i, (v, kind, name, sub, detail) in enumerate(MARKS):
        col = '#C77BA8' if kind == 'flower' else '#8C7A4A'
        top = [22, 22, 86][i]
        st = top + 46
        o.append('<div class="%s-m" data-detail="%s" '
                 'style="left:%.2f%%;--c:%s">'
                 '<div class="lab" style="top:%dpx">'
                 '<div class="nm">%s</div><div class="sb">%s</div></div>'
                 '<div class="stem" style="top:%dpx;height:%dpx"></div>'
                 '<div class="dot"></div></div>'
                 % (P, efig.attr(detail), pos(v), col, top, name, sub,
                    st, 151 - st))

    o.append('</div>')

    o.append('<div class="%s-punch">'
             '<div class="a">分けているのは、物質ではなく量です</div>'
             '<div class="b">濃いと、鼻の中の<b>より広い範囲の受容体</b>まで'
             '反応してしまう——そう説明されています。'
             '<b>分子は変わっていません。変わっているのは、受け取る側です。</b>'
             '</div></div>' % P)

    o.append(efig.close_card(
        P,
        '<b>インドール</b>は、窒素を 1 個だけ含む分子です。'
        '<b>1% より濃いと、はっきりと大便のにおい。</b>'
        'ところが <b>0.01〜0.1% まで薄めると、ジャスミンなど白い花の香り</b>に'
        'なります。ジャスミンの精油では、揮発成分の <b>2〜5%</b> がこれです。'
        '窒素は、N₂ のままなら何もしません。'
        'ところが<b>ひとたび他の元素と組むと、これほど強い個性を出す</b>。'
        '——「最悪の悪臭」と「最高の芳香」を分けていたのは、'
        '<b>物質ではなく濃さ</b>でした。',
        '濃度としきい値は香料業界で広く報告されている値によります'
        '（1% 超で糞便様、0.01〜0.1% で白い花の香り、'
        'ジャスミンアブソリュートで揮発成分の 2〜5%）。'
        '感じ方には個人差があり、<b>境目はきっちりした線ではありません</b>。'
        '「濃いと広い範囲の嗅覚受容体が反応する」という説明は'
        '有力なものですが、<b>におい受容の仕組みには未解明の部分が残ります</b>。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    for v in (0.01, 0.03, 0.1, 1, 2, 3.5, 10):
        print('  %6.2f %% -> %5.1f %%' % (v, pos(v)))
    efig.save('_fig4_indole.qmd', build())
