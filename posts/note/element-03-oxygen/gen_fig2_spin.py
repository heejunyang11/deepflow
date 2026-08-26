# -*- coding: utf-8 -*-
"""
元素 #3 酸素 / 図2 : 酸素は、磁石にくっつく。

この記事の科学の山。「なぜ私たちは 21% の酸素の中で燃えないのか」に答える。

骨:
  酸素分子は、いちばん外側に<対になっていない電子を 2 個>持っている。
  だから液体酸素は磁石に引かれる（窒素は引かれない）。
  そしてこの電子の向きのせいで、酸素が有機物と直接反応するのは
  スピン禁制になる。反応するには電子の向きを変えるしかなく、
  その段差が 7882.39 cm-1 = 94.3 kJ/mol。これが「マッチが要る」理由。

数値はすべて NIST Chemistry WebBook の実測値:
  O2  基底 X 3Sg-  結合長 1.20752 A
      最初の励起状態 a 1Dg  7882.39 cm-1（= 1.269 um = 94.3 kJ/mol）
  N2  基底 X 1Sg+  結合長 1.097685 A
      最初の励起状態 A 3Su+ 50203.63 cm-1（= 600.6 kJ/mol）
  -> 酸素の段差は窒素の 6.4 分の 1。

理論の裏づけ（一次文献）:
  Borden, W. T.; Hoffmann, R.; Stuyver, T.; Chen, B. (2017)
  "Dioxygen: What Makes This Triplet Diradical Kinetically Persistent?"
  J. Am. Chem. Soc. 139, 9010-9018. doi:10.1021/jacs.7b04232

書いてはいけないこと:
  磁化率の数値。検索に出てくる値は出典がはっきりしない。
  「対になっていない電子が 2 個ある」は NIST の項記号 3S から直接出るので、
  磁石に引かれることの説明はそれで足りる。

「#2 で覚えた割り算」（波長 um = 10000 / 波数 cm-1）をここでもう一度使う。
連載として意図的に繰り返している。

出力: _fig2_spin.qmd
"""
import efig
import emol

P, CID = 'ospin', 'ospin1'

R_O2, R_N2 = 1.20752, 1.097685      # 結合長（Å、NIST WebBook）
GAP_O2, GAP_N2 = 7882.39, 50203.63  # 最初の励起状態までの段差（cm⁻¹）
CM_TO_KJ = 11.9626566 / 1000.0      # cm⁻¹ → kJ/mol

G = emol.Group(P, scale=54.0, ball=0.62, spin_sec=21.0)

N2 = G.add(emol.Mol('n2', *emol.pair('N', R_N2), label='窒素分子の立体模型'))
O2 = G.add(emol.Mol('o2', *emol.pair('O', R_O2), label='酸素分子の立体模型'))


def um(wn):
    """波数（cm⁻¹）→ 波長（μm）。#2 で使ったのと同じ割り算。"""
    return 10000.0 / wn


# (鍵, 分子式, 名前, 結合長, いちばん外の部屋に入る電子, 磁石, 段差)
PANEL = [
    ('n2', 'N₂', '窒素', R_N2, 0, False, GAP_N2),
    ('o2', 'O₂', '酸素', R_O2, 2, True, GAP_O2),
]

DET = {
    'n2': '窒素は、いちばん外側の部屋が<b>2つとも空</b>です。'
          'その下の部屋はすべて<b>2個ずつ対</b>で埋まっています。'
          '電子が対になると磁石の性質は打ち消し合うので、'
          '窒素は<b>磁石に引かれません</b>。'
          'しかも電子の向きを変えるには <b>50,204 cm⁻¹</b>'
          '（600.6 kJ/mol）も要ります。'
          'びくともしない——これが窒素です。',
    'o2': '酸素は窒素より電子が<b>2個多い</b>。'
          'その2個は、同じ部屋には入れません。'
          '<b>別々の部屋に、同じ向きで</b>入ります。'
          'つまり<b>対になっていない電子が2個</b>ある。'
          'これが打ち消されずに残るので、'
          '<b>液体酸素は磁石に引き寄せられます</b>。'
          'そして対にするには <b>7,882 cm⁻¹</b>（94.3 kJ/mol）——'
          '窒素の6.4分の1で済みます。'
          '<b>酸素は、いつでも反応したがっている</b>のです。',
}

