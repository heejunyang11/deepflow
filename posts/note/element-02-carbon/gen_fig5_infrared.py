# -*- coding: utf-8 -*-
"""
元素 #2 炭素 / 図5 : なぜ二酸化炭素だけが熱をつかまえるのか。

温室効果が起きるには、条件が 2 つそろわなければならない。
  (1) 揺れたときに電気の偏りが生まれること（対称なら生まれない）
  (2) その揺れの波長のところに、地球の出す熱が実際にあること
5 つ並べると、この 2 つが「両方そろうのは 1 つだけ」だと目で分かる。

  揺れ方            波数        波長      偏る  地球の熱  結果
  N2  伸縮          2359 cm-1   4.24 um   -      8      素通り
  CO2 逆対称伸縮     2349 cm-1   4.26 um   あり   8      つかまえる（でも熱が無い）
  O2  伸縮          1580 cm-1   6.33 um   -     54      素通り
  CO2 対称伸縮       1333 cm-1   7.50 um   -     79      素通り（熱は一番多いのに！）
  CO2 変角           667 cm-1  14.99 um   あり  72      つかまえる ← これだけ

波数（cm-1）と波長（um）の関係は 波数 = 10000 / 波長。
cm-1 を説明なしに置くと読者が置き去りになるので、必ず両方を並べて書くこと。
「1 cm のあいだに波が何個入るか」という言い換えを添える。

なぜ波長が決まるのか（本文と図の説明文で必ず触れる）:
  分子の揺れには決まったテンポがある。光にもテンポがある。
  この 2 つが合ったときだけエネルギーが移る（共鳴）。
  だから「この揺れはこの波長だけを吸う」という対応ができる。

実験値:
  N2  r 1.098 A                Huber & Herzberg (1979)
  O2  r 1.208 A                Huber & Herzberg (1979)
  CO2 r 1.162 A / 180 deg      Herzberg (1966)
  振動数 CO2 667 / 1333 / 2349 cm-1（1333 だけ赤外不活性）NIST CCCBDB
  N2 2359 cm-1 / O2 1580 cm-1  いずれも赤外不活性（等核二原子分子）

振れ幅は実物よりずっと大きく、速さもずっと遅い（実際は毎秒 10^13 回）。
変位は重心が動かないように取ってある（check() で検算）。

出力: _fig5_infrared.qmd
"""
import math
import efig
import emol

P, CID = 'eir', 'eir1'

R_N2, R_O2, R_CO = 1.098, 1.208, 1.162     # 結合長（Å）

# 原子 1 個の重さ（統一原子質量単位）。変位の検算に使う。
MASS = {'C': 12.011, 'N': 14.007, 'O': 15.999}

T_EARTH = 288.15                # 地球を 15℃ の黒体とみなす
BAND = (13.5, 17.0)             # 667 cm⁻¹ の吸収帯のおおよその広がり（μm）
LAM0, LAM1 = 0.0, 40.0          # 下の帯の横軸（μm）

# 玉はこの図だけ小さめ（共有結合半径の 0.52 倍。ほかの図は 0.72 倍）。
# 窒素は三重結合が短いうえ原子が大きいので、0.72 倍のままだと
# 静止していても棒がほとんど見えず、振れた瞬間には玉が重なってしまう。
# 回さないのは、回しながら震わせると何が起きているか読めないため。
G = emol.Group(P, scale=52.0, ball=0.52, auto_spin=False)


def um(wn):
    """波数（cm⁻¹）→ 波長（μm）。1 cm ＝ 10000 μm なので 10000 で割る。"""
    return 10000.0 / wn


# ---------------------------------------------------------------- 分子

def diatomic(elem, r, amp):
    """等核二原子分子の伸びちぢみ。左右が逆向きに動く（重心は動かない）。"""
    atoms = [((-r / 2.0, 0.0, 0.0), elem), ((r / 2.0, 0.0, 0.0), elem)]
    vib = [(-amp, 0.0, 0.0), (amp, 0.0, 0.0)]
    return atoms, [(0, 1)], vib


def _co2():
    return ([((0.0, 0.0, 0.0), 'C'),
             ((-R_CO, 0.0, 0.0), 'O'), ((R_CO, 0.0, 0.0), 'O')],
            [(0, 1), (0, 2)])


