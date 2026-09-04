# -*- coding: utf-8 -*-
"""
元素シリーズの前後リンクを、全記事ぶんまとめて書き出す。

連載の並びをこのファイル 1 箇所だけで持つ。記事を増やすときは SERIES に
1 行足して回し直せば、前後のリンクが全部つながる。1 本ずつ手で書くと
必ずどこかがずれるので、そうしない。

タイトルは各記事の front matter から読む（手で写さない）。
「｜元素の話 #N」の後ろは表示に要らないので落とす。

まだ公開していない回はリンクにせず、「準備中」の札にする。
存在しない URL を踏ませないため。

出力: 各記事フォルダの _nav.qmd
"""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = '/posts/note/'          # サイト内リンクは拡張子なし（CLAUDE.md の規約）

# (フォルダ名, 回の表示, 未公開のときの仮タイトル)
# 公開済みならタイトルは index.qmd から読むので、第3欄は使われない。
SERIES = [
    ('element-00-periodic-table', '#0', None),
    ('element-01-hydrogen',       '#1', None),
    ('element-02-carbon',         '#2', None),
    ('element-03-oxygen',         '#3', None),
    ('element-04-nitrogen',       '#4', None),
    ('element-05-silicon',        '#5', 'ケイ素（Si）— 砂から、計算する道具へ'),
]

CSS = """
<style>
.enav{--ink:#2B2621;--dim:#5F5546;--faint:#7A6E5C;--hb:#BE640A;
  --card:#FFFDF9;--line:#E7DECC;
  display:grid;grid-template-columns:1fr 1fr;gap:12px;
  margin:2.6rem 0 0;padding-top:1.8rem;
  border-top:1px solid var(--line);
  font-family:"Hiragino Sans","Yu Gothic","Noto Sans JP","Meiryo",sans-serif;}
.enav-c{display:flex;flex-direction:column;gap:5px;
  padding:15px 17px;border-radius:13px;
  background:var(--card);border:1px solid var(--line);
  box-shadow:0 1px 2px rgba(96,74,42,.05);
  text-decoration:none;color:var(--ink);
  transition:border-color .17s ease,box-shadow .17s ease,transform .17s ease;}
a.enav-c:hover{border-color:var(--hb);
  box-shadow:0 1px 2px rgba(96,74,42,.05),0 12px 24px -18px rgba(96,74,42,.5);
  transform:translateY(-2px);}
a.enav-c:focus-visible{outline:2px solid var(--hb);outline-offset:2px;}
.enav-next{text-align:right;}

/* 継承色に負けないよう、要素セレクタを含む形で指定する */
.enav .enav-lb{font-size:.78rem;font-weight:700;letter-spacing:.06em;
  color:var(--hb);}
.enav .enav-no{font-size:.72rem;font-weight:700;color:var(--faint);
  font-variant-numeric:tabular-nums;}
.enav .enav-ti{font-size:.97rem;font-weight:700;line-height:1.55;
  color:var(--ink);}
.enav .enav-soon{font-size:.78rem;color:var(--faint);line-height:1.5;}

/* 未公開の回。リンクにしないので、枠を破線にして触れないことを示す */
.enav-c.is-soon{background:transparent;border-style:dashed;box-shadow:none;}
.enav .is-soon .enav-ti{color:var(--dim);font-weight:400;}

/* 空き枠。#0 には前回がないので、桁を合わせるためだけに置く */
.enav-c.is-void{visibility:hidden;}

.enav-idx{grid-column:1 / -1;margin:4px 0 0;text-align:center;}
/* サイト側の a{color:… !important} には勝てない。
   文字色は中の span に持たせて回避する（図と同じ手）。 */
.enav .enav-idx a{font-size:.86rem;text-decoration:none;
  border-bottom:1px solid rgba(122,96,52,.28);padding-bottom:1px;}
.enav .enav-idx a span{color:var(--faint);}
.enav .enav-idx a:hover{border-bottom-color:var(--hb);}
.enav .enav-idx a:hover span{color:var(--hb);}
.enav .enav-idx a:focus-visible{outline:2px solid var(--hb);outline-offset:3px;}

@media (max-width:640px){
  .enav{grid-template-columns:1fr;gap:9px;margin-top:2.2rem;}
  .enav-c{padding:13px 14px;}
  .enav-c.is-void{display:none;}
  .enav .enav-ti{font-size:.9rem;}
}
</style>
"""


def title_of(folder):
    """front matter の title から、シリーズ名の部分を落として返す。"""
    p = os.path.join(HERE, folder, 'index.qmd')
    if not os.path.exists(p):
        return None
    m = re.search(r'^title:\s*"(.*)"\s*$',
                  io.open(p, encoding='utf-8').read(), re.M)
    if not m:
        return None
    # 「…｜元素の話 #1」の後半は前後リンクでは邪魔になるので落とす
    return m.group(1).split('｜')[0].strip()


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;')
             .replace('>', '&gt;').replace('"', '&quot;'))


def card(item, side):
    """side は 'prev' か 'next'。item が None なら空き枠を返す。"""
    if item is None:
        return '<div class="enav-c is-void" aria-hidden="true"></div>'
    folder, no, fallback = item
    label = '← 前回' if side == 'prev' else '次回 →'
    ttl = title_of(folder)
    if ttl is None:                       # まだ書いていない回
        return ('<div class="enav-c enav-%s is-soon">'
                '<span class="enav-lb">%s</span>'
                '<span class="enav-no">%s</span>'
                '<span class="enav-ti">%s</span>'
                '<span class="enav-soon">準備中</span></div>'
                % (side, label, esc(no), esc(fallback or '')))
    return ('<a class="enav-c enav-%s" href="%s%s/">'
            '<span class="enav-lb">%s</span>'
            '<span class="enav-no">%s</span>'
            '<span class="enav-ti">%s</span></a>'
            % (side, BASE, folder, label, esc(no), esc(ttl)))


def build(i):
    prev = SERIES[i - 1] if i > 0 else None
    nxt = SERIES[i + 1] if i + 1 < len(SERIES) else None
    o = [CSS, '<nav class="enav" aria-label="連載内の移動">',
         card(prev, 'prev'), card(nxt, 'next'),
         '<p class="enav-idx"><a href="/note">'
         '<span>⚛️ 元素の話 — 全体の一覧へ</span></a></p>',
         '</nav>']
    return '```{=html}\n' + '\n'.join(o) + '\n```\n'


def main():
    for i, (folder, _no, _fb) in enumerate(SERIES):
        d = os.path.join(HERE, folder)
        if not os.path.isdir(d):
            print('skip  %s（フォルダなし）' % folder)
            continue
        p = os.path.join(d, '_nav.qmd')
        body = build(i)
        io.open(p, 'w', encoding='utf-8', newline='\n').write(body)
        print('saved %-34s %.1f KB' % (p.replace(HERE + os.sep, ''),
                                       len(body.encode('utf-8')) / 1024.0))


if __name__ == '__main__':
    main()
