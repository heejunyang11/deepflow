# -*- coding: utf-8 -*-
"""
元素 #4 窒素 / 図2 : 窒素の三重結合を、既刊で使ってきた物差しの上に置く。

この連載は #1 で「結びつきの強さ（kJ/mol）」という物差しを渡してある。
  体温のゆさぶり   2.5    RT（気体定数 x 300 K）
  水素結合         約 20  寝癖の留め金（#1）
  シスチン結合     約 250 パーマが薬剤で切る（#1）
  O-H 共有結合     463    水を水にしている（#1）
そこへ今回の値を置くだけで、読者は新しい説明装置なしに大きさが分かる。

  窒素の三重結合   941 kJ/mol
    高精度実測 78,691.09 +/- 0.15 cm-1（J. Chem. Phys. 160, 014304 (2024)）
    結合長 1.097685 A（NIST WebBook。#3 で使った値と同じ）

読み取らせたいこと:
  941 は水素結合の 47 倍、O-H 共有結合の 2 倍。**桁がひとつ違う。**
  だから体は開けられない。やる気ではなく力が足りない。

出力: _fig2_triple.qmd
"""
import math
import efig

P, CID = 'ntri', 'ntri2'

LO, HI = 1.0, 2000.0          # 対数軸の左右端 (kJ/mol)
PAD = 3.0
TRACK_Y = 300


def pos(v):
    f = (math.log10(v) - math.log10(LO)) / (math.log10(HI) - math.log10(LO))
    return PAD + f * (100.0 - 2 * PAD)


# key, 名前, 値, 表示, 色トークン, ラベル上端 y, ラベル高さ, 補足, 詳細文
#   縦位置は重なりを実測して決め打ち。文言を変えたら必ず見直すこと。
NODES = [
    ('rt', '体温のゆさぶり', 2.5, '2.5', 'rt', 198, 44, None,
     '体温で分子が持っている熱の激しさです。'
     '<b>これより弱い結びつきは、放っておいても勝手にほどけます。</b>'),
    ('hb', '水素結合', 20.0, '約 20', 'hb', 126, 62, '#1 寝癖の留め金',
     '朝の寝癖を作っていた留め金です。'
     '<b>水をかけただけで外れる</b>くらいの弱さでした。'),
    ('ss', 'シスチン結合', 250.0, '約 250', 'other', 126, 62, '#1 パーマが切る',
     '硫黄どうしの結びつき。'
     '<b>水では切れず、パーマ液の薬剤でようやく切れます。</b>'),
    ('cov', 'O–H 共有結合', 463.0, '463', 'cov', 198, 62, '#1 水を水にしている',
     '水の分子そのものを作っている力です。'
     '<b>これがほどけるときは、水が水でなくなるとき。</b>'),
    ('n2', '窒素の三重結合', 941.0, '941', 'n', 46, 66, '今回',
     '<b>この記事の主役です。</b>水素結合の 47 倍、'
     'O–H 共有結合の 2 倍。'
     '<b>あなたの体は、これを開ける道具を持っていません。</b>'),
]

TICKS = [(1, '1'), (10, '10'), (100, '100'), (1000, '1,000')]
MINOR = [2, 3, 5, 7, 20, 30, 50, 70, 200, 300, 500, 700, 2000]

CSS = """
.%(p)s{--n:#2E6E4E;--rt:#B02A37;}
.%(p)s-stage{position:relative;height:392px;margin:0 8px;}
.%(p)s-track{position:absolute;left:0;right:0;top:300px;height:2px;
  background:linear-gradient(90deg,#DED4C0,#C6B79D 55%%,#DED4C0);border-radius:2px;}
.%(p)s-track::after{content:"";position:absolute;top:-1px;left:0;width:22%%;
  height:4px;border-radius:4px;filter:blur(1px);
  background:linear-gradient(90deg,transparent,#2E6E4E,transparent);
  animation:%(p)s-sweep 7s cubic-bezier(.5,0,.5,1) infinite;}
@keyframes %(p)s-sweep{0%%{left:-24%%;opacity:0}
  12%%{opacity:.85}88%%{opacity:.85}100%%{left:102%%;opacity:0}}

.%(p)s-tick{position:absolute;top:314px;transform:translateX(-50%%);
  text-align:center;color:var(--faint);font-size:.86rem;}
.%(p)s-tick i{display:block;width:1px;height:9px;margin:0 auto 5px;
  background:#D2C6AF;}
.%(p)s-tick.m i{height:5px;background:#E4DACA;}
.%(p)s-unit{position:absolute;top:358px;right:0;color:var(--faint);
  font-size:.86rem;}

/* 体温より弱い側を薄く塗る。ここは「放っておけばほどける」領域 */
.%(p)s-shade{position:absolute;top:44px;height:256px;left:0;
  background:linear-gradient(90deg,rgba(176,42,55,0),rgba(176,42,55,.10));
  border-right:1px dashed rgba(176,42,55,.5);}

.%(p)s-n{position:absolute;top:0;bottom:0;width:0;cursor:default;}
.%(p)s-n .lab{position:absolute;transform:translateX(-50%%);text-align:center;}
.%(p)s-n .dot{position:absolute;top:294px;left:-7px;width:14px;height:14px;
  border-radius:50%%;background:var(--c);
  box-shadow:0 0 0 3px #FFFDF9,0 0 0 4px var(--c);}
.%(p)s-n .stem{position:absolute;left:0;width:1px;
  background:linear-gradient(rgba(122,96,52,.11),var(--c));opacity:.6;}
.%(p)s-n .val{font-size:1.14rem;font-weight:800;color:var(--c);
  white-space:nowrap;line-height:1.35;}
.%(p)s-n .nm{font-size:1rem;font-weight:700;color:var(--ink);
  white-space:nowrap;line-height:1.4;}
.%(p)s-n .sb{font-size:.82rem;color:var(--dim);white-space:nowrap;
  line-height:1.4;margin-top:1px;}
.%(p)s-n[data-k="n2"] .val{font-size:2rem;}
.%(p)s-n[data-k="n2"] .nm{font-size:1.4rem;font-weight:800;}
.%(p)s-n[data-k="n2"] .dot{top:291px;left:-10px;width:20px;height:20px;}
.%(p)s-n[data-k="n2"] .dot::after{content:"";position:absolute;inset:-5px;
  border-radius:50%%;border:2px solid var(--n);
  animation:%(p)s-ring 2.9s ease-out infinite;}
@keyframes %(p)s-ring{0%%{transform:scale(.6);opacity:.75}
  70%%,100%%{transform:scale(2.6);opacity:0}}

.%(p)s-rel{position:absolute;transform:translateX(-50%%);text-align:center;
  color:var(--n);font-size:.94rem;font-weight:700;white-space:nowrap;}
.%(p)s-rel u{display:block;height:1px;margin-top:6px;text-decoration:none;
  background:repeating-linear-gradient(90deg,var(--n) 0 6px,transparent 6px 11px);
  opacity:.75;animation:%(p)s-fade 3.4s ease-in-out infinite;}
@keyframes %(p)s-fade{0%%,100%%{opacity:.28}50%%{opacity:.85}}

@media (max-width:820px){
  .%(p)s-stage{margin:0 2px;height:360px;}
  .%(p)s-n .sb,.%(p)s-rel{display:none;}
  .%(p)s-n .val{font-size:.86rem;}
  .%(p)s-n .nm{font-size:.78rem;}
  .%(p)s-n[data-k="n2"] .val{font-size:1.4rem;}
  .%(p)s-n[data-k="n2"] .nm{font-size:1.05rem;}
  .%(p)s-n[data-k="rt"] .lab{transform:translateX(-16%%);}
  .%(p)s-n[data-k="n2"] .lab{transform:translateX(-78%%);}
  .%(p)s-tick{font-size:.78rem;}
  .%(p)s-unit{font-size:.76rem;}
}
""" % {'p': P}


