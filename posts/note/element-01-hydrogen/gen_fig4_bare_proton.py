# -*- coding: utf-8 -*-
"""
元素 #1 水素 / 図4 : 水素だけが持つ「むき出しの核」。

台本では「電子のシールド」と説明していたが、より正確には次の二点が理由である。
  (1) 水素には内側の電子（内殻電子）が一枚もない。
      電子が相手に引かれると、内側に何も残らず陽子がそのまま露出する。
  (2) その陽子は極端に小さい。
      陽子の半径 約 0.84 fm、水素原子の半径 約 53 pm。
      53e-12 / 0.84e-15 = 約 6.3 万倍 -> 「原子の約 6 万分の 1」
  ゆえに正の電荷が一点に集中し、相手の電子を強く引きつける。これが水素結合。

出力: _fig4_bare_proton.qmd
"""
import efig

P, CID = 'ebare', 'ebare1'

CSS = """
.%(p)s-scene{position:relative;height:236px;margin:16px 8px 0;
  display:flex;align-items:center;justify-content:center;gap:0;}

/* 酸素原子 */
.%(p)s-o{position:relative;width:132px;height:132px;border-radius:50%%;
  background:radial-gradient(circle at 42%% 38%%,rgba(216,85,42,.42),
    rgba(216,85,42,.10) 62%%,rgba(216,85,42,0) 74%%);
  border:1px dashed rgba(216,85,42,.35);flex:none;}
.%(p)s-o::after{content:"";position:absolute;left:50%%;top:50%%;
  width:26px;height:26px;margin:-13px 0 0 -13px;border-radius:50%%;
  background:var(--o);box-shadow:0 0 0 4px rgba(216,85,42,.22);}
.%(p)s-o em{position:absolute;left:50%%;bottom:-24px;transform:translateX(-50%%);
  font-style:normal;font-size:.95rem;font-weight:700;color:var(--o);
  white-space:nowrap;}
.%(p)s-o u{position:absolute;left:50%%;top:50%%;transform:translate(-50%%,-50%%);
  text-decoration:none;font-size:.62rem;font-weight:800;color:#F4DED4;z-index:2;}

/* 結合の軸 */
.%(p)s-bond{position:relative;width:190px;height:2px;flex:none;
  background:linear-gradient(90deg,rgba(216,85,42,.55),rgba(94,150,196,.55));}

/* 共有されている電子。ふだんは真ん中、周期的に酸素側へ寄る */
.%(p)s-e{position:absolute;top:-7px;width:15px;height:15px;border-radius:50%%;
  background:var(--e);box-shadow:0 0 0 3px rgba(47,109,178,.25);
  animation:%(p)s-pull 5s ease-in-out infinite;}
.%(p)s-e.a{left:32%%}.%(p)s-e.b{left:58%%;animation-delay:.12s}
@keyframes %(p)s-pull{0%%,12%%{transform:translateX(0)}
  46%%,74%%{transform:translateX(-52px)}100%%{transform:translateX(0)}}

/* 水素原子 */
/* 見出しの .{P}-h と衝突しないよう、水素原子は -hy にする */
.%(p)s-hy{position:relative;width:74px;height:74px;border-radius:50%%;
  background:radial-gradient(circle at 44%% 40%%,rgba(94,150,196,.40),
    rgba(94,150,196,.08) 64%%,rgba(94,150,196,0) 76%%);
  border:1px dashed rgba(94,150,196,.38);flex:none;
  animation:%(p)s-thin 5s ease-in-out infinite;}
@keyframes %(p)s-thin{0%%,12%%{opacity:1}46%%,74%%{opacity:.18}100%%{opacity:1}}
.%(p)s-p{position:absolute;left:50%%;top:50%%;width:15px;height:15px;
  margin:-7px 0 0 -7px;border-radius:50%%;background:#C42B3C;
  animation:%(p)s-glow 5s ease-in-out infinite;z-index:3;}
@keyframes %(p)s-glow{0%%,12%%{box-shadow:0 0 0 2px rgba(196,43,60,.18)}
  46%%,74%%{box-shadow:0 0 0 7px rgba(196,43,60,.30)}
  100%%{box-shadow:0 0 0 2px rgba(196,43,60,.18)}}
.%(p)s-d{position:absolute;left:50%%;top:-34px;transform:translateX(-50%%);
  font-size:1.15rem;font-weight:800;color:#C42B3C;white-space:nowrap;
  animation:%(p)s-din 5s ease-in-out infinite;}
@keyframes %(p)s-din{0%%,16%%{opacity:0}46%%,74%%{opacity:1}100%%{opacity:0}}
.%(p)s-hl{position:absolute;left:50%%;bottom:-24px;transform:translateX(-50%%);
  font-size:.95rem;font-weight:700;color:var(--h);white-space:nowrap;}

/* 事実カード */
.%(p)s-facts{display:grid;grid-template-columns:1fr 1fr;gap:10px;
  margin:30px 8px 0;}
.%(p)s-fc{padding:14px 16px;border-radius:12px;
  background:rgba(122,96,52,.085);border:1px solid rgba(122,96,52,.152);
  cursor:default;}
.%(p)s-fc b{display:block;font-size:1.1rem;font-weight:800;margin-bottom:5px;
  color:var(--ink);}
.%(p)s-fc span{font-size:.9rem;color:var(--dim);line-height:1.75;}
.%(p)s-fc em{font-style:normal;color:var(--hb);font-weight:800;}

@media (max-width:820px){
  .%(p)s-scene{height:200px;margin:12px 2px 0}
  .%(p)s-o{width:104px;height:104px}
  .%(p)s-bond{width:110px}
  .%(p)s-hy{width:60px;height:60px}
  .%(p)s-facts{grid-template-columns:1fr;gap:7px;margin:26px 2px 0}
  .%(p)s-o em,.%(p)s-hl{font-size:.84rem}
}
""" % {'p': P}