CSS = """
.@@P@@-row{display:grid;
  grid-template-columns:repeat(auto-fit,minmax(240px,1fr));
  gap:14px;margin:18px 0 4px;}

.@@P@@-cell{display:flex;flex-direction:column;align-items:center;gap:2px;
  padding:13px 10px 15px;border-radius:14px;cursor:default;
  background:rgba(122,96,52,.035);
  border:1px solid rgba(122,96,52,.13);
  transition:background .18s ease,border-color .18s ease,transform .18s ease;}
.@@P@@-cell:hover{transform:translateY(-3px);}
.@@P@@-cell.is-key{background:rgba(190,100,10,.07);
  border-color:rgba(190,100,10,.42);}
.@@P@@-cell svg.@@P@@-mol{display:block;width:100%;max-width:210px;height:auto;
  -webkit-user-select:none;user-select:none;}

.@@P@@-f{font-size:1.34rem;font-weight:800;color:var(--ink);margin-top:2px;}
.@@P@@-nm{font-size:.8rem;color:var(--faint);}
.@@P@@-v{font-size:.98rem;font-weight:800;margin-top:9px;
  padding:4px 13px;border-radius:999px;white-space:nowrap;}
.@@P@@-v.is-no{color:var(--dim);background:rgba(122,96,52,.1);}
.@@P@@-v.is-yes{color:#FFFDF9;background:var(--hb);}

.@@P@@-cap{margin:14px 8px 0;font-size:.84rem;color:var(--dim);
  line-height:1.75;}
/* 凡例。矢印の意味を、図と本文のあいだで一度だけ言う場所 */
.@@P@@-key{display:flex;align-items:center;gap:11px;
  margin:16px 8px 0;padding:10px 14px;border-radius:10px;
  background:rgba(190,100,10,.075);border:1px solid rgba(190,100,10,.22);
  font-size:.86rem;color:var(--ink);line-height:1.7;}
.@@P@@-key svg{flex:none;width:14px;height:26px;}
.@@P@@-key b{color:var(--hb);}
.@@P@@-defs{position:absolute;width:0;height:0;overflow:hidden;}

@media (max-width:820px){
  .@@P@@-row{gap:9px;margin:14px 0 2px;}
  .@@P@@-cell{padding:10px 6px 11px;border-radius:11px;}
  .@@P@@-f{font-size:1.08rem;}
  .@@P@@-v{font-size:.86rem;padding:3px 10px;}
  .@@P@@-cap{font-size:.78rem;margin:11px 2px 0;}
  .@@P@@-key{font-size:.79rem;margin:13px 2px 0;padding:9px 11px;gap:9px;}
}
""".replace('@@P@@', P)


# ---------------------------------------------------------------- 電子の部屋

BOX_W, BOX_H, BOX_GAP = 46.0, 30.0, 16.0


def arrow(x, y, up=True, color='#BE640A'):
    """電子1個。向き（スピン）を矢印で表す。"""
    h = BOX_H * 0.62
    y0, y1 = (y + h / 2, y - h / 2) if up else (y - h / 2, y + h / 2)
    hd = 5.0 if up else -5.0
    return ('<g stroke="%s" fill="%s" stroke-width="2.1" '
            'stroke-linecap="round">'
            '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
            '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" stroke="none"/>'
            '</g>'
            % (color, color, x, y0, x, y1,
               x, y1, x - 3.6, y1 + hd, x + 3.6, y1 + hd))


