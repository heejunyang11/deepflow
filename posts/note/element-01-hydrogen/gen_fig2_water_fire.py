# -*- coding: utf-8 -*-
"""
元素 #1 水素 / 図2 : 水と火は反対ではなく、同じものの二つの顔。

  2 H2 + O2  ->  2 H2O + 286 kJ/mol x 2   （燃やす）
  2 H2O + エネルギー -> 2 H2 + O2          （電気で分解する）

正確さの肝:
  「出したエネルギーと同じだけ入れないと戻らない」ことを必ず書く。
  ここを曖昧にすると「水素は無限のエネルギー源」という誤解を生む。
  286 kJ/mol は H2 1 mol あたりの高位発熱量（25 degC、生成する水が液体のとき）。

出力: _fig2_water_fire.qmd
"""
import efig

P, CID = 'eburn', 'eburn1'

CSS = """
.%(p)s-stage{display:grid;grid-template-columns:1fr;gap:8px;
  margin:20px 8px 6px;}
.%(p)s-side{padding:20px 14px;border-radius:14px;text-align:center;
  border:1px solid rgba(122,96,52,.152);}
.%(p)s-hot{background:radial-gradient(90%% 120%% at 50%% 0%%,
  rgba(216,85,42,.16),rgba(216,85,42,.03));}
.%(p)s-cool{background:radial-gradient(90%% 120%% at 50%% 0%%,
  rgba(15,108,138,.14),rgba(15,108,138,.03));}
.%(p)s-side h5{margin:0 0 4px;font-size:1.16rem;font-weight:800;}
.%(p)s-hot h5{color:var(--o)}.%(p)s-cool h5{color:var(--cov)}
.%(p)s-side p{margin:0;font-size:.88rem;color:var(--dim);line-height:1.6;}

.%(p)s-mols{display:flex;justify-content:center;align-items:center;
  gap:16px;min-height:78px;margin:12px 0 10px;}
.%(p)s-m{position:relative;display:flex;align-items:center;}
.%(p)s-a{border-radius:50%%;display:block;}
.%(p)s-a.h{width:17px;height:17px;background:var(--h);
  box-shadow:0 0 0 2px rgba(94,150,196,.25);}
.%(p)s-a.o{width:29px;height:29px;background:var(--o);
  box-shadow:0 0 0 2px rgba(216,85,42,.25);}
.%(p)s-m .h+.h{margin-left:-4px}.%(p)s-m .o+.o{margin-left:-7px}
/* 水分子は直線ではなく約 104.5 度に折れている。この形が極性を生む */
.%(p)s-m.w{align-items:flex-start}
.%(p)s-m.w .h{margin-top:15px}
.%(p)s-m.w .h:first-child{margin-right:-3px}
.%(p)s-m.w .h:last-child{margin-left:-3px}
.%(p)s-hot .%(p)s-m{animation:%(p)s-jit .3s linear infinite;}
.%(p)s-m:nth-child(2){animation-delay:.07s}
.%(p)s-m:nth-child(3){animation-delay:.15s}
.%(p)s-cool .%(p)s-m{animation:%(p)s-bob 3.4s ease-in-out infinite;}
.%(p)s-cool .%(p)s-m:nth-child(2){animation-delay:1.1s}
@keyframes %(p)s-jit{0%%{transform:translate(0,0) rotate(0)}
  25%%{transform:translate(2px,-2px) rotate(4deg)}
  50%%{transform:translate(-2px,1px) rotate(-3deg)}
  75%%{transform:translate(1px,2px) rotate(2deg)}
  100%%{transform:translate(0,0) rotate(0)}}
@keyframes %(p)s-bob{0%%,100%%{transform:translateY(0)}
  50%%{transform:translateY(-5px)}}
.%(p)s-eq{font-size:1.05rem;font-weight:700;letter-spacing:.02em;}
.%(p)s-eq sub{font-size:.7em}

/* 中央の往復 */
.%(p)s-mid{display:flex;gap:22px;padding:4px 0;}
.%(p)s-mid .%(p)s-ar{flex:1;}
.%(p)s-ar{position:relative;text-align:center;}
.%(p)s-ar b{display:block;font-size:.98rem;font-weight:800;}
.%(p)s-ar s{display:block;text-decoration:none;font-size:.85rem;
  color:var(--dim);margin-top:3px;line-height:1.5;}
.%(p)s-ln{position:relative;height:2px;margin:7px 0 5px;border-radius:2px;
  background:linear-gradient(90deg,#DED4C0,#BCAD93,#DED4C0);}
.%(p)s-ln::after{content:"";position:absolute;top:-2px;width:34%%;height:6px;
  border-radius:6px;filter:blur(1.5px);}
.%(p)s-f b{color:var(--o)}
.%(p)s-f .%(p)s-ln::after{background:linear-gradient(90deg,transparent,
  #B0663E,transparent);animation:%(p)s-go 3.6s linear infinite;}
.%(p)s-b b{color:var(--cov)}
.%(p)s-b .%(p)s-ln::after{background:linear-gradient(90deg,transparent,
  #3E88AA,transparent);animation:%(p)s-back 3.6s linear infinite;}
@keyframes %(p)s-go{0%%{left:-36%%;opacity:0}15%%,85%%{opacity:.95}
  100%%{left:102%%;opacity:0}}
@keyframes %(p)s-back{0%%{left:102%%;opacity:0}15%%,85%%{opacity:.95}
  100%%{left:-36%%;opacity:0}}
.%(p)s-tip{font-size:.85rem;color:var(--dim);text-align:center;margin:4px 8px 0;
  line-height:1.65;}

@media (max-width:820px){
  .%(p)s-stage{gap:6px;margin:14px 2px 4px;}
  .%(p)s-mid{gap:10px;}
  .%(p)s-side{padding:14px 10px}
  .%(p)s-mols{gap:11px;min-height:62px}
  .%(p)s-side h5{font-size:1.02rem}
  .%(p)s-side p{font-size:.8rem}
  .%(p)s-ar b{font-size:.86rem}.%(p)s-ar s{font-size:.76rem}
}
""" % {'p': P}


