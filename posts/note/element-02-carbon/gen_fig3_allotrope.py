# -*- coding: utf-8 -*-
"""
元素 #2 炭素 / 図3 : 同じ炭素。並べ方だけが違う。

#1 の次回予告で読者に約束した「ダイヤモンドと鉛筆の芯」の回収。
原子は 1 個も違わないのに、いちばん硬いものと、紙に色を残す柔らかいものになる。

この図の落としどころは、最後の物差しにある。
  黒鉛の層のすきま      3.3555 A
  炭素のファンデルワールス半径 2 つ分  3.40 A
この 2 つがほぼ一致する。つまり層と層は「結合していない、触れているだけ」で、
だから滑って剥がれる。#1 で扱ったファンデルワールス力がここで効いてくる。

座標は結晶構造から生成する（実測の格子定数から起こす）。
  ダイヤモンド  面心立方 + (1/4,1/4,1/4) の 2 原子基本構造
                a = 3.567 A  ->  C-C = a*sqrt(3)/4 = 1.5444 A
  黒鉛          蜂の巣格子を AB 積み
                a = 2.464 A / c = 6.711 A
                層内 C-C = a/sqrt(3) = 1.4226 A / 層間 = c/2 = 3.3555 A
  炭素のファンデルワールス半径 1.70 A  Bondi (1964)
  黒鉛とダイヤモンドの標準生成ギブズエネルギーの差 2.9 kJ/mol
  （黒鉛のほうが安定。ダイヤモンドは速度が遅いだけの準安定な姿）

薄い玉は「切り口。この先も続く」の意味。手が足りていない原子
（ダイヤモンドなら 4 本未満、黒鉛なら 3 本未満）を機械的に薄くしている。

出力: _fig3_allotrope.qmd
"""
import math
import efig
import emol

P, CID = 'ecar', 'ecar1'

A_DIA = 3.567                       # ダイヤモンドの格子定数（Å）
D_DIA = A_DIA * math.sqrt(3) / 4.0  # C–C = 1.5444 Å
A_GR, C_GR = 2.464, 6.711           # 黒鉛の格子定数（Å）
D_GR = A_GR / math.sqrt(3)          # 層内 C–C = 1.4226 Å
GAP = C_GR / 2.0                    # 層間 = 3.3555 Å
VDW = 1.70                          # 炭素のファンデルワールス半径（Bondi 1964）

R_DIA = 2.70                        # 切り出す半径（Å）
R_GR = 3.00

# 縁の原子が多い図なので、薄い玉を既定の 0.42 より少し濃くする
G = emol.Group(P, scale=42.0, spin_sec=25.0, ghost_op=0.52)


# ---------------------------------------------------------------- 構造

def bond_up(atoms, d, tol=0.02):
    """距離が d の組をすべて結ぶ。手が足りない原子は薄い玉にする。"""
    bonds = []
    deg = [0] * len(atoms)
    for i in range(len(atoms)):
        for j in range(i + 1, len(atoms)):
            if abs(emol.dist(atoms[i][0], atoms[j][0]) - d) < tol:
                bonds.append((i, j))
                deg[i] += 1
                deg[j] += 1
    return bonds, deg


def diamond():
    """面心立方 + (1/4,1/4,1/4)。中心の炭素から半径で切り出す。"""
    basis = [(0.0, 0.0, 0.0), (.25, .25, .25)]
    fcc = [(0.0, 0.0, 0.0), (0.0, .5, .5), (.5, 0.0, .5), (.5, .5, 0.0)]
    seen = set()
    pts = []
    n = 2
    for cell in ((i, j, k) for i in range(-n, n + 1)
                 for j in range(-n, n + 1) for k in range(-n, n + 1)):
        for f in fcc:
            for b in basis:
                p = tuple((cell[t] + f[t] + b[t]) * A_DIA for t in range(3))
                if math.sqrt(sum(c * c for c in p)) >= R_DIA + 1e-9:
                    continue
                key = tuple(round(c, 6) for c in p)
                if key in seen:
                    continue
                seen.add(key)
                pts.append(p)
    # 原点にある炭素を中心に据える（近い順に並べておく）
    pts.sort(key=lambda p: (round(math.sqrt(sum(c * c for c in p)), 6), p))
    atoms = [(p, 'C') for p in pts]
    bonds, deg = bond_up(atoms, D_DIA)
    return [(p, 'C', deg[i] < 4) for i, (p, _e) in enumerate(atoms)], bonds