def co2_sym(amp):
    """対称伸縮。酸素が同時に外へ出て同時に戻る。炭素は動かない。"""
    at, bo = _co2()
    return at, bo, [(0.0, 0.0, 0.0), (-amp, 0.0, 0.0), (amp, 0.0, 0.0)]


def co2_asym(amp_o):
    """逆対称伸縮。酸素2個が同じ向きへ、炭素が逆へ。片方が伸び片方が縮む。"""
    amp_c = 2.0 * MASS['O'] * amp_o / MASS['C']
    at, bo = _co2()
    return at, bo, [(-amp_c, 0.0, 0.0), (amp_o, 0.0, 0.0), (amp_o, 0.0, 0.0)]


def co2_bend(amp_o):
    """変角。酸素が上へ、炭素が下へ。重心が動かないよう重さで釣り合わせる。"""
    amp_c = 2.0 * MASS['O'] * amp_o / MASS['C']
    at, bo = _co2()
    return at, bo, [(0.0, -amp_c, 0.0), (0.0, amp_o, 0.0), (0.0, amp_o, 0.0)]


def mk(key, label, spec, sec):
    atoms, bonds, vib = spec
    return G.add(emol.Mol(key, atoms, bonds, label, vib=vib, vib_sec=sec))


# (鍵, 分子式, 分子名, 揺れ方, 波数, 偏るか, 結果)
MOL = [
    ('n2', 'N₂',  '窒素',       '伸びちぢみ',   2359, False, 'pass',
     mk('n2', '窒素分子が伸びちぢみする様子',
        diatomic('N', R_N2, 0.095), 1.5)),
    ('ca', 'CO₂', '二酸化炭素', '逆向きに伸縮', 2349, True,  'weak',
     mk('ca', '二酸化炭素が逆向きに伸びちぢみする様子',
        co2_asym(0.05), 1.4)),
    ('o2', 'O₂',  '酸素',       '伸びちぢみ',   1580, False, 'pass',
     mk('o2', '酸素分子が伸びちぢみする様子',
        diatomic('O', R_O2, 0.105), 1.9)),
    ('cs', 'CO₂', '二酸化炭素', '対称に伸縮',   1333, False, 'pass',
     mk('cs', '二酸化炭素が対称に伸びちぢみする様子',
        co2_sym(0.13), 1.7)),
    ('cb', 'CO₂', '二酸化炭素', '折れ曲がる',    667, True,  'catch',
     mk('cb', '二酸化炭素が折れ曲がる様子',
        co2_bend(0.09), 2.3)),
]

VERDICT = {'pass': '素通り', 'weak': 'つかまえる', 'catch': 'つかまえる'}

DET = {
    'n2': '窒素分子は<b>同じ原子2個</b>。伸びても縮んでも左右が同じままなので、'
          '電気の偏りが<b>生まれません</b>。赤外線は偏りを揺さぶって初めて'
          '吸われるので、窒素は熱を<b>素通り</b>させます。'
          'しかもこの揺れのテンポは <b>2359 cm⁻¹＝4.24 μm</b>。'
          'そこは地球がほとんど熱を出していない場所です。'
          '<b>二重の意味で、関係がありません。</b>',
    'ca': 'これは二酸化炭素の別の揺れ方です。酸素2個が同じ向きへ、'
          '炭素が逆へ動くので、<b>片方の結合が伸びて片方が縮みます</b>。'
          '左右の対称が崩れるので<b>電気の偏りが生まれ、赤外線を吸えます</b>。'
          'ところがテンポが <b>2349 cm⁻¹＝4.26 μm</b>。'
          '<b>そこには地球の熱がほとんどありません</b>'
          '（山の頂上の 8% ほど）。'
          '吸う力はあるのに、吸うものが来ない——温室効果にはほぼ効きません。',
    'o2': '酸素も<b>同じ原子2個</b>なので、理由は窒素とまったく同じです。'
          '左右対称のまま揺れるので、偏りが生まれず<b>素通り</b>。'
          'ただし波長は <b>1580 cm⁻¹＝6.33 μm</b> で、'
          'ここには地球の熱がそこそこあります（頂上の 54%）。'
          '<b>熱はあるのに、吸う仕組みが無い。</b>'
          '窒素と酸素で空気の 99%。空気のほぼ全部が、熱に対して透明です。',
    'cs': 'これも二酸化炭素です。2つの酸素が<b>同時に外へ出て、同時に戻る</b>。'
          'このとき左右の引っぱりが打ち消し合い、<b>偏りが生まれません</b>。'
          '波長は <b>1333 cm⁻¹＝7.50 μm</b>——'
          '<b>地球の熱がいちばん豊富にある帯（頂上の 79%）</b>です。'
          'それでも吸いません。'
          '大事なのは分子の名前ではなく、'
          '<b>揺れ方が左右対称かどうか</b>だけだと分かります。',
    'cb': 'そして、この揺れ方。酸素2個が上へ、炭素が下へ動いて'
          '<b>「く」の字に折れます</b>。折れた瞬間に左右の対称が崩れ、'
          '<b>電気の偏りが生まれる</b>。'
          '波長は <b>667 cm⁻¹＝14.99 μm</b>。'
          'そして地球はここで、頂上の 72% にあたる強さで熱を出しています。'
          '<b>「偏りが生まれる」と「そこに熱がある」が、両方そろう唯一の揺れ</b>。'
          'これが温室効果の正体です。',
}

