# -*- coding: utf-8 -*-
"""
元素 #1 水素 / 図1 : 宇宙をバケツ一杯すくうと、中身はほとんど水素。

点 100 個が宇宙の原子 100 個ぶん。個数の比で描く。
  水素     92.1 %  -> 92 個
  ヘリウム  7.8 %  ->  8 個
  その他    0.1 %  -> 0.1 個（点 1 個にすら足りない）

100 個では「その他」が 1 個も現れない。ここがこの図の山になる。
1 個ぶん確保するには 1000 個ならべる必要がある、と添えて落とす。
足りないぶんは幽霊の点で見せる。面積で 1/10 なので直径は 1/√10 ≒ 0.32 倍。

（質量の比では水素 74 %・ヘリウム 25 %・その他 1 %。個数と重さで比が違うのは
  原子 1 個の重さが違うため。この注意書きを図の中に必ず残すこと）

色は図の中だけで持つ。--h は他の図（水と火・裸の陽子・レモン）でも
「水素／水」を指す寒色として使っているので、共通トークンには手を入れない。

出典: Lodders (2003) / Asplund et al. (2009) の太陽系元素存在度に基づく概数。
出力: _fig1_abundance.qmd
"""
import efig

P, CID = 'euniv', 'euniv1'
COLS = 10
N_H, N_HE = 92, 8
TWINKLE = 6                      # またたきの位相の数

CSS = """
/* 点の色はこの図の中だけの取り決め。地（#FDFAF3）に対するコントラスト比は
   水素 3.21 / ヘリウム 8.14 / その他 6.84。図形なので 3.0 を下限にした。 */
.%(p)s-stage{--uh:#BE7F30;--uhe:#6E4310;--uot:#A82234;
  display:flex;flex-wrap:wrap;align-items:center;gap:26px 34px;
  margin:18px 8px 6px;}

.%(p)s-grid{display:grid;grid-template-columns:repeat(%(c)d,1fr);
  gap:9px;flex:1 1 340px;max-width:430px;
  align-items:center;justify-items:center;}
.%(p)s-grid i{display:block;width:100%%;max-width:28px;aspect-ratio:1;
  border-radius:50%%;}
.%(p)s-grid i.h{background:var(--uh);
  animation:%(p)s-tw 4.4s ease-in-out infinite;}
.%(p)s-grid i.he{background:var(--uhe);}
@keyframes %(p)s-tw{0%%,100%%{opacity:.72}50%%{opacity:1}}
%(tw)s

/* 「その他ぜんぶ」は点 1 個にも満たない。実物の 0.1 個ぶんを描く */
.%(p)s-gh{flex:0 1 260px;display:flex;align-items:center;gap:15px;
  padding:15px 17px;border-radius:13px;
  background:rgba(168,34,52,.05);border:1px dashed rgba(168,34,52,.4);}
.%(p)s-gd{position:relative;flex:0 0 auto;width:56px;height:56px;
  border-radius:50%%;border:2px dashed rgba(168,34,52,.55);
  display:flex;align-items:center;justify-content:center;}
.%(p)s-gd i{display:block;width:18px;height:18px;border-radius:50%%;
  background:var(--uot);}
.%(p)s-gd i::after{content:"";position:absolute;inset:19px;
  border-radius:50%%;border:2px solid var(--uot);
  animation:%(p)s-ring 2.8s ease-out infinite;}
@keyframes %(p)s-ring{0%%{transform:scale(.6);opacity:.75}
  70%%,100%%{transform:scale(3);opacity:0}}
.%(p)s-gt{margin:0;font-size:.9rem;line-height:1.6;color:var(--dim);}
.%(p)s-gt b{display:block;font-size:1.24rem;font-weight:800;
  color:var(--uot);line-height:1.3;margin-bottom:2px;}

/* 凡例。カーソルを合わせるとその仲間だけが残る */
.%(p)s-leg{display:flex;flex-wrap:wrap;gap:8px;margin:18px 8px 0;}
.%(p)s-leg span{display:flex;align-items:center;gap:8px;cursor:default;
  padding:8px 14px;border-radius:10px;font-size:.95rem;color:var(--ink);
  background:rgba(122,96,52,.085);border:1px solid rgba(122,96,52,.152);}
.%(p)s-leg span em{font-style:normal;font-weight:800;font-size:1.16rem;}
.%(p)s-leg span u{width:11px;height:11px;border-radius:50%%;
  text-decoration:none;display:block;}
.%(p)s-leg .lh u{background:#BE7F30}.%(p)s-leg .lhe u{background:#6E4310}
.%(p)s-leg .lot u{width:9px;height:9px;background:#A82234;
  box-shadow:0 0 0 3px rgba(168,34,52,.25)}
.%(p)s[data-f="h"] i:not(.h),.%(p)s[data-f="he"] i:not(.he){
  opacity:.18 !important;animation:none !important;}

@media (max-width:820px){
  .%(p)s-stage{gap:16px;margin:14px 2px 4px}
  .%(p)s-grid{gap:6px}.%(p)s-grid i{max-width:22px}
  .%(p)s-gh{flex:1 1 100%%;padding:12px 13px;gap:12px}
  .%(p)s-gd{width:46px;height:46px}.%(p)s-gd i{width:15px;height:15px}
  .%(p)s-gd i::after{inset:15px}
  .%(p)s-gt{font-size:.82rem}.%(p)s-gt b{font-size:1.06rem}
  .%(p)s-leg{gap:6px;margin:14px 2px 0}
  .%(p)s-leg span{padding:6px 10px;font-size:.82rem}
}
""" % {'p': P, 'c': COLS,
       'tw': '\n'.join('.%s-grid i.t%d{animation-delay:%.2fs}' % (P, k, k * .7)
                       for k in range(TWINKLE))}

