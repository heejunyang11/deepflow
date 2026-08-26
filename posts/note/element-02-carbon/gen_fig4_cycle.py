# -*- coding: utf-8 -*-
"""
元素 #2 炭素 / 図4 : 風から生まれて、風に還る。

炭素は絶えずめぐっている。行きと帰りが釣り合っているので、
大気の量はもともと変わらなかった。そこへ<片道の矢印>が 1 本加わった。

この図で見せたいのは 2 つ。
  1. 大気の炭素は約 4.4 年で入れ替わる（880 ÷ 200）。
     つまりあなたの体の炭素も、平均すれば数年前まで空気だった。
  2. 人間が足す矢印は細い。細いが、戻る矢印が無い。

大事な但し書き（ここを混ぜると嘘になる）:
  「分子 1 個が入れ替わる速さ（数年）」と「増えた総量が元に戻る速さ
  （数百年以上）」はまったく別の話である。前者だけ書くと、
  「二酸化炭素はすぐ抜けるから平気だ」という誤読を招く。図の中に明記する。

数値（いずれも概数。単位は GtC＝10 億トンの炭素）:
  大気 約 880 / 陸の植物 約 450 / 土壌 約 1700 / 海 約 37000
  光合成 約 120 と 呼吸・分解 約 120（ほぼ釣り合う）
  海が吸う 約 80 と 海が出す 約 80（ほぼ釣り合う）
  人間が出す 約 11.5（化石燃料 約 10.4 ＋ 土地利用 約 1.1、片道）
    Global Carbon Budget 2025（化石 38.1 GtCO2 ＝ 10.4 GtC、
    土地利用 4.1 GtCO2 ＝ 1.1 GtC）
  そのうち海が約 3、陸が約 2、残り約 5.5 が大気にたまる
    （2015-2024 年の平均で海 29%、陸 21%）

出力: _fig4_cycle.qmd
"""
import efig

P, CID = 'ecyc', 'ecyc1'

# 貯まっている量（GtC）
STOCK = {'air': 880, 'land': 2150, 'sea': 37000}
# 毎年の出入り（GtC/年）
FLUX = {'photo': 120.0, 'resp': 120.0, 'sea_in': 80.0, 'sea_out': 80.0,
        'human': 11.5}
STAY = 5.5              # 大気にたまる分
W_PER = 0.25            # 矢印の太さ（px あたり GtC/年）

VB_W, VB_H = 900.0, 470.0

# (鍵, 左, 上, 幅, 高さ, 見出し, 中身)
BOX = [
    ('air',  300, 22,  300, 82, '大気', '約 880'),
    ('land', 34,  244, 262, 96, '陸（植物と土）', '約 2,150'),
    ('sea',  604, 244, 262, 96, '海', '約 37,000'),
    ('foss', 330, 384, 240, 66, '化石燃料・土地利用', '人間が掘り出す分'),
]

COLOR = {
    'air': '#E7EEF3', 'land': '#E4EBDD', 'sea': '#DFE9EF', 'foss': '#F2E3DC',
    'edge': 'rgba(122,96,52,.34)',
    'nat': '#8C9AA3', 'back': '#9FA98F', 'human': '#B02A37',
}


def w(f):
    """流れの量（GtC/年）→ 矢印の太さ（px）。細さもそのまま情報になる。"""
    return f * W_PER


def arrow(x1, y1, x2, y2, width, color, op=1.0):
    """まっすぐな矢印。太さは流れの量に比例させる。"""
    import math
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1.0
    ux, uy = dx / L, dy / L
    head = max(11.0, width * 2.1)
    bx, by = x2 - ux * head, y2 - uy * head     # 頭の付け根
    px, py = -uy, ux                            # 垂直方向
    hw = max(width * 1.55, 7.0)
    return ('<g><line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
            'stroke="%s" stroke-width="%.2f" stroke-linecap="butt" '
            'opacity="%.2f"/>'
            '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s" '
            'opacity="%.2f"/></g>'
            % (x1, y1, bx, by, color, width, op,
               x2, y2, bx + px * hw, by + py * hw, bx - px * hw, by - py * hw,
               color, op))


def label(x, y, text, size=15, weight=700, color='#5F5546', anchor='middle'):
    return ('<text x="%.1f" y="%.1f" font-size="%d" font-weight="%d" '
            'fill="%s" text-anchor="%s" paint-order="stroke" '
            'stroke="#FDFAF3" stroke-width="4" stroke-linejoin="round">%s'
            '</text>' % (x, y, size, weight, color, anchor, text))