CSS = """
.@@P@@-row{display:grid;
  grid-template-columns:repeat(auto-fit,minmax(128px,1fr));
  gap:9px;margin:18px 0 6px;}

.@@P@@-cell{display:flex;flex-direction:column;align-items:center;gap:1px;
  padding:11px 4px 13px;border-radius:14px;cursor:default;
  background:rgba(122,96,52,.035);
  border:1px solid rgba(122,96,52,.13);
  transition:background .18s ease,border-color .18s ease,transform .18s ease;}
.@@P@@-cell:hover{transform:translateY(-3px);}
.@@P@@-cell.is-catch{background:rgba(190,100,10,.08);
  border-color:rgba(190,100,10,.45);}
.@@P@@-cell svg{display:block;width:100%;height:auto;
  -webkit-user-select:none;user-select:none;}

.@@P@@-f{font-size:1.1rem;font-weight:800;color:var(--ink);margin-top:3px;}
.@@P@@-nm{font-size:.74rem;color:var(--faint);}
.@@P@@-wn{font-size:.78rem;font-weight:700;color:var(--dim);
  font-variant-numeric:tabular-nums;margin-top:3px;line-height:1.4;
  text-align:center;}
.@@P@@-wn em{font-style:normal;display:block;font-weight:800;color:var(--ink);}
.@@P@@-v{font-size:.86rem;font-weight:800;margin-top:6px;
  padding:3px 10px;border-radius:999px;white-space:nowrap;}
.@@P@@-v.is-pass{color:var(--dim);background:rgba(122,96,52,.1);}
.@@P@@-v.is-weak{color:#8A5A12;background:rgba(190,100,10,.16);}
.@@P@@-v.is-catch{color:#FFFDF9;background:var(--hb);}

/* 波数と波長の対応。ここを外すと cm⁻¹ が読者に届かない */
.@@P@@-unit{margin:16px 8px 0;padding:13px 16px;border-radius:11px;
  background:var(--panel);border:1px solid var(--line2);
  font-size:.9rem;line-height:1.85;color:var(--ink);}
.@@P@@-unit b{color:var(--hb);}
.@@P@@-unit code{font-family:ui-monospace,Menlo,Consolas,monospace;
  font-size:.94em;background:rgba(122,96,52,.09);padding:1px 6px;
  border-radius:5px;color:var(--ink);}

.@@P@@-spec{margin:22px 8px 0;}
.@@P@@-spec svg{display:block;width:100%;height:auto;}

/* まとめの表。2つの条件が両方そろうのは1行だけ、と目で分かるように */
.@@P@@-tw{margin:18px 8px 0;overflow-x:auto;}
.@@P@@-tab{width:100%;border-collapse:collapse;font-size:.86rem;
  min-width:520px;}
.@@P@@-tab th,.@@P@@-tab td{padding:8px 9px;text-align:center;
  border-bottom:1px solid var(--line2);font-variant-numeric:tabular-nums;}
.@@P@@-tab th{font-size:.78rem;font-weight:700;color:var(--faint);
  border-bottom:1.5px solid rgba(122,96,52,.3);}
.@@P@@-tab td:first-child,.@@P@@-tab th:first-child{text-align:left;
  white-space:nowrap;}
.@@P@@-tab tr.is-catch td{background:rgba(190,100,10,.09);font-weight:700;}
.@@P@@-tab tr.is-catch td:first-child{color:var(--hb);}
.@@P@@-yes{color:var(--hb);font-weight:800;}
.@@P@@-no{color:var(--faint);}
.@@P@@-heat{display:flex;align-items:center;gap:6px;justify-content:center;}
.@@P@@-heat u{display:block;height:8px;border-radius:4px;
  background:linear-gradient(90deg,#D8874A,#B0561F);text-decoration:none;}

.@@P@@-cap{margin:13px 8px 0;font-size:.84rem;color:var(--dim);
  line-height:1.75;}
.@@P@@-defs{position:absolute;width:0;height:0;overflow:hidden;}

@media (max-width:820px){
  .@@P@@-row{grid-template-columns:repeat(auto-fit,minmax(108px,1fr));
    gap:6px;margin:14px 0 4px;}
  .@@P@@-cell{padding:8px 2px 10px;border-radius:11px;}
  .@@P@@-f{font-size:.92rem;}
  .@@P@@-nm{font-size:.64rem;}
  .@@P@@-wn{font-size:.68rem;}
  .@@P@@-v{font-size:.74rem;padding:2px 7px;}
  .@@P@@-unit{margin:13px 2px 0;padding:11px 12px;font-size:.8rem;}
  .@@P@@-spec,.@@P@@-tw{margin:16px 2px 0;}
  .@@P@@-cap{font-size:.78rem;margin:11px 2px 0;}
}
""".replace('@@P@@', P)


