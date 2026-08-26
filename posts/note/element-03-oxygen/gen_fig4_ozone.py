# -*- coding: utf-8 -*-
"""
元素 #3 酸素 / 図4 : 毒が、盾になった。オゾン層と紫外線。

#2 の図5（地球の赤外線に CO2 の吸収帯が重なる）と<同じ作り>にする。
あちらは赤外線、こちらは紫外線。連載として意図的に韻を踏ませる。

落としどころ:
  DNA がいちばん強く壊されるのは 260 nm。
  オゾンがいちばん強く吸うのは 255 nm。
  この 2 つがほとんど重なっている。

透過率は模式ではなく<計算>する。
  オゾンのハートレー帯の実測パラメータ:
    ピーク 1.17e-17 cm^2 / 中心 約 255 nm / 半値全幅 約 40 nm
  オゾン全量 300 DU（世界平均）、1 DU = 2.687e16 分子/cm^2
    -> 柱密度 N = 8.061e18 分子/cm^2
  ベール・ランベルト則  透過率 T = exp(-sigma * N)

この計算だけで、
  260 nm  T = 1e-39 台（完全にゼロ）
  290 nm  T = 1e-5 台
  300 nm  T = 6%
  310 nm  T = 61%
  320 nm  T = 94%
となり、実際の「地上の紫外線は 290〜300 nm あたりで切れる」が再現される。

正直に書くこと:
  ・ハートレー帯はガウス形そのものではない（長波長側にハギンズ帯の構造がある）。
    ここでは実測の中心・高さ・幅に合わせたなめらかな曲線で近似している。
  ・そのうえで計算した切れ位置が実際とよく合う、という書き方にする。
  ・DNA については山の位置（260 nm）だけが確かなので、曲線は描かず印だけ置く。

出典:
  ハートレー帯: ピーク 1.17e-17 cm^2、中心 約255 nm、半値全幅 約40 nm
  DNA の吸収極大: 260 nm
  オゾン全量: 世界平均 約 300 DU、1 DU = 2.687e16 分子/cm^2（NOAA / NASA）

出力: _fig4_ozone.qmd
"""
import math
import efig

P, CID = 'oozone', 'oozone1'

SIG_PEAK = 1.17e-17     # ハートレー帯のピーク（cm²/分子）
SIG_C = 255.0           # 中心（nm）
SIG_FWHM = 40.0         # 半値全幅（nm）
DU = 2.687e16           # 1 DU あたりの分子数（cm⁻²）
COLUMN = 300.0          # オゾン全量（DU、世界平均）
N_O3 = COLUMN * DU      # 柱密度（分子/cm²）

DNA_PEAK = 260.0        # DNA の吸収極大（nm）
LAM0, LAM1 = 200.0, 400.0
T_FLOOR = 1e-15         # 縦軸の下限。これより下は「振り切れ」と書く

# 紫外線の区分（nm）
BANDS = [('UV-C', 200.0, 280.0, '#8E5AA8'),
         ('UV-B', 280.0, 315.0, '#5A72B8'),
         ('UV-A', 315.0, 400.0, '#4E93A8')]


def sigma(lam):
    """オゾンの吸収断面積（cm²/分子）。実測の中心・高さ・幅に合わせた曲線。"""
    g = 4.0 * math.log(2.0) * (lam - SIG_C) ** 2 / SIG_FWHM ** 2
    return SIG_PEAK * math.exp(-g)


def trans(lam):
    """ベール・ランベルト則。オゾン層を抜けて地上に届く割合。"""
    t = sigma(lam) * N_O3
    return math.exp(-t) if t < 700 else 0.0


VB_W, VB_H = 900.0, 520.0
TOP = (78.0, 40.0, 858.0, 196.0)        # 上の図（吸う強さ）
BOT = (78.0, 258.0, 858.0, 434.0)       # 下の図（届く割合）

CSS = """
.@@P@@-stage{margin:18px 0 2px;}
.@@P@@-stage svg{display:block;width:100%;height:auto;}
.@@P@@-hit{cursor:default;}

.@@P@@-tw{margin:18px 8px 0;overflow-x:auto;}
.@@P@@-tab{width:100%;border-collapse:collapse;font-size:.87rem;min-width:430px;}
.@@P@@-tab th,.@@P@@-tab td{padding:9px 10px;text-align:center;
  border-bottom:1px solid var(--line2);font-variant-numeric:tabular-nums;}
.@@P@@-tab th{font-size:.78rem;font-weight:700;color:var(--faint);
  border-bottom:1.5px solid rgba(122,96,52,.3);}
.@@P@@-tab td:first-child,.@@P@@-tab th:first-child{text-align:left;
  white-space:nowrap;}
.@@P@@-tab tr.is-key td{background:rgba(142,90,168,.13);font-weight:700;}
.@@P@@-cap{margin:13px 8px 0;font-size:.84rem;color:var(--dim);
  line-height:1.75;}

@media (max-width:820px){
  .@@P@@-tw{margin:14px 2px 0;}
  .@@P@@-cap{font-size:.78rem;margin:11px 2px 0;}
}
""".replace('@@P@@', P)

