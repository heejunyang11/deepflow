# -*- coding: utf-8 -*-
"""
元素 #5 ケイ素 / 図3 : 「半導体」とは、外から開け閉めできる管である。

半導体という言葉は「半分だけ導く」と読める。ところが値打ちはそこにない。
値打ちは<b>外から開け閉めできる</b>ことにある。
その一点を、水道管の比喩で見せる図。

  導体   : 開きっぱなしの管（止められない）
  絶縁体 : 塞がった管（流せない）
  半導体 : ハンドルのついた弁（流す・止めるを選べる）-> 1 と 0

比喩の定義はこの図の中で完結させる（記号の意味を本文任せにしない）。
  水    = 電気
  管    = 電気の通り道
  ハンドル = 外から加える電圧

出力: _fig3_valve.qmd
"""
import efig

P, CID = 'sival', 'sival1'

CSS = """
.%(p)s{--wt:#5E96C4;--pipe:#8C8271;--hd:#BE640A;--on:#2E6E4E;--off:#B02A37;}
.%(p)s-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;
  margin:20px 8px 0;}
.%(p)s-c{padding:13px 13px 10px;border-radius:12px;cursor:default;
  background:rgba(122,96,52,.05);border:1px solid rgba(122,96,52,.14);
  transition:background .18s ease,border-color .18s ease;}
.%(p)s-c:hover{background:rgba(122,96,52,.13);
  border-color:rgba(190,100,10,.45);}
.%(p)s-c.pick{background:rgba(46,110,78,.09);
  border-color:rgba(46,110,78,.34);}
.%(p)s-c svg{display:block;width:100%%;height:auto;}
p.%(p)s-t{font-size:1rem;font-weight:800;color:var(--ink);margin:0 0 1px;}
p.%(p)s-u{font-size:.79rem;color:var(--faint);margin:0 0 8px;line-height:1.6;}

.%(p)s-pipe{fill:none;stroke:var(--pipe);stroke-width:13;
  stroke-linecap:round;opacity:.34;}
.%(p)s-w{fill:none;stroke:var(--wt);stroke-width:7;stroke-linecap:round;
  stroke-dasharray:13 11;}
.%(p)s-flow{animation:%(p)s-run 1.05s linear infinite;}
@keyframes %(p)s-run{to{stroke-dashoffset:-24;}}
/* 半導体の管。流れる時間と止まる時間が交互に来る */
.%(p)s-gate{animation:%(p)s-run 1.05s linear infinite,
  %(p)s-blink 3.4s steps(1) infinite;}
@keyframes %(p)s-blink{0%%,50%%{opacity:1;}50.01%%,100%%{opacity:0;}}
.%(p)s-plug{fill:#D9D0BE;stroke:var(--pipe);stroke-width:2;}
.%(p)s-hand{stroke:var(--hd);stroke-width:5;stroke-linecap:round;fill:none;
  transform-box:fill-box;transform-origin:50%% 100%%;
  animation:%(p)s-turn 3.4s steps(1) infinite;}
@keyframes %(p)s-turn{0%%,50%%{transform:rotate(0deg);}
  50.01%%,100%%{transform:rotate(90deg);}}
.%(p)s-knob{fill:var(--hd);}
.%(p)s-bit{font-size:19px;font-weight:800;
  font-family:"Hiragino Sans","Yu Gothic","Noto Sans JP",sans-serif;}
.%(p)s-b1{fill:var(--on);animation:%(p)s-blink 3.4s steps(1) infinite;}
.%(p)s-b0{fill:var(--off);animation:%(p)s-blink2 3.4s steps(1) infinite;}
@keyframes %(p)s-blink2{0%%,50%%{opacity:0;}50.01%%,100%%{opacity:1;}}

.%(p)s-lg{display:flex;flex-wrap:wrap;gap:14px;margin:16px 8px 0;
  font-size:.84rem;color:var(--dim);}
.%(p)s-lg i{font-style:normal;display:inline-flex;align-items:center;gap:6px;}
.%(p)s-sw{width:22px;height:6px;border-radius:3px;display:inline-block;}

.%(p)s-hit{margin:18px 8px 0;padding:15px 17px;border-radius:12px;
  background:rgba(46,110,78,.09);border:1px solid rgba(46,110,78,.26);}
.%(p)s-hit .a{font-size:1.3rem;font-weight:800;color:var(--on);
  line-height:1.45;}
.%(p)s-hit .b{font-size:.88rem;color:var(--dim);margin-top:4px;line-height:1.7;}

@media (max-width:820px){
  .%(p)s-grid{grid-template-columns:1fr;gap:10px;margin:14px 2px 0;}
  .%(p)s-lg{margin:12px 2px 0;font-size:.78rem;gap:10px;}
  .%(p)s-hit{margin:14px 2px 0;padding:13px 14px;}
  .%(p)s-hit .a{font-size:1.05rem;}
}
""" % {'p': P}

VB = '0 0 220 150'


def pipe(inner):
    return ('<svg viewBox="%s" role="img" aria-label="水道管のたとえ">'
            '<path class="{p}-pipe" d="M14 76 H206"/>%s</svg>'
            .format(p=P) % (VB, inner))


