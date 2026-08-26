# -*- coding: utf-8 -*-
"""
元素 #2 炭素 / 図2 : 同じ4本の手。酸素と出会ったあとが、違った。

炭素とケイ素はどちらも 14 族で、手は 4 本。それでも片方は吸って吐ける
気体になり、片方は動かない岩になった。分かれ道は「酸素と二重結合を
作れるかどうか」だけである。これが #0 で予告した C-Si の対の回収になる。

数値の扱いについて（大事）:
  平均結合エンタルピーは使わない。Si-Si の値が出典によって 222〜340 kJ/mol
  と 50% も食い違い、記事の中心的な主張をその上に立てられないため。
  代わりに、議論の余地のない実測量だけを使う。
    CO2   直線・C=O 1.162 A・180 deg   NIST CCCBDB（Herzberg 1966）
    a石英 Si-O 1.6092 A・Si-O-Si 143.73 deg
          Levien, Prewitt & Weidner (1980) Am. Mineral. 65, 920-930
    共有結合半径 C 0.76 / Si 1.11 A     Cordero et al. (2008)
    地殻の存在度 Si 約 28% / C 約 0.02%（質量比）
    CO2 の昇華点 -78.5 degC / 石英が溶けるのは 1600 degC 超

石英の骨組みについて:
  結晶構造そのもの（P3121 の分率座標）は再現していない。実測の Si-O 距離と
  Si-O-Si 角から、隅を共有する SiO4 四面体を組み立てたものである。
  組んだあとに距離と角度を測り直し、実測値を再現していることを確認している
  （check() を見よ）。図の説明文でもそう書くこと。「石英の結晶構造」と
  言い切ってはいけない。

出力: _fig2_silicon.qmd
"""
import math
import efig
import emol

P, CID = 'esil', 'esil1'

CO = 1.162          # CO2 の C=O（Å）
SIO = 1.6092        # a石英の Si-O（Å）
SIOSI = 143.73      # a石英の Si-O-Si（度）

# 温度の帯。左端と右端（℃）
T0, T1 = -150.0, 1800.0

G = emol.Group(P, scale=42.0, spin_sec=23.0)


# ---------------------------------------------------------------- 骨組み

def unit(v):
    n = math.sqrt(sum(c * c for c in v)) or 1.0
    return [c / n for c in v]


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]]


def perp(u):
    """u に垂直な単位ベクトルを 1 本作る。"""
    k = (0.0, 0.0, 1.0) if abs(u[2]) < 0.9 else (1.0, 0.0, 0.0)
    return unit(cross(u, k))


def cone(axis, half_deg, phis):
    """axis から half_deg 傾けた向きを、軸まわりに phis の角度で並べる。"""
    a = unit(axis)
    p = perp(a)
    q = cross(a, p)
    t = math.radians(half_deg)
    out = []
    for f in phis:
        r = math.radians(f)
        out.append([a[k] * math.cos(t)
                    + (p[k] * math.cos(r) + q[k] * math.sin(r)) * math.sin(t)
                    for k in range(3)])
    return out


def quartz():
    """隅を共有する SiO4 四面体を、実測の距離と角から組む。

    中心の Si と、それを囲む酸素 4 個までが実線。その先の Si と酸素は
    「まだ続く」ことを示す薄い玉にする。実物は結晶の端まで続いている。
    """
    at = [((0.0, 0.0, 0.0), 'Si')]
    bo = []
    o_idx = []
    for v in emol.tetra():
        at.append((tuple(c * SIO for c in v), 'O'))
        o_idx.append(len(at) - 1)
        bo.append((0, len(at) - 1))

    si_idx = []
    t = math.radians(180.0 - SIOSI)          # 折れ角 143.73 度の補角
    for oi in o_idx:
        po = at[oi][0]
        u = unit(po)                          # 中心 Si -> O の向き
        n = perp(u)
        v = [u[k] * math.cos(t) + n[k] * math.sin(t) for k in range(3)]
        at.append((tuple(po[k] + v[k] * SIO for k in range(3)), 'Si', True))
        si_idx.append(len(at) - 1)
        bo.append((oi, len(at) - 1))

    for oi, si in zip(o_idx, si_idx):
        back = unit([at[oi][0][k] - at[si][0][k] for k in range(3)])
        for w in cone(back, 180.0 - 109.4712, (60, 180, 300)):
            at.append((tuple(at[si][0][k] + w[k] * SIO for k in range(3)),
                       'O', True))
            bo.append((si, len(at) - 1))
    return at, bo


