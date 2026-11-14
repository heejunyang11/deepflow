# -*- coding: utf-8 -*-
"""
元素 #7 ナトリウム / 図1 : 川の水と海の水は、別の水です。

世界の川の平均と海水について、主要イオンが運ぶ電気（ミリ当量）の割合を
横棒で並べる。上の棒がプラス（陽イオン）、下の棒がマイナス（陰イオン）。
川は Ca と HCO3、海は Na と Cl が主役になる。

割合は濃さ（mg）と当量重量から、この場で計算する。写さない。
  川 : Livingstone (1963) USGS PP 440-G の世界平均（mg/L）
  海 : Millero et al. (2008) の Reference Composition（塩分 35、mg/kg）

検算: どちらも陽イオンと陰イオンの電荷がほぼ釣り合うこと（|CBE| < 1 %）。
写し違いがあれば、ここで崩れる。

出力: _fig1_river_sea.qmd
"""
import efig

P, CID = 'nars', 'nars1'

# 当量重量 (g/eq) = モル質量 / |電荷|。IUPAC 2021 の慣用値から。
EQW = dict(Ca=40.078 / 2, Mg=24.305 / 2, Na=22.990, K=39.098,
           HCO3=61.016, SO4=96.06 / 2, Cl=35.453, NO3=62.004,
           CO3=60.008 / 2, Br=79.904)

RIVER = dict(Ca=15, Mg=4.1, Na=6.3, K=2.3,
             HCO3=58.4, SO4=11.2, Cl=7.8, NO3=1.0)          # mg/L
SEA = dict(Na=10781.45, Mg=1283.72, Ca=412.08, K=399.19,
           Cl=19352.71, SO4=2712.35, HCO3=104.81, CO3=14.34, Br=67.28)  # mg/kg

CATS = ['Ca', 'Mg', 'Na', 'K']
ANIS = ['HCO3', 'SO4', 'Cl']          # 残り（NO3・CO3・Br）は「その他」に

LABEL = dict(Ca='Ca²⁺', Mg='Mg²⁺', Na='Na⁺', K='K⁺',
             HCO3='HCO₃⁻', SO4='SO₄²⁻', Cl='Cl⁻', etc='他')
NAME = dict(Ca='カルシウム', Mg='マグネシウム', Na='ナトリウム', K='カリウム',
            HCO3='炭酸水素イオン', SO4='硫酸イオン', Cl='塩化物イオン', etc='その他')


def shares(d):
    meq = {k: v / EQW[k] for k, v in d.items()}
    cat = sum(meq.get(k, 0) for k in CATS)
    ani = sum(v for k, v in meq.items() if k not in CATS)
    c = [(k, 100 * meq.get(k, 0) / cat) for k in CATS]
    a = [(k, 100 * meq.get(k, 0) / ani) for k in ANIS]
    a.append(('etc', 100 - sum(x for _k, x in a)))
    cbe = 100 * (cat - ani) / (cat + ani)
    return c, a, cbe


W, H = 680, 318
X0, BW = 112, 540
BH = 30


def bar(o, y, parts):
    x = X0
    for k, pct in parts:
        w = BW * pct / 100.0
        if w <= 0.05:
            continue
        det = '<b>%s（%s）</b>：電気の量で <b>%.0f%%</b>' % (NAME[k], LABEL[k], pct)
        o.append('<g class="%s-seg" data-detail="%s">' % (P, efig.attr(det)))
        o.append('<rect class="%s-%s" x="%.1f" y="%d" width="%.1f" height="%d"/>'
                 % (P, k, x, y, max(w - 1.2, 0.6), BH))
        if w > 46:
            o.append('<text class="%s-in%s" x="%.1f" y="%d">%s %.0f%%</text>'
                     % (P, ' %s-dk' % P if k in ('Na', 'Cl', 'HCO3', 'Ca') else '',
                        x + w / 2, y + BH / 2 + 5, LABEL[k], pct))
        elif w > 22:
            o.append('<text class="%s-in%s" x="%.1f" y="%d">%s</text>'
                     % (P, ' %s-dk' % P if k in ('Na', 'Cl', 'HCO3', 'Ca') else '',
                        x + w / 2, y + BH / 2 + 5, LABEL[k]))
        o.append('</g>')
        x += w


def build_svg():
    o = ['<svg viewBox="0 0 %d %d" role="img" aria-label="世界の川の平均と海水について、'
         '主要なイオンが運ぶ電気の割合を比べた横棒グラフ。川はカルシウムと炭酸水素イオン、'
         '海はナトリウムと塩化物イオンが大半を占める">' % (W, H)]
    rows = [('川の水', '世界の川の平均', RIVER, 26),
            ('海の水', '塩分 35 の海水', SEA, 172)]
    for title, sub, d, y in rows:
        c, a, _cbe = shares(d)
        o.append('<text class="%s-t" x="16" y="%d">%s</text>' % (P, y + 6, title))
        o.append('<text class="%s-ts" x="84" y="%d">%s</text>' % (P, y + 6, sub))
        o.append('<text class="%s-side" x="%d" y="%d">＋の電気</text>' % (P, X0 - 10, y + 36))
        o.append('<text class="%s-side" x="%d" y="%d">−の電気</text>' % (P, X0 - 10, y + 76))
        bar(o, y + 16, c)
        bar(o, y + 56, a)
    o.append('</svg>')
    return '\n'.join(o)