DET = {
    'o3': '<b>オゾン（O₃）が紫外線を吸う強さ</b>です。'
          '山の頂上は <b>255 nm</b>。'
          'オゾンは紫外線を受けると<b>いったんバラバラに壊れ</b>、'
          'また組み直されます。'
          'この壊れて直るのを繰り返すことで、'
          '紫外線のエネルギーを吸い取り続けているのです。'
          'オゾン自体は減りません。',
    'dna': '<b>DNA がいちばん強く光を吸う波長が 260 nm</b>です。'
           '吸うということは、<b>エネルギーを受け取って壊れる</b>ということ。'
           'そして——オゾンの山の頂上は 255 nm。'
           '<b>ほとんど重なっています</b>。'
           'DNA を壊す波長を、オゾンがちょうど吸ってくれている。',
    'trans': '<b>地上に届く割合</b>です。縦軸は1目盛りごとに1000分の1になります。'
             '290 nm より短い紫外線は <b>10万分の1以下</b>しか通りません。'
             '260 nm では図の下限を振り切って<b>ほぼ完全にゼロ</b>です。'
             'この計算は、オゾンの吸収の実測値と'
             'オゾン全量（300 DU）から出したものです。',
}


# ---------------------------------------------------------------- 描画

def stage():
    def sx(lam, box):
        x0, _y0, x1, _y1 = box
        return x0 + (lam - LAM0) / (LAM1 - LAM0) * (x1 - x0)

    o = ['<svg viewBox="0 0 %.0f %.0f" role="img" aria-label="'
         'オゾンが紫外線を吸う強さと、地上に届く割合">' % (VB_W, VB_H)]
    o.append('<defs><linearGradient id="%s-g" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0%%" stop-color="#8E5AA8" stop-opacity=".42"/>'
             '<stop offset="100%%" stop-color="#8E5AA8" stop-opacity=".06"/>'
             '</linearGradient></defs>' % P)

    # 紫外線の区分の帯（上下の図をまたいで通す）
    for name, a, b, col in BANDS:
        x = sx(a, TOP)
        w = sx(b, TOP) - x
        o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" '
                 'fill="%s" opacity=".055"/>'
                 % (x, TOP[1] - 22, w, BOT[3] - TOP[1] + 22, col))
        o.append('<text x="%.1f" y="%.1f" font-size="13" font-weight="700" '
                 'fill="%s" text-anchor="middle">%s</text>'
                 % (x + w / 2.0, TOP[1] - 8, col, name))

    # ---- 上：吸う強さ
    x0, y0, x1, y1 = TOP
    pts = [(sx(LAM0 + (LAM1 - LAM0) * i / 500.0, TOP),
            y1 - sigma(LAM0 + (LAM1 - LAM0) * i / 500.0) / SIG_PEAK * (y1 - y0))
           for i in range(501)]
    path = 'M%.1f %.1f ' % pts[0] + ' '.join('L%.1f %.1f' % p for p in pts[1:])
    o.append('<g class="%s-hit" data-detail="%s">' % (P, efig.attr(DET['o3'])))
    o.append('<path d="%s L%.1f %.1f L%.1f %.1f Z" fill="url(#%s-g)"/>'
             % (path, x1, y1, x0, y1, P))
    o.append('<path d="%s" fill="none" stroke="#6B3D85" stroke-width="2.6"/>'
             % path)
    o.append('</g>')
    o.append('<text x="%.1f" y="%.1f" font-size="14" font-weight="800" '
             'fill="#5C3272" text-anchor="middle" paint-order="stroke" '
             'stroke="#FDFAF3" stroke-width="4">オゾンが吸う（山の頂上 255 nm）'
             '</text>' % (sx(SIG_C, TOP), y0 - 4))
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
             'stroke="rgba(122,96,52,.45)" stroke-width="1.2"/>'
             % (x0, y1, x1, y1))
    o.append('<text x="%.1f" y="%.1f" font-size="12.5" fill="#7A6E5C" '
             'text-anchor="end">吸う強さ</text>' % (x0 - 8, (y0 + y1) / 2.0))

    # DNA の印（上下を貫く）
    dx = sx(DNA_PEAK, TOP)
    o.append('<g class="%s-hit" data-detail="%s">' % (P, efig.attr(DET['dna'])))
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#B02A37" '
             'stroke-width="2" stroke-dasharray="6 4"/>'
             % (dx, y0 - 2, dx, BOT[3]))
    o.append('<text x="%.1f" y="%.1f" font-size="14" font-weight="800" '
             'fill="#B02A37" text-anchor="start" paint-order="stroke" '
             'stroke="#FDFAF3" stroke-width="4">DNA が壊れる 260 nm</text>'
             % (dx + 9, y0 + 22))
    o.append('</g>')

    # ---- 下：届く割合（縦は対数）
    x0, y0, x1, y1 = BOT
    lo = math.log10(T_FLOOR)

    def sy(t):
        v = max(t, T_FLOOR)
        return y1 - (math.log10(v) - lo) / (0.0 - lo) * (y1 - y0)

    for e in range(0, int(lo) - 1, -3):
        yy = sy(10.0 ** e)
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                 'stroke="rgba(122,96,52,.16)" stroke-width="1"/>'
                 % (x0, yy, x1, yy))
        lab = '1' if e == 0 else '10<tspan baseline-shift="super" '\
                                 'font-size="9">%d</tspan>' % e
        o.append('<text x="%.1f" y="%.1f" font-size="12" fill="#7A6E5C" '
                 'text-anchor="end">%s</text>' % (x0 - 8, yy + 4, lab))

    pts = [(sx(LAM0 + (LAM1 - LAM0) * i / 500.0, BOT),
            sy(trans(LAM0 + (LAM1 - LAM0) * i / 500.0))) for i in range(501)]
    path = 'M%.1f %.1f ' % pts[0] + ' '.join('L%.1f %.1f' % p for p in pts[1:])
    o.append('<g class="%s-hit" data-detail="%s">' % (P, efig.attr(DET['trans'])))
    o.append('<path d="%s" fill="none" stroke="#1F6B4A" stroke-width="2.8"/>'
             % path)
    o.append('</g>')
    o.append('<text x="%.1f" y="%.1f" font-size="14" font-weight="800" '
             'fill="#16523A" text-anchor="start" paint-order="stroke" '
             'stroke="#FDFAF3" stroke-width="4">地上に届く割合</text>'
             % (sx(336, BOT), sy(trans(336)) - 14))
    o.append('<text x="%.1f" y="%.1f" font-size="13" font-weight="700" '
             'fill="#16523A" text-anchor="middle" paint-order="stroke" '
             'stroke="#FDFAF3" stroke-width="4">ここで切れる</text>'
             % (sx(299, BOT), sy(trans(299)) - 12))

    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
             'stroke="rgba(122,96,52,.45)" stroke-width="1.3"/>'
             % (x0, y1, x1, y1))
    for lam in range(200, 401, 25):
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                 'stroke="rgba(122,96,52,.45)" stroke-width="1.2"/>'
                 % (sx(lam, BOT), y1, sx(lam, BOT), y1 + 5))
        o.append('<text x="%.1f" y="%.1f" font-size="12.5" fill="#7A6E5C" '
                 'text-anchor="middle">%d</text>' % (sx(lam, BOT), y1 + 21, lam))
    o.append('<text x="%.1f" y="%.1f" font-size="13" fill="#7A6E5C" '
             'text-anchor="middle">紫外線の波長（nm）</text>'
             % ((x0 + x1) / 2.0, y1 + 44))
    o.append('<text x="%.1f" y="%.1f" font-size="12.5" fill="#7A6E5C" '
             'text-anchor="end">届く割合</text>' % (x0 - 8, y0 - 6))
    o.append('</svg>')
    return ''.join(o)


