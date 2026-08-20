# -*- coding: utf-8 -*-
"""
元素 #1 水素 / 図3 : 「ちょうどいい弱さ」を一本の対数数直線に並べる。

  O–H 共有結合      463 kJ/mol    平均結合エンタルピー。水の 1 本目 497 と
                                  2 本目 426（Luo 2007）の平均で、解離エネル
                                  ギーそのものではない。混同しないこと
  水素結合          約 20 kJ/mol  水の O–H...O。文献値は 15-25
  体温の熱エネルギー 2.494 kJ/mol RT = 8.314 J/(mol K) x 300 K
  ファンデルワールス力 約 1 kJ/mol

読み取らせたいこと:
  水素結合は共有結合の約 1/23。しかし体温の熱エネルギーの約 8 倍。
  ゆえに「体温では勝手にほどけない。しかし押せばほどける」。

出力: _fig3_bond_energy.qmd
"""
import math
import efig

P, CID = 'ebond', 'ebond3'
LO, HI = 0.5, 1000.0          # 対数軸の左右端 (kJ/mol)
PAD = 2.5                     # 左右の余白 (%)。端の目盛りラベルが切れないように
TRACK_Y = 320
RT = 2.494                    # 体温の熱エネルギー


def pos(v):
    """kJ/mol -> トラック上の位置 (%)"""
    f = (math.log10(v) - math.log10(LO)) / (math.log10(HI) - math.log10(LO))
    return PAD + f * (100.0 - 2 * PAD)


# key, 表示名, 値, 単位表示, 色トークン, ラベル上端 y, ラベル高さ, 補足, 詳細文
#   縦位置は重なりを実測して決め打ちしている。文言を変えたら必ず見直すこと。
NODES = [
    ('hb', '水素結合', 20.0, '約 20', 'hb', 96, 90,
     '水の分子どうしをつなぐ力',
     'この記事の主役です。体温では勝手にほどけないのに、'
     '少し押せばほどける。おかげでタンパク質は形を変えられます。'),
    ('rt', '体温の熱エネルギー', RT, '2.5', 'rt', 196, 48, None,
     '体温（約 27 ℃）で分子が持っている熱の激しさです。'
     'これが「ほどける／ほどけない」の境目になります。'),
    ('cov', '共有結合  O–H', 463.0, '463', 'cov', 196, 66,
     '水の分子そのものを作る力',
     '水素と酸素をつないで H₂O という分子にしている力です。'
     'これがほどけるときは、水が水でなくなるときです。'),
    ('vdw', 'ファンデルワールス力', 1.0, '約 1', 'vdw', 258, 48, None,
     'いちばん弱い引き合いです。体温の熱エネルギーより弱いので、'
     'くっついてもすぐにほどけてしまいます。'),
]

TICKS = [(1, '1'), (10, '10'), (100, '100'), (1000, '1,000')]
MINOR = [2, 3, 5, 7, 20, 30, 50, 70, 200, 300, 500, 700]

