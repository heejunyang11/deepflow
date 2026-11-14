# -*- coding: utf-8 -*-
"""
元素 #5 ケイ素 / 図2 : 水晶が 1 秒を 32,768 回に刻む仕組み。

開幕で出した謎（腕時計の QUARTZ とは何か）を、ここで解く。
答えは 2 段になっている。

  (1) 水晶は、電気をかけると決まった速さで震える（圧電効果）
      -> 震える回数を数えれば、時間が測れる
  (2) 32,768 = 2^15。半分にする回路を 15 段つなぐだけで 1 になる
      -> いちばん単純な回路で 1 秒が作れる

なぜ 32,768 なのかを「2 を 15 回かけた数だから」と示すのがこの図の主眼。
数を書き並べるだけでは伝わらないので、半分にしていく階段として描く。

注意（2026-09-05 の検証で訂正）:
  「2 の累乗でないと端数が出て時計が狂う」は誤り。分周は整数演算なので
  30,000 Hz でもカウンタを組めば正確に 1 秒が作れる。
  2^15 が選ばれるのは精度ではなく、2 分周回路 15 段で済み、
  回路が単純・小型・低消費電力になるため。

出力: _fig2_quartz.qmd
"""
import efig

P, CID = 'siqz', 'siqz1'

HZ = 32768
STEPS = [HZ >> i for i in range(16)]      # 32768, 16384, ... , 1

CSS = """
.%(p)s{--qz:#0F6C8A;--sp:#BE640A;--si:#2E6E4E;}
.%(p)s-two{display:grid;grid-template-columns:1fr 1.15fr;gap:16px;
  margin:20px 8px 0;align-items:stretch;}
.%(p)s-b{padding:14px 15px 12px;border-radius:12px;
  background:rgba(122,96,52,.05);border:1px solid rgba(122,96,52,.14);
  cursor:default;transition:background .18s ease,border-color .18s ease;}
.%(p)s-b:hover{background:rgba(122,96,52,.13);
  border-color:rgba(190,100,10,.45);}
p.%(p)s-t{font-size:1rem;font-weight:800;color:var(--ink);margin:0 0 2px;}
p.%(p)s-u{font-size:.8rem;color:var(--faint);margin:0 0 9px;line-height:1.6;}
.%(p)s-b svg{display:block;width:100%%;height:auto;}

/* 音叉型の水晶。付け根を軸にして、左右の腕がしなる */
.%(p)s-arm{fill:#E9E2D4;stroke:var(--qz);stroke-width:2;
  stroke-linejoin:round;transform-box:fill-box;}
.%(p)s-armL{transform-origin:50%% 100%%;animation:%(p)s-fl 1.1s ease-in-out infinite;}
.%(p)s-armR{transform-origin:50%% 100%%;animation:%(p)s-fr 1.1s ease-in-out infinite;}
@keyframes %(p)s-fl{0%%,100%%{transform:rotate(-1.6deg);}50%%{transform:rotate(1.6deg);}}
@keyframes %(p)s-fr{0%%,100%%{transform:rotate(1.6deg);}50%%{transform:rotate(-1.6deg);}}
.%(p)s-base{fill:#D9D0BE;stroke:var(--qz);stroke-width:2;}
.%(p)s-wire{stroke:var(--sp);stroke-width:2;fill:none;stroke-linecap:round;}
.%(p)s-spark{fill:var(--sp);animation:%(p)s-pulse 1.1s ease-in-out infinite;}
@keyframes %(p)s-pulse{0%%,100%%{opacity:.25;}50%%{opacity:1;}}
.%(p)s-cap{font-size:11px;fill:var(--dim);
  font-family:"Hiragino Sans","Yu Gothic","Noto Sans JP",sans-serif;}

/* 半分にしていく階段 */
.%(p)s-st{display:flex;flex-direction:column;gap:3px;margin-top:2px;}
.%(p)s-r{display:grid;grid-template-columns:2.1rem 1fr auto;gap:8px;
  align-items:center;font-size:.82rem;color:var(--dim);}
.%(p)s-r em{font-style:normal;font-size:.72rem;color:var(--faint);
  font-variant-numeric:tabular-nums;text-align:right;}
.%(p)s-bar{height:9px;border-radius:5px;background:var(--qz);opacity:.85;}
.%(p)s-r b{font-variant-numeric:tabular-nums;font-weight:700;
  color:var(--ink);font-size:.82rem;}
.%(p)s-r.last b{color:var(--sp);font-size:.95rem;}
.%(p)s-r.last .%(p)s-bar{background:var(--sp);}

.%(p)s-hit{margin:18px 8px 0;padding:15px 17px;border-radius:12px;
  background:rgba(15,108,138,.08);border:1px solid rgba(15,108,138,.24);}
.%(p)s-hit .a{font-size:1.32rem;font-weight:800;color:var(--qz);
  line-height:1.45;}
.%(p)s-hit .b{font-size:.88rem;color:var(--dim);margin-top:4px;line-height:1.7;}

@media (max-width:820px){
  .%(p)s-two{grid-template-columns:1fr;gap:10px;margin:14px 2px 0;}
  .%(p)s-hit{margin:14px 2px 0;padding:13px 14px;}
  .%(p)s-hit .a{font-size:1.05rem;}
  .%(p)s-r{grid-template-columns:1.9rem 1fr auto;font-size:.76rem;}
}
""" % {'p': P}


