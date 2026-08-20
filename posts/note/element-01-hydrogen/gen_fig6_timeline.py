# -*- coding: utf-8 -*-
"""
元素 #1 水素 / 図6 : ビッグバンから、今日のレモンまで。

台本の訂正が二点入っている。
  (1) 「137 億年前」-> 約 138 億年前。Planck 2018 の 13.787 Gyr が現在の標準値。
  (2) 「水素はビッグバンで最初に生まれた原子」-> 厳密には
      陽子（核）が約 100 万分の 1 秒後、中性の水素原子になったのは約 38 万年後。

対数の時間軸（秒）:
  1e-6 秒       陽子ができる
  180 秒（3 分） 軽い原子核ができる
  1.20e13 秒（38 万年） 中性の水素原子ができる＝宇宙の晴れ上がり
  4.35e17 秒（138 億年） 今日

出力: _fig6_timeline.qmd
"""
import math
import efig

P, CID = 'etime', 'etime1'

YEAR = 3.156e7            # 1 年の秒数
T0, T1 = 1e-6, 4.35e17

MARKS = [
    (1e-6, '100 万分の 1 秒後', '陽子が生まれる', '#BE5326', 1,
     'ビッグバンの直後、宇宙はまだ想像を絶する高温でした。'
     'そこから冷えるにつれてクォークが集まり、<b>陽子</b>——つまり'
     '水素の原子核——ができます。'),
    (180, '3 分後', '軽い原子核ができる', '#D69A2E', 0,
     'この 3 分間で、陽子の一部がヘリウムの原子核に変わりました。'
     '<b>宇宙にあるヘリウムのほとんどは、この 3 分間の産物</b>です。'),
    (3.8e5 * YEAR, '38 万年後', '中性の水素原子ができる', '#5E96C4', 1,
     'ようやく温度が下がり、陽子が電子をつかまえて'
     '<b>中性の水素原子</b>になりました。'
     'このとき宇宙は初めて透明になります（宇宙の晴れ上がり）。'),
    (1.38e10 * YEAR, '138 億年後', '今日、あなたの口の中', '#C1650A', 0,
     '皆さんが今日かじったレモンの酸っぱさ——その水素イオンの陽子は、'
     '<b>宇宙が生まれて 100 万分の 1 秒後にできたもの</b>です。'
     'それから 138 億年、一度も壊れていません。'),
]

CSS = """
.%(p)s-stage{position:relative;margin:22px 8px 0;}
.%(p)s-scale{position:relative;height:3px;margin:104px 0 0;border-radius:3px;
  background:linear-gradient(90deg,#EADFE8,#E6DCE8 30%%,#D8CDB8 65%%,#EDE1C4);}
.%(p)s-scale::after{content:"";position:absolute;top:-3px;width:20%%;height:9px;
  border-radius:9px;filter:blur(2px);
  background:linear-gradient(90deg,transparent,#8A6C28,transparent);
  animation:%(p)s-sweep 8s cubic-bezier(.45,0,.55,1) infinite;}
@keyframes %(p)s-sweep{0%%{left:-22%%;opacity:0}10%%{opacity:.9}
  86%%{opacity:.9}100%%{left:102%%;opacity:0}}

.%(p)s-m{position:absolute;transform:translateX(-50%%);text-align:center;
  cursor:default;width:172px;}
.%(p)s-m i{display:block;width:13px;height:13px;margin:0 auto;
  border-radius:50%%;background:var(--c);border:2px solid #FDFAF3;
  box-shadow:0 0 0 3px var(--c);}
.%(p)s-m b{display:block;font-size:.98rem;font-weight:800;color:var(--c);
  line-height:1.35;}
.%(p)s-m s{display:block;text-decoration:none;font-size:.88rem;
  color:var(--ink);line-height:1.45;margin-top:2px;}
.%(p)s-m.up{bottom:22px}.%(p)s-m.dn{top:22px}
.%(p)s-m.dn i{margin-bottom:5px}
.%(p)s-m.up i{margin-top:5px}
.%(p)s-ends{display:flex;justify-content:space-between;
  font-size:.82rem;color:var(--faint);margin-top:104px;}

@media (max-width:820px){
  .%(p)s-stage{margin:18px 2px 0}
  .%(p)s-m{width:96px}
  .%(p)s-m b{font-size:.8rem}.%(p)s-m s{font-size:.74rem}
  .%(p)s-scale{margin-top:96px}.%(p)s-ends{margin-top:96px}
}
""" % {'p': P}


def pos(t):
    return (math.log10(t) - math.log10(T0)) / \
        (math.log10(T1) - math.log10(T0)) * 100.0


def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, 'ビッグバンから、今日のレモンまで',
                        '横軸は時間ですが、目盛りは対数です。'
                        '左端から右端まで、宇宙のぜんぶの歴史が入っています。')]

    o.append('<div class="%s-stage">' % P)
    o.append('<div class="%s-scale">' % P)
    for t, when, what, col, up, det in MARKS:
        x = pos(t)
        # 端の札がカードからはみ出さないように寄せる
        shift = '' if 8 < x < 92 else (
            'margin-left:56px;' if x <= 8 else 'margin-left:-56px;')
        cls = 'up' if up else 'dn'
        inner = ('<b>%s</b><s>%s</s><i></i>' % (when, what)) if up else \
                ('<i></i><b>%s</b><s>%s</s>' % (when, what))
        o.append('<div class="%s-m %s" style="left:%.3f%%;%s--c:%s" '
                 'data-detail="%s">%s</div>'
                 % (P, cls, x, shift, col, det, inner))
    o.append('</div>')
    o.append('<div class="%s-ends"><span>← 宇宙の誕生</span>'
             '<span>今日 →</span></div>' % P)
    o.append('</div>')

    o.append(efig.close_card(
        P,
        '皆さんがレモンをかじって「酸っぱい」と感じるとき、'
        '舌がふれているのは<b>宇宙が生まれて 100 万分の 1 秒後にできた陽子</b>です。'
        'たとえ話ではありません。それから <b>138 億年</b>、'
        'その陽子は一度も壊れずに旅を続けて、今日あなたの口の中にいます。',
        '宇宙の年齢は 138.0 億年（Planck Collaboration 2018 の 13.787 Gyr）。'
        '晴れ上がりは約 38 万年後。目盛りは対数なので、'
        '左のわずかな幅にも長い時間が入っている点に注意してください。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    efig.save('_fig6_timeline.qmd', build())