def rooms(n_out):
    """いちばん外側の部屋（2つ）と、その下が満席であることを示す図。

    窒素は 2 つとも空。酸素は 1 個ずつ、同じ向きで入る。
    「同じ部屋に 2 個入れず、別々の部屋に同じ向きで入る」のは
    電子の決まり（フントの規則）で、ここが磁石の性質の出どころになる。
    """
    w, h = 220.0, 132.0
    cx = w / 2.0
    x0 = cx - BOX_W - BOX_GAP / 2.0
    x1 = cx + BOX_GAP / 2.0
    ytop = 26.0

    o = ['<svg viewBox="0 0 %.0f %.0f" role="img" aria-label="'
         'いちばん外側の部屋に入る電子">' % (w, h)]
    o.append('<text x="%.1f" y="14" font-size="12.5" fill="#7A6E5C" '
             'text-anchor="middle">いちばん外側の部屋</text>' % cx)
    for bx in (x0, x1):
        o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="5" '
                 'fill="#FFFDF9" stroke="rgba(122,96,52,.45)" '
                 'stroke-width="1.4"/>' % (bx, ytop, BOX_W, BOX_H))
    if n_out == 2:
        # 別々の部屋に、同じ向きで
        for bx in (x0, x1):
            o.append(arrow(bx + BOX_W / 2.0, ytop + BOX_H / 2.0, True))
    else:
        for bx in (x0, x1):
            o.append('<text x="%.1f" y="%.1f" font-size="12" fill="#A79A85" '
                     'text-anchor="middle">空</text>'
                     % (bx + BOX_W / 2.0, ytop + BOX_H / 2.0 + 4))

    # 下の部屋はすべて満席
    ylow = ytop + BOX_H + 22.0
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="26" rx="6" '
             'fill="rgba(122,96,52,.1)" stroke="rgba(122,96,52,.28)" '
             'stroke-width="1.2"/>'
             % (x0, ylow, BOX_W * 2 + BOX_GAP))
    o.append('<text x="%.1f" y="%.1f" font-size="12.5" fill="#5F5546" '
             'text-anchor="middle">下の部屋は、すべて2個ずつ対で満席</text>'
             % (cx, ylow + 17))
    if n_out == 2:
        o.append('<text x="%.1f" y="%.1f" font-size="13" font-weight="800" '
                 'fill="#BE640A" text-anchor="middle">'
                 '対になっていない電子が 2 個</text>' % (cx, h - 6))
    else:
        o.append('<text x="%.1f" y="%.1f" font-size="13" font-weight="700" '
                 'fill="#7A6E5C" text-anchor="middle">'
                 '対になっていない電子は 0 個</text>' % (cx, h - 6))
    o.append('</svg>')
    return ''.join(o)


# ---------------------------------------------------------------- 段差

LAD_W, LAD_H = 900.0, 236.0


def ladder():
    """電子の向きを変えるのに要るエネルギーを、窓素と酸素で並べる。"""
    x0, x1 = 150.0, 830.0
    ybase, ytop = 196.0, 34.0
    top_val = GAP_N2

    def sy(v):
        return ybase - v / top_val * (ybase - ytop)

    o = ['<svg viewBox="0 0 %.0f %.0f" role="img" aria-label="'
         '電子の向きを変えるのに要るエネルギーの比較">' % (LAD_W, LAD_H)]
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
             'stroke="rgba(122,96,52,.4)" stroke-width="1.3"/>'
             % (x0 - 30, ybase, x1, ybase))
    o.append('<text x="%.1f" y="%.1f" font-size="13" fill="#5F5546" '
             'text-anchor="end">いまの姿</text>' % (x0 - 40, ybase + 5))

    for k, (label, gap, col) in enumerate((
            ('窒素 N₂', GAP_N2, '#7A6E5C'), ('酸素 O₂', GAP_O2, '#BE640A'))):
        cx = x0 + 130 + k * 380
        y = sy(gap)
        o.append('<rect x="%.1f" y="%.1f" width="230" height="%.1f" rx="7" '
                 'fill="%s" opacity="%.2f"/>'
                 % (cx - 115, y, ybase - y, col, .16 if k == 0 else .2))
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                 'stroke="%s" stroke-width="2.6"/>'
                 % (cx - 115, y, cx + 115, y, col))
        o.append('<text x="%.1f" y="%.1f" font-size="15" font-weight="800" '
                 'fill="%s" text-anchor="middle">%s</text>'
                 % (cx, y - 26, col, label))
        o.append('<text x="%.1f" y="%.1f" font-size="14" font-weight="700" '
                 'fill="%s" text-anchor="middle">%s cm⁻¹</text>'
                 % (cx, y - 8, col, '{:,}'.format(int(round(gap)))))
        o.append('<text x="%.1f" y="%.1f" font-size="13" fill="#5F5546" '
                 'text-anchor="middle">%.1f kJ/mol ／ %.2f μm</text>'
                 % (cx, (y + ybase) / 2.0 + 5, gap * CM_TO_KJ, um(gap)))

    o.append('<text x="%.1f" y="%.1f" font-size="13" fill="#7A6E5C" '
             'text-anchor="end" transform="rotate(-90 %.1f %.1f)">'
             '電子の向きを変えるのに要るエネルギー</text>'
             % (x0 - 60, (ytop + ybase) / 2.0 + 40,
                x0 - 60, (ytop + ybase) / 2.0 + 40))
    o.append('<text x="%.1f" y="%.1f" font-size="14" font-weight="800" '
             'fill="#BE640A" text-anchor="middle">窒素の 6.4 分の 1</text>'
             % (x0 + 510, sy(GAP_O2) - 46))
    o.append('</svg>')
    return ''.join(o)