# ---------------------------------------------------------------- 黒体

def planck(lam_um, T):
    """波長 lam_um（μm）における黒体の分光放射輝度（単位は任意）。

    短い波長では指数が跳ね上がって計算が壊れる。物理的にはそこでの
    放射はゼロと言ってよいので、あふれる手前で 0 を返す。
    """
    if lam_um <= 1e-6:
        return 0.0
    h, c, k = 6.62607015e-34, 2.99792458e8, 1.380649e-23
    lam = lam_um * 1e-6
    x = h * c / (lam * k * T)
    if x > 700.0:                      # exp(700) で倍精度の限界
        return 0.0
    return (2 * h * c ** 2 / lam ** 5) / (math.exp(x) - 1.0)


def wien(T):
    """ピークの波長（μm）。"""
    return 2897.771955 / T


def heat(wn):
    """その波長に地球の熱がどれだけあるか。山の頂上を 100 とした高さ。"""
    return planck(um(wn), T_EARTH) / planck(wien(T_EARTH), T_EARTH) * 100.0


def band_share(a, b, T, n=4000):
    """波長 a〜b に入るエネルギーが全体に占める割合。台形則で数値積分する。"""
    def integ(x0, x1):
        s = 0.0
        d = (x1 - x0) / n
        for i in range(n):
            s += (planck(x0 + i * d, T) + planck(x0 + (i + 1) * d, T)) * d / 2.0
        return s
    return integ(a, b) / integ(0.5, 200.0)


SPEC_W, SPEC_H = 900.0, 262.0
PLOT = (58.0, 56.0, 872.0, 196.0)          # 左上と右下


