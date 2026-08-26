# -*- coding: utf-8 -*-
"""
元素 #3 酸素 / 図5 : ヘモグロビンの S 字曲線。

肺で酸素を積み、組織で降ろす。この往復ができるのは、
ヘモグロビンの結合曲線が<直線でも単純な曲線でもなく S 字>だからである。

曲線は空想ではなく、公表されている式をそのまま描く。
  Severinghaus, J. W. (1979)
  "Simple, accurate equations for human blood O2 dissociation computations"
  J. Appl. Physiol. 46, 599-602.
      S = 1 / ( 23400 / (PO2^3 + 150 * PO2) + 1 )     PO2 は mmHg
この式に 40 mmHg を入れると 75.0% が出る。教科書に載っている
「静脈血の酸素飽和度は約75%」がそのまま再現される（check() で検算）。

比べる相手として、協同性が無い場合（ミオグロビンのような単純な曲線）を
同じ P50 で描く。運動中の筋肉（20 mmHg）で差が最大になる。
  S字   : 肺 97.7% -> 20 mmHg で 32.0%   渡せる量 65.7 ポイント
  単純曲線: 肺 79.0% -> 20 mmHg で 42.9%   渡せる量 36.1 ポイント
S 字のほうが 1.8 倍多く渡せる。これがこの図の落としどころ。

書き方の注意:
  「なぜ S 字になるのか」＝4つの結合場所が互いに影響し合うため（協同性）。
  これは確立した事実。ただしヒル係数などの当てはめ値は式の道具であって
  実体ではないので、数式の細部には踏みこまない。

出力: _fig5_hemoglobin.qmd
"""
import efig

P, CID = 'ohem', 'ohem1'

P50 = 26.6          # 飽和度 50% になる酸素分圧（mmHg）
PMAX = 110.0        # 横軸の右端

# (酸素分圧, 名前, 説明)
MARK = [
    (100.0, '肺', '肺胞のまわり。ここで満タンに積む'),
    (40.0, '休んでいる体', '安静時の組織。ここで少し降ろす'),
    (20.0, '運動中の筋肉', '酸素を使い切っている場所。ここで一気に降ろす'),
]


def sev(po2):
    """Severinghaus (1979) の式。公表されている式をそのまま使う。"""
    if po2 <= 0:
        return 0.0
    return 1.0 / (23400.0 / (po2 ** 3 + 150.0 * po2) + 1.0)


def simple(po2):
    """協同性が無い場合。同じ P50 の単純な曲線（比較用）。"""
    return po2 / (po2 + P50)


VB_W, VB_H = 900.0, 460.0
PLOT = (86.0, 30.0, 828.0, 372.0)

CSS = """
.@@P@@-stage{margin:18px 0 2px;}
.@@P@@-stage svg{display:block;width:100%;height:auto;}
.@@P@@-hit{cursor:default;}
.@@P@@-hit circle{transition:r .16s ease;}

.@@P@@-tw{margin:18px 8px 0;overflow-x:auto;}
.@@P@@-tab{width:100%;border-collapse:collapse;font-size:.87rem;min-width:460px;}
.@@P@@-tab th,.@@P@@-tab td{padding:9px 10px;text-align:center;
  border-bottom:1px solid var(--line2);font-variant-numeric:tabular-nums;}
.@@P@@-tab th{font-size:.78rem;font-weight:700;color:var(--faint);
  border-bottom:1.5px solid rgba(122,96,52,.3);}
.@@P@@-tab td:first-child,.@@P@@-tab th:first-child{text-align:left;
  white-space:nowrap;}
.@@P@@-tab tr.is-key td{background:rgba(190,100,10,.09);font-weight:700;}
.@@P@@-tab tr.is-key td:first-child{color:var(--hb);}
.@@P@@-cap{margin:13px 8px 0;font-size:.84rem;color:var(--dim);
  line-height:1.75;}

@media (max-width:820px){
  .@@P@@-tw{margin:14px 2px 0;}
  .@@P@@-cap{font-size:.78rem;margin:11px 2px 0;}
}
""".replace('@@P@@', P)

