# -*- coding: utf-8 -*-
"""
元素 #2 炭素 / 図1 : 手の数は、外側の席で決まる。

ヘリウム 0 本、水素 1 本、酸素 2 本、窒素 3 本、炭素 4 本。
「4 本だから王様」ではなく、「4 本＝満席までちょうど半分だから、
分け合うしかない」という #0 の続きとして読ませる。

形は絵ではなく計算で出す。実測の結合長と結合角から 3 次元の座標を組み、
emol.py が回して投影する。棒の長さも球の大きさも実寸比なので、
右へ行くほど手がわずかに長くなる（C > N > O、周期表を右へ行くほど
原子が小さい）という本当の傾向がそのまま図に出る。

実験値（NIST CCCBDB 収録）:
  H2   H-H 0.741 A                 Huber & Herzberg (1979)
  H2O  O-H 0.958 A / 104.4776 deg  Hoy & Bunker (1979)
  NH3  N-H 1.012 A / 106.67 deg    Herzberg (1966)
  CH4  C-H 1.087 A / 109.471 deg   Hirota (1979), Sverdlov et al. (1974)

出力: _fig1_hands.qmd
"""
import efig
import emol

P, CID = 'ehand', 'ehand1'

G = emol.Group(P, scale=42.0, spin_sec=19.0)

# (記号, 分子式, 分子名, 手の数, 原子, 結合)
SPEC = [
    ('He', 'He',  'ヘリウム',   0,
     [((0.0, 0.0, 0.0), 'He')], []),
    ('H',  'H₂',  '水素',       1,
     emol.pair('H', 0.741)),
    ('O',  'H₂O', '水',         2,
     emol.hub('O', 0.958, emol.bent(104.4776))),
    ('N',  'NH₃', 'アンモニア', 3,
     emol.hub('N', 1.012, emol.pyramid(106.67))),
    ('C',  'CH₄', 'メタン',     4,
     emol.hub('C', 1.087, emol.tetra())),
]


def _mols():
    out = []
    for row in SPEC:
        sym, formula, name, hands = row[0], row[1], row[2], row[3]
        if len(row) == 6:
            atoms, bonds = row[4], row[5]
        else:
            atoms, bonds = row[4]
        out.append((sym, formula, name, hands,
                    G.add(emol.Mol(sym, atoms, bonds, '%s の立体模型' % sym))))
    return out


MOL = _mols()

DET = {
    'He': 'ヘリウムの外側の席は<b>2個で満席</b>です'
          '（いちばん内側の席だけは、2個で埋まります）。'
          'ほしいものも、押しつけたいものもありません。手は<b>0本</b>。'
          'ほかの原子とほとんど結びつかず、原子1個のまま漂っています。',
    'H':  '水素の外側には電子が<b>1個</b>。満席まであと1個です。'
          '相手と1個ずつ出し合って分け合えば席が埋まるので、手は<b>1本</b>。'
          '水素どうしが手をつないだのが水素分子（H₂）で、'
          'その長さ <b>0.741 Å</b> は、あらゆる結合の中でも最も短い部類です。',
    'O':  '酸素の外側には電子が<b>6個</b>。満席まであと2個なので、手は<b>2本</b>。'
          '2本の手で水素を1個ずつつかまえたのが水（H₂O）です。'
          '2本は一直線ではなく<b>104.5°</b>に折れていて、'
          'この「くの字」が水のふるまいのほとんどを決めています。',
    'N':  '窒素の外側には電子が<b>5個</b>。あと3個で満席なので、手は<b>3本</b>。'
          '3本で水素をつかまえたのがアンモニア（NH₃）です。'
          '手は平らに広がらず<b>三角錐</b>に開きます。'
          '余った1組の電子が上から押さえるためで、角は<b>106.7°</b>です。',
    'C':  '炭素の外側には電子が<b>4個</b>。'
          '<b>満席まで、ちょうど半分</b>です。'
          '押しつけるには多すぎ、奪い取るには足りない。'
          '残された道は「分け合う」しかありません。'
          '4本の手は<b>正四面体</b>の頂点へ、たがいに<b>109.5°</b>離れて伸びます。'
          'この形が、炭素にどこまでも枝分かれする自由を与えました。',
}