def spectrum():
    """地球が出す赤外線の分布に、5つの揺れの波長を打ちこんだ図。

    上の軸に波数（cm⁻¹）、下の軸に波長（μm）を置く。
    同じ目盛りの上に両方を並べることで、
    「波数が大きい＝波長が短い」という逆数の関係がそのまま見える。
    """
    x0, y0, x1, y1 = PLOT
    peak = planck(wien(T_EARTH), T_EARTH)

    def sx(l):
        return x0 + (l - LAM0) / (LAM1 - LAM0) * (x1 - x0)

    def sy(v):
        return y1 - v / peak * (y1 - y0)

    pts = [(sx(LAM0 + (LAM1 - LAM0) * i / 600.0),
            sy(planck(LAM0 + (LAM1 - LAM0) * i / 600.0, T_EARTH)))
           for i in range(601)]
    curve = 'M%.1f %.1f ' % pts[0] + ' '.join('L%.1f %.1f' % p for p in pts[1:])

    o = ['<svg viewBox="0 0 %.0f %.0f" role="img" '
         'aria-label="地球が出す赤外線の分布と、5つの揺れの波長">'
         % (SPEC_W, SPEC_H)]
    o.append('<defs><linearGradient id="%s-sky" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0%%" stop-color="#D8874A" stop-opacity=".5"/>'
             '<stop offset="100%%" stop-color="#D8874A" stop-opacity=".1"/>'
             '</linearGradient></defs>' % P)

    # 二酸化炭素が吸う帯
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" '
             'fill="rgba(190,100,10,.18)" stroke="rgba(190,100,10,.5)" '
             'stroke-width="1"/>'
             % (sx(BAND[0]), y0, sx(BAND[1]) - sx(BAND[0]), y1 - y0))

    o.append('<path d="%s L%.1f %.1f L%.1f %.1f Z" fill="url(#%s-sky)"/>'
             % (curve, x1, y1, x0, y1, P))
    o.append('<path d="%s" fill="none" stroke="#B0561F" stroke-width="2.4" '
             'stroke-linejoin="round"/>' % curve)

    # 上の軸：波数
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
             'stroke="rgba(122,96,52,.4)" stroke-width="1.2"/>'
             % (x0, y0 - 22, x1, y0 - 22))
    for wn in (2500, 2000, 1500, 1000, 750, 500, 400, 300):
        lx = sx(um(wn))
        if lx < x0 or lx > x1:
            continue
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                 'stroke="rgba(122,96,52,.4)" stroke-width="1.2"/>'
                 % (lx, y0 - 22, lx, y0 - 17))
        o.append('<text x="%.1f" y="%.1f" font-size="12.5" fill="#7A6E5C" '
                 'text-anchor="middle">%d</text>' % (lx, y0 - 27, wn))
    o.append('<text x="%.1f" y="%.1f" font-size="12.5" fill="#7A6E5C" '
             'text-anchor="start">波数（cm⁻¹）</text>' % (x0 - 48, y0 - 27))

    # 揺れの位置を曲線の上に打つ
    for key, formula, _n, mode, wn, dip, verdict, _m in MOL:
        lx, ly = sx(um(wn)), sy(planck(um(wn), T_EARTH))
        col = '#BE640A' if dip else '#7A6E5C'
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                 'stroke="%s" stroke-width="1.4" stroke-dasharray="3 3" '
                 'opacity=".85"/>' % (lx, ly, lx, y1, col))
        o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" '
                 'stroke="#FDFAF3" stroke-width="1.8"/>'
                 % (lx, ly, 7.5 if verdict == 'catch' else 5.5, col))

    # 変角だけは名前を添える。ここが答えなので
    cb = [m for m in MOL if m[0] == 'cb'][0]
    lx, ly = sx(um(cb[4])), sy(planck(um(cb[4]), T_EARTH))
    o.append('<text x="%.1f" y="%.1f" font-size="15" font-weight="800" '
             'fill="#8A4A08" text-anchor="middle" paint-order="stroke" '
             'stroke="#FDFAF3" stroke-width="4">CO₂ の「く」の字</text>'
             % (lx, ly - 30))
    o.append('<text x="%.1f" y="%.1f" font-size="13" font-weight="700" '
             'fill="#8A4A08" text-anchor="middle" paint-order="stroke" '
             'stroke="#FDFAF3" stroke-width="4">667 cm⁻¹ ＝ 15.0 μm</text>'
             % (lx, ly - 12))

    lp = wien(T_EARTH)
    o.append('<text x="%.1f" y="%.1f" font-size="13" fill="#8A3E14" '
             'text-anchor="middle" paint-order="stroke" stroke="#FDFAF3" '
             'stroke-width="4">地球の熱の山（頂上 %.1f μm）</text>'
             % (sx(lp), sy(planck(lp, T_EARTH)) - 12, lp))

    # 下の軸：波長
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
             'stroke="rgba(122,96,52,.45)" stroke-width="1.2"/>'
             % (x0, y1, x1, y1))
    for lam in (0, 5, 10, 15, 20, 25, 30, 35, 40):
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                 'stroke="rgba(122,96,52,.45)" stroke-width="1.2"/>'
                 % (sx(lam), y1, sx(lam), y1 + 5))
        o.append('<text x="%.1f" y="%.1f" font-size="12.5" fill="#7A6E5C" '
                 'text-anchor="middle">%d</text>' % (sx(lam), y1 + 21, lam))
    o.append('<text x="%.1f" y="%.1f" font-size="12.5" fill="#7A6E5C" '
             'text-anchor="start">波長（μm）</text>' % (x0 - 48, y1 + 21))
    o.append('<text x="%.1f" y="%.1f" font-size="12.5" fill="#7A6E5C" '
             'text-anchor="middle" transform="rotate(-90 %.1f %.1f)">'
             '出す強さ</text>' % (x0 - 30, (y0 + y1) / 2.0,
                                 x0 - 30, (y0 + y1) / 2.0))
    o.append('</svg>')
    return ''.join(o)