# ---------------------------------------------------------------- 検算

def check():
    print('コントラスト（地 #FDFAF3 に対して）:')
    emol.check_contrast(['N', 'O'])
    print('NIST WebBook の実測値:')
    print('  O₂ 結合長 %.5f Å ／ 段差 %.2f cm⁻¹ = %.1f kJ/mol = %.3f μm'
          % (R_O2, GAP_O2, GAP_O2 * CM_TO_KJ, um(GAP_O2)))
    print('  N₂ 結合長 %.6f Å ／ 段差 %.2f cm⁻¹ = %.1f kJ/mol'
          % (R_N2, GAP_N2, GAP_N2 * CM_TO_KJ))
    print('  酸素の段差は窒素の %.2f 分の1' % (GAP_N2 / GAP_O2))
    assert GAP_N2 / GAP_O2 > 6.0
    # 酸素のほうが結合が長い（π* に電子が入って結合が弱くなっているため）
    assert R_O2 > R_N2
    print('  酸素の結合は窒素より %.4f Å 長い（π* に電子が入ったぶん弱い）'
          % (R_O2 - R_N2))
    print('枠 %.1f:' % G.vb)
    for m in G.mols:
        x0, x1, y0, y1 = G._box[m.key]
        print('  %-3s 幅 %5.1f × %5.1f  枠を %3.0f%% 使う'
              % (m.key, x1 - x0, y1 - y0, max(x1 - x0, y1 - y0) / G.vb * 100))
        for i, j in m.bonds:
            gap = (emol.dist(m.atoms[i][0], m.atoms[j][0])
                   - 2 * emol.RAD[m.atoms[i][1]] * G.ball) * G.scale
            assert gap > 6.0, '%s: 玉が大きすぎて棒が見えない' % m.key


# ---------------------------------------------------------------- 組み立て