def graphite():
    """蜂の巣格子を AB 積みで 2 枚。層は水平（xz 面）に置く。

    縦軸まわりに回しても層は水平のままなので、すきまが常に見える。
    """
    a1 = (A_GR, 0.0, 0.0)
    a2 = (A_GR / 2.0, 0.0, A_GR * math.sqrt(3) / 2.0)
    bb = (A_GR / 2.0, 0.0, A_GR / (2.0 * math.sqrt(3)))   # 隣の副格子へ
    sites = []
    n = 3
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            base = tuple(i * a1[k] + j * a2[k] for k in range(3))
            for b in ((0.0, 0.0, 0.0), bb):
                sites.append(tuple(base[k] + b[k] for k in range(3)))

    atoms = []
    for y, shift in ((GAP / 2.0, (0.0, 0.0, 0.0)), (-GAP / 2.0, bb)):
        for s in sites:
            p = (s[0] + shift[0], y, s[2] + shift[2])
            if math.hypot(p[0], p[2]) < R_GR:
                atoms.append((p, 'C'))
    bonds, deg = bond_up(atoms, D_GR)
    return [(p, 'C', deg[i] < 3) for i, (p, _e) in enumerate(atoms)], bonds


DIA = G.add(emol.Mol('dia', *diamond(), label='ダイヤモンドの立体模型'))
GRA = G.add(emol.Mol('gra', *graphite(), label='黒鉛の立体模型').recenter())


# ---------------------------------------------------------------- 文言

PANEL = [
    ('dia', 'ダイヤモンド', '4本とも、使い切る',
     '炭素が<b>4本の手をすべて使って</b>、隣の炭素と正四面体につながります。'
     'C–C は <b>1.5445 Å</b>。この網は立体なので、どの向きから押しても'
     '支える方向があります。地球上でいちばん硬い物質になったのはそのためです。'
     '電気は通しません。電子が全部、結合に使われてしまっていて、'
     '動ける電子が1個も残っていないからです。'),
    ('gra', '黒鉛（鉛筆の芯）', '3本で平ら。4本目は、みんなのもの',
     '黒鉛の炭素は<b>3本の手だけ</b>を使い、六角形の平らな網を作ります。'
     '網の中の C–C は <b>1.4226 Å</b>。ダイヤモンドより<b>短く、つまり強い</b>のです。'
     'ところが網と網のあいだには、結合が1本もありません。'
     'すきまは <b>3.3555 Å</b>——炭素のファンデルワールス半径2つ分（3.40 Å）と'
     'ほぼ同じで、これは「触れているだけ」の距離です。'
     '余った4本目の電子は網全体に広がっていて、'
     'これが黒鉛が電気を通す理由になっています。'),
]

BARS = [
    ('層の中の結合', D_GR, '%.4f Å' % D_GR, 'in'),
    ('層と層のすきま', GAP, '%.4f Å' % GAP, 'out'),
]
BAR_MAX = 3.7

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

.@@P@@-f{font-size:1.2rem;font-weight:800;color:var(--ink);margin-top:4px;}
.@@P@@-v{font-size:.98rem;font-weight:700;color:var(--hb);margin-top:3px;
  text-align:center;line-height:1.5;}

/* 長さの物差し。棒の長さは Å に比例させてある */
.@@P@@-scale{margin:24px 8px 2px;position:relative;}
.@@P@@-line{display:grid;grid-template-columns:9.5em 1fr;gap:12px;
  align-items:center;margin:0 0 11px;}
.@@P@@-line>span{font-size:.86rem;color:var(--dim);text-align:right;}
.@@P@@-track{position:relative;height:19px;}
.@@P@@-len{position:absolute;left:0;top:0;bottom:0;border-radius:5px;
  display:flex;align-items:center;justify-content:flex-end;
  padding-right:9px;font-size:.78rem;font-weight:700;color:#FFFDF9;
  font-variant-numeric:tabular-nums;white-space:nowrap;}
