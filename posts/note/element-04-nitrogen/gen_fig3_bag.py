# -*- coding: utf-8 -*-
"""
元素 #4 窒素 / 図3 : ポテチの袋に、なぜ窒素なのか。

「開かない」という性質は欠点ではなく、そのまま用途になる。
候補を 4 つ並べると、消去法で窒素しか残らないことが見える。

  空気（そのまま）  酸素が油を酸化させる          -> 不可
  ヘリウム          完璧に反応しない。ただし高価    -> 不可（値段）
  二酸化炭素        油に溶けて袋がしぼむ           -> 不可
  窒素              安い・無害・何もしない          -> 採用

読み取らせたいこと:
  体が窒素を使えない理由と、ポテチを守れる理由は、**まったく同じ**。
  三重結合が固すぎて、隣の油に見向きもしない。

出力: _fig3_bag.qmd
"""
import efig

P, CID = 'nbag', 'nbag3'

#  key, 名前, 判定(y/n), 短評, 詳細文
CAND = [
    ('air', '空気のまま', 'n', '酸素が、油を酸化させる',
     '空気の 21% は酸素です。'
     '<a href="/posts/note/element-03-oxygen/">前回</a>見たとおり、'
     '酸素は放っておけば何とでも結びつきます。'
     '<b>揚げ物は数日で古くなります。</b>'),
    ('he', 'ヘリウム', 'n', '完璧。ただし高すぎる',
     '<b>貴ガス</b>——外側の電子が満ちていて、差し出す手がありません。'
     'まったく反応しないので、保存という点では理想的です。'
     'ただし<b>高価</b>で、お菓子の袋には割が合いません。'
     '（<a href="/posts/note/element-01-hydrogen/">第1回</a>で'
     '「宇宙の原子 100 個のうち 8 個はヘリウム」と数えました。'
     '<b>宇宙では2番目に多いのに、地球では希少</b>です。'
     '軽すぎて大気から逃げてしまうため、'
     '天然ガス田から集めるしかありません。）'),
    ('co2', '二酸化炭素', 'n', '油に溶けて、袋がしぼむ',
     '安く手に入りますが、<b>油に溶けこみます</b>。'
     '袋がしぼんでクッションにならず、味も変わってしまいます。'),
    ('n2', '窒素', 'y', '安い・無害・何もしない',
     '<b>これが採用されました。</b>'
     '空気の 78% なので、集めるのが安い。'
     'そして<b>三重結合が固すぎて、隣にある油に見向きもしません</b>。'
     '体が窒素を使えない理由と、まったく同じ性質です。'),
]

CSS = """
.%(p)s{--n2:#2E6E4E;--ng:#A2988A;}
.%(p)s-lab{margin:20px 8px 9px;font-size:.92rem;color:var(--dim);}
.%(p)s-list{display:grid;gap:9px;margin:0 8px;}
.%(p)s-r{display:grid;grid-template-columns:auto 1fr auto;align-items:center;
  gap:14px;padding:14px 17px;border-radius:12px;cursor:default;
  background:rgba(122,96,52,.055);border:1px solid rgba(122,96,52,.14);
  transition:background .18s ease;}
.%(p)s-r:hover{background:rgba(122,96,52,.14);}
.%(p)s-r.win{background:rgba(46,110,78,.10);
  border-color:rgba(46,110,78,.30);border-left:4px solid var(--n2);}
.%(p)s-r.win:hover{background:rgba(46,110,78,.18);}
.%(p)s-r .nm{font-size:1.02rem;font-weight:800;color:var(--ink);
  white-space:nowrap;}
.%(p)s-r.win .nm{color:var(--n2);}
.%(p)s-r .cm{font-size:.9rem;color:var(--dim);line-height:1.6;}
.%(p)s-mk{font-size:1.3rem;font-weight:800;line-height:1;}
.%(p)s-mk.y{color:var(--n2);}
.%(p)s-mk.n{color:var(--ng);}

/* 袋の断面。窒素が詰まって張っている様子を、絵で一度だけ見せる */
.%(p)s-bagwrap{margin:20px 8px 0;display:flex;justify-content:center;}
.%(p)s-bagwrap svg{width:100%%;max-width:430px;height:auto;}

.%(p)s-note{margin:16px 8px 6px;padding:15px 17px;border-radius:12px;
  background:rgba(46,110,78,.08);border:1px solid rgba(46,110,78,.24);
  font-size:.95rem;line-height:1.8;color:var(--ink);}
.%(p)s-note b{color:var(--n2);}

@media (max-width:820px){
  .%(p)s-lab{font-size:.84rem;margin:16px 2px 8px;}
  .%(p)s-list{margin:0 2px;gap:7px;}
  .%(p)s-r{grid-template-columns:1fr auto;gap:8px 10px;padding:11px 13px;}
  .%(p)s-r .nm{font-size:.9rem;}
  .%(p)s-r .cm{grid-column:1/-1;font-size:.8rem;}
  .%(p)s-bagwrap{margin:16px 2px 0;}
  .%(p)s-note{margin:13px 2px 4px;padding:12px 13px;font-size:.85rem;}
}
""" % {'p': P}


