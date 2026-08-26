# -*- coding: utf-8 -*-
"""
元素 #0 序章 / 図1 : DeepFlows オリジナルの周期表。

読み取らせたいこと:
  縦の列は「いちばん外側の電子の数」が同じ仲間であり、性格が似る。
  そしてこの連載で取り上げる 14 元素が、表のどこに散らばっているか。

作り:
  - 118 元素を CSS grid（18 列）に置く。位置は Python が計算して焼き込む
  - 上の帯が族のヘッダー。3〜12 族は遷移金属としてひとまとめにする
  - ヘッダーにカーソルを置くとその列だけが残り、読み取り帯に説明が出る
  - 取り上げる 14 元素はオレンジ（--hb）で光らせる
  - JS が動かなくても、表としては完全に成立する

出力: _fig1_periodic.qmd
"""
import efig

P, CID = 'eptb', 'eptb0'

# 原子番号順。index 0 が水素。
NAMES = """
H 水素
He ヘリウム
Li リチウム
Be ベリリウム
B ホウ素
C 炭素
N 窒素
O 酸素
F フッ素
Ne ネオン
Na ナトリウム
Mg マグネシウム
Al アルミニウム
Si ケイ素
P リン
S 硫黄
Cl 塩素
Ar アルゴン
K カリウム
Ca カルシウム
Sc スカンジウム
Ti チタン
V バナジウム
Cr クロム
Mn マンガン
Fe 鉄
Co コバルト
Ni ニッケル
Cu 銅
Zn 亜鉛
Ga ガリウム
Ge ゲルマニウム
As ヒ素
Se セレン
Br 臭素
Kr クリプトン
Rb ルビジウム
Sr ストロンチウム
Y イットリウム
Zr ジルコニウム
Nb ニオブ
Mo モリブデン
Tc テクネチウム
Ru ルテニウム
Rh ロジウム
Pd パラジウム
Ag 銀
Cd カドミウム
In インジウム
Sn スズ
Sb アンチモン
Te テルル
I ヨウ素
Xe キセノン
Cs セシウム
Ba バリウム
La ランタン
Ce セリウム
Pr プラセオジム
Nd ネオジム
Pm プロメチウム
Sm サマリウム
Eu ユウロピウム
Gd ガドリニウム
Tb テルビウム
Dy ジスプロシウム
Ho ホルミウム
Er エルビウム
Tm ツリウム
Yb イッテルビウム
Lu ルテチウム
Hf ハフニウム
Ta タンタル
W タングステン
Re レニウム
Os オスミウム
Ir イリジウム
Pt 白金
Au 金
Hg 水銀
Tl タリウム
Pb 鉛
Bi ビスマス
Po ポロニウム
At アスタチン
Rn ラドン
Fr フランシウム
Ra ラジウム
Ac アクチニウム
Th トリウム
Pa プロトアクチニウム
U ウラン
Np ネプツニウム
Pu プルトニウム
Am アメリシウム
Cm キュリウム
Bk バークリウム
Cf カリホルニウム
Es アインスタイニウム
Fm フェルミウム
Md メンデレビウム
No ノーベリウム
Lr ローレンシウム
Rf ラザホージウム
Db ドブニウム
Sg シーボーギウム
Bh ボーリウム
Hs ハッシウム
Mt マイトネリウム
Ds ダームスタチウム
Rg レントゲニウム
Cn コペルニシウム
Nh ニホニウム
Fl フレロビウム
Mc モスコビウム
Lv リバモリウム
Ts テネシン
Og オガネソン
"""
EL = [ln.split() for ln in NAMES.strip().split('\n')]

# この連載で取り上げる 14 元素。値は読み取り帯に出す一言。
# 北九州の講義台本 14 本と同じ顔ぶれ。
PICK = {
    1:  '朝の寝癖が、水で直る理由。',
    6:  '同じ元素から、ダイヤモンドと鉛筆の芯ができる。',
    7:  'ポテトチップスの袋を満たしている、ほどけない結びつき。',
    8:  '呼吸と、錆と、岩の半分。',
    11: '水に投げこむと燃える金属が、食卓の塩になる。',
    12: '葉が緑である理由。',
    13: 'かつては金より高価だった金属。',
    14: '砂から、コンピュータへ。',
    15: '骨と、DNAと、農業を変えた元素。',
    16: '温泉のにおい、火山の黄色。',
    17: '猛毒の気体が、水道とプールを守っている。',
    19: '細胞が電気を使うための元素。',
    20: '骨、貝殻、そして鍾乳洞。',
    26: '血の赤さと、釘の錆は同じもの。',
}
ORDER = {1: '第1回', 6: '第2回'}   # 公開順が決まっているのはここまで


