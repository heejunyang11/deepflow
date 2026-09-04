# -*- coding: utf-8 -*-
"""
元素 #4 窒素 / 図1 : 空気の分子 100 個。そのうち体が使えるのは何個か。

#1 は「宇宙の原子 100 個」、#2 は「空気の分子 1 万個」を並べた。
今回は 100 個。連載として同じ数え方を繰り返すことで、比較が効く。

乾燥空気の体積比（＝分子数の比）:
  窒素   78.084 %
  酸素   20.946 %
  アルゴン 0.934 %
  二酸化炭素 約 0.043 %   -> 100 個では 1 個も出てこない

読み取らせたいこと:
  (1) 100 個のうち 78 個が窒素。二酸化炭素は 1 個も出ない（1,800 倍以上の差）
  (2) その 78 個は、**全部が鍵のかかった状態**。体は 1 個も使えない
  -> 「食べ物の山の中で飢えている」という記事の問いが、絵として立つ

出力: _fig1_air.qmd
"""
import efig

P, CID = 'nair', 'nair1'

N2, O2, AR, CO2 = 78.084, 20.946, 0.934, 0.0428

# 100 個に丸める。合計がちょうど 100 になるよう、多い順に配る
CELLS = [('n2', 78), ('o2', 21), ('ar', 1)]

INFO = {
    'n2': ('窒素 N₂', '78.084%',
           '<b>100 個のうち 78 個。</b>ところがこの 78 個は、'
           'すべて<b>三重結合という鍵</b>がかかっています。'
           'あなたの体は、この中から 1 原子も取り出せません。'),
    'o2': ('酸素 O₂', '20.946%',
           '<a href="/posts/note/element-03-oxygen/">前回</a>の主役。'
           'こちらは体が使えます。<b>使えるほうが少数派</b>だというのが、'
           'この図の見どころです。'),
    'ar': ('アルゴン Ar', '0.934%',
           '3 番目に多い成分です。'
           '<b>まったく何とも反応しません</b>（貴ガス）。'
           '窒素が「開かない」のとは理由が違い、こちらは'
           '<b>もともと手を出す気がない</b>タイプです。'),
    'co2': ('二酸化炭素 CO₂', '約 0.043%',
            '<a href="/posts/note/element-02-carbon/">第2回</a>で'
            '1 万個のうち 4 個として数えたものです。'
            '<b>100 個では 1 個も出てきません。</b>'
            '窒素は、二酸化炭素の <b>1,800 倍以上</b>あります。'),
}

CSS = """
.%(p)s{--n2:#2E6E4E;--o2:#D8552A;--ar:#7A6AA0;--co2:#8C8271;}
.%(p)s-lab{margin:20px 8px 9px;font-size:.92rem;color:var(--dim);}
.%(p)s-grid{display:grid;grid-template-columns:repeat(20,1fr);gap:4px;
  margin:0 8px;}
.%(p)s-c{position:relative;aspect-ratio:1;border-radius:3px;
  background:var(--c);opacity:.9;}
/* 窒素のマスだけ、閉じた鍵を示す斜線を重ねる */
.%(p)s-c.lock::after{content:"";position:absolute;inset:0;border-radius:3px;
  background:repeating-linear-gradient(45deg,
    rgba(255,253,249,.55) 0 1.5px,transparent 1.5px 4px);}

.%(p)s-key{display:flex;flex-wrap:wrap;gap:8px;margin:14px 8px 0;}
.%(p)s-k{display:flex;align-items:center;gap:8px;padding:9px 13px;
  border-radius:10px;cursor:default;
  background:rgba(122,96,52,.06);border:1px solid rgba(122,96,52,.14);
  border-left:4px solid var(--c);transition:background .18s ease;}
.%(p)s-k:hover{background:rgba(122,96,52,.15);}
.%(p)s-k b{font-size:.94rem;font-weight:800;color:var(--c);}
.%(p)s-k s{text-decoration:none;font-size:.84rem;color:var(--dim);
  font-variant-numeric:tabular-nums;}
.%(p)s-k i{font-style:normal;font-size:.78rem;color:var(--faint);}

.%(p)s-hit{margin:20px 8px 6px;padding:16px 18px;border-radius:12px;
  background:rgba(46,110,78,.09);border:1px solid rgba(46,110,78,.26);}
.%(p)s-hit .a{font-size:1.5rem;font-weight:800;color:var(--n2);
  line-height:1.45;}
.%(p)s-hit .b{font-size:.9rem;color:var(--dim);margin-top:4px;line-height:1.7;}

@media (max-width:820px){
  .%(p)s-lab{font-size:.84rem;margin:16px 2px 8px;}
  .%(p)s-grid{grid-template-columns:repeat(10,1fr);gap:3px;margin:0 2px;}
  .%(p)s-key{margin:12px 2px 0;gap:6px;}
  .%(p)s-k{padding:7px 10px;gap:6px;}
  .%(p)s-k b{font-size:.84rem;}
  .%(p)s-k s{font-size:.76rem;}
  .%(p)s-k i{display:none;}
  .%(p)s-hit{margin:16px 2px 4px;padding:13px 14px;}
  .%(p)s-hit .a{font-size:1.15rem;}
  .%(p)s-hit .b{font-size:.8rem;}
}
""" % {'p': P}