def bag():
    """パンパンに張った袋の断面。中に N₂ を散らす。"""
    o = ['<svg viewBox="0 0 420 180" role="img" '
         'aria-label="窒素が詰まったポテトチップスの袋">']
    # 袋の輪郭（上下をふくらませる）
    o.append('<path d="M28 26 C120 6 300 6 392 26 '
             'C404 70 404 110 392 154 '
             'C300 174 120 174 28 154 '
             'C16 110 16 70 28 26 Z" '
             'fill="#F2EADA" stroke="#C9B896" stroke-width="2"/>')
    # シール部
    for y in (20, 160):
        o.append('<rect x="24" y="%d" width="372" height="7" rx="3.5" '
                 'fill="#DCCFB4"/>' % y)
    # 中身：チップスの断片
    for cx, cy, r in [(120, 118, 15), (168, 132, 12), (232, 124, 14),
                      (290, 134, 11), (196, 108, 10)]:
        o.append('<ellipse cx="%d" cy="%d" rx="%d" ry="%.1f" fill="#E0B96A" '
                 'stroke="#C79A46" stroke-width="1.4" opacity=".95"/>'
                 % (cx, cy, r, r * .62))
    # 窒素分子（二つ玉を短い棒でつないだ形）
    for cx, cy, s in [(96, 62, 1.0), (170, 48, .85), (250, 60, .95),
                      (322, 50, .8), (136, 88, .7), (296, 96, .75)]:
        d = 9 * s
        o.append('<g opacity=".92">'
                 '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                 'stroke="#2E6E4E" stroke-width="%.1f" stroke-linecap="round"/>'
                 '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#3E8A63"/>'
                 '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#3E8A63"/>'
                 '</g>'
                 % (cx - d, cy, cx + d, cy, 3.2 * s,
                    cx - d, cy, 6.4 * s, cx + d, cy, 6.4 * s))
    o.append('<text x="210" y="163" font-size="13" fill="#7A6E5C" '
             'text-anchor="middle">中身は、ほぼ 100% の窒素</text>')
    o.append('</svg>')
    return ''.join(o)


def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, '袋の中身は、空気ではありません',
                        'ポテトチップスの袋に何を詰めるか。'
                        '候補を並べると、消去法で窒素しか残りません。'
                        '行にカーソルを合わせる（スマホはタップ）と説明が出ます。')]

    o.append('<div class="%s-bagwrap">%s</div>' % (P, bag()))

    o.append('<p class="%s-lab">詰めるものの候補</p>' % P)
    o.append('<div class="%s-list">' % P)
    for key, name, mk, cm, detail in CAND:
        o.append('<div class="%s-r%s" data-detail="%s">'
                 '<span class="nm">%s</span><span class="cm">%s</span>'
                 '<span class="%s-mk %s">%s</span></div>'
                 % (P, ' win' if mk == 'y' else '', efig.attr(detail),
                    name, cm, P, mk, '○' if mk == 'y' else '×'))
    o.append('</div>')

    o.append('<div class="%s-note">'
             'そして<b>袋がパンパンなのにも意味があります</b>。'
             'クッションです。輸送中に潰れないよう、わざと張らせてある。'
             '<b>空気だと思っていたものは、緩衝材であり、酸化防止剤でした。</b>'
             '</div>' % P)

    o.append(efig.close_card(
        P,
        'ポテトチップスの袋に詰まっているのは、<b>ほぼ 100% の窒素</b>です。'
        '酸素は油を酸化させ、ヘリウムは高すぎ、二酸化炭素は油に溶ける。'
        '残ったのが窒素でした。'
        '<b>安く、無害で、そして何もしない。</b>'
        '三重結合が固すぎて、隣にある油に見向きもしないからです。'
        '——<b>あなたの体が窒素を使えない理由と、'
        'ポテチが守られている理由は、まったく同じ性質</b>です。',
        '図の袋と分子は仕組みを示すための模式で、'
        '実際の大きさの比ではありません。'
        '窒素充填は食品包装で広く使われている方法で、'
        '油脂の酸化と、輸送時の破損の両方を防ぐ目的があります。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    efig.save('_fig3_bag.qmd', build())
