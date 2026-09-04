# -*- coding: utf-8 -*-
"""
元素 #4 窒素 / 図5 : 941 の鍵を、誰が開けているのか。

年あたりの窒素固定量（Tg N ＝ 100 万トン）:
  雷            3〜5        瞬間 3 万度で無理やり引き裂く
  生き物        100〜175    根粒菌など。常温常圧でやってのける
  ハーバー・ボッシュ 100〜120  高温高圧＋鉄触媒

**講演資料などで「雷が植物の栄養の 10〜20% を供給する」とされることがあるが、
上の推定と桁が合わない。** 自然に開かれる分を分母にして 2〜5%、
人工固定まで含めると 1〜2%。**分母を明示しないと読者が検算できない**ので両方出す。
さらに雷を陸地に配ると 0.2〜0.34 kg N/ha・年で、水稲の必要量 100 kg N/ha の
1% にも足りない。**「雷が稲を育てる」はこの図では説明がつかない**（結びで回収）。

推定に幅があるので、棒は帯（範囲）で描く。#3 酸素の収支図と同じ作法。

出力: _fig5_fixation.qmd
"""
import efig

P, CID = 'nfix', 'nfix5'

#  key, 名前, 下限, 上限, 色, 一言, 詳細文
WAYS = [
    ('lit', '雷', 3.0, 5.0, '#C1650A', '瞬間 3 万度でこじ開ける',
     '稲妻の温度は<b>約 3 万度</b>。太陽の表面（約 6 千度）より'
     'はるかに熱い。この一瞬の高温と電気が三重結合を引き裂き、'
     '砕けた窒素が雨に溶けて土に落ちます。'
     '<b>ただし量はごくわずかで、稲を育てるには遠く及びません。</b>'),
    ('bio', '生き物', 100.0, 175.0, '#2E6E4E', '根粒菌・土の細菌・藍藻',
     'いちばん有名なのはマメ科の根に住む<b>根粒菌</b>です。'
     '豆を引き抜けば、根に小さな粒がびっしり付いているのが見えます。'
     'ただし担い手はそれだけではなく、<b>土の中で単独で暮らす細菌も、'
     '海に漂う藍藻（シアノバクテリア）も、同じことをしています</b>。'
     '<b>人類が高温高圧の工場でやることを、常温常圧でやってのける。</b>'),
    ('hb', 'ハーバー・ボッシュ法', 100.0, 120.0, '#5E96C4',
     '高温高圧＋鉄の触媒',
     '1909 年にハーバーが原理を示し、ボッシュが工場にしました。'
     '<b>いま地球にいる人のおよそ半分が、この反応で作られた窒素を食べています。</b>'
     '100 年以上たっても、原理は変わっていません。'),
]

SPAN = 180.0        # 棒の全長に対応させる量（Tg N/年）
TOT_LO = sum(w[2] for w in WAYS)
TOT_HI = sum(w[3] for w in WAYS)


def pct(v):
    return 100.0 * v / SPAN


CSS = """
.%(p)s{--lit:#C1650A;--bio:#2E6E4E;--hb:#5E96C4;}
.%(p)s-lab{margin:20px 8px 10px;font-size:.92rem;color:var(--dim);}
.%(p)s-rows{display:grid;gap:15px;margin:0 8px;}
.%(p)s-r{cursor:default;}
.%(p)s-r .hd{display:flex;align-items:baseline;gap:10px;margin:0 0 6px;}
.%(p)s-r .nm{font-size:1.04rem;font-weight:800;color:var(--c);}
.%(p)s-r .sb{font-size:.84rem;color:var(--dim);margin-left:auto;
  text-align:right;line-height:1.5;}
.%(p)s-tr{position:relative;height:28px;border-radius:7px;
  background:rgba(122,96,52,.07);border:1px solid rgba(122,96,52,.13);
  overflow:hidden;transition:background .18s ease;}
.%(p)s-r:hover .%(p)s-tr{background:rgba(122,96,52,.15);}
.%(p)s-bd{position:absolute;top:0;bottom:0;left:0;border-radius:6px;
  background:linear-gradient(90deg,
    color-mix(in srgb,var(--c) 36%%,transparent),
    color-mix(in srgb,var(--c) 82%%,transparent));}
/* 推定に幅があるので、右端をぼかす */
.%(p)s-bd::after{content:"";position:absolute;top:0;bottom:0;right:0;
  width:34%%;background:linear-gradient(90deg,transparent,rgba(255,253,249,.6));}
.%(p)s-tk{position:absolute;top:-2px;bottom:-2px;width:2px;
  background:var(--c);opacity:.85;}
.%(p)s-vl{position:absolute;top:50%%;transform:translateY(-50%%);
  font-size:.84rem;font-weight:700;color:var(--ink);white-space:nowrap;
  padding:0 10px;}

.%(p)s-hit{margin:22px 8px 6px;padding:17px 19px;border-radius:12px;
  background:rgba(193,101,10,.09);border:1px solid rgba(193,101,10,.28);}
.%(p)s-hit .a{font-size:1.4rem;font-weight:800;color:var(--lit);
  line-height:1.5;}
.%(p)s-hit .b{font-size:.9rem;color:var(--dim);margin-top:5px;
  line-height:1.75;}
.%(p)s-hit .b b{color:var(--ink);}

@media (max-width:820px){
  .%(p)s-lab{font-size:.84rem;margin:16px 2px 9px;}
  .%(p)s-rows{margin:0 2px;gap:12px;}
  .%(p)s-r .nm{font-size:.9rem;}
  .%(p)s-r .sb{display:none;}
  .%(p)s-tr{height:24px;}
  .%(p)s-vl{font-size:.74rem;padding:0 7px;}
  .%(p)s-hit{margin:17px 2px 4px;padding:13px 14px;}
  .%(p)s-hit .a{font-size:1.08rem;}
  .%(p)s-hit .b{font-size:.8rem;}
}
""" % {'p': P}