def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, '空気の分子 100 個のうち、78 個が窒素です',
                        '乾燥した空気の成分を、分子 100 個で表しました。'
                        '下の札にカーソルを合わせる（スマホはタップ）と説明が出ます。')]

    o.append('<p class="%s-lab">空気の分子 100 個</p>' % P)
    o.append('<div class="%s-grid">' % P)
    for key, n in CELLS:
        for _ in range(n):
            o.append('<div class="%s-c%s" style="--c:var(--%s)"></div>'
                     % (P, ' lock' if key == 'n2' else '', key))
    o.append('</div>')

    o.append('<div class="%s-key">' % P)
    for key in ('n2', 'o2', 'ar', 'co2'):
        name, pct, detail = INFO[key]
        cnt = dict(CELLS).get(key, 0)
        o.append('<div class="%s-k" data-detail="%s" style="--c:var(--%s)">'
                 '<b>%s</b><s>%s</s><i>%s</i></div>'
                 % (P, efig.attr(detail), key, name, pct,
                    ('%d 個' % cnt) if cnt else '100 個では 0 個'))
    o.append('</div>')

    o.append('<div class="%s-hit" data-detail="%s">'
             '<div class="a">この 78 個は、すべて鍵がかかっています</div>'
             '<div class="b">斜線を入れたマスが窒素です。'
             '一生かけて吸い続けても、<b>あなたはここから 1 原子も取り出せません</b>。'
             'なぜ開かないのかは、次の図で。</div></div>'
             % (P, efig.attr(
                 'この図の主題です。<b>量の問題ではありません。</b>'
                 '窒素は酸素より多いのに、体はそのすべてを素通りさせています。')))

    o.append(efig.close_card(
        P,
        '乾燥した空気は、<b>78% が窒素</b>、21% が酸素、'
        '残りの 1% ほどにアルゴンなどが入ります。'
        '二酸化炭素は 0.043% ほどで、<b>100 個ではひとつも出てきません</b>'
        '（窒素は二酸化炭素の <b>1,800 倍以上</b>）。'
        'そして窒素の 78 個は、<b>すべて三重結合という鍵がかかった状態</b>です。'
        '<b>いちばん多い成分が、いちばん使えない。</b>'
        'これがこの記事の出発点になります。',
        '乾燥空気の体積比（＝分子数の比）：窒素 78.084%、酸素 20.946%、'
        'アルゴン 0.934%、二酸化炭素 約 0.043%。'
        '100 個に丸めているため、アルゴンは 1 個、'
        '二酸化炭素は 0 個として描いています。'
        '<a href="/posts/note/element-02-carbon/">第2回</a>では'
        '同じ空気を 1 万個で数え、二酸化炭素を 4 個として描きました。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    print('合計 %d 個' % sum(n for _, n in CELLS))
    print('N2 / CO2 = %.0f 倍' % (N2 / CO2))
    efig.save('_fig1_air.qmd', build())
