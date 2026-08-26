# -*- coding: utf-8 -*-
"""
元素 #3 酸素 / 図1 : 酸素原子はどこにでもある。珍しいのは「自由な O₂」のほう。

読者の思いこみを最初に外すための図。
「酸素＝呼吸する気体」と思っている人に、酸素原子は水にも岩にも体にも
びっしり詰まっていて、むしろ<気体として自由でいるほうが異常>だと見せる。

  水     質量の 88.8%  が酸素   ← 計算で出る（15.999 / 18.015）
  人体   質量の 65%    が酸素
  地殻   質量の 約46%  が酸素   ← 地球でいちばん多い元素
  乾燥空気 20.95%      が酸素   ← ただしこれだけが「自由な O2」

前半3つは<化合物に閉じこめられた酸素>で、他の元素と手を組んで動けない。
最後の1つだけが<ペアを組んで漂う自由な酸素>で、これは太陽系では地球だけ。
しかも生命が作り続けなければ、岩を錆びさせるなどして消えてしまう。

書き方の注意（HY指示「説は説と」）:
  「酸素ガスがあるのは地球だけ」は言いすぎ。彗星やエウロパから微量の O2 が
  見つかっている。正しくは「大気の2割を占めるような大量の O2 は地球だけ」。

出典:
  原子量（水の計算に使用）: IUPAC 2021 標準原子量 O 15.999 / H 1.008
  人体: 質量比で酸素 65%（#2 と同じ出典）
  地殻: 酸素 約46%（CRC Handbook。版により 46.1〜46.6%）
  乾燥空気: 酸素 20.946%（#2 の図6 と同じ値）

出力: _fig1_where.qmd
"""
import efig

P, CID = 'owhere', 'owhere1'

M_O, M_H = 15.999, 1.008
WATER = 2 * M_O / (2 * M_O + 4 * M_H) * 100.0   # H2O 2分子ぶんでも比は同じ

# (鍵, 名前, 酸素の割合%, 但し書き, 自由か)
ROW = [
    ('water', '水', M_O / (M_O + 2 * M_H) * 100.0,
     '水素とがっちり組んでいる', False),
    ('body',  'あなたの体', 65.0, 'ほとんどが水とタンパク質の中', False),
    ('crust', '地殻（岩と砂）', 46.0, 'ケイ素や鉄と組んで岩になっている', False),
    ('air',   '空気（乾燥）', 20.946, '**酸素どうしがペアを組んで漂っている**', True),
]

DET = {
    'water': '水の重さの<b>%.1f%%</b>は酸素です。'
             '水素2個と酸素1個でできていますが、'
             '酸素は水素の<b>16倍</b>重いので、'
             '重さで見ると圧倒的に酸素なのです。'
             'あなたの体重の6割は水——'
             'つまり体の大部分は、すでに酸素でできています。'
             'ただしこの酸素は水素とがっちり組んでいて、'
             '<b>そのままでは呼吸に使えません</b>。'
             % (M_O / (M_O + 2 * M_H) * 100.0),
    'body':  '人の体の重さの<b>65%</b>が酸素です。'
             '<a href="/posts/note/element-02-carbon/">前回</a>見たとおり、'
             '2位が炭素（18.5%）、3位が水素（9.5%）、4位が窒素（3.3%）。'
             'この4つで96%を超えます。'
             '<b>酸素は、あなたを作っている元素の第1位</b>です。',
    'crust': '地殻の重さの<b>約46%</b>が酸素で、これは<b>地球でいちばん多い元素</b>です。'
             '2位のケイ素（約28%）と組んで二酸化ケイ素になり、'
             '岩や砂を作っています。'
             '足もとの地面を持ち上げれば、その半分近くは酸素の重さです。'
             'ただしこれも<b>岩の中に閉じこめられていて、動きません</b>。',
    'air':   'そしてここだけが違います。'
             '乾燥した空気の<b>20.9%</b>は、'
             '酸素どうしがペアを組んだ<b>O₂ という気体</b>です。'
             '他の元素と組んでいない、<b>自由な酸素</b>。'
             'これは放っておけば岩を錆びさせ、生き物を焼き、'
             'やがて消えてしまう<b>不安定な状態</b>です。'
             'それでも 2 割の濃さが保たれています。'
             '<b>生き物が作り続けているから</b>です。',
}

BAR_MAX = 100.0