DET = {
    'lung': '<b>肺</b>。酸素分圧は約 100 mmHg。'
            'ここでヘモグロビンは <b>97.7%</b> まで酸素を積みます。'
            'S字の<b>平らな天井</b>にあたる部分なので、'
            '多少分圧が下がっても満タンのまま——'
            '高い山に登っても、しばらくは平気でいられる理由です。',
    'rest': '<b>休んでいる体の組織</b>。酸素分圧は約 40 mmHg。'
            'ここで飽和度は <b>75.0%</b> まで落ちます。'
            'つまり積んできた酸素のうち<b>4分の1ほどを降ろした</b>だけ。'
            '残りは持ったまま帰ります。'
            'これは無駄ではなく、<b>非常用の備え</b>です。',
    'work': '<b>運動している筋肉</b>。酸素分圧は 20 mmHg あたりまで落ちます。'
            'すると飽和度は一気に <b>32.0%</b> へ。'
            'S字の<b>急な坂</b>にあたる部分なので、'
            '<b>少し分圧が下がるだけで大量に降ろせる</b>のです。'
            '必要な場所で、必要なだけ手放す。'
            'これがS字であることの意味です。',
    'flat': 'これは<b>協同性が無かったら</b>どうなるかを描いた曲線です。'
            '同じ半分の点（P50）を通しても、形はS字になりません。'
            '肺でも <b>79.0%</b> しか積めず、'
            '運動中の筋肉でも <b>42.9%</b> までしか降ろせない。'
            '<b>渡せる量は S 字の半分ほど</b>です。'
            'ヘモグロビンが4つの結合場所を持ち、'
            'それらが互いに影響し合うからこそ、この差が生まれます。',
}


# ---------------------------------------------------------------- 描画