CSS = """
/* 1 行 5 列。分子は枠いっぱいまで大きくなる（上限を決め打ちしない）。

   最小幅を 130px にしてあるのは、5 列を保てる下限だから。
   .fig-wide が効くのは画面 1280px 以上だけで、それより狭いと図は本文幅
   （最大 802px、内側の余白を引いて約 750px）に戻る。150px にすると
   5*150+4*10=790px となって入らず、「4 列＋1 列」に折り返してしまう。
   130px なら 5*130+4*10=690px で収まる。手の数が 0→1→2→3→4 と
   一列に並ぶことがこの図の骨なので、折り返させてはいけない。 */
.@@P@@-row{display:grid;
  grid-template-columns:repeat(auto-fit,minmax(130px,1fr));
  gap:10px;margin:18px 0 6px;}

.@@P@@-cell{display:flex;flex-direction:column;align-items:center;gap:1px;
  padding:10px 4px 12px;border-radius:14px;cursor:default;
  background:rgba(122,96,52,.035);
  border:1px solid rgba(122,96,52,.13);
  transition:background .18s ease,border-color .18s ease,transform .18s ease;}
.@@P@@-cell:hover{background:rgba(190,100,10,.07);
  border-color:rgba(190,100,10,.42);transform:translateY(-3px);}

/* 炭素の枠だけは、触れる前から少し前に出しておく */
.@@P@@-cell.is-key{background:rgba(190,100,10,.06);
  border-color:rgba(190,100,10,.3);}

.@@P@@-cell svg{display:block;width:100%;height:auto;
  -webkit-user-select:none;user-select:none;}

.@@P@@-n{font-size:1.6rem;font-weight:800;line-height:1.15;color:var(--ink);
  font-variant-numeric:tabular-nums;margin-top:2px;}
.@@P@@-n em{font-style:normal;font-size:.9rem;font-weight:700;margin-left:2px;}
.@@P@@-cell.is-key .@@P@@-n{color:var(--hb);}
.@@P@@-f{font-size:1.02rem;font-weight:700;color:var(--dim);}
.@@P@@-nm{font-size:.8rem;color:var(--faint);}

/* グラデーションの置き場。場所は取らせない */
.@@P@@-defs{position:absolute;width:0;height:0;overflow:hidden;}

@media (max-width:820px){
  .@@P@@-row{grid-template-columns:repeat(auto-fit,minmax(112px,1fr));
    gap:7px;margin:14px 0 4px;}
  .@@P@@-cell{padding:7px 3px 9px;border-radius:11px;}
  .@@P@@-n{font-size:1.2rem;}
  .@@P@@-f{font-size:.88rem;}
  .@@P@@-nm{font-size:.72rem;}
}
""".replace('@@P@@', P)


def check():
    print('コントラスト（地 #FDFAF3 に対して）:')
    emol.check_contrast([e for _s, _f, _n, _h, m in MOL for e in m.elems()])
    print('枠 %.1f（一周ぶん試した結果）:' % G.vb)
    for sym, _f, _n, _h, m in MOL:
        x0, x1, y0, y1 = G._box[sym]
        print('  %-3s 一周で占める幅 %5.1f × %5.1f  枠を %3.0f%% 使う'
              % (sym, x1 - x0, y1 - y0, max(x1 - x0, y1 - y0) / G.vb * 100))
        assert x1 - x0 <= G.vb + .01 and y1 - y0 <= G.vb + .01, '%s がはみ出す' % sym
        # 玉が棒を食いつぶしていないこと
        for i, j in m.bonds:
            gap = (emol.dist(m.atoms[i][0], m.atoms[j][0])
                   - emol.RAD[m.atoms[i][1]] * G.ball
                   - emol.RAD[m.atoms[j][1]] * G.ball) * G.scale
            assert gap > 6.0, '%s は球が大きすぎて棒が見えない（%.1f）' % (sym, gap)
    # 実測の結合角が、組み立てたあとも保たれているか。
    # 正四面体角は arccos(-1/3)=109.47122... なので、丸めた文献値と直に
    # 比べると必ず外れる。許容差はその丸め幅（0.0001°）に合わせる。
    import math
    for sym, ang in (('O', 104.4776), ('N', 106.67),
                     ('C', math.degrees(math.acos(-1.0 / 3.0)))):
        m = [x for _s, _f, _n, _h, x in MOL if x.key == sym][0]
        got = emol.angle(m.atoms[1][0], m.atoms[0][0], m.atoms[2][0])
        print('  %-3s 結合角 %.5f°（実測 %.5f°）' % (sym, got, ang))
        assert abs(got - ang) < 1e-4


def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, '手の数は、外側の席で決まる',
                        'それぞれの分子はゆっくり回っています。'
                        'つかんで動かせば自分で回せます。'
                        'カーソルを合わせる（スマホはタップ）と、'
                        'その元素の事情が下に出ます。'),
         G.defs(),
         '<div class="%s-row">' % P]

    for sym, formula, name, hands, _m in MOL:
        o.append('<div class="%s-cell%s" data-detail="%s">'
                 % (P, ' is-key' if sym == 'C' else '', efig.attr(DET[sym])))
        o.append(G.svg(sym))
        o.append('<span class="%s-n">%d<em>本</em></span>' % (P, hands))
        o.append('<span class="%s-f">%s</span>' % (P, formula))
        o.append('<span class="%s-nm">%s</span>' % (P, name))
        o.append('</div>')
    o.append('</div>')

    o.append(efig.close_card(
        P,
        'ヘリウムは0本、水素は1本、酸素は2本、窒素は3本。'
        'そして<b>炭素は4本</b>です。'
        '多いから王様なのではありません。4本は'
        '<b>押しつけるにも受け取るにも中途半端な数</b>で、'
        'そのため炭素は相手を選ばず、炭素どうしでも果てしなくつながっていけます。',
        '形は絵ではなく、実測値から立体を組んで投影したものです。'
        '棒の長さと角度は H–H 0.741 Å／O–H 0.958 Å・104.48°／'
        'N–H 1.012 Å・106.67°／C–H 1.087 Å・109.47°'
        '（NIST CCCBDB 収録の実験値）。'
        '球の大きさは共有結合半径（Cordero et al. 2008）で、'
        '5つの図はすべて同じ縮尺です。1 Å＝1億分の1センチ。'
        '右へ行くほど手が長いのは、周期表を左へ戻るほど原子が大きいためです。',
        CID))
    o.append(G.spin_js(CID, '.%s-cell svg[viewBox]' % P))
    return '\n'.join(o)


if __name__ == '__main__':
    check()
    efig.save('_fig1_hands.qmd', build())