def table():
    """2つの条件が両方そろうのは1行だけ、と目で分かる表。"""
    o = ['<div class="%s-tw"><table class="%s-tab">' % (P, P),
         '<thead><tr><th>揺れ方</th><th>波数</th><th>波長</th>'
         '<th>電気の偏り</th><th>そこにある地球の熱</th><th>結果</th></tr>'
         '</thead><tbody>']
    for key, formula, name, mode, wn, dip, verdict, _m in \
            sorted(MOL, key=lambda m: m[4], reverse=True):
        h = heat(wn)
        o.append('<tr class="%s">' % ('is-catch' if verdict == 'catch' else ''))
        o.append('<td>%s %s</td>' % (formula, mode))
        o.append('<td>%d cm⁻¹</td><td>%.2f μm</td>' % (wn, um(wn)))
        o.append('<td class="%s-%s">%s</td>'
                 % (P, 'yes' if dip else 'no', '生まれる' if dip else '生まれない'))
        o.append('<td><span class="%s-heat"><u style="width:%.0fpx"></u>'
                 '%.0f</span></td>' % (P, max(3.0, h * 0.68), h))
        o.append('<td>%s</td></tr>' % VERDICT[verdict])
    o.append('</tbody></table></div>')
    return ''.join(o)


# ---------------------------------------------------------------- 検算