def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, '水素だけが持つ「むき出しの核」',
                        '電子が相手に引かれたとき、水素は隠すものを何も持っていません。'
                        'これが水素結合の正体です。')]

    o.append('<div class="%s-scene">' % P)
    o.append('<div class="%s-o"><u>O</u><em>酸素原子</em></div>' % P)
    o.append('<div class="%s-bond"><i class="%s-e a"></i>'
             '<i class="%s-e b"></i></div>' % (P, P, P))
    o.append('<div class="%s-hy"><span class="%s-d">δ＋</span>'
             '<i class="%s-p"></i><em class="%s-hl">水素原子</em></div>'
             % (P, P, P, P))
    o.append('</div>')

    o.append('<div class="%s-facts">' % P)
    o.append('<div class="%s-fc" data-detail="%s"><b>内側の電子が、一枚もない</b>'
             '<span>ほかの原子は、外側の電子をとられても内側の電子が核を隠して'
             'います。水素の電子は<em>たった 1 個</em>。それが引かれると、'
             '中から<em>裸の陽子</em>が出てきます。</span></div>'
             % (P, ('ほかの原子は内側の電子が核を隠すので、電子をとられても'
                    '「裸」にはなりません。<b>水素だけは内側に何もない</b>ので、'
                    '陽子がそのまま外に出ます。')))
    o.append('<div class="%s-fc" data-detail="%s"><b>その陽子は、けた違いに小さい</b>'
             '<span>陽子の大きさは、水素原子のおよそ<em>6 万分の 1</em>。'
             '同じプラスの電気が<em>一点に集中</em>するので、'
             '相手の電子を強く引きつけます。</span></div>'
             % (P, ('陽子の半径は約 0.84 fm、水素原子は約 53 pm。'
                    'その比はおよそ <b>6 万分の 1</b> です。'
                    '野球ボールを原子とすると、陽子はその中心に置いた'
                    '<b>目に見えないほど小さな粒</b>にあたります。')))
    o.append('</div>')

    o.append(efig.close_card(
        P,
        '水素が酸素と結びつくと、水素の電子は酸素の側へ引き寄せられます。'
        'このとき水素側には<b>裸の陽子</b>が残り、そこがプラスに帯電します。'
        'この「むき出しのプラス」が、となりの水分子の酸素を引きつける——'
        'これが<b>水素結合</b>です。',
        '陽子の電荷半径 0.8409 fm（CODATA 2018）、水素原子のボーア半径 '
        '52.9 pm による。図は仕組みを示す模式図で、縮尺は正確ではありません。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    efig.save('_fig4_bare_proton.qmd', build())