CO2 = G.add(emol.Mol(
    'co2',
    [((0.0, 0.0, 0.0), 'C')]
    + [(tuple(c * CO for c in v), 'O') for v in emol.linear()],
    [(0, 1), (0, 2)], '二酸化炭素の立体模型'))

QTZ = G.add(emol.Mol('sio2', *quartz(), label='石英の骨組みの立体模型')
            .recenter())


# ---------------------------------------------------------------- 文言

PANEL = [
    ('co2', 'CO₂', '二酸化炭素', '3個で、終わり',
     '炭素は酸素と<b>二重結合</b>を作れます。手を2本ずつ差し出せば、'
     '酸素2個で4本すべてが埋まる。<b>原子3個で完結して、'
     'それ以上は何とも結びつきません</b>。'
     'そのため二酸化炭素は小さな粒のまま空気中を漂い、'
     '−78.5℃まで冷やして初めて固まります。'
     '植物が吸って体にし、私たちが吐いて返す。'
     '<b>行って、帰ってこられる</b>のです。'),
    ('sio2', 'SiO₂', '二酸化ケイ素（石英）', '終わりが、来ない',
     'ケイ素は炭素より一回り大きく（共有結合半径 1.11 Å 対 0.76 Å）、'
     'ふつうの条件では<b>二重結合を作りません</b>。'
     '手を1本ずつしか使えないので、酸素4個と単結合でつながります。'
     'その酸素はまた別のケイ素とつながり、それがまた——と'
     '<b>どこまでも続きます</b>。図の薄い部分は「この先も続く」という意味です。'
     '行き着く先が岩であり、砂です。溶かすには1600℃を超える熱が要ります。'),
]

# (温度℃, 見出し, 説明)。左右どちらへ寄せるかは位置から決める
MARKS = [
    (-78.5,  'CO₂',  '−78.5℃で気体になる'),
    (1600.0, 'SiO₂', '1600℃を超えないと溶けない'),
]

CSS = """
.@@P@@-row{display:grid;
  grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
  gap:14px;margin:18px 0 4px;}

.@@P@@-cell{display:flex;flex-direction:column;align-items:center;gap:2px;
  padding:12px 8px 14px;border-radius:14px;cursor:default;
  background:rgba(122,96,52,.035);
  border:1px solid rgba(122,96,52,.13);
  transition:background .18s ease,border-color .18s ease,transform .18s ease;}
.@@P@@-cell:hover{background:rgba(190,100,10,.07);
  border-color:rgba(190,100,10,.42);transform:translateY(-3px);}
.@@P@@-cell svg{display:block;width:100%;height:auto;
  -webkit-user-select:none;user-select:none;}

.@@P@@-f{font-size:1.3rem;font-weight:800;color:var(--ink);margin-top:4px;}
.@@P@@-nm{font-size:.82rem;color:var(--faint);}
.@@P@@-v{font-size:1.02rem;font-weight:700;color:var(--hb);margin-top:5px;}

/* 温度の帯。目盛りの位置は Python が計算して焼き込む */
.@@P@@-temp{margin:26px 8px 2px;padding-top:34px;position:relative;}
.@@P@@-bar{position:relative;height:13px;border-radius:7px;
  background:linear-gradient(90deg,#3F72A4 0%,#8FA9B8 8%,#D8C79A 42%,
    #D08A2A 72%,#B0361B 100%);
  border:1px solid rgba(122,96,52,.3);}
.@@P@@-mk{position:absolute;top:-1px;bottom:-1px;width:2px;
  background:var(--ink);}
.@@P@@-mk i{position:absolute;bottom:16px;display:block;white-space:nowrap;
  font-style:normal;line-height:1.35;}
.@@P@@-mk i b{display:block;font-size:.95rem;font-weight:800;color:var(--ink);}
.@@P@@-mk i s{display:block;font-size:.76rem;text-decoration:none;
  color:var(--faint);}
.@@P@@-mk.at-l i{left:-1px;}
.@@P@@-mk.at-r i{right:-1px;text-align:right;}

/* 水が液体でいられる範囲。左端に押しこまれていることを見せる */
.@@P@@-span{position:absolute;top:-1px;bottom:-1px;
  background:rgba(255,255,255,.55);
  border-left:1px solid rgba(43,38,33,.45);
  border-right:1px solid rgba(43,38,33,.45);}
.@@P@@-axis{display:flex;justify-content:space-between;
  margin:7px 0 0;font-size:.74rem;color:var(--faint);
  font-variant-numeric:tabular-nums;}
.@@P@@-cap{margin:9px 8px 0;font-size:.84rem;color:var(--dim);
  line-height:1.7;}

.@@P@@-defs{position:absolute;width:0;height:0;overflow:hidden;}

@media (max-width:820px){
  .@@P@@-row{gap:9px;margin:14px 0 2px;}
  .@@P@@-cell{padding:9px 5px 10px;border-radius:11px;}
  .@@P@@-f{font-size:1.08rem;}
  .@@P@@-v{font-size:.92rem;}
  .@@P@@-temp{margin:22px 2px 2px;padding-top:40px;}
  .@@P@@-mk i b{font-size:.84rem;}
  .@@P@@-mk i s{font-size:.68rem;white-space:normal;max-width:9.5em;}
  .@@P@@-cap{font-size:.78rem;margin:8px 2px 0;}
}
""".replace('@@P@@', P)