.@@P@@-len.is-in{background:linear-gradient(90deg,#4A423A,#6E6154);}
.@@P@@-len.is-out{background:linear-gradient(90deg,#B0A48C,#8C8271);}
/* ファンデルワールス半径 2 つ分の位置。ここと「すきま」がほぼ重なる */
.@@P@@-vdw{position:absolute;top:-6px;bottom:-6px;width:0;
  border-left:2px dashed var(--rt);}
.@@P@@-vdw i{position:absolute;left:7px;top:-3px;white-space:nowrap;
  font-style:normal;font-size:.76rem;font-weight:700;color:var(--rt);}
.@@P@@-cap{margin:16px 8px 0;font-size:.84rem;color:var(--dim);
  line-height:1.75;}

.@@P@@-defs{position:absolute;width:0;height:0;overflow:hidden;}

@media (max-width:820px){
  .@@P@@-row{gap:9px;margin:14px 0 2px;}
  .@@P@@-cell{padding:9px 5px 10px;border-radius:11px;}
  .@@P@@-f{font-size:1.02rem;}
  .@@P@@-v{font-size:.88rem;}
  .@@P@@-scale{margin:20px 2px 2px;}
  .@@P@@-line{grid-template-columns:1fr;gap:3px;margin-bottom:14px;}
  .@@P@@-line>span{text-align:left;font-size:.8rem;}
  .@@P@@-vdw i{font-size:.68rem;left:5px;}
  .@@P@@-cap{font-size:.78rem;margin:14px 2px 0;}
}
""".replace('@@P@@', P)


# ---------------------------------------------------------------- 検算

def check():
    print('コントラスト（地 #FDFAF3 に対して）:')
    emol.check_contrast(['C'])

    print('ダイヤモンド: a=%.4f Å -> C–C %.4f Å' % (A_DIA, D_DIA))
    print('黒鉛: a=%.4f / c=%.4f Å -> 層内 %.4f Å ／ 層間 %.4f Å'
          % (A_GR, C_GR, D_GR, GAP))
    print('ファンデルワールス半径2つ分 %.2f Å ／ 層間との差 %.4f Å（%.1f%%）'
          % (2 * VDW, 2 * VDW - GAP, (2 * VDW - GAP) / GAP * 100))
    assert abs(2 * VDW - GAP) < 0.06, 'すきまとファンデルワールス径がずれすぎ'

    for m, d, deg_full in ((DIA, D_DIA, 4), (GRA, D_GR, 3)):
        ds = [emol.dist(m.atoms[i][0], m.atoms[j][0]) for i, j in m.bonds]
        solid = sum(1 for _p, _e, g in m.atoms if not g)
        print('%s: 原子 %d（うち手が揃っている %d）／結合 %d／結合長 %.4f〜%.4f Å'
              % (m.key, len(m.atoms), solid, len(m.bonds), min(ds), max(ds)))
        assert abs(min(ds) - d) < 0.02 and abs(max(ds) - d) < 0.02
        assert solid >= 1, '%s に手の揃った原子が1個も無い' % m.key

    # ダイヤモンドの中心は正四面体か
    ctr = 0
    nb = [j for i, j in DIA.bonds if i == ctr] + [i for i, j in DIA.bonds if j == ctr]
    angs = [emol.angle(DIA.atoms[a][0], DIA.atoms[ctr][0], DIA.atoms[b][0])
            for x, a in enumerate(nb) for b in nb[x + 1:]]
    print('  中心の C の結合角 %.4f〜%.4f°（正四面体 109.4712）'
          % (min(angs), max(angs)))
    assert len(nb) == 4 and abs(min(angs) - 109.4712) < 1e-3

    # 黒鉛の層は 2 枚あって、間に結合が 1 本も無いこと
    ys = sorted(set(round(p[1], 4) for p, _e, _g in GRA.atoms))
    cross = [(i, j) for i, j in GRA.bonds
             if abs(GRA.atoms[i][0][1] - GRA.atoms[j][0][1]) > 0.1]
    print('  黒鉛の層の高さ %s ／ 層をまたぐ結合 %d 本' % (ys, len(cross)))
    assert len(ys) == 2 and not cross, '層のあいだに結合を引いてはいけない'
    # 層内の角は 120 度
    i0 = [k for k, (_p, _e, g) in enumerate(GRA.atoms) if not g][0]
    nb0 = [j for i, j in GRA.bonds if i == i0] + [i for i, j in GRA.bonds if j == i0]
    a0 = [emol.angle(GRA.atoms[a][0], GRA.atoms[i0][0], GRA.atoms[b][0])
          for x, a in enumerate(nb0) for b in nb0[x + 1:]]
    print('  黒鉛の層内の結合角 %.2f〜%.2f°（六角形なら 120）' % (min(a0), max(a0)))
    assert abs(min(a0) - 120.0) < 1e-3

    print('枠 %.1f（一周ぶん試した結果）:' % G.vb)
    for m in G.mols:
        x0, x1, y0, y1 = G._box[m.key]
        print('  %-4s 一周で占める幅 %5.1f × %5.1f  枠を %3.0f%% 使う'
              % (m.key, x1 - x0, y1 - y0, max(x1 - x0, y1 - y0) / G.vb * 100))
        for i, j in m.bonds:
            gap = (emol.dist(m.atoms[i][0], m.atoms[j][0])
                   - 2 * emol.RAD['C'] * G.ball) * G.scale
            assert gap > 5.0, '%s: 玉が大きすぎて棒が見えない' % m.key


# ---------------------------------------------------------------- 組み立て

def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, '同じ炭素。並べ方だけが違う',
                        'どちらも炭素だけでできています。原子は1個も違いません。'
                        'ゆっくり回っています。つかんで動かせば自分で回せます。'
                        '<b>2つは同じ縮尺</b>で、薄い玉は'
                        '「切り口。この先も続く」という意味です。'),
         G.defs(),
         '<div class="%s-row">' % P]

    for key, name, verdict, det in PANEL:
        o.append('<div class="%s-cell" data-detail="%s">' % (P, efig.attr(det)))
        o.append(G.svg(key))
        o.append('<span class="%s-f">%s</span>' % (P, name))
        o.append('<span class="%s-v">%s</span>' % (P, verdict))
        o.append('</div>')
    o.append('</div>')

    # 長さの物差し
    o.append('<div class="%s-scale">' % P)
    for label, val, txt, cls in BARS:
        o.append('<div class="%s-line"><span>%s</span><div class="%s-track">'
                 % (P, label, P))
        o.append('<div class="%s-len is-%s" style="width:%.2f%%">%s</div>'
                 % (P, cls, val / BAR_MAX * 100.0, txt))
        if cls == 'out':
            o.append('<div class="%s-vdw" style="left:%.2f%%">'
                     '<i>3.40 Å ＝ ファンデルワールス半径2つ分</i></div>'
                     % (P, 2 * VDW / BAR_MAX * 100.0))
        o.append('</div></div>')
    o.append('<p class="%s-cap">層と層のすきまは、'
             '<b>炭素どうしが「ぶつかるだけ」の距離とほぼ同じ</b>です。'
             'つまり網の上に網が<b>ただ乗っているだけ</b>で、結合していません。'
             '紙にこすると、いちばん上の網が滑って剥がれ、紙に残る。'
             'それが鉛筆の字です。</p>' % P)
    o.append('</div>')

    o.append(efig.close_card(
        P,
        'ダイヤモンドと鉛筆の芯は、<b>まったく同じ炭素</b>です。'
        '原子は1個も違いません。違うのは並べ方だけで、'
        '片方は地球上でいちばん硬いものになり、'
        'もう片方は指でこすれば紙に色を残すものになりました。'
        'そして、もうひとつ。常温常圧では'
        '<b>黒鉛のほうが安定です</b>（標準生成ギブズエネルギーの差は 2.9 kJ/mol）。'
        'ダイヤモンドは、いつか黒鉛に変わるはずのものが、'
        '変化があまりに遅いために<b>永遠に見えているだけ</b>なのです。',
        '座標は実測の格子定数から起こしたものです。'
        'ダイヤモンドは面心立方＋(¼,¼,¼) の構造で a＝3.567 Å'
        '（C–C＝a√3/4＝1.5445 Å）、'
        '黒鉛は蜂の巣格子の AB 積みで a＝2.464 Å・c＝6.711 Å'
        '（層内＝a/√3＝1.4226 Å、層間＝c/2＝3.3555 Å）。'
        '炭素のファンデルワールス半径 1.70 Å は Bondi (1964)。'
        '球の大きさは共有結合半径（Cordero et al. 2008）で、'
        '2つの図は同じ縮尺です。'
        '薄い玉は切り口にあたる原子（手が足りていないもの）で、'
        '実物はその先も続いています。',
        CID))
    o.append(G.spin_js(CID, '.%s-cell svg[viewBox]' % P))
    return '\n'.join(o)


if __name__ == '__main__':
    check()
    efig.save('_fig3_allotrope.qmd', build())
