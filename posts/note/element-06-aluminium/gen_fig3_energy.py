# -*- coding: utf-8 -*-
"""
元素 #6 アルミニウム / 図3 : 電気の缶詰。

缶 1 本ぶんのアルミを作る電気を、40 W の電球が何時間ともるかで見せる。

  新しく作る（鉱石から）:
    電気分解に使う電気 13.2 kWh/kg（IAI、2022 年の世界平均）
    350 mL 缶 1 本 ≒ 15 g
    → 13.2 × 0.015 = 0.198 kWh → 40 W で 4.95 時間 ≒ 約 5 時間
  溶かし直す（再生）:
    IAI「再生は新地金の約 5 % のエネルギー」（採掘から鋳造までの一次エネルギーの比較）
    → 同じ割合で換算すると 0.0099 kWh → 40 W で約 15 分

2 つの数字は基準が少し違う（前者は電気分解の電力、後者は総エネルギーの比）。
図では「目安の換算」と明記し、比を見せることに徹する。

出力: _fig3_energy.qmd
"""
import efig

P, CID = 'alkwh', 'alkwh1'

KWH_PER_KG = 13.2        # 電気分解の電力（IAI 2022、世界平均）
CAN_G = 15.0             # 350 mL 缶
BULB_W = 40.0
RECYCLE = 0.05           # 新地金に対する再生のエネルギー比（IAI）

E_NEW = KWH_PER_KG * CAN_G / 1000.0          # kWh
H_NEW = E_NEW / (BULB_W / 1000.0)            # 時間
E_REC = E_NEW * RECYCLE
MIN_REC = E_REC / (BULB_W / 1000.0) * 60.0   # 分

W, H = 680, 250
BX0, BDX = 170, 78       # 電球の並び（右端の数字と重ならない間隔）


def bulb(cx, cy, fill, idx, lit=True):
    """電球 1 個。fill は 0〜1（1 時間を 1 個として、どこまでともるか）。"""
    r = 22
    o = []
    cid = '%s-cp%d' % (P, idx)
    # ガラス球の輪郭で切り抜き、下から fill の割合だけ明るく塗る
    o.append('<clipPath id="%s"><circle cx="%.1f" cy="%.1f" r="%d"/></clipPath>' % (cid, cx, cy, r))
    o.append('<circle class="%s-glass" cx="%.1f" cy="%.1f" r="%d"/>' % (P, cx, cy, r))
    if fill > 0:
        h = 2 * r * fill
        o.append('<rect class="%s-lit%s" x="%.1f" y="%.1f" width="%d" height="%.1f" '
                 'clip-path="url(#%s)"/>'
                 % (P, ' %s-glow' % P if lit else '', cx - r, cy + r - h, 2 * r, h, cid))
    o.append('<circle class="%s-rim" cx="%.1f" cy="%.1f" r="%d"/>' % (P, cx, cy, r))
    o.append('<rect class="%s-base" x="%.1f" y="%.1f" width="18" height="14" rx="3"/>'
             % (P, cx - 9, cy + r - 2))
    return '\n'.join(o)


def build_svg():
    o = ['<svg viewBox="0 0 %d %d" role="img" aria-label="缶1本分のアルミを作る電気を、'
         '40ワットの電球がともる時間で比べた図">' % (W, H)]
    # 新しく作る
    y1 = 70
    o.append('<g data-detail="%s">' % efig.attr(
        '鉱石から新しく作ると、缶 1 本（約 15 g）ぶんで<b>約 0.2 kWh</b>の電気を使います。'
        '40 W の電球なら<b>約 5 時間</b>。<b>その電気が、缶の形で手元に届いています。</b>'))
    o.append('<rect class="%s-hitr" x="0" y="%d" width="%d" height="84"/>' % (P, y1 - 40, W))
    o.append('<text class="%s-rt" x="150" y="%d">鉱石から</text>' % (P, y1 - 4))
    o.append('<text class="%s-rt" x="150" y="%d">新しく作る</text>' % (P, y1 + 14))
    full = int(H_NEW)
    frac = H_NEW - full
    for i in range(full + (1 if frac > 0.05 else 0)):
        f = 1.0 if i < full else frac
        o.append(bulb(BX0 + 30 + i * BDX, y1, f, i))
    o.append('<text class="%s-big" x="%d" y="%d">約 %d 時間</text>'
             % (P, W - 8, y1 + 7, round(H_NEW)))
    o.append('</g>')

    # 溶かし直す
    y2 = 180
    o.append('<g data-detail="%s">' % efig.attr(
        '使い終わった缶を溶かし直すなら、エネルギーは<b>新しく作るときの約 5 %</b>で済みます。'
        '電球に換算すると<b>15 分ほど</b>。'
        'リサイクルとは、<b>この電気をもう一度払わずに済ませること</b>です。'))
    o.append('<rect class="%s-hitr" x="0" y="%d" width="%d" height="84"/>' % (P, y2 - 40, W))
    o.append('<text class="%s-rt %s-rc" x="150" y="%d">使い終わった缶を</text>' % (P, P, y2 - 4))
    o.append('<text class="%s-rt %s-rc" x="150" y="%d">溶かし直す</text>' % (P, P, y2 + 14))
    o.append(bulb(BX0 + 30, y2, MIN_REC / 60.0, 9))
    o.append('<text class="%s-big %s-bc" x="%d" y="%d">約 %d 分</text>'
             % (P, P, W - 8, y2 + 7, round(MIN_REC / 5.0) * 5))
    o.append('</g>')

    o.append('<text class="%s-lg" x="%d" y="%d">電球 1 個 ＝ 40 W の電球が 1 時間ともる電気</text>'
             % (P, BX0 + 10, H - 6))
    o.append('</svg>')
    return '\n'.join(o)


