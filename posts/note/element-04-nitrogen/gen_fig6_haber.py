# -*- coding: utf-8 -*-
"""
元素 #4 窒素 / 図6 : 糞 → 戦争 → 空気。窒素を手に入れるための百年。

この記事の後半は化学ではなく世界史になる。年表で一本にする。

  1840年代  グアノ（ペルー沖の島の海鳥の糞）と、カリーチ（アタカマの硝石鉱床）。
            カリーチは糞ではなく大気起源の硝酸の蓄積。両者は別物
  1856年8月18日 グアノ諸島法（米）成立（ピアース署名）。無主のグアノの島は
            市民が合衆国領として主張してよい。※上院通過7/24・下院通過8/16。7月成立ではない
  1879-1883 硝石戦争（太平洋戦争）。チリ対ペルー＋ボリビア
            -> ボリビアは海岸州を失い、いまも内陸国
  1909年    ハーバーが鉄触媒で空気から窒素を取り出す原理を示す
  1913年    ボッシュが工場規模へ（BASF オッパウ）
  現在      年 1.7 億トンのアンモニア。世界の全エネルギー生産の 1〜2%
            人口の約半分（2008 年で 48%）がこの窒素を食べている

読み取らせたいこと:
  人類は窒素を手に入れるために、鳥の糞を奪い合い、戦争をし、
  最後に空気から取ることを覚えた。そして同じ反応がパンと爆薬の両方を作った。

出力: _fig6_haber.qmd
"""
import efig

P, CID = 'nhab', 'nhab6'

#  年, 見出し, 本文, 色トークン, 印
EVENTS = [
    ('1840年代', '2つの資源が、見つかる', 'gua',
     '<b>グアノ</b>＝ペルー沖のチンチャ諸島などに積もった海鳥の糞。'
     '<b>カリーチ（チリ硝石）</b>＝アタカマ砂漠の鉱床で、'
     'こちらは糞ではなく、<b>海塩や大気で生じた硝酸が1000万年規模の'
     '乾燥のもとで積もったもの</b>です。'
     '<b>別の場所の、別のもの</b>でした。'),
    ('1856年8月', 'アメリカが、法律を作る', 'gua',
     '<b>グアノ諸島法</b>（8月18日成立）。無人でどこの国のものでもない'
     'グアノの島は、<b>アメリカ市民が合衆国領として主張してよい</b>'
     'という法律です。100 を超える島が申し立てられ、'
     '<b>いくつかは現在もアメリカ領</b>です。'),
    ('1879–83', '硝石戦争', 'war',
     'チリ対ペルー＋ボリビア。きっかけは<b>ボリビアがチリ系の硝石会社に'
     'かけた輸出税</b>でした。争われたのは<b>グアノではなくカリーチ</b>で、'
     '名前がそう言っています（<b>Saltpeter War</b>）。'
     '<b>ボリビアは海岸州を失って内陸国になりました</b>'
     '（正式な割譲は1904年の条約）。'),
    ('1909年', 'ハーバー、空気に手をつける', 'air',
     'ドイツには硝石が出ません。<b>海を封鎖されれば、畑も軍隊も止まる。</b>'
     'フリッツ・ハーバーが狙ったのは、頭の上に無限にある<b>空気</b>でした。'
     '答えは<b>鉄の触媒</b>——高温高圧の中で、鉄が三重結合を開く手助けをする。'),
    ('1913年', 'ボッシュ、工場にする', 'air',
     'カール・ボッシュが工場の規模まで持ち上げます。'
     '「<b>空気からパンを作る</b>」と呼ばれた技術です。'
     'そして<b>同じ技術が、爆薬を無尽蔵にしました</b>。'
     '硝石が要らないということは、火薬も輸入が要らないということです。'),
    ('現在', '原理は、変わっていません', 'now',
     '<b>100 年以上たったいまも、当時見つかった鉄触媒を使っています。</b>'
     '変わったのは規模だけ。'
     '<b>人類が使うエネルギーの 1〜2% が、'
     '空気から窒素を引きはがすことに使われています。</b>'),
]

NOW = [
    ('年 1.7 億トン', 'アンモニアの生産量。約 8 割が肥料になります'),
    ('世界のエネルギーの 1〜2%', '941 という数字が、そのまま電気代になっています'),
    ('人口の約半分', '2000 年で 44%、2008 年で 48% という推定です'),
]