DET = {
    'h': 'ふつうの星は、ほとんどが<b>水素</b>のかたまりです。'
         '「星をひとつあげる」と言ってバケツですくってきたら、'
         '中身はほぼ水素ガスだった——というのは冗談ではなく本当のことです。',
    'he': '<b>ヘリウム</b>は水素の次に多い元素です。'
          'そのほとんどは、宇宙が生まれて 3 分ほどのあいだに水素から作られました。',
    'ot': 'その他ぜんぶを合わせても、<b>点 0.1 個ぶん</b>にしかなりません。'
          '点 1 個にするには、原子を 1000 個ならべる必要があります。'
          'そのわずかな中に、炭素も酸素もケイ素も鉄も、'
          'そして皆さんの体を作っている元素が全部入っています。',
}


def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, 'バケツ一杯の星をすくうと、中身はほとんど水素',
                        '点 100 個が、宇宙にある原子 100 個ぶんです。'
                        '下の札にカーソルを合わせる（スマホはタップ）と、'
                        'その仲間だけが残ります。'),
         '<div class="%s-stage">' % P, '<div class="%s-grid">' % P]

    for i in range(N_H):
        o.append('<i class="h t%d"></i>' % (i % TWINKLE))
    for i in range(N_HE):
        o.append('<i class="he"></i>')
    o.append('</div>')

    # 100 個では出てこない「その他」を、0.1 個ぶんの点として脇に置く
    o.append('<div class="%s-gh" data-detail="%s">'
             '<div class="%s-gd"><i></i></div>'
             '<p class="%s-gt"><b>0.1 個</b>その他ぜんぶ。'
             '100 個では<b style="display:inline;font-size:1em;margin:0">'
             '1 個も出てきません</b>。'
             '点 1 個にするには、1000 個ならべる必要があります。</p>'
             '</div>' % (P, DET['ot'], P, P))
    o.append('</div>')

    o.append('<div class="%s-leg">' % P)
    for key, cls, name, n in (('h', 'lh', '水素', '92'),
                              ('he', 'lhe', 'ヘリウム', '8'),
                              (None, 'lot', 'その他ぜんぶ', '0.1')):
        f = ' data-f="%s"' % key if key else ''
        o.append('<span class="%s"%s data-detail="%s">'
                 '<u></u>%s <em>%s</em> 個</span>'
                 % (cls, f, DET[key or 'ot'], name, n))
    o.append('</div>')

    o.append(efig.close_card(
        P,
        '宇宙にある原子を 100 個ならべると、<b>92 個が水素</b>、'
        '8 個がヘリウム。そして<b>その他ぜんぶは、1 個も出てきません</b>。'
        '炭素も酸素も鉄も金も、この 100 個には顔を出さないのです。'
        '星も、太陽も、その正体はほとんど水素のかたまりです。',
        '個数の比です。重さで比べると水素 74 %・ヘリウム 25 %・その他 1 % ほどに'
        'なります（原子 1 個の重さが元素ごとに違うためです）。'
        'Lodders (2003)、Asplund et al. (2009) による概数。',
        CID))

    # 凡例にカーソルを合わせている間だけ絞り込む。data-f を持つ札のみ
    o.append("""
<script>
(function(){
  var r=document.getElementById('%(id)s');if(!r)return;
  r.querySelectorAll('.%(p)s-leg span[data-f]').forEach(function(s){
    function on(){r.setAttribute('data-f',s.getAttribute('data-f'));}
    function off(){r.removeAttribute('data-f');}
    s.addEventListener('mouseenter',on);s.addEventListener('click',on);
    s.addEventListener('mouseleave',off);
  });
})();
</script>""" % {'p': P, 'id': CID})
    return '\n'.join(o)


if __name__ == '__main__':
    efig.save('_fig1_abundance.qmd', build())
