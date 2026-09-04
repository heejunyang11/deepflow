# -*- coding: utf-8 -*-
"""
元素シリーズ / 検証依頼パックを作る。

なぜ要るか:
  #1 水素の「DNAは細胞分裂のときスルスルほどける」は事実として誤りだった
  （実際はヘリカーゼが ATP を使ってこじ開けている）。これは書いた本人には
  見つけられない種類の誤りで、**書いていない第三者**が読んで初めて出た。
  一方、分かりにくさ（未定義の語・説明の順番）は HY が読んで初めて出た。
  数値と型の誤りは機械で出る。三者で守備範囲が違う。

作り方の原則:
  **こちらで主張を選ばない。** 選ぶと、自分が間違っていると思っていない文を
  リストから落としてしまう（DNA の一文がまさにそれだった）。
  よって本文は全文を、節ごと・文番号つきで渡す。数値を含む文に印をつけるだけ。

使い方:
  python make_review_packet.py element-03-oxygen
  -> _review/element-03-oxygen.md ができる。これを丸ごと貼って検証を頼む。

**出力先が _review/ なのは、Quarto に拾わせないため。**
posts/ 配下に .md を置くと listing が記事として収集し、
サイトに「検証のお願い」というページが出てしまう（2026-08-26 に実際に起きた。
_site/ に HTML が生成され、sitemap.xml と search.json にも載った）。
Quarto は先頭が _ のディレクトリを出力対象から外すので、そこへ逃がす。

出力: _review/<フォルダ名>.md
"""
import io
import os
import re
import sys

NUMPAT = re.compile(r'[0-9０-９]|[％%]|倍|分の|万|億|兆')

INSTRUCTIONS = u"""# 検証のお願い

この記事の**事実の正しさ**だけを見てください。文章の良し悪しは対象外です。

## 読者像

日本語で読む**高校生と、理科を専門にしない大人**です。中学生も読みます。
数式は出しません。専門用語は、出すなら必ずその場で日常の言葉に言い換えています。

## 判定の区分（必ずこの3つに分けてください）

| 区分 | 意味 |
|---|---|
| **誤り** | 事実として違う。書き直しが要る |
| **簡略化** | 粗いが、向きは合っている。読者が持ち帰る像は間違っていない |
| **追加提案** | 直す必要はないが、足せばより正確・より面白くなる |

## 守っていただきたいこと

1. **「入門向けだから」は、簡略化を許す理由にはなっても、誤りを許す理由にはなりません。**
   対象読者が誰であっても、事実として違うものは「誤り」に入れてください。
2. **一度「誤り」と判定したものを、対象読者を理由に取り下げないでください。**
   区分が違うだけで、指摘そのものは残ります。
3. **「追加提案」は積極的に別枠へ回してください。** 入門記事に仕組みを一つ足す提案は、
   たいてい記事を良くするより難しくします。修正と混ぜないでください。
4. 迷ったものは「**判断できない**」と書いてください。無理に3区分へ入れないでください。

## 出力の形

区分ごとにまとめ、**文番号**（下の本文についている番号）で場所を示してください。
「誤り」については、**何が正しいのか**を一行で書いてください。

---
"""


def sentences(text):
    """日本語の文に割る。—— と 。で切り、記号だけの行は捨てる。"""
    t = re.sub(r'\{\{<[^>]*>\}\}', '', text)
    t = re.sub(r'-{5,}', '', t)
    t = re.sub(r'::: *\{[^}]*\}', '', t)
    t = t.replace(':::', '')
    out = []
    for para in re.split(r'\n\s*\n', t):
        p = para.strip()
        if not p or p.startswith('#'):
            continue
        p = re.sub(r'\s+', ' ', p)
        for s in re.split(r'(?<=。)', p):
            s = s.strip()
            if len(re.sub(r'[\s*>|\-—]', '', s)) >= 4:
                out.append(s)
    return out


def figure_sources(folder, body):
    """図の出典行を拾う。すでに根拠を示してある箇所を検証側に見せるため。"""
    out = []
    for inc in re.findall(r'\{\{< include (\S+) >\}\}', body):
        if inc == '_nav.qmd':
            continue
        p = os.path.join(folder, inc)
        if not os.path.exists(p):
            continue
        s = io.open(p, encoding='utf-8').read()
        m = re.search(r'<p class="[^"]*-src">(.*?)</p>', s, re.S)
        if m:
            txt = re.sub(r'<[^>]+>', '', m.group(1))
            out.append((inc, re.sub(r'\s+', ' ', txt).strip()))
    return out


def build(folder):
    idx = os.path.join(folder, 'index.qmd')
    src = io.open(idx, encoding='utf-8').read()
    fm, body = src.split('---', 2)[1], src.split('---', 2)[2]
    title = re.search(r'^title: "(.+)"$', fm, re.M).group(1)

    o = [INSTRUCTIONS, u'# 記事：%s\n' % title]

    # 節ごとに、文番号をつけて全文
    o.append(u'## 本文（全文・文番号つき）\n')
    o.append(u'数字や単位を含む文には **[数]** の印がついています。'
             u'印のない文にも仕組みの主張は入っているので、'
             u'**印だけを見ないでください。**\n')
    n = 0
    chunks = re.split(r'^(#{2,3} .+)$', body, flags=re.M)
    head = None
    for c in chunks:
        if re.match(r'^#{2,3} ', c or ''):
            head = c.strip()
            if 'もっと知りたい人へ' in head:
                head = None
                break
            o.append(u'\n### %s\n' % head.lstrip('# '))
            continue
        if head is None and n == 0:
            # 前書き（見出しの前）
            ss = sentences(c)
            if ss:
                o.append(u'\n### （書き出し）\n')
        for s in sentences(c or ''):
            n += 1
            flag = u' **[数]**' if NUMPAT.search(s) else u''
            o.append(u'%d. %s%s' % (n, s, flag))

    # 図の出典行
    figs = figure_sources(folder, body)
    if figs:
        o.append(u'\n## 図につけてある出典（参考）\n')
        o.append(u'本文の数値の根拠は、ここに書いてあります。'
                 u'**この記述自体が正しいかどうかも見てください。**\n')
        for name, txt in figs:
            o.append(u'- **%s**：%s' % (name, txt))

    # 記事末尾の参考文献
    m = re.search(r'## もっと知りたい人へ\n(.*?)(?:\{\{< include|\Z)', body, re.S)
    if m:
        o.append(u'\n## 記事末尾の「もっと知りたい人へ」\n')
        o.append(m.group(1).strip())

    # Quarto に拾われない場所へ出す（先頭が _ のディレクトリは出力対象外）
    here = os.path.dirname(os.path.abspath(__file__))
    outdir = os.path.join(here, '_review')
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    out = os.path.join(outdir, '%s.md' % os.path.basename(folder.rstrip('/\\')))
    io.open(out, 'w', encoding='utf-8', newline='\n').write(u'\n'.join(o))
    print(u'saved %-40s  文 %d ／ うち数値を含む文 %d ／ %.1f KB'
          % (os.path.relpath(out, here), n,
             sum(1 for l in o if l.endswith(u'**[数]**')),
             os.path.getsize(out) / 1024.0))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: python make_review_packet.py element-03-oxygen')
        sys.exit(1)
    build(sys.argv[1])