def stage():
    x0, y0, x1, y1 = PLOT

    def sx(p):
        return x0 + p / PMAX * (x1 - x0)

    def sy(s):
        return y1 - s * (y1 - y0)

    o = ['<svg viewBox="0 0 %.0f %.0f" role="img" aria-label="'
         'ヘモグロビンの酸素結合曲線">' % (VB_W, VB_H)]
    o.append('<defs><linearGradient id="%s-g" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0%%" stop-color="#B0361B" stop-opacity=".16"/>'
             '<stop offset="100%%" stop-color="#B0361B" stop-opacity=".03"/>'
             '</linearGradient></defs>' % P)

    # 目盛りの線
    for s in (0.0, .25, .5, .75, 1.0):
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                 'stroke="rgba(122,96,52,.16)" stroke-width="1"/>'
                 % (x0, sy(s), x1, sy(s)))
        o.append('<text x="%.1f" y="%.1f" font-size="15.5" fill="#7A6E5C" '
                 'text-anchor="end">%d%%</text>' % (x0 - 9, sy(s) + 4, s * 100))

    def path(f):
        pts = [(sx(PMAX * i / 400.0), sy(f(PMAX * i / 400.0)))
               for i in range(401)]
        return 'M%.1f %.1f ' % pts[0] + ' '.join('L%.1f %.1f' % p
                                                 for p in pts[1:])

    # 協同性が無い場合（比較用）
    o.append('<g class="%s-hit" data-detail="%s">' % (P, efig.attr(DET['flat'])))
    o.append('<path d="%s" fill="none" stroke="#8C8271" stroke-width="2.2" '
             'stroke-dasharray="7 5"/>' % path(simple))
    o.append('<text x="%.1f" y="%.1f" font-size="16.5" font-weight="700" '
             'fill="#6E6558" text-anchor="start" paint-order="stroke" '
             'stroke="#FDFAF3" stroke-width="4">協同性が無かったら</text>'
             % (sx(60), sy(simple(60)) + 22))
    o.append('</g>')

    # 本物のヘモグロビン
    o.append('<path d="%s L%.1f %.1f L%.1f %.1f Z" fill="url(#%s-g)"/>'
             % (path(sev), x1, y1, x0, y1, P))
    o.append('<path d="%s" fill="none" stroke="#B0361B" stroke-width="3" '
             'stroke-linejoin="round"/>' % path(sev))
    o.append('<text x="%.1f" y="%.1f" font-size="18" font-weight="800" '
             'fill="#8A2A12" text-anchor="start" paint-order="stroke" '
             'stroke="#FDFAF3" stroke-width="4">ヘモグロビン（S字）</text>'
             % (sx(56), sy(sev(56)) - 16))

    # 3 つの場所
    for po2, name, note in MARK:
        key = {100.0: 'lung', 40.0: 'rest', 20.0: 'work'}[po2]
        s = sev(po2)
        o.append('<g class="%s-hit" data-detail="%s">'
                 % (P, efig.attr(DET[key])))
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                 'stroke="rgba(176,54,27,.5)" stroke-width="1.3" '
                 'stroke-dasharray="4 3"/>' % (sx(po2), sy(s), sx(po2), y1))
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                 'stroke="rgba(176,54,27,.5)" stroke-width="1.3" '
                 'stroke-dasharray="4 3"/>' % (x0, sy(s), sx(po2), sy(s)))
        o.append('<circle cx="%.1f" cy="%.1f" r="8" fill="#B0361B" '
                 'stroke="#FDFAF3" stroke-width="2.2"/>' % (sx(po2), sy(s)))
        dy = -18 if po2 != 100.0 else -18
        o.append('<text x="%.1f" y="%.1f" font-size="16.5" font-weight="800" '
                 'fill="#8A2A12" text-anchor="%s" paint-order="stroke" '
                 'stroke="#FDFAF3" stroke-width="4">%s %.1f%%</text>'
                 % (sx(po2) + (-12 if po2 == 100.0 else 12), sy(s) + dy,
                    'end' if po2 == 100.0 else 'start', name, s * 100))
        o.append('</g>')

    # 軸
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
             'stroke="rgba(122,96,52,.45)" stroke-width="1.3"/>'
             % (x0, y1, x1, y1))
    for po2 in (0, 20, 40, 60, 80, 100):
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                 'stroke="rgba(122,96,52,.45)" stroke-width="1.2"/>'
                 % (sx(po2), y1, sx(po2), y1 + 5))
        o.append('<text x="%.1f" y="%.1f" font-size="15.5" fill="#7A6E5C" '
                 'text-anchor="middle">%d</text>' % (sx(po2), y1 + 21, po2))
    o.append('<text x="%.1f" y="%.1f" font-size="17" fill="#7A6E5C" '
             'text-anchor="middle">まわりの酸素の濃さ（酸素分圧 mmHg）</text>'
             % ((x0 + x1) / 2.0, y1 + 44))
    o.append('<text x="%.1f" y="%.1f" font-size="17" fill="#7A6E5C" '
             'text-anchor="middle" transform="rotate(-90 %.1f %.1f)">'
             'ヘモグロビンが酸素を持っている割合</text>'
             % (x0 - 58, (y0 + y1) / 2.0, x0 - 58, (y0 + y1) / 2.0))
    o.append('</svg>')
    return ''.join(o)


def table():
    o = ['<div class="%s-tw"><table class="%s-tab">' % (P, P),
         '<thead><tr><th>場所</th><th>酸素の濃さ</th>'
         '<th>ヘモグロビン（S字）</th><th>協同性が無かったら</th></tr>'
         '</thead><tbody>']
    for po2, name, _n in MARK:
        key = 'is-key' if po2 == 20.0 else ''
        o.append('<tr class="%s"><td>%s</td><td>%d mmHg</td>'
                 '<td>%.1f%%</td><td>%.1f%%</td></tr>'
                 % (key, name, po2, sev(po2) * 100, simple(po2) * 100))
    d1 = (sev(100.0) - sev(20.0)) * 100
    d2 = (simple(100.0) - simple(20.0)) * 100
    o.append('<tr class="is-key"><td>肺 → 運動中の筋肉で<b>渡せる量</b></td>'
             '<td>—</td><td>%.1f ポイント</td><td>%.1f ポイント</td></tr>'
             % (d1, d2))
    o.append('</tbody></table></div>')
    return ''.join(o)