def pos(t):
    """温度（℃）→ 帯の左からの割合（%）。"""
    return (t - T0) / (T1 - T0) * 100.0


# ---------------------------------------------------------------- 検算

def check():
    print('コントラスト（地 #FDFAF3 に対して）:')
    emol.check_contrast([e for m in G.mols for e in m.elems()])

    at, bo = QTZ.atoms, QTZ.bonds
    ds = [emol.dist(at[i][0], at[j][0]) for i, j in bo]
    print('石英の骨組み: 原子 %d / 結合 %d' % (len(at), len(bo)))
    print('  Si–O     %.4f 〜 %.4f Å（実測 %.4f）' % (min(ds), max(ds), SIO))
    assert abs(min(ds) - SIO) < 1e-6 and abs(max(ds) - SIO) < 1e-6

    ctr = [k for k, (_p, e, g) in enumerate(at) if e == 'Si' and not g][0]
    o1 = [j for i, j in bo if i == ctr]
    osio = [emol.angle(at[a][0], at[ctr][0], at[b][0])
            for x, a in enumerate(o1) for b in o1[x + 1:]]
    print('  O–Si–O   %.2f 〜 %.2f°（正四面体 109.47）' % (min(osio), max(osio)))
    assert abs(min(osio) - 109.4712) < 1e-3

    sios = [emol.angle(at[ctr][0], at[o][0], at[s][0])
            for o in o1 for i, s in bo if i == o and at[s][1] == 'Si']
    print('  Si–O–Si  %.2f 〜 %.2f°（実測 %.2f）' % (min(sios), max(sios), SIOSI))
    assert abs(min(sios) - SIOSI) < 1e-3 and abs(max(sios) - SIOSI) < 1e-3

    a2 = CO2.atoms
    print('CO₂: C=O %.4f Å（実測 %.4f）／O–C–O %.2f°（実測 180）'
          % (emol.dist(a2[0][0], a2[1][0]), CO,
             emol.angle(a2[1][0], a2[0][0], a2[2][0])))
    assert abs(emol.angle(a2[1][0], a2[0][0], a2[2][0]) - 180.0) < 1e-6

    print('枠 %.1f（一周ぶん試した結果）:' % G.vb)
    for m in G.mols:
        x0, x1, y0, y1 = G._box[m.key]
        print('  %-5s 一周で占める幅 %5.1f × %5.1f  枠を %3.0f%% 使う'
              % (m.key, x1 - x0, y1 - y0, max(x1 - x0, y1 - y0) / G.vb * 100))
        # 玉が棒を食いつぶしていないこと。CO2 の C=O は本当に短いので下限は 5px
        for i, j in m.bonds:
            gi = 0.72 if m.atoms[i][2] else 1.0
            gj = 0.72 if m.atoms[j][2] else 1.0
            gap = (emol.dist(m.atoms[i][0], m.atoms[j][0])
                   - emol.RAD[m.atoms[i][1]] * G.ball * gi
                   - emol.RAD[m.atoms[j][1]] * G.ball * gj) * G.scale
            assert gap > 5.0, '%s: 玉が大きすぎて棒が見えない（%.1fpx）' % (m.key, gap)

    print('温度の帯: CO₂ %.1f%% ／ 0℃ %.1f%% ／ 100℃ %.1f%% ／ 石英 %.1f%%'
          % (pos(-78.5), pos(0), pos(100), pos(1600)))


