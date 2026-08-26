# -*- coding: utf-8 -*-
"""
元素 #2 炭素 / 図6 : 空気の分子 1 万個のうち、二酸化炭素は 4 個。

#1 の図1 は「点 100 個で宇宙を描く」だった。この記事はその対で終える。
今度は 1 万個で空気を描く。連載としての韻を踏ませるための図でもある。

見せたいのは 1 点だけ。
  1 万個のうち、産業革命前から在ったのが 2.8 個。人間が足したのが 1.4 個。
  たった 1.4 個。それでも気温は動いた。「少ないこと」と「効かないこと」は別。

作り方:
  1 万個を 200 列 x 50 行に並べる。ただし丸を 1 万個置くと重すぎるので、
  同じ気体が続く区間を「行ごとの帯」にまとめて描く（20 個ほどの矩形で済む）。
  境目は整数でなくてよいので、4.228 個ぶんといった端数もそのまま描ける。
  さらに最後の 10 個だけを引き伸ばした帯を下に置き、
  二酸化炭素の内訳（もともと 2.8 ／ 人間 1.428）を読めるようにする。

組成（乾燥空気の体積比、ppm）:
  CO2 422.8   NOAA 世界平均 2024 年（産業革命前は 280）
  Ar  9340
  O2  209460
  その他 約 27.3（ネオン 18.18・ヘリウム 5.24・メタン・クリプトンなど）
  N2  残り = 780749.9（= 78.07%。よく載っている 78.084% とほぼ一致する）

出力: _fig6_ppm.qmd
"""
import math
import efig

P, CID = 'eppm', 'eppm1'

COL, ROW = 200, 50            # 1 万個の並べ方
CELL = 5.0                    # 1 個ぶんの大きさ（px）
TAIL = 10                     # 下で引き伸ばす個数

PPM_CO2 = 422.8               # NOAA 世界平均 2024 年
PPM_PRE = 280.0               # 産業革命前
PPM_AR = 9340.0
PPM_O2 = 209460.0
PPM_ETC = 27.3

# (鍵, 見出し, ppm, 色)。並べる順に書く。二酸化炭素が最後に来るようにする。
def _segs():
    known = PPM_CO2 + PPM_AR + PPM_O2 + PPM_ETC
    return [
        ('n2',  '窒素 N₂',        1e6 - known,        '#828F99'),
        ('o2',  '酸素 O₂',        PPM_O2,             '#839777'),
        ('ar',  'アルゴン Ar',    PPM_AR,             '#9A8E74'),
        ('etc', 'その他',         PPM_ETC,            '#6E6558'),
        ('pre', 'CO₂（もとから）', PPM_PRE,           '#B78020'),
        ('add', 'CO₂（人間が足した分）', PPM_CO2 - PPM_PRE, '#B02A37'),
    ]


SEG = _segs()

DET = {
    'n2':  '<b>窒素</b>が 1 万個のうち <b>約 7,807 個</b>。'
           '空気のほとんどはこれです。'
           '三重結合でがっちり閉じていて、めったに何とも反応しません。'
           '熱に対しても透明で、毛布の役目は果たしません。',
    'o2':  '<b>酸素</b>が <b>約 2,095 個</b>。'
           '私たちが吸っているのはこれですが、'
           'これも熱に対しては透明です。'
           '窒素と合わせて 9,902 個——<b>空気の 99%</b>が'
           '赤外線を素通りさせます。',
    'ar':  '<b>アルゴン</b>が <b>約 93 個</b>。'
           '18 族なので何ともつながりません。'
           '二酸化炭素の 20 倍以上あるのに、気候には何もしません。',
    'etc': '<b>その他ぜんぶ</b>——ネオン、ヘリウム、メタン、クリプトン……'
           'を合わせても <b>0.3 個ぶん</b>にしかなりません。',
    'pre': '<b>もともとあった二酸化炭素</b>。'
           '産業革命の前は 280 ppm、つまり 1 万個のうち <b>2.8 個</b>でした。'
           'この 2.8 個があったからこそ、地球は'
           '<b>平均 15℃ という住める温度</b>に保たれてきました。'
           'まったく無ければ、地球は凍りついています。',
    'add': '<b>人間が足した分</b>。280 → 422.8 ppm。'
           '1 万個のうち <b>1.4 個</b>ぶんです。'
           'たったこれだけ、と思われるかもしれません。'
           'ですが 2.8 個が 15℃ を支えていたのですから、'
           'そこへ 1.4 個——<b>5 割増し</b>——を足せば、'
           '気温が動かないほうがおかしいのです。',
}