# ---------------------------------------------------------------- 検算

def check():
    print('Severinghaus (1979) の式の検算:')
    for po2, want in ((26.6, 49.4), (40.0, 75.0), (100.0, 97.7)):
        got = sev(po2) * 100
        print('  PO₂ %5.1f mmHg -> %.2f%%（教科書値 %.1f%%）' % (po2, got, want))
        assert abs(got - want) < 0.4, 'Severinghaus の式が合わない'
    print('比較用の単純な曲線（同じ P50 = %.1f）:' % P50)
    for po2 in (20.0, 40.0, 100.0):
        print('  PO₂ %5.1f mmHg -> %.2f%%' % (po2, simple(po2) * 100))
    d1 = (sev(100.0) - sev(20.0)) * 100
    d2 = (simple(100.0) - simple(20.0)) * 100
    print('肺→運動中の筋肉で渡せる量: S字 %.1f ／ 単純 %.1f （%.2f 倍）'
          % (d1, d2, d1 / d2))
    assert d1 > d2 * 1.7, 'S字の利点が出ていない'
    # 半分の点で両者が交わっていること（同じ P50 で比べている証拠）
    assert abs(simple(P50) - 0.5) < 1e-9


def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, 'なぜ、S字でなければならなかったのか',
                        'ヘモグロビンがどれだけ酸素を持っているかを、'
                        'まわりの酸素の濃さに対して描いたものです。'
                        '赤い丸や点線の曲線にカーソルを合わせる'
                        '（スマホはタップ）と、その意味が下に出ます。'),
         '<div class="%s-stage">%s</div>' % (P, stage())]

    o.append(table())
    o.append('<p class="%s-cap">同じ「半分の点」を通しているのに、'
             '<b>渡せる量が倍近く違います</b>。'
             'S字の平らな天井のおかげで肺ではめいっぱい積め、'
             'S字の急な坂のおかげで'
             '<b>酸素が足りない場所ほど、一気に手放せる</b>。'
             '必要としている場所に、必要な量だけ届く仕組みです。</p>' % P)

    o.append(efig.close_card(
        P,
        'ヘモグロビンには酸素をつかむ場所が<b>4つ</b>あります。'
        'そして1つ目がつかまると、残りの3つが<b>つかまえやすく変化</b>する。'
        '逆に1つ手放すと、残りも手放しやすくなる。'
        'この「仲間につられる」性質（協同性）が、結合の曲線をS字にしました。'
        '<b>酸素の多いところでは貪欲に、少ないところでは気前よく。</b>'
        'もし協同性が無かったら、'
        '運動中の筋肉に届けられる酸素は<b>半分ほど</b>になっていたはずです。',
        '曲線は空想ではなく、公表されている式をそのまま描いたものです。'
        '<b>Severinghaus, J. W. (1979)</b> '
        '"Simple, accurate equations for human blood O₂ dissociation '
        'computations" <i>J. Appl. Physiol.</i> 46, 599–602 の式 '
        'S ＝ 1 ÷ ( 23400 ÷ (PO₂³ ＋ 150·PO₂) ＋ 1 )。'
        'この式に 40 mmHg を入れると 75.0% が出ます——'
        '教科書にある「静脈血の酸素飽和度は約75%」がそのまま再現されます。'
        '比較用の点線は、協同性が無い場合（S ＝ PO₂ ÷ (PO₂ ＋ P50)）を'
        '同じ P50（26.6 mmHg）で描いたものです。'
        '酸素分圧の値（肺 約100・安静時の組織 約40・'
        '運動中の筋肉 20 前後）は生理学の標準的な目安で、'
        '個人や状態によって動きます。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    check()
    efig.save('_fig5_hemoglobin.qmd', build())