CSS = """
.%(p)s-stage{position:relative;height:410px;margin:0 8px;}
.%(p)s-track{position:absolute;left:0;right:0;top:320px;height:2px;
  background:linear-gradient(90deg,#DED4C0,#C6B79D 55%%,#DED4C0);border-radius:2px;}
.%(p)s-track::after{content:"";position:absolute;top:-1px;left:0;width:22%%;
  height:4px;border-radius:4px;filter:blur(1px);
  background:linear-gradient(90deg,transparent,#7A6AA0,transparent);
  animation:%(p)s-sweep 7s cubic-bezier(.5,0,.5,1) infinite;}
@keyframes %(p)s-sweep{0%%{left:-24%%;opacity:0}
  12%%{opacity:.85}88%%{opacity:.85}100%%{left:102%%;opacity:0}}
.%(p)s-band{position:absolute;top:317px;height:8px;border-radius:8px;
  background:var(--hb);opacity:.85;box-shadow:0 0 0 1px rgba(190,100,10,.30);}

.%(p)s-tick{position:absolute;top:334px;transform:translateX(-50%%);
  text-align:center;color:var(--faint);font-size:.82rem;}
.%(p)s-tick i{display:block;width:1px;height:9px;margin:0 auto 5px;
  background:#D2C6AF;}
.%(p)s-tick.m i{height:5px;background:#E4DACA;}
.%(p)s-unit{position:absolute;top:378px;right:0;color:var(--faint);
  font-size:.82rem;}

.%(p)s-shade{position:absolute;top:90px;height:230px;left:0;
  background:linear-gradient(90deg,rgba(196,43,60,0),rgba(196,43,60,.11));
  border-right:1px dashed rgba(196,43,60,.55);}

.%(p)s-n{position:absolute;top:0;bottom:0;width:0;cursor:default;}
.%(p)s-n .lab{position:absolute;transform:translateX(-50%%);text-align:center;}
.%(p)s-n .dot{position:absolute;top:314px;left:-7px;width:14px;height:14px;
  border-radius:50%%;background:var(--c);
  box-shadow:0 0 0 3px #FFFDF9,0 0 0 4px var(--c);}
.%(p)s-n .stem{position:absolute;left:0;width:1px;
  background:linear-gradient(rgba(122,96,52,.114),var(--c));opacity:.6;}
.%(p)s-n .val{font-size:1.12rem;font-weight:800;color:var(--c);
  letter-spacing:.01em;white-space:nowrap;line-height:1.35;}
.%(p)s-n .nm{font-size:1rem;font-weight:700;color:var(--ink);
  white-space:nowrap;line-height:1.4;}
.%(p)s-n .sb{font-size:.83rem;color:var(--dim);white-space:nowrap;
  line-height:1.4;margin-top:1px;}
.%(p)s-n[data-k="hb"] .val{font-size:1.8rem;}
.%(p)s-n[data-k="hb"] .nm{font-size:1.4rem;font-weight:800;}
.%(p)s-n[data-k="hb"] .dot{top:311px;left:-10px;width:20px;height:20px;}
.%(p)s-n[data-k="hb"] .dot::after{content:"";position:absolute;inset:-5px;
  border-radius:50%%;border:2px solid var(--hb);
  animation:%(p)s-ring 2.9s ease-out infinite;}
@keyframes %(p)s-ring{0%%{transform:scale(.6);opacity:.75}
  70%%,100%%{transform:scale(2.6);opacity:0}}

.%(p)s-rel{position:absolute;transform:translateX(-50%%);text-align:center;
  color:var(--hb);font-size:.92rem;font-weight:700;white-space:nowrap;}
.%(p)s-rel u{display:block;height:1px;margin-top:6px;text-decoration:none;
  background:repeating-linear-gradient(90deg,var(--hb) 0 6px,transparent 6px 11px);
  opacity:.75;animation:%(p)s-fade 3.4s ease-in-out infinite;}
@keyframes %(p)s-fade{0%%,100%%{opacity:.28}50%%{opacity:.85}}

@media (max-width:820px){
  .%(p)s-stage{margin:0 2px;}
  .%(p)s-n .sb,.%(p)s-rel{display:none;}
  .%(p)s-n .val{font-size:.84rem;}
  .%(p)s-n .nm{font-size:.78rem;}
  .%(p)s-n[data-k="hb"] .val{font-size:1.3rem;}
  .%(p)s-n[data-k="hb"] .nm{font-size:1.05rem;}
  .%(p)s-n[data-k="vdw"] .lab{transform:translateX(-18%%);}
  .%(p)s-n[data-k="cov"] .lab{transform:translateX(-82%%);}
  .%(p)s-tick{font-size:.76rem;}
  .%(p)s-unit{font-size:.74rem;}
}

/* 握手のたとえ帯。
   数直線だけでは「20 という数の弱さ」が体に入らないので、
   同じ4つを握手の深さに置き換えて下に並べる。
   点と同じ色トークン（--c）を継ぐので、どの点の話かは色で分かる。 */
.%(p)s-hslab{margin:20px 8px 8px;font-size:.92rem;color:var(--dim);}
.%(p)s-hs{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;
  margin:0 8px;}
.%(p)s-hc{padding:13px 9px 12px;border-radius:12px;text-align:center;
  background:rgba(122,96,52,.085);
  border:1px solid rgba(122,96,52,.171);cursor:default;
  transition:background .18s ease,border-color .18s ease;}
.%(p)s-hc:hover{background:rgba(122,96,52,.162);
  border-color:rgba(122,96,52,.38);}
/* 体温だけは結びつきではないので、枠を破線にして区別する */
.%(p)s-hc.q{border-style:dashed;}
.%(p)s-hc svg{display:block;width:64px;height:40px;margin:0 auto 9px;
  color:var(--c);}
.%(p)s-hc b{display:block;font-size:.9rem;font-weight:800;color:var(--c);
  line-height:1.45;}
.%(p)s-hc b em{font-style:normal;font-weight:600;font-size:.85em;opacity:.78;}
.%(p)s-hc s{display:block;text-decoration:none;font-size:.8rem;
  color:var(--dim);line-height:1.55;margin-top:4px;}
@media (max-width:820px){
  .%(p)s-hslab{font-size:.84rem;margin:16px 2px 7px;}
  .%(p)s-hs{grid-template-columns:repeat(2,1fr);gap:8px;margin:0 2px;}
  .%(p)s-hc{padding:11px 6px 10px;}
  .%(p)s-hc svg{width:54px;height:34px;margin-bottom:7px;}
  .%(p)s-hc b{font-size:.8rem;}
  .%(p)s-hc s{font-size:.72rem;}
}
""" % {'p': P}


