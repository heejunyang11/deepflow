# -*- coding: utf-8 -*-
"""
元素 #1 水素 / 図5 : レモン一滴の中に、水素イオンは何個いるか。

  pH 2.4  ->  [H+] = 10^-2.4 = 3.98e-3 mol/L
  一滴 0.05 mL = 5e-5 L      -> 1.99e-7 mol
  x アボガドロ数 6.022e23    -> 1.20e17 個 = 約 12 京個
  日本の人口 1.2e8 で割ると 1e9 -> ひとりに 10 億個ずつ配れる

出力: _fig5_lemon.qmd
"""
import math
import efig

P, CID = 'elemon', 'elemon1'

PH_LO, PH_HI = 0, 14
LIQUIDS = [
    (1.5, '胃液', '#AC1C2E', 42,
     '胃の中は、レモンよりもさらに酸っぱい状態です。'
     '食べ物を溶かすために、これだけ濃い水素イオンを自分で作っています。'),
    (2.4, 'レモン', '#AE7A06', 0,
     'レモンの酸っぱさの正体は、<b>水にとけた水素イオン</b>です。'
     '舌はこの水素イオンを感じ取っています。'),
    (7.0, '水', '#2C7A4C', 42,
     '真水は酸性でもアルカリ性でもない、ちょうど真ん中です。'),
    (8.1, '海水', '#0F6C8A', 0,
     '海水はほんの少しアルカリ性です。'
     'ただし大気の二酸化炭素がとけこむことで、'
     'ゆっくり酸性の側へ動いていることが分かっています。'),
    (10.0, 'せっけん水', '#6858B0', 42,
     'アルカリ性です。水素イオンが少ない側です。'),
]

STEPS = [
    ('pH 2.4 の水には', '1 L あたり 0.004 mol の水素イオン',
     '10<sup>−2.4</sup> ＝ 0.00398 mol/L'),
    ('一滴は 0.05 mL なので', '0.0000002 mol',
     '0.00398 × 0.00005 L'),
    ('原子の個数になおすと', '約 12 京個',
     '× 6.02 × 10<sup>23</sup>（アボガドロ数）'),
]

CSS = """
.%(p)s-stage{position:relative;margin:22px 8px 0;}
/* 目盛りはバーを基準に置く。stage を基準にすると上下がそろわない */
.%(p)s-scale{position:relative;height:16px;margin:92px 0 0;}
.%(p)s-bar{position:absolute;inset:0;border-radius:8px;
  background:linear-gradient(90deg,#AC1C2E 0%%,#BE620A 22%%,#9C7808 42%%,
    #2C7A4C 50%%,#0F6C8A 66%%,#6858B0 86%%,#8842BE 100%%);
  box-shadow:0 0 0 1px rgba(122,96,52,.16);}
.%(p)s-t{position:absolute;transform:translateX(-50%%);text-align:center;
  cursor:default;}
.%(p)s-t i{display:block;width:12px;height:12px;margin:0 auto;
  border-radius:50%%;background:var(--c);border:2px solid #FDFAF3;
  box-shadow:0 0 0 2px var(--c);}
.%(p)s-t b{display:block;font-size:.94rem;font-weight:700;white-space:nowrap;
  color:var(--ink);}
.%(p)s-t s{display:block;text-decoration:none;font-size:.83rem;
  color:var(--dim);}
.%(p)s-t.up{bottom:26px}.%(p)s-t.dn{top:26px}
.%(p)s-t.dn i{margin-bottom:3px}
.%(p)s-ends{display:flex;justify-content:space-between;
  font-size:.82rem;color:var(--faint);margin-top:92px;}

/* 落ちる滴 */
.%(p)s-drop{position:absolute;left:%(lx).3f%%;top:-64px;width:13px;height:17px;
  margin-left:-6px;background:var(--h);border-radius:0 60%% 60%% 60%%;
  transform:rotate(-45deg);box-shadow:0 0 0 3px rgba(94,150,196,.25);
  animation:%(p)s-fall 4.2s cubic-bezier(.5,0,.85,.4) infinite;}
@keyframes %(p)s-fall{0%%{top:-64px;opacity:0}
  12%%{opacity:1}44%%{top:-8px;opacity:1}52%%,100%%{top:-8px;opacity:0}}
.%(p)s-splash{position:absolute;left:%(lx).3f%%;top:-6px;width:26px;height:26px;
  margin-left:-13px;border-radius:50%%;border:2px solid var(--h);
  animation:%(p)s-sp 4.2s ease-out infinite;}
@keyframes %(p)s-sp{0%%,44%%{transform:scale(.2);opacity:0}
  52%%{transform:scale(.6);opacity:.9}80%%,100%%{transform:scale(2.2);opacity:0}}

/* 計算 */
.%(p)s-calc{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;
  margin:26px 8px 0;}
.%(p)s-st{padding:14px 15px;border-radius:12px;
  background:rgba(122,96,52,.085);border:1px solid rgba(122,96,52,.152);
  animation:%(p)s-in .9s ease-out both;}
.%(p)s-st:nth-child(2){animation-delay:.35s}
.%(p)s-st:nth-child(3){animation-delay:.7s}
@keyframes %(p)s-in{from{opacity:0;transform:translateY(9px)}
  to{opacity:1;transform:none}}
.%(p)s-st em{font-style:normal;display:block;font-size:.85rem;color:var(--dim);}
.%(p)s-st b{display:block;font-size:1.18rem;font-weight:800;margin:5px 0 6px;
  color:var(--ink);}
.%(p)s-st s{display:block;text-decoration:none;font-size:.79rem;
  color:var(--faint);}
.%(p)s-st:last-child{border-color:rgba(193,101,10,.45);
  background:rgba(193,101,10,.10);}
.%(p)s-st:last-child b{color:var(--hb);font-size:1.75rem;
  text-shadow:0 0 20px rgba(193,101,10,.55);}

@media (max-width:820px){
  .%(p)s-calc{grid-template-columns:1fr;gap:7px;margin:20px 2px 0}
  .%(p)s-st{padding:10px 12px}
  .%(p)s-st b{font-size:1.05rem;margin:3px 0 4px}
  .%(p)s-st:last-child b{font-size:1.4rem}
  .%(p)s-t s{display:none}
  .%(p)s-t b{font-size:.8rem}
  .%(p)s-stage{margin:20px 2px 0}
}
""" % {'p': P, 'lx': (2.4 - PH_LO) / (PH_HI - PH_LO) * 100.0}