def sv_conductor():
    return pipe('<path class="{p}-w {p}-flow" d="M14 76 H206"/>'
                .format(p=P))


def sv_insulator():
    return pipe(
        '<path class="{p}-w" d="M14 76 H92" opacity=".5"/>'
        '<rect class="{p}-plug" x="96" y="58" width="28" height="36" rx="5"/>'
        .format(p=P))


def sv_semi():
    return pipe(
        '<path class="{p}-w {p}-gate" d="M14 76 H206"/>'
        # 弁の胴とハンドル
        '<rect class="{p}-plug" x="98" y="56" width="24" height="40" rx="6"/>'
        '<path class="{p}-hand" d="M110 52 V26"/>'
        '<circle class="{p}-knob" cx="110" cy="22" r="7"/>'
        '<text class="{p}-bit {p}-b1" x="176" y="42" text-anchor="middle">1</text>'
        '<text class="{p}-bit {p}-b0" x="176" y="42" text-anchor="middle">0</text>'
        .format(p=P))


CARDS = [
    ('導体', '金属など', 'sv_conductor', '',
     '銅やアルミの電線です。<b>電気は流れますが、止められません。</b>'
     '蛇口のない管に水が流れ続けているのと同じで、'
     'これだけでは「計算」はできません。'),
    ('絶縁体', 'ゴム・ガラスなど', 'sv_insulator', '',
     'ゴムやプラスチックです。<b>電気は流れません。</b>'
     '塞がった管に水が来ないのと同じで、こちらも計算には使えません。'
     '電線の被覆のように、<b>流さないための材料</b>です。'),
    ('半導体', 'ケイ素', 'sv_semi', ' pick',
     '<b>ここが本題です。</b>ハンドルを回せば流れ、戻せば止まる。'
     'この<b>ハンドルにあたるのが、外から加える電圧</b>です。'
     '「半分導く」ことに値打ちがあるのではありません。'
     '<b>流すか止めるかを、外から決められる</b>ことに値打ちがあります。'),
]


def build():
    o = [efig.css(P, CSS),
         efig.open_card(
             P, CID,
             '半導体の値打ちは、「半分導く」ことではありません',
             '電気を水に、通り道を管にたとえました。'
             '3 枚にカーソルを合わせる（スマホはタップ）と説明が出ます。')]

    o.append('<div class="%s-grid">' % P)
    for name, sub, fn, pick, detail in CARDS:
        o.append('<div class="%s-c%s" data-detail="%s">'
                 % (P, pick, efig.attr(detail)))
        o.append('<p class="%s-t">%s</p><p class="%s-u">%s</p>'
                 % (P, name, P, sub))
        o.append(globals()[fn]())
        o.append('</div>')
    o.append('</div>')

    o.append('<div class="%s-lg">'
             '<i><span class="%s-sw" style="background:var(--wt)"></span>'
             '青い流れ＝電気</i>'
             '<i><span class="%s-sw" style="background:var(--pipe);'
             'opacity:.4"></span>灰色の管＝電気の通り道</i>'
             '<i><span class="%s-sw" style="background:var(--hd)"></span>'
             'ハンドル＝外から加える電圧</i></div>' % (P, P, P, P))

    o.append('<div class="%s-hit" data-detail="%s">'
             '<div class="a">開いた＝1、閉じた＝0</div>'
             '<div class="b">この弁を指先ほどの板に何十億個も並べ、'
             '<b>片方の弁の出口を、次の弁のハンドルにつなぐ</b>。'
             'それだけで、計算する機械ができあがります。</div></div>'
             % (P, efig.attr(
                 '弁が弁を操る——ここが肝心なところです。'
                 '<b>出てきた水が、次の弁のハンドルを回す。</b>'
                 'この繋ぎ方ができるので、'
                 '「A と B の両方が開いていたら開く」といった'
                 '判断を、電気の流れだけで組み立てられます。')))

    o.append(efig.close_card(
        P,
        '電気を<b>いつも通す</b>のが導体、<b>まったく通さない</b>のが絶縁体。'
        'ケイ素はその中間にいますが、大事なのは中間にいることではありません。'
        '<b>外から電圧をかけると、通す・通さないを切り替えられる</b>ことです。'
        '通っている状態を <b>1</b>、止まっている状態を <b>0</b> と読めば、'
        'それがそのまま計算の材料になります。'
        '<b>石ころが判断する</b>とは、このことです。',
        '水と管は、電気の流れを説明するための比喩です。'
        '実際の素子（MOSFET）では、絶縁膜をはさんだ電極（ゲート）に電圧をかけると、'
        'その真下のケイ素の中に電気の通り道ができたり消えたりします。'
        '通り道そのものを機械的に塞いでいるのではありません。'
        'なお何も混ぜていない純粋なケイ素は、室温ではほとんど電気を通しません。'
        '通り道を作れるようにするために何をするのかは、次の図で扱います。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    efig.save('_fig3_valve.qmd', build())