def fork_svg():
    """音叉型の水晶。左右の腕が、逆向きにしなる。"""
    return (
        '<svg viewBox="0 0 200 190" role="img" '
        'aria-label="音叉の形をした水晶が震えている図">'
        # 腕（左右）
        '<path class="{p}-arm {p}-armL" d="M62 22 h30 v104 h-30 z"/>'
        '<path class="{p}-arm {p}-armR" d="M108 22 h30 v104 h-30 z"/>'
        # 付け根
        '<path class="{p}-base" d="M56 126 h88 v34 h-88 z"/>'
        # 電極の線と火花
        '<path class="{p}-wire" d="M40 143 h16 M144 143 h16"/>'
        '<circle class="{p}-spark" cx="34" cy="143" r="5"/>'
        '<circle class="{p}-spark" cx="166" cy="143" r="5"/>'
        '<text class="{p}-cap" x="100" y="180" text-anchor="middle">'
        '電気をかけると、決まった速さで震える</text>'
        '</svg>'.format(p=P))


def stairs():
    o = ['<div class="%s-st">' % P]
    for i, v in enumerate(STEPS):
        w = 100.0 * v / HZ
        last = ' last' if v == 1 else ''
        lab = ('%d 回' % v) if v > 1 else '1 回 ＝ 1 秒'
        o.append('<div class="%s-r%s"><em>%d回目</em>'
                 '<span class="%s-bar" style="width:%.4f%%;'
                 'min-width:%dpx"></span><b>%s</b></div>'
                 % (P, last, i, P, w, 3 if w < 1 else 6,
                    format(v, ',') if v > 1 else lab))
    o.append('</div>')
    return '\n'.join(o)


def build():
    o = [efig.css(P, CSS),
         efig.open_card(
             P, CID,
             '石ころが、1 秒を 32,768 回に刻んでいます',
             '腕時計に書かれた QUARTZ の中身です。'
             '左右の箱にカーソルを合わせる（スマホはタップ）と説明が出ます。')]

    o.append('<div class="%s-two">' % P)

    o.append('<div class="%s-b" data-detail="%s">' % (P, efig.attr(
        '水晶を押しつぶすと、両端に電気が生まれます。'
        '逆に電気をかけると、形が変わります。'
        'これを<b>圧電効果</b>と呼びます。'
        'ただし放っておくと揺れは減衰するので、'
        '<b>小さな増幅回路が押し返して、減った分を補い続けます。</b>'
        '震える速さは水晶の形と大きさで決まり、温度が変わってもほとんどずれません。'
        '<b>時計に使われるのは、この安定さのためです。</b>'
        '（時計用の水晶は天然石ではなく、水熱合成で育てた人工水晶です。）')))
    o.append('<p class="%s-t">① 電気で、震える</p>'
             '<p class="%s-u">水晶は押されると電気を出し、'
             '電気をかけられると形を変えます（圧電効果）。</p>' % (P, P))
    o.append(fork_svg())
    o.append('</div>')

    o.append('<div class="%s-b" data-detail="%s">' % (P, efig.attr(
        '<b>32,768 は、2 を 15 回かけた数です。</b>'
        '「入ってきた回数を半分にして出す」という単純な回路を'
        '15 個つなぐだけで、32,768 回の震えが 1 回になります。'
        '<b>2 の累乗でない数でも、時計は狂いません</b>——'
        'カウンタを組めば正確に数えられます。'
        '2 の累乗が選ばれているのは<b>回路がいちばん単純になるから</b>で、'
        '部品が少なく、小さく、電気を食わずに済みます。')))
    o.append('<p class="%s-t">② 15 回、半分にする</p>'
             '<p class="%s-u">32,768 ＝ 2 を 15 回かけた数。'
             '半分にする回路を 15 個通すと、ぴったり 1 になります。</p>'
             % (P, P))
    o.append(stairs())
    o.append('</div>')

    o.append('</div>')

    o.append('<div class="%s-hit" data-detail="%s">'
             '<div class="a">2<sup>15</sup> ＝ 32,768</div>'
             '<div class="b">中途半端に見えるこの数字は、'
             '<b>2 を 15 回かけた数</b>でした。'
             '半分にする回路を 15 個つなぐだけで、1 秒が作れます。</div>'
             '</div>'
             % (P, efig.attr(
                 '<b>精度のためではありません。</b>30,000 回でも、'
                 'カウンタを組めば正確に 1 秒は作れます。'
                 '2 の累乗にすると<b>「半分にする」だけの回路で済む</b>ので、'
                 '小さく、低消費電力にできます。')))

    o.append(efig.close_card(
        P,
        '水晶は、電気をかけると<b>決まった速さで震えます</b>（圧電効果）。'
        '腕時計に入っている音叉の形をした水晶は、'
        '<b>1 秒間に 32,768 回</b>震えます。'
        'この数は <b>2 を 15 回かけた数</b>なので、'
        '「半分にする」という<b>いちばん単純な回路</b>を 15 個つなぐだけで、'
        '1 秒が作れます。'
        '<b>時間を測っているのは、砂と同じ成分の石ころです。</b>',
        '圧電効果は 1880 年にジャックとピエールのキュリー兄弟が見つけ、'
        '翌 1881 年に、電気をかけると形が変わる逆向きの効果も確かめられました。'
        '腕時計用の水晶振動子が 32,768 Hz（＝2<sup>15</sup> Hz）である理由は、'
        '2 分周回路を 15 段つなぐだけで 1 Hz が得られるためです。'
        '<b>2 の累乗でない周波数でもカウンタで正確に 1 秒は作れる</b>ので、'
        'これは精度ではなく<b>回路の単純さ・小型化・低消費電力</b>のための選択です。'
        '周波数の水準そのものは、精度と電池寿命の折り合いで決まっています。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    assert 2 ** 15 == HZ
    print('2^15 =', HZ, '/ 段数', len(STEPS) - 1)
    efig.save('_fig2_quartz.qmd', build())