CSS = """
.%(p)s{--litc:#F2B632;--glass:#FFF7E6;--rim:#C9B99A;--base:#9A8D78;--al:#5B6F80;--rec:#0F6C8A;}
.%(p)s-wrap{margin:18px 8px 0;}
.%(p)s-wrap svg{display:block;width:100%%;height:auto;}
.%(p)s-wrap text{font-family:"Hiragino Sans","Yu Gothic","Noto Sans JP",sans-serif;}
.%(p)s-hitr{fill:transparent;}
.%(p)s-wrap g[data-detail]{cursor:default;}
.%(p)s-wrap g[data-detail]:hover .%(p)s-hitr{fill:rgba(122,96,52,.06);}
.%(p)s-rt{font-size:13.5px;font-weight:800;fill:var(--al);text-anchor:end;}
.%(p)s-rc{fill:var(--rec);}
.%(p)s-glass{fill:var(--glass);}
.%(p)s-lit{fill:var(--litc);}
.%(p)s-rim{fill:none;stroke:var(--rim);stroke-width:2;}
.%(p)s-base{fill:var(--base);}
.%(p)s-big{font-size:22px;font-weight:800;fill:var(--al);text-anchor:end;
  font-variant-numeric:tabular-nums;}
.%(p)s-bc{fill:var(--rec);}
.%(p)s-lg{font-size:11.5px;fill:var(--faint);}
.%(p)s-glow{animation:%(p)s-glow 2.6s ease-in-out infinite;}
@keyframes %(p)s-glow{0%%,100%%{opacity:1;}50%%{opacity:.78;}}
@media (max-width:820px){.%(p)s-wrap{margin:12px 0 0;}}
""" % {'p': P}


def build():
    o = [efig.css(P, CSS),
         efig.open_card(
             P, CID,
             'アルミ缶は、電気の缶詰です',
             '缶 1 本（350 mL・約 15 g）ぶんのアルミを作るのに使う電気を、'
             '40 W の電球がともる時間に置き換えました。行にカーソルを合わせる'
             '（スマホはタップ）と説明が出ます。')]
    o.append('<div class="%s-wrap">%s</div>' % (P, build_svg()))
    o.append(efig.close_card(
        P,
        'アルミは、酸素を<b>電気で引き剥がして</b>作ります。'
        '缶 1 本ぶんで、40 W の電球を<b>約 5 時間</b>ともせる電気です。'
        'ところが、いちど金属になったものを溶かし直すなら、'
        '<b>その約 20 分の 1</b> で済みます。'
        'リサイクルすれば、<b>この電気をもう一度払わずに済みます</b>。',
        '新しく作る側：電気分解に使う電力 13.2 kWh/kg（International Aluminium Institute、'
        '2022 年の世界平均）× 缶 15 g ＝ 約 0.2 kWh。'
        '溶かし直す側：再生に要るエネルギーは新地金の約 5 %'
        '（<a href="https://international-aluminium.org/landing/aluminium-recycling-saves-95-of-the-energy-needed-for-primary-aluminium-production/">IAI</a>。'
        '採掘から鋳造までの一次エネルギーでの比較）を、同じ割合で電球に換算した目安です。'
        '鉱石からアルミナを取り出す工程の熱や、鋳造・炭素電極の製造で使う電力は、'
        '新しく作る側の電球に含めていません。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    print('新しく作る  %.3f kWh  → 40 W で %.2f 時間' % (E_NEW, H_NEW))
    print('溶かし直す  %.4f kWh → 40 W で %.1f 分' % (E_REC, MIN_REC))
    efig.save('_fig3_energy.qmd', build())