def pos(z):
    """原子番号 -> (行, 列)。ランタノイド／アクチノイドは 9・10 行目へ送る。"""
    if z == 1:
        return 1, 1
    if z == 2:
        return 1, 18
    if z <= 4:
        return 2, z - 2
    if z <= 10:
        return 2, z + 8
    if z <= 12:
        return 3, z - 10
    if z <= 18:
        return 3, z
    if z <= 36:
        return 4, z - 18
    if z <= 54:
        return 5, z - 36
    if z <= 56:
        return 6, z - 54
    if z <= 71:
        return 9, z - 53
    if z <= 86:
        return 6, z - 68
    if z <= 88:
        return 7, z - 86
    if z <= 103:
        return 10, z - 85
    return 7, z - 100


def group(z):
    """族。3〜12 族はまとめて 'tm'、f ブロックは 'f' とする。"""
    r, c = pos(z)
    if r >= 9:
        return 'f'
    if 3 <= c <= 12:
        return 'tm'
    return str(c)


# 族ヘッダー。(表示, data-g, 列の開始, 列数, 説明)
HEADS = [
    ('1', '1', 1, 1,
     '<b>1族 — アルカリ金属</b>　いちばん外側の電子を <b>1個</b> だけ持っていて、'
     'それを手放したがります。水に入れると激しく反応するのは、そのためです。'
     'ナトリウム（Na）とカリウム（K）がこの列です。'
     'ただし<b>水素だけは例外</b>で、金属ではありません。'),
    ('2', '2', 2, 1,
     '<b>2族 — アルカリ土類金属</b>　外側の電子は <b>2個</b>。'
     '1族ほど激しくはありませんが、やはり手放したがります。'
     'マグネシウム（Mg）とカルシウム（Ca）がここ。'
     '骨も、貝殻も、鍾乳洞も、この列の元素でできています。'),
    ('3 〜 12', 'tm', 3, 10,
     '<b>3〜12族 — 遷移金属</b>　電子のやりとりが一段ややこしく、'
     '同じ元素がいくつもの姿をとります。'
     '金属の色や、磁石になる性質は、この区画から生まれます。'
     '<b>鉄（Fe）</b>はここの住人です。'),
    ('13', '13', 13, 1,
     '<b>13族</b>　外側の電子は <b>3個</b>。アルミニウム（Al）がここです。'
     '軽くて丈夫で、しかも表面に自分で保護膜を作ります。'),
    ('14', '14', 14, 1,
     '<b>14族</b>　外側の電子は <b>4個</b>。手放すにも受け取るにも中途半端なので、'
     '<b>手をつないで骨組みを作る</b>ほうを選びます。'
     '炭素（C）が生命を、ケイ素（Si）が岩石を作れるのは、このためです。'),
    ('15', '15', 15, 1,
     '<b>15族</b>　外側の電子は <b>5個</b>。あと3個で満ちるので、'
     '3本の手で結びつきます。窒素（N）とリン（P）。'
     'DNAの背骨は、この2つでできています。'),
    ('16', '16', 16, 1,
     '<b>16族 — カルコゲン</b>　外側の電子は <b>6個</b>。あと2個ほしいので、'
     '2本の手で結びつきます。酸素（O）と硫黄（S）。'
     '呼吸も、温泉のにおいも、この列です。'),
    ('17', '17', 17, 1,
     '<b>17族 — ハロゲン</b>　外側の電子は <b>7個</b>。'
     '<b>あと1個で満ちる</b>ので、何が何でも1個ほしがります。'
     '反応が激しいのは、そのためです。塩素（Cl）がここです。'),
    ('18', '18', 18, 1,
     '<b>18族 — 貴ガス</b>　外側の電子が <b>満ちています</b>。'
     'ほしいものが何もないので、ほとんど何とも反応しません。'
     'ヘリウム（He）やネオン（Ne）。'
     'この列だけが、周期表の中で満ち足りています。'),
]