VB_W, VB_H = 1000.0, 500.0
FIELD_Y = 52.0
STRIP_Y, STRIP_H = 384.0, 62.0

CSS = """
.@@P@@-stage{margin:18px 0 2px;}
.@@P@@-stage svg{display:block;width:100%;height:auto;}
.@@P@@-hit{cursor:default;}
.@@P@@-hit rect{transition:opacity .16s ease;}
.@@P@@-hit:hover rect{opacity:.78;}

.@@P@@-leg{display:flex;flex-wrap:wrap;gap:7px;margin:14px 8px 0;}
.@@P@@-leg span{display:flex;align-items:center;gap:7px;
  padding:5px 11px;border-radius:9px;font-size:.85rem;color:var(--ink);
  background:rgba(122,96,52,.06);border:1px solid rgba(122,96,52,.14);}
.@@P@@-leg u{width:12px;height:12px;border-radius:3px;
  text-decoration:none;display:block;}
.@@P@@-leg b{font-variant-numeric:tabular-nums;}

@media (max-width:820px){
  .@@P@@-leg{gap:5px;margin:11px 2px 0;}
  .@@P@@-leg span{padding:4px 8px;font-size:.74rem;}
}
""".replace('@@P@@', P)


# ---------------------------------------------------------------- 計算

def cells(ppm):
    """ppm → 1 万個のうち何個ぶんか。"""
    return ppm / 1e6 * (COL * ROW)


def bounds():
    """各区間の始まりと終わり（個）を積み上げて返す。"""
    out = []
    a = 0.0
    for key, name, ppm, color in SEG:
        b = a + cells(ppm)
        out.append((key, name, ppm, color, a, b))
        a = b
    return out