def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, '941 の鍵を、誰が開けているのか',
                        '1 年あたりに開かれる窒素の量です。棒はすべて同じ物差し。'
                        '行にカーソルを合わせる（スマホはタップ）と説明が出ます。')]

    o.append('<p class="%s-lab">1 年に開かれる窒素の量'
             '（100 万トン単位）</p>' % P)
    o.append('<div class="%s-rows">' % P)
    for key, name, lo, hi, col, sub, detail in WAYS:
        val = '%d 〜 %d' % (lo, hi)
        left = ('left:%.2f%%' % min(pct(hi) + 1.4, 60.0)) \
            if pct(hi) < 26 else 'left:0'
        o.append('<div class="%s-r" data-detail="%s" style="--c:var(--%s)">'
                 '<div class="hd"><span class="nm">%s</span>'
                 '<span class="sb">%s</span></div>'
                 '<div class="%s-tr">'
                 '<div class="%s-bd" style="width:%.2f%%"></div>'
                 '<div class="%s-tk" style="left:%.2f%%"></div>'
                 '<div class="%s-vl" style="%s">%s</div></div></div>'
                 % (P, efig.attr(detail), key, name, sub,
                    P, P, pct(hi), P, pct(lo), P, left, val))
    o.append('</div>')

    # 分母を 2 通り出す。本文は「自然に開かれる分」を使うので、そちらを大きく。
    nat_lo, nat_hi = 5.0 + 175.0, 3.0 + 100.0
    s_nat_lo = 100.0 * 3.0 / nat_lo
    s_nat_hi = 100.0 * 5.0 / nat_hi
    s_all_lo = 100.0 * 3.0 / TOT_HI
    s_all_hi = 100.0 * 5.0 / TOT_LO
    o.append('<div class="%s-hit" data-detail="%s">'
             '<div class="a">自然に開かれる分のうち、雷は %.0f〜%.0f%%</div>'
             '<div class="b"><b>雷が稲を育てるという言い伝えを、'
             'これで説明することはできません。</b>'
             '雷が届ける窒素は、陸地に配っても 1 ヘクタールあたり 0.3 キロほど。'
             '水稲が必要とする量（100 キロ前後）の <b>1%% にも足りません</b>。'
             'そして雷と生き物を合わせても、'
             '<b>80 億人を食べさせるには足りませんでした。</b></div></div>'
             % (P, efig.attr(
                 '分母の取り方で数字が変わります。'
                 '<b>自然に開かれる分（雷＋生き物）を分母にすると %.0f〜%.0f%%、'
                 '人間の工場まで含めた総量を分母にすると %.0f〜%.0f%%</b> です。'
                 'なお講演資料などで「雷が植物の栄養の 10〜20%% を供給する」と'
                 'されることがありますが、<b>上の推定とは桁が合いません</b>。'
                 % (s_nat_lo, s_nat_hi, s_all_lo, s_all_hi)),
                s_nat_lo, s_nat_hi))

    o.append(efig.close_card(
        P,
        '三重結合を開けるのは、自然界では <b>雷</b>（瞬間 3 万度）と'
        '<b>生き物</b>（常温常圧）の 2 通りでした。'
        'そこへ 20 世紀に <b>ハーバー・ボッシュ法</b>が加わります。'
        '量で見ると <b>雷はごくわずか</b>で、'
        '<b>人間の工場は、地球上の生き物ぜんぶに匹敵する量を開けている</b>ことが'
        '分かります。'
        '<b>「雷が稲を育てる」は、この図では説明がつきません。</b>'
        'その答えは記事の最後にあります。',
        '年あたりの固定量（Tg N＝100 万トン）：雷 3〜5、'
        '生物的固定 100〜175、ハーバー・ボッシュ法 100〜120。'
        '<b>いずれも推定に幅があるので、棒の右端をぼかしてあります</b>'
        '（#3 酸素の収支図と同じ描き方です）。'
        '<b>割合は分母の取り方で変わります</b>——自然に開かれる分（雷＋生き物）'
        'を分母にすると 2〜5%、人工固定まで含めた総量を分母にすると 1〜2% です。'
        '本文は前者を使っています。'
        '生物的固定の推定は文献差が大きく、陸域だけで 60〜90 Tg N/年 と'
        'する報告もあります。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    print('合計 %.0f 〜 %.0f Tg N/年' % (TOT_LO, TOT_HI))
    print('雷の割合 %.1f 〜 %.1f %%'
          % (100 * 3.0 / TOT_HI, 100 * 5.0 / TOT_LO))
    efig.save('_fig5_fixation.qmd', build())