CSS = """
.%(p)s-scroll{margin:16px 0 0;overflow-x:auto;padding-bottom:6px;
  -webkit-overflow-scrolling:touch;}
.%(p)s-tbl{display:grid;min-width:812px;gap:3px;
  grid-template-columns:repeat(18,1fr);
  grid-template-rows:26px repeat(7,40px) 16px repeat(2,40px);}

/* --- 族ヘッダー --- */
.%(p)s-g{display:flex;align-items:center;justify-content:center;
  border-radius:7px;font-size:.8rem;font-weight:700;letter-spacing:.02em;
  color:var(--dim);background:rgba(122,96,52,.095);
  border:1px solid rgba(122,96,52,.133);cursor:pointer;
  transition:color .16s ease,background .16s ease,border-color .16s ease;}
.%(p)s-g:hover{color:var(--ink);background:rgba(94,150,196,.16);
  border-color:rgba(94,150,196,.4);}

/* --- 元素のマス --- */
.%(p)s-c{position:relative;display:flex;flex-direction:column;
  align-items:center;justify-content:center;border-radius:7px;
  background:rgba(122,96,52,.085);
  border:1px solid rgba(122,96,52,.152);cursor:default;
  transition:opacity .16s ease,background .16s ease,
    border-color .16s ease,transform .16s ease;}
.%(p)s-c u{position:absolute;top:2px;left:4px;text-decoration:none;
  font-size:.56rem;font-weight:600;color:var(--faint);line-height:1;}
.%(p)s-c b{font-size:1.02rem;font-weight:800;color:var(--ink);line-height:1;
  margin-top:3px;}
.%(p)s-c:hover{background:rgba(94,150,196,.18);
  border-color:rgba(94,150,196,.45);transform:translateY(-1px);}
.%(p)s-c.dim{opacity:.28;}

/* --- 連載で取り上げる 14 元素 --- */
.%(p)s-c.pk{background:linear-gradient(180deg,rgba(190,100,10,.28),
    rgba(190,100,10,.13));border-color:rgba(190,100,10,.6);
  box-shadow:0 1px 2px rgba(190,100,10,.16);}
.%(p)s-c.pk u{color:rgba(138,72,6,.9);}
.%(p)s-c.pk b{color:#8A4806;}
.%(p)s-c.pk:hover{background:rgba(190,100,10,.4);
  border-color:rgba(190,100,10,.95);}
.%(p)s-c.pk i{position:absolute;right:3px;bottom:3px;width:5px;height:5px;
  border-radius:50%%;background:var(--hb);font-style:normal;
  animation:%(p)s-pulse 3.2s ease-in-out infinite;}
@keyframes %(p)s-pulse{0%%,100%%{opacity:.35}50%%{opacity:1}}

/* --- f ブロックの差し込み位置 --- */
.%(p)s-ph{display:flex;align-items:center;justify-content:center;
  border-radius:7px;font-size:.58rem;line-height:1.25;text-align:center;
  color:var(--faint);background:rgba(122,96,52,.057);
  border:1px dashed rgba(122,96,52,.304);}
.%(p)s-rw{display:flex;align-items:center;justify-content:flex-end;
  padding-right:8px;font-size:.66rem;color:var(--faint);}

.%(p)s-leg{display:flex;flex-wrap:wrap;gap:8px 20px;margin:14px 8px 0;
  font-size:.84rem;color:var(--dim);align-items:center;}
.%(p)s-leg span{display:inline-flex;align-items:center;gap:7px;}
.%(p)s-leg em{width:13px;height:13px;border-radius:4px;font-style:normal;}
.%(p)s-leg .k1{background:linear-gradient(180deg,rgba(190,100,10,.5),
    rgba(190,100,10,.22));border:1px solid rgba(190,100,10,.75);}
.%(p)s-leg .k2{background:rgba(122,96,52,.095);
  border:1px solid rgba(122,96,52,.266);}
/* 表の上に出す注意書き。
   efig.py の共通CSS `.eptb p{color:inherit}` は詳細度 (0,1,1) なので、
   ここも `p.` を付けて (0,1,1) に揃えないと色が効かない。 */
p.%(p)s-hint{margin:16px 8px 0;font-size:.88rem;font-weight:700;
  color:var(--rt);letter-spacing:.01em;}

@media (max-width:820px){
  .%(p)s-tbl{min-width:668px;gap:2px;
    grid-template-rows:22px repeat(7,33px) 13px repeat(2,33px);}
  .%(p)s-c b{font-size:.86rem;}
  .%(p)s-c u{font-size:.5rem;}
  .%(p)s-g{font-size:.68rem;}
  .%(p)s-ph{font-size:.5rem;}
  .%(p)s-rw{display:none;}
  .%(p)s-leg{font-size:.76rem;gap:6px 14px;}
  p.%(p)s-hint{font-size:.8rem;margin:13px 2px 0;}
}
""" % {'p': P}