def mol(atoms, cls=''):
    return ('<span class="%s-m %s">' % (P, cls)
            + ''.join('<i class="%s-a %s"></i>' % (P, a) for a in atoms)
            + '</span>')


def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, '水と火は、反対ではありません',
                        '同じ材料の「はげしく踊っている姿」と「落ち着いた姿」です。'
                        '左右の箱にカーソルを合わせる（スマホはタップ）と説明が出ます。')]

    o.append('<div class="%s-stage">' % P)

    # --- 左：火 ---
    o.append('<div class="%s-side %s-hot" data-detail="%s">' % (P, P, (
        '水素と酸素がはげしくぶつかり合って、光と熱を出しています。'
        'これが<b>燃える</b>ということです。'
        '燃やしたあとに残るのは、すすでも灰でもなく<b>水</b>だけです。')))
    o.append('<h5>はげしく踊っている姿 ＝ 火</h5>')
    o.append('<p>水素と酸素が、ばらばらのまま飛び回っている</p>')
    o.append('<div class="%s-mols">%s%s%s</div>'
             % (P, mol('hh'), mol('hh'), mol('oo')))
    o.append('<div class="%s-eq" style="color:var(--o)">'
             '2 H<sub>2</sub> ＋ O<sub>2</sub></div>' % P)
    o.append('</div>')

    # --- 中央：往復 ---
    o.append('<div class="%s-mid">' % P)
    o.append('<div class="%s-ar %s-f"><b>燃やす　→</b>'
             '<div class="%s-ln"></div>'
             '<s>水素 1 mol あたり<br><b style="display:inline;font-size:1em">'
             '286 kJ</b> の熱が出る</s></div>' % (P, P, P))
    o.append('<div class="%s-ar %s-b"><b>←　電気で分解する</b>'
             '<div class="%s-ln"></div>'
             '<s>戻すには、出したのと<br>同じだけのエネルギーが要る</s></div>'
             % (P, P, P))
    o.append('</div>')

    # --- 右：水 ---
    o.append('<div class="%s-side %s-cool" data-detail="%s">' % (P, P, (
        '水素と酸素が結びついて落ち着いた姿が<b>水</b>です。'
        'ラボアジエはこの元素に「水（ハイドロ）を作るもの（ゲン）」という名前を'
        'つけました。<b>ハイドロゲン</b>＝水素です。')))
    o.append('<h5>落ち着いた姿 ＝ 水</h5>')
    o.append('<p>水素と酸素が結びついて、ひとつの分子になっている</p>')
    o.append('<div class="%s-mols">%s%s</div>'
             % (P, mol('hoh', 'w'), mol('hoh', 'w')))
    o.append('<div class="%s-eq" style="color:var(--cov)">'
             '2 H<sub>2</sub>O</div>' % P)
    o.append('</div>')

    o.append('</div>')  # stage
    o.append('<p class="%s-tip">水を電気で分解すると水素が生まれ、'
             'その水素を燃やすとまた水に戻ります。'
             '火と水は、この輪の別々の場面にすぎません。</p>' % P)

    o.append(efig.close_card(
        P,
        'ラボアジエは、この元素に「<b>水を作るもの</b>」という名前をつけました。'
        '燃やせば水になり、水を分解すれば戻ってくる。'
        'ただし<b>戻すには、出したのと同じだけのエネルギーが要ります</b>。'
        '水素は「無限のエネルギー」ではなく、<b>エネルギーの運び屋</b>です。',
        '286 kJ/mol は水素 1 mol あたりの高位発熱量（25 ℃、生じる水が液体のとき）。'
        '実際の電気分解では熱の出入りがあるため、必要な電気エネルギーは '
        '237 kJ/mol、残りは周囲からの熱でまかなわれます。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    efig.save('_fig2_water_fire.qmd', build())