def check():
    print('コントラスト（地 #FDFAF3 に対して）:')
    emol.check_contrast([e for m in G.mols for e in m.elems()])

    print('波数と波長、そこにある地球の熱:')
    for key, _f, _n, mode, wn, dip, verdict, m in MOL:
        print('  %-3s %-8s %5d cm⁻¹ = %5.2f μm   熱 %5.1f   偏り %-5s %s'
              % (key, mode, wn, um(wn), heat(wn),
                 'あり' if dip else 'なし', VERDICT[verdict]))
        assert abs(um(wn) * wn - 10000.0) < 1e-9

    # 両方そろうのは 1 つだけ、という図の骨をここで固定する
    both = [m for m in MOL if m[5] and heat(m[4]) > 50.0]
    print('「偏りが生まれる」かつ「地球の熱が半分以上ある」揺れ: %d 個 -> %s'
          % (len(both), [m[0] for m in both]))
    assert len(both) == 1 and both[0][0] == 'cb', \
        'この図の骨（両方そろうのは変角だけ）が崩れている'

    print('変位の検算（重心が動いていないか）:')
    for key, _f, _n, _mode, _wn, _d, _v, m in MOL:
        for ax in range(3):
            s = sum(MASS[e] * v[ax] for (_p, e, _g), v in zip(m.atoms, m.vib))
            assert abs(s) < 1e-9, '%s: 軸%d で重心が動いている' % (key, ax)
        amp = max(math.sqrt(sum(c * c for c in v)) for v in m.vib)
        print('  %-3s 最大の振れ幅 %.3f Å ／ 重心のずれ 0' % (key, amp))

    cb = [m for m in MOL if m[0] == 'cb'][0][7]
    print('  変角: 静止 %.1f° -> 振れた端 %.1f°'
          % (emol.angle(cb.at(0.0)[1], cb.at(0.0)[0], cb.at(0.0)[2]),
             emol.angle(cb.at(1.0)[1], cb.at(1.0)[0], cb.at(1.0)[2])))
    ca = [m for m in MOL if m[0] == 'ca'][0][7]
    p = ca.at(1.0)
    print('  逆対称伸縮: 振れた端の C=O は %.3f Å と %.3f Å（片方が伸び片方が縮む）'
          % (emol.dist(p[0], p[1]), emol.dist(p[0], p[2])))
    assert abs(emol.dist(p[0], p[1]) - emol.dist(p[0], p[2])) > 0.1

    sh = band_share(BAND[0], BAND[1], T_EARTH)
    print('地球（%.2f K）のピーク %.2f μm ／ %.1f〜%.1f μm に入るエネルギーは %.1f%%'
          % (T_EARTH, wien(T_EARTH), BAND[0], BAND[1], sh * 100))

    print('枠 %.1f:' % G.vb)
    for m in G.mols:
        x0, x1, y0, y1 = G._box[m.key]
        print('  %-3s 幅 %5.1f × %5.1f  枠を %3.0f%% 使う'
              % (m.key, x1 - x0, y1 - y0, max(x1 - x0, y1 - y0) / G.vb * 100))
        eq = [emol.dist(m.at(0.0)[i], m.at(0.0)[j]) for i, j in m.bonds]
        worst = 1.0
        for ph in (-1.0, 0.0, 1.0):
            pp = m.at(ph)
            for k, (i, j) in enumerate(m.bonds):
                d = emol.dist(pp[i], pp[j])
                worst = min(worst, d / eq[k])
                gap = (d - emol.RAD[m.atoms[i][1]] * G.ball
                       - emol.RAD[m.atoms[j][1]] * G.ball) * G.scale
                assert gap > 4.0, '%s: 振れた端で玉が重なる（%.1fpx）' % (m.key, gap)
        print('       振れた端でも結合は静止時の %.0f%% まで' % (worst * 100))
        # 実際の振動は数%しか伸び縮みしない。見せるために誇張してあるが、
        # 2 割も縮めると分子が壊れて見える。そこを下限にする。
        assert worst > 0.82, '%s: 結合を縮めすぎ（%.0f%%）' % (m.key, worst * 100)
    return sh


# ---------------------------------------------------------------- 組み立て