def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, '周期表 — 縦にならぶと、性格が似る',
                        '上の帯（族の番号）にカーソルを合わせる'
                        '（スマホはタップ）と、その列だけが残ります。'
                        'オレンジに光っているのが、この連載で取り上げる14元素です。'),
         '<p class="%s-hint">'
         '横に切れている場合は、表を左右にスワイプしてください。</p>' % P,
         '<div class="%s-scroll"><div class="%s-tbl">' % (P, P)]

    # --- 族ヘッダー ---
    for label, g, c0, span, detail in HEADS:
        o.append('<div class="%s-g" data-g="%s" data-detail="%s" '
                 'style="grid-row:1;grid-column:%d / span %d">%s</div>'
                 % (P, g, detail, c0, span, label))

    # --- 118 元素 ---
    for i, (sym, ja) in enumerate(EL):
        z = i + 1
        r, c = pos(z)
        g = group(z)
        if z in PICK:
            cls, mark = ' pk', '<i></i>'
            badge = ORDER.get(z, 'この連載で取り上げます')
            detail = ('<b>%s（%s）</b>　原子番号 %d　／　%s<br>%s'
                      % (ja, sym, z, badge, PICK[z]))
        else:
            cls, mark = '', ''
            detail = '<b>%s（%s）</b>　原子番号 %d' % (ja, sym, z)
        o.append('<div class="%s-c%s" data-g="%s" data-detail="%s" '
                 'style="grid-row:%d;grid-column:%d">'
                 '<u>%d</u><b>%s</b>%s</div>'
                 % (P, cls, g, detail, r + 1, c, z, sym, mark))

    # --- 6・7 周期の 3 列目に入る差し込みマーク ---
    for r, txt, detail in ((6, 'La<br>〜Lu',
                            '<b>ランタノイド</b>　15個まとめて、この1マスに入ります。'
                            '性質がよく似ているので、表の下へ切り出して並べる'
                            'のがふつうです。'),
                           (7, 'Ac<br>〜Lr',
                            '<b>アクチノイド</b>　こちらも15個で1マス。'
                            'ウラン（U）やプルトニウム（Pu）はこの仲間です。')):
        o.append('<div class="%s-ph" data-g="f" data-detail="%s" '
                 'style="grid-row:%d;grid-column:3">%s</div>'
                 % (P, detail, r + 1, txt))

    # --- 切り出した f ブロックの行ラベル ---
    for r, txt in ((9, 'ランタノイド'), (10, 'アクチノイド')):
        o.append('<div class="%s-rw" style="grid-row:%d;grid-column:1 / span 3">'
                 '%s</div>' % (P, r + 1, txt))

    o.append('</div></div>')

    o.append('<div class="%s-leg">'
             '<span><em class="k1"></em>この連載で取り上げる14元素</span>'
             '<span><em class="k2"></em>そのほかの元素</span>'
             '</div>' % P)

    o.append(efig.close_card(
        P,
        '縦の列は、いちばん外側の電子の数が同じ仲間です。'
        '<b>つまり、縦にならぶ元素は性格が似ます。</b>'
        '上の帯か、元素のマスにカーソルを合わせる（スマホはタップ）と、'
        'ここに説明が出ます。',
        '配置は IUPAC の周期表に従いました。'
        '日本語名は日本化学会 原子量専門委員会「原子量表（2026）」に収録の'
        '名称で、118 元素すべてを照合しています。'
        '113番ニホニウムは理化学研究所のグループが発見し、2016年に命名されました。',
        CID))

    # 族ヘッダーにカーソルを置いているあいだ、その列だけを残す
    o.append("""
<script>
(function(){
  var r=document.getElementById('%(id)s');if(!r)return;
  var cells=r.querySelectorAll('.%(p)s-c');
  function set(g){
    cells.forEach(function(c){
      c.classList.toggle('dim', g!==null && c.getAttribute('data-g')!==g);
    });
  }
  r.querySelectorAll('.%(p)s-g').forEach(function(h){
    var g=h.getAttribute('data-g');
    function on(){set(g);}
    h.addEventListener('mouseenter',on);
    h.addEventListener('click',on);
    h.addEventListener('mouseleave',function(){set(null);});
  });
})();
</script>""" % {'p': P, 'id': CID})
    return '\n'.join(o)


if __name__ == '__main__':
    efig.save('_fig1_periodic.qmd', build())