DET = {
    'air': '大気には炭素が<b>約 880 GtC</b>（GtC は10億トンの炭素）'
           'あります。毎年およそ 200 GtC が出入りしているので、'
           '<b>約 4.4 年ですっかり入れ替わる</b>計算になります。'
           'いま吸っている空気の炭素は、数年前には'
           '葉っぱか海の中にあったものです。',
    'land': '陸の植物と土に、あわせて<b>約 2,150 GtC</b>'
            '（植物 約450・土 約1,700）。'
            '植物は光合成で空気から炭素を取りこみ、'
            '呼吸と、枯れたあとの分解で、ほぼ同じだけ返します。'
            'あなたの体の炭素も、'
            'たどればこの経路で空気から来たものです。',
    'sea': '海には<b>約 37,000 GtC</b>——'
           '大気の <b>40 倍以上</b>が溶けています。'
           '海面ではたえず二酸化炭素が出入りしていて、'
           '毎年およそ 80 GtC ずつを吸い、ほぼ同じだけ出しています。'
           '冷たい海ほどよく溶かします。',
    'photo': '<b>光合成</b>。植物が空気中の二酸化炭素を取りこみ、'
             '自分の体に変えます。年に <b>約 120 GtC</b>。'
             'この図でいちばん太い矢印です。',
    'resp': '<b>呼吸と分解</b>。生き物が息を吐き、'
            '枯れたものが微生物に分解されて、炭素が空気へ戻ります。'
            '年に <b>約 120 GtC</b>——光合成と<b>ほぼ同じ量</b>です。'
            'この釣り合いが、大気の量を一定に保ってきました。',
    'sea_in': '<b>海が吸う</b>。二酸化炭素は水によく溶けます。'
              '年に <b>約 80 GtC</b>。',
    'sea_out': '<b>海が出す</b>。溶けていた分が海面から戻ります。'
               '年に <b>約 80 GtC</b>——吸う量と<b>ほぼ同じ</b>です。',
    'human': '<b>人間が足す分</b>。化石燃料を燃やして 約 10.4、'
             '森を切るなどして 約 1.1。あわせて年に <b>約 11.5 GtC</b>。'
             '光合成の 10 分の 1 ほどで、矢印も細くしか描けません。'
             'ですが決定的な違いがあります——'
             '<b>この矢印には、戻りがありません</b>。'
             '半分ほどは海と陸が吸ってくれますが、'
             '残る <b>約 5.5</b> が毎年たまり続けます。',
}

CSS = """
.@@P@@-stage{margin:18px 0 4px;}
.@@P@@-stage svg{display:block;width:100%;height:auto;}
.@@P@@-hit{cursor:default;}
.@@P@@-hit:hover .@@P@@-box{filter:brightness(.965);}
.@@P@@-box{transition:filter .16s ease;}

.@@P@@-note{margin:18px 8px 0;padding:14px 16px;border-radius:11px;
  background:rgba(176,42,55,.055);border:1px solid rgba(176,42,55,.28);
  font-size:.88rem;line-height:1.8;color:var(--ink);}
.@@P@@-note b{color:var(--rt);}

@media (max-width:820px){
  .@@P@@-note{margin:14px 2px 0;padding:11px 12px;font-size:.8rem;}
}
""".replace('@@P@@', P)


def box(key, x, y, bw, bh, head, sub):
    o = ['<g class="%s-hit" data-detail="%s">' % (P, efig.attr(DET[key]))
         if key in DET else '<g>']
    o.append('<rect class="%s-box" x="%.1f" y="%.1f" width="%.1f" height="%.1f" '
             'rx="14" fill="%s" stroke="%s" stroke-width="1.3"/>'
             % (P, x, y, bw, bh, COLOR[key], COLOR['edge']))
    o.append(label(x + bw / 2.0, y + bh / 2.0 - 4, head, 21, 800, '#2B2621'))
    o.append(label(x + bw / 2.0, y + bh / 2.0 + 21, sub, 15, 700, '#5F5546'))
    o.append('</g>')
    return ''.join(o)