# ---------------------------------------------------------------- 組み立て

def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, '同じ4本の手。酸素と出会ったあとが、違った',
                        '炭素とケイ素は周期表の同じ列（14族）で、'
                        'どちらも手は4本です。'
                        'どちらもゆっくり回っています。つかんで動かせば'
                        '自分で回せます。<b>2つは同じ縮尺で描いてあります。</b>'),
         G.defs(),
         '<div class="%s-row">' % P]

    for key, formula, name, verdict, det in PANEL:
        o.append('<div class="%s-cell" data-detail="%s">' % (P, efig.attr(det)))
        o.append(G.svg(key))
        o.append('<span class="%s-f">%s</span>' % (P, formula))
        o.append('<span class="%s-nm">%s</span>' % (P, name))
        o.append('<span class="%s-v">%s</span>' % (P, verdict))
        o.append('</div>')
    o.append('</div>')

    # 温度の帯
    o.append('<div class="%s-temp">' % P)
    o.append('<div class="%s-bar">' % P)
    o.append('<div class="%s-span" style="left:%.2f%%;right:%.2f%%" '
             'title="水が液体でいられる範囲"></div>'
             % (P, pos(0), 100.0 - pos(100)))
    for t, head, note in MARKS:
        side = 'at-l' if pos(t) < 50 else 'at-r'
        o.append('<div class="%s-mk %s" style="left:%.2f%%">'
                 '<i><b>%s</b><s>%s</s></i></div>' % (P, side, pos(t), head, note))
    o.append('</div>')
    o.append('<div class="%s-axis"><span>%d℃</span><span>0℃</span>'
             '<span>%d℃</span></div>' % (P, int(T0), int(T1)))
    o.append('<p class="%s-cap">白く抜いた細い帯が、'
             '<b>水が液体でいられる範囲（0〜100℃）</b>です。'
             '私たちの世界は、この物差しの左端に押しこまれています。</p>' % P)
    o.append('</div>')

    o.append(efig.close_card(
        P,
        '炭素とケイ素は、どちらも手が4本です。'
        'それでも一方は<b>吸って吐ける気体</b>になり、'
        'もう一方は<b>動かない岩</b>になりました。'
        '分かれ道は、酸素と出会ったときに'
        '<b>二重結合を作れるかどうか</b>だけです。'
        '地殻の重さの約28%はケイ素で、炭素は約0.02%。'
        '<b>量では千倍以上の差で負けている炭素</b>が生命の材料になれたのは、'
        'めぐって戻ってこられたからです。',
        'CO₂ は直線・C=O 1.162 Å（NIST CCCBDB 収録の実験値、Herzberg 1966）。'
        '石英側は<b>結晶構造そのものではなく</b>、実測の Si–O 1.6092 Å と '
        'Si–O–Si 143.73°（Levien, Prewitt &amp; Weidner 1980, '
        '<i>Am. Mineral.</i> 65, 920–930）から、隅を共有する SiO₄ 四面体を'
        '組み立てたものです（組んだあとに距離と角度を測り直して確認しています）。'
        '球の大きさは共有結合半径（Cordero et al. 2008）。'
        'ケイ素も特別に大きな置き換え基で守れば二重結合を作れます'
        '（West, Fink &amp; Michl 1981）が、ふつうの条件では作りません。'
        '地殻の存在度と融点は概数です。',
        CID))
    o.append(G.spin_js(CID, '.%s-cell svg[viewBox]' % P))
    return '\n'.join(o)


if __name__ == '__main__':
    check()
    efig.save('_fig2_silicon.qmd', build())