def runs(a, b):
    """個の区間 a〜b を、行ごとの（行, 左, 右）に切り分ける。"""
    out = []
    r0 = int(a // COL)
    r1 = int(math.ceil(b / COL)) - 1
    for r in range(r0, r1 + 1):
        s = max(a, r * COL) - r * COL
        e = min(b, (r + 1) * COL) - r * COL
        if e - s > 1e-9:
            out.append((r, s, e))
    return out


def label(x, y, text, size=15, weight=700, color='#5F5546', anchor='middle'):
    return ('<text x="%.1f" y="%.1f" font-size="%s" font-weight="%d" '
            'fill="%s" text-anchor="%s" paint-order="stroke" '
            'stroke="#FDFAF3" stroke-width="3.5" stroke-linejoin="round">%s'
            '</text>' % (x, y, size, weight, color, anchor, text))


# ---------------------------------------------------------------- 描画

def stage():
    B = bounds()
    o = ['<svg viewBox="0 0 %.0f %.0f" role="img" '
         'aria-label="空気の分子1万個の内訳。二酸化炭素は4個ぶんしかない">'
         % (VB_W, VB_H)]

    o.append(label(0, 30, '空気の分子を 1 万個ならべると', 19, 800,
                   '#2B2621', 'start'))

    # --- 本体。同じ気体が続くところは行ごとの帯にまとめる
    for key, _name, _ppm, color, a, b in B:
        o.append('<g class="%s-hit" data-detail="%s">' % (P, efig.attr(DET[key])))
        for r, s, e in runs(a, b):
            o.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" '
                     'fill="%s"/>'
                     % (s * CELL, FIELD_Y + r * CELL, (e - s) * CELL, CELL,
                        color))
        o.append('</g>')

    # --- 数えられるように、10 個ごと・5 行ごとの薄い罫を重ねる
    fh = ROW * CELL
    for c in range(10, COL, 10):
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                 'stroke="#FDFAF3" stroke-opacity=".30" stroke-width="1"/>'
                 % (c * CELL, FIELD_Y, c * CELL, FIELD_Y + fh))
    for r in range(5, ROW, 5):
        o.append('<line x1="0" y1="%.1f" x2="%.1f" y2="%.1f" '
                 'stroke="#FDFAF3" stroke-opacity=".30" stroke-width="1"/>'
                 % (FIELD_Y + r * CELL, COL * CELL, FIELD_Y + r * CELL))
    o.append('<rect x="0" y="%.1f" width="%.1f" height="%.1f" fill="none" '
             'stroke="rgba(122,96,52,.35)" stroke-width="1.2"/>'
             % (FIELD_Y, COL * CELL, fh))

    # --- 最後の 10 個を拡大する
    tail_x = (COL - TAIL) * CELL
    fy = FIELD_Y + fh
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" '
             'stroke="#B02A37" stroke-width="2"/>'
             % (tail_x - 1, fy - CELL - 1, TAIL * CELL + 2, CELL + 2))
    o.append('<path d="M%.1f %.1f L0 %.1f M%.1f %.1f L%.1f %.1f" fill="none" '
             'stroke="#B02A37" stroke-width="1.2" stroke-dasharray="5 4"/>'
             % (tail_x, fy + 2, STRIP_Y, COL * CELL, fy + 2,
                COL * CELL, STRIP_Y))
    o.append(label(VB_W / 2.0, STRIP_Y - 14,
                   'いちばん最後の 10 個を、横いっぱいに引き伸ばすと',
                   16, 700, '#7A6E5C'))

    # --- 引き伸ばした帯
    lo = COL * ROW - TAIL
    per = VB_W / TAIL
    for key, _name, _ppm, color, a, b in B:
        if b <= lo:
            continue
        s = (max(a, lo) - lo) * per
        e = (b - lo) * per
        o.append('<g class="%s-hit" data-detail="%s">' % (P, efig.attr(DET[key])))
        o.append('<rect x="%.2f" y="%.1f" width="%.2f" height="%.1f" '
                 'fill="%s" stroke="rgba(43,38,33,.22)" stroke-width="1"/>'
                 % (s, STRIP_Y, e - s, STRIP_H, color))
        o.append('</g>')

    for i in range(1, TAIL):
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                 'stroke="#FDFAF3" stroke-opacity=".45" stroke-width="1"/>'
                 % (i * per, STRIP_Y, i * per, STRIP_Y + STRIP_H))

    # --- 引き伸ばした帯への書きこみ
    pre_a = [x for x in B if x[0] == 'pre'][0]
    add_a = [x for x in B if x[0] == 'add'][0]
    pc = ((pre_a[4] + pre_a[5]) / 2.0 - lo) * per
    ac = ((add_a[4] + add_a[5]) / 2.0 - lo) * per
    o.append(label(pc, STRIP_Y + 37, '2.8 個', 21, 800, '#FFFDF9'))
    o.append(label(ac, STRIP_Y + 37, '1.4 個', 21, 800, '#FFFDF9'))
    o.append(label(pc, STRIP_Y + STRIP_H + 22, 'もとから（280 ppm）',
                   14, 700, '#8A6212'))
    o.append(label(ac, STRIP_Y + STRIP_H + 22, '人間が足した（142.8 ppm）',
                   14, 700, '#B02A37'))
    o.append(label(((add_a[4] - lo) * per + VB_W) / 2.0,
                   STRIP_Y + STRIP_H + 44,
                   '↑ 1 万個のうち、これだけ', 14, 700, '#B02A37'))
    o.append('</svg>')
    return ''.join(o)


def legend():
    o = ['<div class="%s-leg">' % P]
    for key, name, _ppm, color, a, b in bounds():
        n = b - a
        txt = ('%.1f 個' % n) if n < 10 else ('%s 個' % '{:,}'.format(int(round(n))))
        o.append('<span data-detail="%s"><u style="background:%s"></u>%s '
                 '<b>%s</b></span>' % (efig.attr(DET[key]), color, name, txt))
    o.append('</div>')
    return ''.join(o)