def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, '酸素は、磁石にくっつく',
                        '空気の中で圧倒的に多いのは窒素です。'
                        'ところが<b>液体窒素は磁石に反応せず、'
                        '液体酸素は磁石に引き寄せられます</b>。'
                        'この違いが、私たちが燃えない理由につながっています。'
                        'カーソルを合わせる（スマホはタップ）と、'
                        'その事情が下に出ます。'),
         G.defs(),
         '<div class="%s-row">' % P]

    for key, formula, name, r, n_out, mag, gap in PANEL:
        o.append('<div class="%s-cell%s" data-detail="%s">'
                 % (P, ' is-key' if mag else '', efig.attr(DET[key])))
        o.append(G.svg(key, extra_class='%s-mol' % P))
        o.append('<span class="%s-f">%s</span>' % (P, formula))
        o.append('<span class="%s-nm">%s ／ 結合の長さ %.3f Å</span>'
                 % (P, name, r))
        o.append(rooms(n_out))
        o.append('<span class="%s-v is-%s">%s</span>'
                 % (P, 'yes' if mag else 'no',
                    '磁石に引かれる' if mag else '磁石に引かれない'))
        o.append('</div>')
    o.append('</div>')

    # 凡例。矢印が何を表すのかを書いていないと、図だけ見た人が迷う。
    o.append('<p class="%s-key">'
             '<svg viewBox="0 0 14 26" aria-hidden="true">%s</svg>'
             '<span>矢印 <b>1本が、電子1個</b>。'
             '矢印の向きが、本文でいう「向き」です。'
             '同じ向きにそろっているのが、酸素だけの特徴になります。</span>'
             '</p>' % (P, arrow(7.0, 13.0, True)))

    o.append('<p class="%s-cap">電子は、同じ部屋に入るときは'
             '<b>必ず逆向きの2個で対</b>になります。'
             '対になると磁石の性質は打ち消し合います。'
             'ところが酸素は電子が2個多く、その2個は'
             '<b>別々の部屋に、同じ向きで</b>入ることになる。'
             '打ち消されずに残ったこの2個が、'
             '酸素を磁石に引き寄せています。</p>' % P)

    o.append('<div style="margin:22px 8px 0">%s</div>' % ladder())
    o.append('<p class="%s-cap">対になっていない2個を'
             '<b>対にそろえる</b>のに要るエネルギーです。'
             '<b>本文でいう「壁」の高さが、これにあたります。</b>'
             '窒素は 50,204 cm⁻¹、酸素はその<b>6.4分の1</b>の 7,882 cm⁻¹。'
             '<b>波長になおすと 1.27 μm</b>——'
             '<a href="/posts/note/element-02-carbon/">前回</a>覚えた'
             '「10000 ÷ 波数」を、そのまま使えます。</p>' % P)

    o.append(efig.close_card(
        P,
        '酸素は、いちばん外側に<b>対になっていない電子を2個</b>持っています。'
        'そのため液体酸素は磁石に引き寄せられ、液体窒素は引かれません。'
        'そして——ここからが本題です。'
        '私たちの体を作っている分子は、電子がすべて対になっています。'
        '<b>向きのそろっていない酸素は、そのままでは反応できません。</b>'
        'どちらかが向きを変えるまで、待たされる。'
        'この「待たされる」が、'
        '<b>21%の酸素に囲まれていても私たちが燃えない理由</b>です。'
        '火にマッチが要るのも、体温で酸素を使うのに'
        '鉄を含む酵素が要るのも、すべて同じ理由からです。',
        '結合の長さと電子の状態は NIST Chemistry WebBook 収録の実験値です。'
        'O₂ の基底状態は X ³Σg⁻（結合長 1.20752 Å）で、'
        '最初の励起状態 a ¹Δg までが 7,882.39 cm⁻¹。'
        'N₂ の基底状態は X ¹Σg⁺（結合長 1.097685 Å）で、'
        '最初の励起状態 A ³Σu⁺ までが 50,203.63 cm⁻¹。'
        'kJ/mol への換算は 1 cm⁻¹ ＝ 11.96266 J/mol、'
        '波長への換算は 10000 ÷ 波数 です。'
        '「対になっていない電子が2個ある」ことは、項記号の左肩の 3'
        '（三重項）から直接読み取れます。'
        '酸素がなぜ反応しにくいままでいられるのかの理論的な検討は '
        '<b>Borden, Hoffmann, Stuyver &amp; Chen (2017)</b> '
        '<i>J. Am. Chem. Soc.</i> 139, 9010–9018 にあります。'
        '「部屋」の絵は電子の入り方を簡単にしたもので、'
        '実際にはいちばん外側の2つは π* とよばれる軌道です。',
        CID))
    o.append(G.spin_js(CID, '.%s-mol' % P))
    return '\n'.join(o)


if __name__ == '__main__':
    check()
    efig.save('_fig2_spin.qmd', build())