def pos(ph):
    return (ph - PH_LO) / (PH_HI - PH_LO) * 100.0


def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, 'レモン一滴の中に、水素イオンは何個いるか',
                        '酸っぱさの正体は水素イオンです。'
                        'では、たった一滴に何個いるのか数えてみます。')]

    o.append('<div class="%s-stage">' % P)
    o.append('<div class="%s-scale">' % P)
    o.append('<div class="%s-bar"></div>' % P)
    o.append('<div class="%s-drop"></div><div class="%s-splash"></div>' % (P, P))
    for ph, name, col, dn, det in LIQUIDS:
        cls = 'dn' if dn else 'up'
        inner = ('<i></i><b>%s</b><s>pH %g</s>' % (name, ph)) if dn else \
                ('<b>%s</b><s>pH %g</s><i></i>' % (name, ph))
        o.append('<div class="%s-t %s" style="left:%.3f%%;--c:%s" '
                 'data-detail="%s">%s</div>'
                 % (P, cls, pos(ph), col, det, inner))
    o.append('</div>')
    o.append('<div class="%s-ends"><span>← 酸っぱい（酸性）</span>'
             '<span>アルカリ性 →</span></div>' % P)
    o.append('</div>')

    o.append('<div class="%s-calc">' % P)
    for head, big, small in STEPS:
        o.append('<div class="%s-st"><em>%s</em><b>%s</b><s>%s</s></div>'
                 % (P, head, big, small))
    o.append('</div>')

    o.append(efig.close_card(
        P,
        'レモンをしぼった<b>たった一滴</b>の中に、水素イオンが '
        '<b>約 12 京個</b>（1.2 × 10<sup>17</sup> 個）います。'
        '日本人ひとりひとりに <b>10 億個ずつ</b>配ってもまだ余る数です。',
        'レモン果汁の pH は 2.0〜2.6 程度。ここでは 2.4 として計算しました。'
        '一滴は 0.05 mL としています。'
        'pH は「水素イオンの濃さ」を対数で表した目盛りで、'
        '1 下がるごとに濃さは 10 倍になります。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    efig.save('_fig5_lemon.qmd', build())