CSS = """
.@@P@@-list{margin:20px 8px 0;}
.@@P@@-line{margin:0 0 15px;cursor:default;}
.@@P@@-head{display:flex;align-items:baseline;justify-content:space-between;
  gap:10px;margin:0 0 5px;}
.@@P@@-nm{font-size:1rem;font-weight:700;color:var(--ink);}
.@@P@@-pc{font-size:1.12rem;font-weight:800;color:var(--dim);
  font-variant-numeric:tabular-nums;}
.@@P@@-line.is-free .@@P@@-pc{color:var(--hb);}
.@@P@@-track{position:relative;height:22px;border-radius:6px;
  background:rgba(122,96,52,.09);overflow:hidden;}
.@@P@@-fill{position:absolute;left:0;top:0;bottom:0;border-radius:6px;
  background:linear-gradient(90deg,#5E7F92,#3E5F73);
  transition:filter .16s ease;}
.@@P@@-line.is-free .@@P@@-fill{
  background:linear-gradient(90deg,#D8874A,#B0561F);}
.@@P@@-line:hover .@@P@@-fill{filter:brightness(1.12);}
.@@P@@-note{font-size:.82rem;color:var(--faint);margin:4px 0 0;}
.@@P@@-line.is-free .@@P@@-note{color:var(--hb);font-weight:700;}

.@@P@@-split{margin:22px 8px 0;display:grid;
  grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;}
.@@P@@-box{padding:14px 16px;border-radius:12px;font-size:.9rem;
  line-height:1.8;color:var(--ink);}
.@@P@@-box.is-lock{background:rgba(62,95,115,.08);
  border:1px solid rgba(62,95,115,.28);}
.@@P@@-box.is-free{background:rgba(190,100,10,.08);
  border:1px solid rgba(190,100,10,.36);}
.@@P@@-box b{display:block;font-size:1.02rem;margin:0 0 4px;}
.@@P@@-box.is-lock b{color:#33566B;}
.@@P@@-box.is-free b{color:var(--hb);}

.@@P@@-cap{margin:14px 8px 0;font-size:.84rem;color:var(--dim);
  line-height:1.75;}

@media (max-width:820px){
  .@@P@@-list{margin:16px 2px 0;}
  .@@P@@-nm{font-size:.9rem;}
  .@@P@@-pc{font-size:1rem;}
  .@@P@@-split{margin:18px 2px 0;gap:9px;}
  .@@P@@-box{padding:11px 12px;font-size:.82rem;}
  .@@P@@-cap{font-size:.78rem;margin:11px 2px 0;}
}
""".replace('@@P@@', P)


def check():
    print('水の中の酸素: %.4f%%（原子量 O %.3f / H %.3f から計算）'
          % (M_O / (M_O + 2 * M_H) * 100.0, M_O, M_H))
    assert abs(M_O / (M_O + 2 * M_H) * 100.0 - 88.81) < 0.02
    print('各行:')
    for key, name, pc, note, free in ROW:
        print('  %-14s %6.2f%%  %s' % (name, pc, '自由な O₂' if free else '化合物の中'))
    # 自由な酸素は1行だけ、という図の骨
    assert sum(1 for r in ROW if r[4]) == 1


def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, '酸素は、どこにでもいます',
                        '重さのうち何％が酸素かを並べました。'
                        'カーソルを合わせる（スマホはタップ）と、'
                        'その中身が下に出ます。'),
         '<div class="%s-list">' % P]

    for key, name, pc, note, free in ROW:
        o.append('<div class="%s-line%s" data-detail="%s">'
                 % (P, ' is-free' if free else '', efig.attr(DET[key])))
        o.append('<div class="%s-head"><span class="%s-nm">%s</span>'
                 '<span class="%s-pc">%.1f%%</span></div>' % (P, P, name, P, pc))
        o.append('<div class="%s-track"><div class="%s-fill" '
                 'style="width:%.2f%%"></div></div>'
                 % (P, P, pc / BAR_MAX * 100.0))
        o.append('<p class="%s-note">%s</p></div>'
                 % (P, note.replace('**', '')))
    o.append('</div>')

    o.append('<div class="%s-split">' % P)
    o.append('<div class="%s-box is-lock"><b>閉じこめられた酸素</b>'
             '水・体・岩の中の酸素は、ほかの元素とがっちり手を組んでいます。'
             '量では圧倒的に多いのですが、<b>動けません</b>。'
             '火星も月も、酸素はこの姿でしか存在しません。</div>' % P)
    o.append('<div class="%s-box is-free"><b>自由な酸素（O₂）</b>'
             '空気の2割だけが、どこにも縛られていない酸素です。'
             '<b>本来なら、すぐに何かと結びついて消えてしまう姿</b>。'
             'それが 2 割の濃さで保たれ続けている——'
             'ここに、この記事の話の全部があります。</div>' % P)
    o.append('</div>')

    o.append(efig.close_card(
        P,
        '酸素<b>原子</b>は、宇宙でも地球でもありふれています。'
        '水の重さの <b>%.1f%%</b>、地殻の <b>約46%%</b>、'
        'あなたの体の <b>65%%</b>。'
        '地球でいちばん多い元素は、鉄でも炭素でもなく酸素です。'
        'めずらしいのは、そちらではありません。'
        '<b>他の何とも組まずに、O₂ という気体のまま漂っていること</b>——'
        'こちらのほうが、はるかに異常なのです。'
        % (M_O / (M_O + 2 * M_H) * 100.0),
        '水の値は標準原子量（酸素 15.999、水素 1.008）からの計算です。'
        '人体は質量比で酸素 65%（酸素・炭素・水素・窒素の4つで96%を超えます）。'
        '地殻は約46%（CRC Handbook。版により 46.1〜46.6%）。'
        '乾燥空気の酸素は 20.946%。'
        '<b>「自由な O₂ があるのは地球だけ」とは書いていません。</b>'
        '彗星やエウロパなどからごく微量の O₂ が見つかっています。'
        '地球が特別なのは、<b>大気の2割を占めるほど大量に、'
        'かつ長期間保たれている</b>点です。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    check()
    efig.save('_fig1_where.qmd', build())
