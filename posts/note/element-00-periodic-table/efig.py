# -*- coding: utf-8 -*-
"""
元素シリーズの図の共通土台。

各図は「ダークカード + 見出し + ステージ + 読み取り帯 + 出典」という
同じ骨格を持つ。その骨格の CSS と HTML をここで一手に作る。
図ごとの CSS はそれぞれの gen_figN_*.py が足す。

方針:
  - 位置や数値の計算は Python が済ませて HTML に焼き込む
    → JavaScript が動かなくても図として成立する
  - 見た目と動きは CSS
  - JS は補助（ホバー/タップでの出し分け）だけ
  - 外部依存ゼロ。qmd には ```{=html} ブロックとして貼る
"""
import io

# クラス名は図ごとの接頭辞で必ず区切る。サイト全体の CSS と衝突させないため。
BASE_CSS = """
/* 明暗の三段。カード地 #FDFAF3 に対するコントラスト比は
   ink 14.4 : dim 7.0 : faint 4.8。faint は出典行に使うので、
   小さい字でも読めるよう WCAG AA（4.5:1）を下回らせない。 */
.%(p)s{--ink:#2B2621;--dim:#5F5546;--faint:#7A6E5C;
  --hb:#BE640A;--cov:#0F6C8A;--rt:#B02A37;--vdw:#8C8271;
  --h:#5E96C4;--he:#D69A2E;--other:#C42B3C;--o:#D8552A;--e:#2F6DB2;
  --card:#FFFDF9;--card2:#FDFAF3;--line:#E7DECC;
  --panel:#FAF5EB;--line2:#ECE3D2;--tint:122,96,52;
  position:relative;margin:2.2rem 0;padding:26px 26px 20px;border-radius:18px;
  background:linear-gradient(180deg,var(--card),var(--card2));
  border:1px solid var(--line);
  box-shadow:0 1px 2px rgba(96,74,42,.05),0 14px 30px -20px rgba(96,74,42,.34);
  color:var(--ink);overflow:hidden;
  font-family:"Hiragino Sans","Yu Gothic","Noto Sans JP","Meiryo",sans-serif;}
/* 方眼紙の罫。明色になって初めて意味を持つ装飾なので、暗色版より少し出す。 */
.%(p)s::before{content:"";position:absolute;inset:0;pointer-events:none;
  background:
    linear-gradient(rgba(var(--tint),.07) 1px,transparent 1px) 0 0/100%% 34px,
    linear-gradient(90deg,rgba(var(--tint),.07) 1px,transparent 1px) 0 0/34px 100%%;
  mask-image:radial-gradient(120%% 90%% at 30%% 0%%,#000 30%%,transparent 78%%);}
/* サイト側テーマの p / b / h5 への色指定を打ち消す。
   ただしこの行は要素セレクタを含むので詳細度が (0,1,1) になる。
   図の側の指定も p.〜 の形にして同着にしないと、こちらが勝ってしまう。 */
.%(p)s p,.%(p)s b,.%(p)s strong,.%(p)s h5,.%(p)s span,
.%(p)s em,.%(p)s s,.%(p)s u,.%(p)s i,.%(p)s sub,.%(p)s sup{color:inherit;}
p.%(p)s-h{font-size:1.5rem;font-weight:800;letter-spacing:.01em;
  margin:0 0 5px;color:var(--ink);}
p.%(p)s-s{font-size:.95rem;color:var(--dim);margin:0 0 4px;line-height:1.65;}
.%(p)s-read{margin:2px 8px 0;padding:15px 17px;border-radius:11px;
  background:var(--panel);border:1px solid var(--line2);
  font-size:1rem;line-height:1.85;color:var(--ink);min-height:2.6em;}
.%(p)s-read b{color:var(--hb);}
p.%(p)s-src{margin:12px 8px 0;font-size:.82rem;color:var(--faint);
  line-height:1.7;}
@media (max-width:820px){
  .%(p)s{padding:20px 12px 16px;}
  .%(p)s-h{font-size:1.25rem;}
  .%(p)s-s{font-size:.86rem;}
  .%(p)s-read{font-size:.92rem;margin:2px 2px 0;padding:13px 14px;}
  .%(p)s-src{font-size:.76rem;}
}
@media (prefers-reduced-motion:reduce){.%(p)s *{animation:none !important;}}
"""

# ホバー/タップで読み取り帯を差し替える共通スクリプト。
# data-detail を持つ要素があれば拾う。
HOVER_JS = """
<script>
(function(){
  var r=document.getElementById('%(id)s');if(!r)return;
  var out=r.querySelector('.%(p)s-read');if(!out)return;
  var base=out.innerHTML;
  r.querySelectorAll('[data-detail]').forEach(function(n){
    function on(){out.innerHTML=n.getAttribute('data-detail');}
    n.addEventListener('mouseenter',on);
    n.addEventListener('click',on);
    n.addEventListener('mouseleave',function(){out.innerHTML=base;});
  });
})();
</script>
"""


def attr(s):
    """属性値に入れる文字列を安全にする。

    読み取り帯へ差し替える文章には <b> などのタグが入っている。
    生のまま属性に書くと、SVG の中では XML として不正になる。
    実体参照にしておけば、JavaScript が getAttribute で読み戻したとき
    元の HTML に戻るので、タグはそのまま効く。
    """
    return (s.replace('&', '&amp;').replace('<', '&lt;')
             .replace('>', '&gt;').replace('"', '&quot;'))


def css(prefix, extra=''):
    return '<style>' + (BASE_CSS % {'p': prefix}) + extra + '</style>'


def open_card(prefix, cid, title, sub):
    # fig-wide は styles.css 側で定義。広い画面のとき、図だけ本文より広く見せる
    return ('<div class="%s fig-wide" id="%s">\n'
            '<p class="%s-h">%s</p>\n'
            '<p class="%s-s">%s</p>\n' % (prefix, cid, prefix, title, prefix, sub))


def close_card(prefix, read, src, cid=None, js=True):
    o = '<div class="%s-read">%s</div>\n' % (prefix, read)
    o += '<p class="%s-src">%s</p>\n</div>\n' % (prefix, src)
    if js and cid:
        o += HOVER_JS % {'p': prefix, 'id': cid}
    return o


def save(name, html):
    """.qmd で保存するときは ```{=html} フェンスで包む。

    index.qmd からは {{< include _figN_xxx.qmd >}} で読み込む。
    先頭が _ のファイルは Quarto が単独ページとして出力しないので、
    図の部品置き場として都合がよい。
    """
    body = html
    if name.endswith('.qmd'):
        body = '```{=html}\n' + html + '\n```\n'
    with io.open(name, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(body)
    print('saved %-30s %5.1f KB' % (name, len(body.encode('utf-8')) / 1024.0))
