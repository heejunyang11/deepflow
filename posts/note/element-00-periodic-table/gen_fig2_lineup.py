# -*- coding: utf-8 -*-
"""
元素 #0 序章 / 図2 : この連載で取り上げる 14 元素の顔ぶれ。

読み取らせたいこと:
  14 個がばらばらに選ばれたのではなく、族（縦の列）で対になっていること。
  Na と K、C と Si、N と P、O と S、Mg と Ca —— 同じ列の相棒が並んでいる。

図1（周期表）でオレンジに光っているマスと、色をそろえてある。

出力: _fig2_lineup.qmd
"""
import efig

P, CID = 'elup', 'elup0'

# (原子番号, 記号, 和名, カードの一言, 族ラベル, 読み取り帯に出す説明)
LINE = [
    (1, 'H', '水素', '朝の寝癖が、水で直る理由', '1族',
     '周期表のいちばん左上。1族に置かれていますが金属ではなく、'
     'どの仲間にも収まりきらない特別な元素です。'),
    (6, 'C', '炭素', '同じ元素から、ダイヤと鉛筆の芯', '14族',
     '4本の手で骨組みを作れるので、生命の材料になりました。'
     '<b>ケイ素（Si）と同じ列</b>です。'),
    (7, 'N', '窒素', '空気の8割を占める、ほどけない結びつき', '15族',
     '空気のおよそ8割はこの元素です。<b>リン（P）と同じ列</b>。'),
    (8, 'O', '酸素', '呼吸と、錆と、岩の半分', '16族',
     '地殻の重さの半分近くを占めます。<b>硫黄（S）と同じ列</b>なので、'
     'ふるまいがよく似ています。'),
    (11, 'Na', 'ナトリウム', '水で燃える金属が、食卓の塩になる', '1族',
     '<b>カリウム（K）と同じ列</b>。性格がよく似ているのは、そのためです。'),
    (12, 'Mg', 'マグネシウム', '葉が緑である理由', '2族',
     '葉緑素の中心にすわっている元素です。'
     '<b>カルシウム（Ca）と同じ列</b>。'),
    (13, 'Al', 'アルミニウム', 'かつては金より高価だった金属', '13族',
     '地殻でいちばん多い金属です。'
     '安く作れるようになったのは19世紀の終わりでした。'),
    (14, 'Si', 'ケイ素', '砂から、コンピュータへ', '14族',
     '地殻では酸素に次いで多い元素。<b>炭素（C）と同じ列</b>なので、'
     '炭素と同じように骨組みを作れます。'),
    (15, 'P', 'リン', '骨と、DNAと、農業を変えた元素', '15族',
     '<b>窒素（N）と同じ列</b>。生き物に必要な量は少ないのに、'
     'これが尽きると何も育ちません。'),
    (16, 'S', '硫黄', '温泉のにおい、火山の黄色', '16族',
     '<b>酸素（O）と同じ列</b>。ふるまいも酸素とよく似ています。'),
    (17, 'Cl', '塩素', '猛毒の気体が、水道を守っている', '17族',
     'あと1個で電子が満ちるので、1族のナトリウムと出会うと'
     '<b>塩</b>になります。'),
    (19, 'K', 'カリウム', '細胞が電気を使うための元素', '1族',
     '<b>ナトリウム（Na）と同じ列</b>ですが、'
     '体の中での役割は対照的です。'),
    (20, 'Ca', 'カルシウム', '骨、貝殻、そして鍾乳洞', '2族',
     '<b>マグネシウム（Mg）と同じ列</b>。'
     '地下水の硬さを決めているのもこの元素です。'),
    (26, 'Fe', '鉄', '血の赤さと、釘の錆は同じもの', '遷移金属',
     'この連載で取り上げる中で、<b>唯一の遷移金属</b>です。'
     '3〜12族のまん中あたりにいます。'),
]
ORDER = {1: '第1回', 6: '第2回'}