def table():
    o = ['<div class="%s-tw"><table class="%s-tab">' % (P, P),
         '<thead><tr><th>波長</th><th>オゾンが吸う強さ</th>'
         '<th>地上に届く割合</th><th></th></tr></thead><tbody>']
    rows = [(260, 'DNA が壊れる波長'), (280, 'UV-C の端'),
            (290, ''), (300, ''), (310, ''), (320, ''), (350, 'UV-A')]
    for lam, note in rows:
        t = trans(float(lam))
        ts = ('%.0f%%' % (t * 100)) if t > 0.005 else (
            '10<sup>%d</sup> 以下' % math.floor(math.log10(t))
            if t > 0 else 'ほぼゼロ')
        o.append('<tr class="%s"><td>%d nm</td><td>%.0f%%</td>'
                 '<td>%s</td><td>%s</td></tr>'
                 % ('is-key' if lam == 260 else '', lam,
                    sigma(float(lam)) / SIG_PEAK * 100, ts, note))
    o.append('</tbody></table></div>')
    return ''.join(o)


# ---------------------------------------------------------------- 検算

def check():
    print('オゾンの柱密度 %.3e 分子/cm²（%.0f DU × %.3e）' % (N_O3, COLUMN, DU))
    print('計算した透過率:')
    for lam in (255, 260, 280, 290, 300, 305, 310, 320, 350):
        t = trans(float(lam))
        print('  %3d nm  σ=%.3e cm²  τ=%8.2f  届く割合 %s'
              % (lam, sigma(float(lam)), sigma(float(lam)) * N_O3,
                 ('%.3f%%' % (t * 100)) if t > 1e-6 else '%.1e' % t))
    # 実際の「地上の紫外線は 290〜300 nm あたりで切れる」を再現できているか
    assert trans(280.0) < 1e-10, '280 nm が通ってしまっている'
    assert trans(290.0) < 1e-4, '290 nm が通りすぎ'
    assert 0.01 < trans(300.0) < 0.20, '300 nm の透過が実際とずれている'
    assert trans(320.0) > 0.85, '320 nm が通らなすぎ'
    print('  -> 実際の切れ位置（290〜300 nm）を再現できている')
    # オゾンの山と DNA の山が重なっていること
    print('オゾンの山 %.0f nm ／ DNA の山 %.0f nm ／ ずれ %.0f nm'
          % (SIG_C, DNA_PEAK, abs(SIG_C - DNA_PEAK)))
    assert abs(SIG_C - DNA_PEAK) < 10.0
    print('  DNA の波長でオゾンが吸う強さは、山の頂上の %.1f%%'
          % (sigma(DNA_PEAK) / SIG_PEAK * 100))