def build(share):
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, 'なぜ二酸化炭素だけが、熱をつかまえるのか',
                        '5つとも揺れています。'
                        '<b>そのうち3つは同じ二酸化炭素で、揺れ方だけが違います。</b>'
                        'カーソルを合わせる（スマホはタップ）と、'
                        'その揺れの事情が下に出ます。'),
         G.defs(),
         '<div class="%s-row">' % P]

    for key, formula, name, mode, wn, dip, verdict, _m in MOL:
        o.append('<div class="%s-cell%s" data-detail="%s">'
                 % (P, ' is-catch' if verdict == 'catch' else '',
                    efig.attr(DET[key])))
        o.append(G.svg(key))
        o.append('<span class="%s-f">%s</span>' % (P, formula))
        o.append('<span class="%s-nm">%s・%s</span>' % (P, name, mode))
        o.append('<span class="%s-wn">%d cm⁻¹<em>＝ %.2f μm</em></span>'
                 % (P, wn, um(wn)))
        o.append('<span class="%s-v is-%s">%s</span>'
                 % (P, verdict, VERDICT[verdict]))
        o.append('</div>')
    o.append('</div>')

    # 波数の読み方。ここを飛ばすと cm⁻¹ が読者に届かない
    o.append('<div class="%s-unit"><b>cm⁻¹（波数）とは、'
             '「1 cm のあいだに波が何個入るか」</b>です。'
             '数が大きいほど波は短くなります。波長との関係はただの割り算で、'
             '<code>波長（μm）＝ 10000 ÷ 波数（cm⁻¹）</code>。'
             'たとえば <code>10000 ÷ 667 ＝ 15.0 μm</code>。'
             '化学では分子の揺れのテンポを cm⁻¹ で、'
             '気象では光を μm で呼ぶ習わしなので、'
             'この2つは<b>同じものの言い換え</b>だと思ってください。'
             '<br>そして分子は、<b>自分の揺れとテンポが合った波長の光だけ</b>を'
             '吸います（共鳴）。ブランコを押すのと同じで、'
             '合っていない間隔で押しても大きくなりません。'
             'ですから「この揺れは、この波長だけを吸う」という'
             '一対一の対応ができます。</div>' % P)

    o.append('<div class="%s-spec">%s</div>' % (P, spectrum()))
    o.append('<p class="%s-cap">オレンジ色の丸が'
             '<b>電気の偏りが生まれる揺れ</b>、'
             '灰色の丸が<b>生まれない揺れ</b>です。'
             '丸の高さが、そのままその波長に地球が出している熱の量になります。'
             '上の軸（波数 cm⁻¹）と下の軸（波長 μm）は同じ位置を指していて、'
             '目盛りの間隔が違うのは、両者が<b>逆数の関係</b>だからです。</p>' % P)

    o.append(table())
    o.append('<p class="%s-cap">熱をつかまえるには、'
             '<b>①電気の偏りが生まれること</b>と'
             '<b>②その波長に地球の熱があること</b>の両方が要ります。'
             '①だけでは吸うものが来ず、②だけでは吸う仕組みがない。'
             '<b>両方そろっているのは、いちばん下の1行だけ</b>です。</p>' % P)

    o.append(efig.close_card(
        P,
        '空気の <b>99%</b> を占める窒素と酸素は、'
        'どれだけ揺れても左右対称のままなので<b>偏りが生まれません</b>。'
        '二酸化炭素でさえ、対称に伸びちぢみする揺れ方'
        '（7.50 μm、<b>地球の熱がいちばん豊富な帯</b>）では素通りさせます。'
        '逆に、偏りが生まれる逆対称の揺れ方は 4.26 μm——'
        '<b>そこに地球の熱がほとんどありません</b>。'
        '残ったのは、折れ曲がる揺れ方ひとつ。'
        '<b>667 cm⁻¹ ＝ 15.0 μm</b> で偏りが生まれ、'
        'しかもそこは地球が山の頂上の7割の強さで熱を出している場所です。'
        '<b>この一致が、地球の気温を決めています。</b>',
        '結合長は N–N 1.098 Å／O–O 1.208 Å（Huber &amp; Herzberg 1979）、'
        'CO₂ は C=O 1.162 Å・180°（Herzberg 1966）。'
        '振動数は CO₂ 667・1333・2349 cm⁻¹、N₂ 2359 cm⁻¹、O₂ 1580 cm⁻¹'
        '（いずれも NIST CCCBDB 収録の実験値。1333 cm⁻¹ と N₂・O₂ は赤外不活性）。'
        '波長は 10000÷波数 で換算しました。'
        '「地球の熱」は 15℃（288.15 K）の黒体をプランクの式で計算した強さで、'
        'ピーク（%.2f μm、ウィーンの変位則）を 100 とした相対値です。'
        '帯の幅（%.1f〜%.1f μm）は 667 cm⁻¹ の吸収帯のおおよその広がりで、'
        'ここに入るエネルギーは地球が出す赤外線全体の約 %.0f%% にあたります。'
        '<b>揺れの振れ幅は実物よりずっと大きく、速さもずっと遅くしてあります</b>'
        '（実際は毎秒 10 兆回ほど）。'
        '変位は重心が動かないように重さで釣り合わせてあります。'
        '玉はこの図だけ小さめ（共有結合半径の0.52倍、ほかの図は0.72倍）に'
        '描いてあります。窒素は結合が短く原子が大きいので、'
        '同じ大きさのままでは動きが見えないためです。'
        % (wien(T_EARTH), BAND[0], BAND[1], share * 100),
        CID))
    o.append(G.spin_js(CID, '.%s-cell svg[viewBox]' % P))
    return '\n'.join(o)


if __name__ == '__main__':
    efig.save('_fig5_infrared.qmd', build(check()))