CSS = """
.%(p)s-grid{display:grid;gap:10px;margin:18px 8px 0;
  grid-template-columns:repeat(auto-fill,minmax(178px,1fr));}
.%(p)s-c{position:relative;display:flex;gap:11px;align-items:flex-start;
  padding:12px 12px 12px 11px;border-radius:12px;cursor:default;
  background:linear-gradient(180deg,rgba(190,100,10,.16),
    rgba(190,100,10,.06));
  border:1px solid rgba(190,100,10,.34);
  transition:background .17s ease,border-color .17s ease,
    transform .17s ease;}
.%(p)s-c:hover{background:rgba(190,100,10,.3);
  border-color:rgba(190,100,10,.8);transform:translateY(-2px);}

.%(p)s-sym{position:relative;flex:0 0 auto;width:46px;height:46px;
  display:flex;align-items:center;justify-content:center;border-radius:10px;
  background:#FFFDF9;border:1px solid rgba(190,100,10,.45);}
.%(p)s-sym u{position:absolute;top:3px;left:5px;text-decoration:none;
  font-size:.58rem;font-weight:600;color:rgba(138,72,6,.85);line-height:1;}
.%(p)s-sym b{font-size:1.35rem;font-weight:800;color:#8A4806;line-height:1;
  margin-top:4px;}

.%(p)s-tx{min-width:0;padding-top:1px;}
.%(p)s-tx h5{margin:0;font-size:1rem;font-weight:800;color:var(--ink);
  line-height:1.3;}
.%(p)s-tx s{display:block;text-decoration:none;margin-top:4px;
  font-size:.79rem;line-height:1.5;color:var(--dim);}
.%(p)s-tx em{display:inline-block;margin-top:6px;padding:1px 7px;
  border-radius:999px;font-style:normal;font-size:.68rem;font-weight:700;
  color:#FDFAF3;background:var(--hb);}
.%(p)s-tx em.w{color:var(--faint);background:rgba(122,96,52,.133);
  border:1px solid rgba(122,96,52,.228);}

.%(p)s-note{margin:16px 8px 0;padding:14px 16px;border-radius:11px;
  background:rgba(122,96,52,.085);border:1px solid rgba(122,96,52,.152);
  font-size:.9rem;line-height:1.8;color:var(--dim);}
.%(p)s-note b{color:var(--hb);}

@media (max-width:820px){
  .%(p)s-grid{grid-template-columns:repeat(auto-fill,minmax(150px,1fr));
    gap:8px;margin:14px 2px 0;}
  .%(p)s-c{padding:10px 9px;gap:9px;}
  .%(p)s-sym{width:40px;height:40px;}
  .%(p)s-sym b{font-size:1.15rem;}
  .%(p)s-tx h5{font-size:.9rem;}
  .%(p)s-tx s{font-size:.72rem;}
  .%(p)s-note{font-size:.82rem;margin:13px 2px 0;padding:12px 13px;}
}
""" % {'p': P}


def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, 'この連載で取り上げる14元素',
                        'カードにカーソルを合わせる（スマホはタップ）と、'
                        '周期表のどこにいるかが分かります。'),
         '<div class="%s-grid">' % P]

    for z, sym, ja, hook, grp, detail in LINE:
        badge = ORDER.get(z)
        tag = ('<em>%s</em>' % badge) if badge else '<em class="w">%s</em>' % grp
        o.append('<div class="%s-c" data-detail="%s">'
                 '<div class="%s-sym"><u>%d</u><b>%s</b></div>'
                 '<div class="%s-tx"><h5>%s</h5><s>%s</s>%s</div>'
                 '</div>'
                 % (P, detail, P, z, sym, P, ja, hook, tag))

    o.append('</div>')

    o.append('<p class="%s-note">'
             'この14個は、思いつきで選んだわけではありません。'
             'よく見ると、<b>同じ列の相棒がそろって入っています</b>——'
             'ナトリウムとカリウム（1族）、マグネシウムとカルシウム（2族）、'
             '炭素とケイ素（14族）、窒素とリン（15族）、酸素と硫黄（16族）。'
             '片方が生き物の側で、もう片方が岩石や地下水の側にいることが多く、'
             '<b>2つ並べて読むと、地球と生命が同じ仕組みでできている</b>のが'
             '見えてきます。</p>' % P)

    o.append(efig.close_card(
        P,
        'まずは <b>水素（H）</b> から始めて、'
        '炭素（C）へ進みます。3回目以降の順番はまだ決めていません。'
        'カードにカーソルを合わせる（スマホはタップ）と、'
        'その元素が周期表のどの列にいるかが出ます。',
        '顔ぶれは、生き物と地球をかたちづくる主要な元素から選びました。'
        '今後増えることがあります。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    efig.save('_fig2_lineup.qmd', build())