CSS = """
.%(p)s{--na:#7B4FA0;--ca:#C9822A;--mg:#6E8B4E;--k:#B9A7C9;
  --hco3:#2F6D9E;--cl:#2E8B7A;--so4:#C8B48A;--etc:#DDD3C0;}
.%(p)s-wrap{margin:14px 8px 0;}
.%(p)s-wrap svg{display:block;width:100%%;height:auto;}
.%(p)s-wrap text{font-family:"Hiragino Sans","Yu Gothic","Noto Sans JP",sans-serif;}
.%(p)s-Na{fill:var(--na);} .%(p)s-Ca{fill:var(--ca);} .%(p)s-Mg{fill:var(--mg);}
.%(p)s-K{fill:var(--k);} .%(p)s-HCO3{fill:var(--hco3);} .%(p)s-Cl{fill:var(--cl);}
.%(p)s-SO4{fill:var(--so4);} .%(p)s-etc{fill:var(--etc);}
.%(p)s-seg{cursor:default;}
.%(p)s-seg:hover rect{filter:brightness(1.1);}
.%(p)s-t{font-size:16px;font-weight:800;fill:var(--ink);}
.%(p)s-ts{font-size:11.5px;fill:var(--faint);}
.%(p)s-side{font-size:11.5px;fill:var(--dim);text-anchor:end;}
.%(p)s-in{font-size:12px;font-weight:700;fill:var(--ink);text-anchor:middle;
  font-variant-numeric:tabular-nums;pointer-events:none;}
.%(p)s-dk{fill:#fff;}
.%(p)s-cmp{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:12px 8px 0;}
.%(p)s-c{padding:11px 15px;border-radius:11px;line-height:1.6;font-size:.88rem;
  color:var(--dim);background:rgba(122,96,52,.05);border:1px solid var(--line2);}
.%(p)s-c b{display:block;font-size:.95rem;color:var(--ink);}
.%(p)s-c .n{font-size:1.45rem;font-weight:800;font-variant-numeric:tabular-nums;}
.%(p)s-c1 .n{color:var(--na);} .%(p)s-c2 .n{color:var(--ca);}
@media (max-width:820px){.%(p)s-wrap{margin:10px 0 0;}
  .%(p)s-cmp{grid-template-columns:1fr;margin:10px 2px 0;gap:8px;}}
""" % {'p': P}


def build():
    na_x = SEA['Na'] / RIVER['Na']
    ca_x = SEA['Ca'] / RIVER['Ca']
    o = [efig.css(P, CSS),
         efig.open_card(
             P, CID,
             '川の水はカルシウムの水、海の水はナトリウムの水',
             '水に溶けているイオンが運ぶ電気の量を、プラスとマイナスに分けて'
             '割合で示しました。棒の長さはどちらも100%です。'
             '色の帯にカーソルを合わせる（スマホはタップ）と、名前と割合が出ます。')]
    o.append('<div class="%s-wrap">%s</div>' % (P, build_svg()))
    o.append('<div class="%s-cmp">' % P)
    o.append('<div class="%s-c %s-c1"><b>海水のナトリウムは、川の</b>'
             '<span class="n">約%d倍</span></div>' % (P, P, round(na_x, -2)))
    o.append('<div class="%s-c %s-c2"><b>海水のカルシウムは、川の</b>'
             '<span class="n">約%d倍</span>にとどまる</div>' % (P, P, round(ca_x)))
    o.append('</div>')
    o.append(efig.close_card(
        P,
        '川では、プラスの電気の半分以上を<b>カルシウム</b>が運び、マイナスは'
        '<b>炭酸水素イオン</b>が3分の2を占めます。海では、プラスの8割近くが'
        '<b>ナトリウム</b>、マイナスの9割が<b>塩化物イオン</b>です。'
        '海は、川の水をそのまま煮詰めたものではありません。',
        '川：Livingstone, D. A. (1963) USGS Professional Paper 440-G の世界平均。'
        '海：Millero et al. (2008) <i>Deep-Sea Research I</i> 55, 50–72 の標準海水の組成（塩分 35）。'
        '濃さ（mg）を当量重量で割ってミリ当量にし、それぞれの合計に占める割合を出しました。'
        '「他」は硝酸・炭酸・臭化物イオンなど。倍率は海水（kg あたり）と川（L あたり）の'
        'mg を比べた目安です。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    for name, d in (('river', RIVER), ('sea', SEA)):
        c, a, cbe = shares(d)
        print('%-5s CBE %+.2f %%' % (name, cbe), ' '.join('%s %.1f' % t for t in c + a))
        assert abs(cbe) < 1.0, '%s の電荷が釣り合わない。値を写し違えていないか' % name
    print('Na x%.0f  Ca x%.1f' % (SEA['Na'] / RIVER['Na'], SEA['Ca'] / RIVER['Ca']))
    efig.save('_fig1_river_sea.qmd', build())