def grip(sep, sw, weld=False, gapmark=False):
    """二つのフックの噛み合いで結びつきの強さを表すアイコン。

    sep が小さいほど深く噛み合い、sw（線の太さ）が強さを補強する。
    weld=True は「溶接された握手」＝共有結合、
    gapmark=True は「触れていない」＝ファンデルワールス力に使う。
    """
    c1, c2 = 32.0 - sep / 2.0, 32.0 + sep / 2.0
    # 半径 11 の円弧を 270 度ぶん描くと、右（左）が開いたフックになる
    d1 = 'M%.1f 12.2 A11 11 0 1 0 %.1f 27.8' % (c1 + 7.8, c1 + 7.8)
    d2 = 'M%.1f 12.2 A11 11 0 1 1 %.1f 27.8' % (c2 - 7.8, c2 - 7.8)
    s = ['<svg viewBox="0 0 64 40" aria-hidden="true">',
         '<g fill="none" stroke="currentColor" stroke-width="%.1f" '
         'stroke-linecap="round">' % sw,
         '<path d="%s"/><path d="%s"/>' % (d1, d2),
         '</g>']
    if weld:
        s.append('<rect x="27" y="15.5" width="10" height="9" rx="2.5" '
                 'fill="currentColor" opacity=".9"/>')
    if gapmark:
        s.append('<path d="M27 20 h10" stroke="currentColor" '
                 'stroke-width="1.4" stroke-dasharray="2 2.5" opacity=".55"/>')
    s.append('</svg>')
    return ''.join(s)


def shake():
    """体温のゆさぶり。結びつきではないので、握手ではなく揺れで描く。"""
    return ('<svg viewBox="0 0 64 40" aria-hidden="true">'
            '<g fill="none" stroke="currentColor" stroke-width="2.4" '
            'stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M22 20 q5 -9 10 0 t10 0"/>'
            '<path d="M13 14 l-5 6 5 6" opacity=".65"/>'
            '<path d="M51 14 l5 6 -5 6" opacity=".65"/>'
            '</g></svg>')