CSS = """
.%(p)s{--gua:#8C7A4A;--war:#B02A37;--air:#5E96C4;--now:#2E6E4E;}
.%(p)s-tl{position:relative;margin:22px 8px 0;padding-left:96px;}
/* 縦の背骨 */
.%(p)s-tl::before{content:"";position:absolute;left:78px;top:10px;bottom:10px;
  width:2px;background:linear-gradient(180deg,
    var(--gua) 0%%,var(--war) 34%%,var(--air) 66%%,var(--now) 100%%);
  opacity:.55;border-radius:2px;}
.%(p)s-e{position:relative;padding:0 0 20px;cursor:default;}
.%(p)s-e:last-child{padding-bottom:2px;}
.%(p)s-yr{position:absolute;left:-96px;top:1px;width:64px;text-align:right;
  font-size:.9rem;font-weight:800;color:var(--c);
  font-variant-numeric:tabular-nums;letter-spacing:-.01em;}
.%(p)s-dot{position:absolute;left:-24px;top:5px;width:13px;height:13px;
  border-radius:50%%;background:var(--c);
  box-shadow:0 0 0 3px #FFFDF9,0 0 0 4px var(--c);}
.%(p)s-e h5{margin:0 0 3px;font-size:1.04rem;font-weight:800;color:var(--ink);
  line-height:1.5;}
.%(p)s-e p{margin:0;font-size:.9rem;color:var(--dim);line-height:1.8;}
.%(p)s-e:hover h5{color:var(--c);}

.%(p)s-now{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;
  margin:22px 8px 6px;}
.%(p)s-n{padding:15px 14px;border-radius:12px;text-align:center;
  background:rgba(46,110,78,.08);border:1px solid rgba(46,110,78,.24);}
.%(p)s-n b{display:block;font-size:1.14rem;font-weight:800;color:var(--now);
  line-height:1.45;}
.%(p)s-n s{display:block;text-decoration:none;font-size:.8rem;color:var(--dim);
  line-height:1.6;margin-top:4px;}

@media (max-width:820px){
  .%(p)s-tl{margin:18px 2px 0;padding-left:74px;}
  .%(p)s-tl::before{left:58px;}
  .%(p)s-yr{left:-74px;width:48px;font-size:.78rem;}
  .%(p)s-dot{left:-20px;width:11px;height:11px;}
  .%(p)s-e h5{font-size:.92rem;}
  .%(p)s-e p{font-size:.8rem;}
  .%(p)s-now{grid-template-columns:1fr;gap:7px;margin:18px 2px 4px;}
  .%(p)s-n{padding:12px 12px;}
  .%(p)s-n b{font-size:1rem;}
  .%(p)s-n s{font-size:.75rem;}
}
""" % {'p': P}


def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, '糞 → 戦争 → 空気',
                        '窒素を手に入れるために、人類がたどった百年です。'
                        '各行にカーソルを合わせる（スマホはタップ）と説明が出ます。')]

    o.append('<div class="%s-tl">' % P)
    for yr, head, tok, detail in EVENTS:
        o.append('<div class="%s-e" data-detail="%s" style="--c:var(--%s)">'
                 '<span class="%s-yr">%s</span>'
                 '<span class="%s-dot"></span>'
                 '<h5>%s</h5><p>%s</p></div>'
                 % (P, efig.attr(detail), tok, P, yr, P, head,
                    detail.replace('<b>', '').replace('</b>', '')))
    o.append('</div>')

    o.append('<div class="%s-now">' % P)
    for big, sub in NOW:
        o.append('<div class="%s-n"><b>%s</b><s>%s</s></div>' % (P, big, sub))
    o.append('</div>')

    o.append(efig.close_card(
        P,
        '火薬にも肥料にも、窒素の化合物が要ります。'
        'ところが空気からは取れないので、<b>大量に手に入れるには掘るしかありませんでした</b>。'
        'そのために——<b>アメリカは法律を作って島を取りに行き、'
        'チリとペルーとボリビアは戦争をしました</b>。'
        'ボリビアはそのとき海を失い、いまも内陸国のままです。'
        'そして 20 世紀に、ドイツの化学者が<b>空気から取る方法</b>を見つけます。'
        '<b>その方法は 100 年以上たったいまも同じで、'
        '人類の約半分を養い、世界のエネルギーの 1〜2% を使っています。</b>',
        'グアノ諸島法は <b>1856 年 8 月 18 日成立</b>（上院通過 7 月 24 日、下院通過 8 月 16 日）。'
        '硝石戦争（太平洋戦争）は 1879〜1883 年で、'
        'きっかけはボリビアがチリ系の硝石会社に課した輸出税で、<b>争われたのはグアノではなくカリーチ（チリ硝石）</b>でした。ペルーとの講和は 1883 年、ボリビア海岸州の正式な割譲は 1904 年の条約です。'
        'ハーバー・ボッシュ法は<b>アルヴィン・ミタシュが見つけた鉄触媒</b>を'
        '現在も使っており、原理は開発当初から根本的に変わっていません。'
        '人口の割合は Erisman <i>et al.</i> (2008) '
        '<i>Nature Geoscience</i> 1, 636–639 による推定で、'
        '<b>「世界人口の約半分」であって「体内の窒素の約半分」ではありません</b>。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    efig.save('_fig6_haber.qmd', build())