def stage():
    o = ['<svg viewBox="0 0 %.0f %.0f" role="img" '
         'aria-label="炭素の循環。光合成と呼吸がほぼ釣り合い、'
         'そこへ人間による片道の流れが加わっている">' % (VB_W, VB_H)]

    # --- 陸と大気（左）
    o.append('<g class="%s-hit" data-detail="%s">' % (P, efig.attr(DET['photo'])))
    o.append(arrow(322, 104, 196, 244, w(FLUX['photo']), COLOR['nat']))
    o.append(label(196, 176, '光合成 約120', 16, 800, '#4E5A61', 'end'))
    o.append('</g>')
    o.append('<g class="%s-hit" data-detail="%s">' % (P, efig.attr(DET['resp'])))
    o.append(arrow(268, 244, 394, 104, w(FLUX['resp']), COLOR['back']))
    o.append(label(370, 205, '呼吸・分解 約120', 16, 800, '#5A6350', 'start'))
    o.append('</g>')

    # --- 海と大気（右）
    o.append('<g class="%s-hit" data-detail="%s">' % (P, efig.attr(DET['sea_in'])))
    o.append(arrow(578, 104, 704, 244, w(FLUX['sea_in']), COLOR['nat']))
    o.append(label(704, 176, '海が吸う 約80', 16, 800, '#4E5A61', 'start'))
    o.append('</g>')
    o.append('<g class="%s-hit" data-detail="%s">' % (P, efig.attr(DET['sea_out'])))
    o.append(arrow(632, 244, 506, 104, w(FLUX['sea_out']), COLOR['back']))
    o.append(label(530, 205, '海が出す 約80', 16, 800, '#5A6350', 'end'))
    o.append('</g>')

    # --- 人間（下から上へ、片道）
    o.append('<g class="%s-hit" data-detail="%s">' % (P, efig.attr(DET['human'])))
    o.append(arrow(450, 384, 450, 108, w(FLUX['human']), COLOR['human']))
    o.append(label(462, 340, '約11.5（戻りなし）', 16, 800, '#B02A37', 'start'))
    o.append('</g>')

    for key, x, y, bw, bh, head, sub in BOX:
        o.append(box(key, x, y, bw, bh, head, sub))

    # --- 釣り合いの印
    o.append(label(450, 150, '行き 120 ＝ 帰り 120 ／ 行き 80 ＝ 帰り 80',
                   15, 700, '#7A6E5C'))
    o.append(label(450, 172, 'ここは、ずっと釣り合ってきた', 14, 400, '#7A6E5C'))

    # --- たまる分
    o.append('<rect x="612" y="26" width="252" height="74" rx="12" '
             'fill="rgba(176,42,55,.07)" stroke="rgba(176,42,55,.36)" '
             'stroke-width="1.3"/>')
    o.append(label(738, 56, '毎年 約 %.1f がたまる' % STAY, 17, 800, '#B02A37'))
    o.append(label(738, 79, '出した約11.5のうち、海が約3・陸が約2を吸う',
                   12.5, 400, '#8A5A55'))

    o.append(label(38, VB_H - 8, '単位はすべて GtC／年（GtC＝10億トンの炭素）。'
                   '矢印の太さは量に比例。', 13, 400, '#7A6E5C', 'start'))
    o.append('</svg>')
    return ''.join(o)


def check():
    turn = STOCK['air'] / (FLUX['photo'] + FLUX['sea_in'])
    print('大気 %d GtC ÷ 出入り %.0f GtC/年 = %.2f 年で入れ替わる'
          % (STOCK['air'], FLUX['photo'] + FLUX['sea_in'], turn))
    print('海は大気の %.1f 倍' % (STOCK['sea'] / float(STOCK['air'])))
    print('人間の矢印は光合成の %.1f%%（太さ %.1fpx 対 %.1fpx）'
          % (FLUX['human'] / FLUX['photo'] * 100,
             w(FLUX['human']), w(FLUX['photo'])))
    assert abs(FLUX['photo'] - FLUX['resp']) < 1e-9
    assert abs(FLUX['sea_in'] - FLUX['sea_out']) < 1e-9
    assert 4.0 < turn < 5.0
    return turn


def build(turn):
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, '風から生まれて、風に還る',
                        '炭素は絶えずめぐっています。'
                        '箱や矢印にカーソルを合わせる（スマホはタップ）と、'
                        'その中身が下に出ます。'),
         '<div class="%s-stage">%s</div>' % (P, stage())]

    o.append('<p class="%s-note"><b>ここを混ぜてはいけません。</b>'
             '二酸化炭素の分子1個が入れ替わるのに<b>数年</b>。'
             'これは上の計算どおりです。'
             'ですが、<b>増えた総量がならされて元に戻るには数百年以上</b>'
             'かかります。この2つはまったく別の話です。'
             '「すぐ入れ替わるのだから、増えた分もすぐ消える」'
             '——とはなりません。'
             '入れ替わるのは<b>どの分子がそこにいるか</b>であって、'
             '<b>何個いるか</b>ではないためです。</p>' % P)

    o.append(efig.close_card(
        P,
        '植物は空気から年に <b>約120</b> を取りこみ、'
        '呼吸と分解でほぼ同じだけ返します。'
        '海も <b>約80</b> を吸って、ほぼ同じだけ出します。'
        '行きと帰りが釣り合っているので、大気の量は変わってきませんでした。'
        '大気の炭素は <b>約 %.1f 年</b>ですっかり入れ替わる勘定で、'
        'つまり<b>あなたの体の炭素も、数年前までは空気だった</b>のです。'
        'そこへ、片道の矢印が1本加わりました。'
        '<b>細く見えますが、戻りがありません。</b>' % turn,
        '数値はすべて概数です。'
        '貯蔵量と自然の出入り（光合成・呼吸・海面での交換）は'
        'IPCC 第6次評価報告書 第1作業部会 第5章の炭素循環図にもとづきます。'
        '人間が出す分は Global Carbon Budget 2025 の '
        '2025年見通し（化石 38.1 GtCO₂＝約10.4 GtC、'
        '土地利用 4.1 GtCO₂＝約1.1 GtC）。'
        '海と陸が吸う割合は 2015–2024 年平均で海 29%・陸 21%。'
        '「約4.4年」は大気の量を毎年の出入りで割った目安であって、'
        '増えた分が元に戻るまでの時間ではありません。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    efig.save('_fig4_cycle.qmd', build(check()))