# 握手のたとえ帯。数直線の4点と 1 対 1 に対応させる。
#   key（色トークン）, 名前, 値, たとえ, アイコン, 読み取り帯に出す文
HANDS = [
    ('cov', '共有結合', '463', 'コンクリートで<br>固めた握手',
     grip(8, 5.2, weld=True),
     '水の分子そのものを作っている力です。これがほどけるときは、'
     '<b>水が水でなくなるとき</b>です。'),
    ('hb', '水素結合', '約 20', '小指を<br>からめた握手',
     grip(18, 3.2),
     'この記事の主役です。<b>放っておけば離れないのに、'
     'その気になれば離せる</b>——この一点に生き物がぶら下がっています。'),
    ('rt', '体温のゆさぶり', '2.5', '肩をポンと<br>叩かれる程度',
     shake(),
     'これは結びつきではなく、<b>ほどこうとする側の力</b>です。'
     '水素結合はこれの約 8 倍あるので、体温では外れません。'),
    ('vdw', 'ファンデル<br>ワールス力', '約 1', '指先が<br>触れただけ',
     grip(30, 2.0, gapmark=True),
     '体温のゆさぶりより弱いので、'
     '<b>くっついてもすぐにほどけてしまいます</b>。'),
]


def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, '水素結合は「ちょうどいい弱さ」',
                        '結びつきの強さを一本の数直線に並べました。'
                        '丸にカーソルを合わせる（スマホはタップ）と説明が出ます。'),
         '<div class="%s-stage">' % P]

    o.append('<div class="%s-shade" style="width:%.3f%%"></div>' % (P, pos(RT)))
    o.append('<div class="%s-track"></div>' % P)
    o.append('<div class="%s-band" style="left:%.3f%%;width:%.3f%%"></div>'
             % (P, pos(15), pos(25) - pos(15)))

    for v, lab in TICKS:
        o.append('<div class="%s-tick" style="left:%.3f%%"><i></i>%s</div>'
                 % (P, pos(v), lab))
    for v in MINOR:
        o.append('<div class="%s-tick m" style="left:%.3f%%"><i></i></div>'
                 % (P, pos(v)))
    o.append('<div class="%s-unit">結びつきの強さ（kJ/mol・対数目盛）</div>' % P)

    o.append('<div class="%s-rel" style="left:%.3f%%;top:14px;width:%.3f%%">'
             '共有結合の約 1/23 の弱さ<u></u></div>'
             % (P, (pos(20) + pos(463)) / 2, pos(463) - pos(20)))
    o.append('<div class="%s-rel" style="left:%.3f%%;top:54px;width:%.3f%%">'
             '体温の約 8 倍の強さ<u></u></div>'
             % (P, (pos(RT) + pos(20)) / 2, pos(20) - pos(RT)))

    for key, name, val, disp, tok, top, labh, sub, detail in NODES:
        st = top + labh + 6
        sh = TRACK_Y - st - 8
        lab = ('<div class="val">%s<span style="font-size:.6em;font-weight:600;'
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
                 % (P, key, detail, pos(val), tok, top, lab, stem))

    o.append('</div>')

    o.append('<p class="%s-hslab">同じ4つを、握手の深さに置き換えると</p>' % P)
    o.append('<div class="%s-hs">' % P)
    for tok, name, val, cap, icon, detail in HANDS:
        o.append('<div class="%s-hc%s" data-detail="%s" '
                 'style="--c:var(--%s)">%s<b>%s <em>%s</em></b><s>%s</s></div>'
                 % (P, ' q' if tok == 'rt' else '', detail, tok,
                    icon, name, val, cap))
    o.append('</div>')

    o.append(efig.close_card(
        P,
        '水素結合は、共有結合の <b>約 1/23</b> しかない弱い力です。'
        'ところが体温の熱エネルギーの <b>約 8 倍</b>はあります。'
        'つまり<b>体温では勝手にほどけないのに、少し押せばほどける</b>。'
        'コンクリートで固めた握手と、小指をからめただけの握手ほどの差です。'
        'この絶妙な強さが、生き物の形を支えています。',
        '共有結合の 463 kJ/mol は O–H の平均結合エンタルピーです'
        '（水の 1 本目 497、2 本目 426 の平均。値は Luo (2007) による）。'
        '水素結合は水の O–H···O の代表値（文献値 15–25 kJ/mol）。'
        '体温の熱エネルギーは RT（気体定数 × 300 K）。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    efig.save('_fig3_bond_energy.qmd', build())