# ---------------------------------------------------------------- 検算

def _lum(h):
    def ch(c):
        c /= 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (int(h[i:i + 2], 16) for i in (1, 3, 5))
    return .2126 * ch(r) + .7152 * ch(g) + .0722 * ch(b)


def contrast(a, b='#FDFAF3'):
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + .05) / (lo + .05)


def check():
    B = bounds()
    print('1 万個の内訳:')
    tot = 0.0
    for key, name, ppm, color, a, b in B:
        n = b - a
        tot += n
        c = contrast(color)
        print('  %-22s %9.3f 個 (%9.1f ppm)  地とのコントラスト %.2f:1 %s'
              % (name, n, ppm, c, 'OK' if c >= 3.0 else '*** 低い ***'))
        assert c >= 3.0, '%s の色が薄すぎる' % name
    print('  合計 %.6f 個' % tot)
    assert abs(tot - COL * ROW) < 1e-6, '合計が 1 万個にならない'

    n2 = [x for x in B if x[0] == 'n2'][0]
    print('窒素は %.4f%%（よく載っている 78.084%% との差 %.3f 点）'
          % (n2[2] / 1e4, 78.084 - n2[2] / 1e4))
    assert abs(n2[2] / 1e4 - 78.084) < 0.05

    add = [x for x in B if x[0] == 'add'][0]
    pre = [x for x in B if x[0] == 'pre'][0]
    print('二酸化炭素 合計 %.3f 個（もとから %.1f ＋ 人間 %.3f）＝ %.1f ppm'
          % (add[5] - pre[4], pre[5] - pre[4], add[5] - add[4], PPM_CO2))
    print('人間が足した分は、もとからあった量の %.0f%% 増し'
          % ((PPM_CO2 - PPM_PRE) / PPM_PRE * 100))
    # 最後の 10 個の中に二酸化炭素がすべて入っていること
    assert pre[4] > COL * ROW - TAIL, '拡大の窓に二酸化炭素が収まっていない'


def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, '1 万個のうち、4 個',
                        '#1 では点100個で宇宙を描きました。'
                        '今度は1万個で空気を描きます。'
                        'ひとかたまりにカーソルを合わせる'
                        '（スマホはタップ）と、その中身が下に出ます。'),
         '<div class="%s-stage">%s</div>' % (P, stage()),
         legend()]

    o.append(efig.close_card(
        P,
        '空気の分子を1万個ならべると、窒素が約7,807個、酸素が約2,095個、'
        'アルゴンが約93個。そして<b>二酸化炭素は4個</b>です。'
        'そのうち<b>産業革命の前からあったのが2.8個</b>、'
        '<b>人間が足したのが1.4個</b>。'
        'たった1.4個、と思うかもしれません。'
        'ですが、その2.8個があったからこそ地球は平均15℃に保たれてきたのです。'
        'そこへ<b>5割増し</b>を足せば、気温が動かないほうがおかしい。'
        '<b>少ないことと、効かないことは、別のことです。</b>',
        '乾燥空気の体積比です。二酸化炭素は <b>422.8 ppm</b>'
        '（NOAA 世界平均、2024年）、産業革命前は 280 ppm。'
        'アルゴン 9,340 ppm、酸素 209,460 ppm、'
        'その他（ネオン・ヘリウム・メタンなど）約 27 ppm、'
        '窒素は残りとして計算しています（78.07%、'
        'よく載っている 78.084% とほぼ一致します）。'
        '世界の平均気温は 1850–1900 年より'
        '<b>約 1.09℃</b> 高くなりました（2011–2020年の平均、'
        'IPCC 第6次評価報告書）。近年は単年で 1.5℃ を超えた年もあります。'
        '図では 1 万個を 200 列 × 50 行に並べ、'
        '同じ気体が続くところは帯にまとめて描いています'
        '（端数もそのままの幅で描いてあります）。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    check()
    efig.save('_fig6_ppm.qmd', build())