def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, '941 — これまでのどれより、桁がひとつ大きい',
                        'この連載で使ってきた「結びつきの強さ」の物差しに、'
                        '窒素の三重結合を置きました。'
                        '丸にカーソルを合わせる（スマホはタップ）と説明が出ます。'),
         '<div class="%s-stage">' % P]

    o.append('<div class="%s-shade" style="width:%.3f%%"></div>' % (P, pos(2.5)))
    o.append('<div class="%s-track"></div>' % P)

    for v, lab in TICKS:
        o.append('<div class="%s-tick" style="left:%.3f%%"><i></i>%s</div>'
                 % (P, pos(v), lab))
    for v in MINOR:
        o.append('<div class="%s-tick m" style="left:%.3f%%"><i></i></div>'
                 % (P, pos(v)))
    o.append('<div class="%s-unit">結びつきの強さ（kJ/mol・対数目盛）</div>' % P)

    o.append('<div class="%s-rel" style="left:%.3f%%;top:10px;width:%.3f%%">'
             '水素結合の 47 倍<u></u></div>'
             % (P, (pos(20) + pos(941)) / 2, pos(941) - pos(20)))

    for key, name, val, disp, tok, top, labh, sub, detail in NODES:
        st = top + labh + 6
        sh = TRACK_Y - st - 8
        lab = ('<div class="val">%s<span style="font-size:.58em;font-weight:600;'
               'opacity:.8"> kJ/mol</span></div><div class="nm">%s</div>'
               % (disp, name))
        if sub:
            lab += '<div class="sb">%s</div>' % sub
        stem = ('<div class="stem" style="top:%dpx;height:%dpx"></div>'
                % (st, sh)) if sh > 4 else ''
        o.append('<div class="%s-n" data-k="%s" data-detail="%s" '
                 'style="left:%.3f%%;--c:var(--%s)">'
                 '<div class="lab" style="top:%dpx">%s</div>%s'
                 '<div class="dot"></div></div>'
                 % (P, key, efig.attr(detail), pos(val), tok, top, lab, stem))

    o.append('</div>')

    o.append(efig.close_card(
        P,
        '窒素の三重結合は <b>941 kJ/mol</b>。'
        '寝癖の留め金（水素結合 約20）の <b>47 倍</b>、'
        'パーマの薬剤がやっと切るシスチン結合（約250）の <b>約4倍</b>、'
        '水を水にしている共有結合（463）の、さらに <b>2 倍</b>です。'
        '<b>自然界の二原子分子の中で、最も強い部類の結びつき</b>にあたります。'
        'あなたの体がこれを開けられないのは、'
        '<b>やる気の問題ではなく、力が足りないから</b>です。',
        '941 kJ/mol は高精度実測 78,691.09 ± 0.15 cm⁻¹'
        '（<i>J. Chem. Phys.</i> 160, 014304 (2024)）を換算したもの。'
        '比較に使った 20・250・463 kJ/mol と体温の 2.5 kJ/mol は'
        '<a href="/posts/note/element-01-hydrogen/">第1回</a>で使った値です'
        '（体温は RT ＝ 気体定数 × 300 K）。'
        '結合の強さは測り方によって数 kJ/mol 前後します。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    print('941 / 20  = %.0f 倍' % (941 / 20.))
    print('941 / 250 = %.1f 倍' % (941 / 250.))
    print('941 / 463 = %.2f 倍' % (941 / 463.))
    for v in (2.5, 20, 250, 463, 941):
        print('  %7.1f -> %5.2f %%' % (v, pos(v)))
    efig.save('_fig2_triple.qmd', build())