def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, '毒が、盾になった',
                        '上がオゾンの吸う強さ、下が地上に届く割合です。'
                        '曲線にカーソルを合わせる（スマホはタップ）と、'
                        'その意味が下に出ます。'),
         '<div class="%s-stage">%s</div>' % (P, stage())]

    o.append(table())
    o.append('<p class="%s-cap">下の段の縦軸は、1目盛りごとに'
             '<b>1000分の1</b>になります。'
             '<b>290 nm より短い紫外線は、10万分の1以下しか地上に届きません。</b>'
             'そして DNA がいちばん壊されやすい 260 nm では、'
             '図の下限を振り切ってほぼ完全にゼロです。</p>' % P)

    o.append(efig.close_card(
        P,
        '植物が捨てた酸素は、そのままでは体を錆びさせる毒です。'
        'ところが空の高いところで強い紫外線が当たると、'
        '酸素原子3個が組んだ<b>オゾン（O₃）</b>に変わります。'
        'そしてオゾンがいちばん強く吸う波長は <b>255 nm</b>——'
        '<b>DNA がいちばん強く壊される 260 nm と、ほとんど重なっています</b>。'
        'この一致のおかげで、いま外に出て日を浴びても'
        '肌の中の DNA は無事でいられます。'
        '天気予報の「UV指数」も、日焼け止めの数字も、'
        'この層がどれだけ働いているかを測ったものです。'
        '<b>捨てた毒が、めぐって自分を守る盾になっている。</b>',
        '地上に届く割合は模式図ではなく計算です。'
        'オゾンの吸収（ハートレー帯）の実測値——'
        'ピーク 1.17×10⁻¹⁷ cm²、中心 約255 nm、半値全幅 約40 nm——に'
        '合わせたなめらかな曲線を使い、'
        'オゾン全量 300 DU（世界平均。1 DU ＝ 2.687×10¹⁶ 分子/cm²）を'
        '通したときの透過率をベール・ランベルト則で求めました。'
        'その結果、地上の紫外線が <b>290〜300 nm あたりで切れる</b>という'
        '実際の姿が再現されます。'
        '<b>ただし、ハートレー帯はガウス形そのものではありません</b>'
        '（長波長側にはハギンズ帯とよばれる別の構造があります）。'
        'ここでは山の位置・高さ・幅を実測に合わせた近似です。'
        'DNA については吸収極大の位置（260 nm）だけが確かなので、'
        '曲線は描かず、印だけを置いています。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    check()
    efig.save('_fig4_ozone.qmd', build())
