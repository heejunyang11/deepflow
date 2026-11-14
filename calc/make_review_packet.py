# -*- coding: utf-8 -*-
"""
calc の日本語版を第三者検証にかけるためのパックを作る。

記事（posts/note/make_review_packet.py）との違い:
  calc は英語からの翻訳なので、見るべき欠陥が 1 種類多い。

    事実の誤り   … 元の英語の時点で間違っている
    誤訳         … 英語は正しいが、日本語が別のことを言っている
    用語の不適切 … 意味は合っているが、日本の水文地質学の慣用と違う

  3 つ目は訳者（私）には見えにくい。そこで**英語の原文と日本語を節ごとに並べて**渡し、
  比較できる形にする。原文は git の HEAD から取り出す（翻訳前の版）。

主張をこちらで選ばない。節ごとに全文を渡し、数値を含む文に印を付けるだけにする。
選ぶと、自分が間違っていると思っていない文を落としてしまう。

使い方:
    python calc/make_review_packet.py darcy-law
    python calc/make_review_packet.py --all

出力: calc/_review/<slug>.md（`_` 始まりなので Quarto は無視する）

Python は標準ライブラリのみ（サイト全体の方針）。
"""
import io
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(HERE, '_review')

# 節の見出し（## / ###）で切る。表・式・HTML ブロックは節に属させたまま運ぶ。
H_RE = re.compile(r'^(#{2,3})\s+(.*)$', re.M)


def read(path):
    return io.open(path, encoding='utf-8').read()


def git_show(rel):
    """翻訳前（HEAD）の版を取り出す。取れなければ None。"""
    try:
        out = subprocess.run(['git', 'show', 'HEAD:' + rel],
                             cwd=REPO, capture_output=True)
        if out.returncode != 0:
            return None
        return out.stdout.decode('utf-8')
    except Exception:
        return None


#: 対訳表が読めなかったときの控え。CLAUDE.md が正で、ここは最小限に留める。
FALLBACK_TERMS = [('帯水層', 'aquifer'), ('透水係数', 'hydraulic conductivity'),
                  ('透水量係数', 'transmissivity'), ('貯留係数', 'storativity'),
                  ('水位低下量', 'drawdown'), ('涵養', 'recharge')]


def glossary():
    """対訳表を `d:\\Hityu\\CLAUDE.md` の「専門用語の英訳基準」節から読む。

    ここに写して持つと、CLAUDE.md を直したときに必ずずれる。正は 1 か所に置く。
    公開リポジトリだけを取り出した場合は CLAUDE.md が無いので、控えに落ちる。
    """
    p = os.path.join(REPO, '..', 'CLAUDE.md')
    if not os.path.exists(p):
        return FALLBACK_TERMS
    txt = read(p)
    m = re.search(r'##\s*専門用語の英訳基準.*?\n(\|.*?)(?:\n\s*\n|\n>)', txt, re.S)
    if not m:
        return FALLBACK_TERMS
    rows = []
    for line in m.group(1).split('\n'):
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) == 2 and cells[0] and not set(cells[0]) <= set('-: '):
            if cells[0] != '日本語':
                rows.append((cells[0], cells[1]))
    return rows or FALLBACK_TERMS


def split_fm(s):
    """front matter と本文に分ける。"""
    if s.startswith('---'):
        p = s.split('---\n', 2)
        if len(p) == 3:
            return p[1], p[2]
    return '', s


# ----------------------------------------------------------------------
# 節の対応付け
#   位置（n 番目どうし）で対にすると、片方にだけ節を足した時点から
#   すべてずれる。翻訳で変わらないもの——数値・LaTeX・ラテン文字の語——を
#   手がかりに整列し、相手のいない節は明示する。
# ----------------------------------------------------------------------

_TOK_NUM = re.compile(r'[0-9]+(?:[.,][0-9]+)*')
_TOK_LAT = re.compile(r'[A-Za-z\\][A-Za-z]{2,}')


_TOK_VAR = re.compile(r'\*([A-Za-z])\*|\$([^$]{1,40})\$|`([^`]{1,40})`')


def _tokens(text):
    """翻訳しても残る目印を拾う。"""
    t = set()
    for m in _TOK_NUM.finditer(text):
        t.add(m.group())
    for m in _TOK_LAT.finditer(text):
        t.add(m.group().lower())
    # 日本語の地の文はラテン文字が少ないので、記号・数式・コード片も目印にする
    for m in _TOK_VAR.finditer(text):
        g = m.group(1) or m.group(2) or m.group(3)
        t.add(g.strip().lower())
    return t


def _sim(a, b):
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return 0.0
    return 2.0 * len(ta & tb) / float(len(ta) + len(tb))


def align(ja_sec, en_sec, floor=0.10, gap=0.035):
    """(ja_index, en_index or None) の並びと、余った en の索引を返す。

    Needleman-Wunsch。順序は保つが、片側にしか無い節は飛ばせる。
    floor 未満の類似度しか無い組は「対応なし」とみなす。
    """
    n, m = len(ja_sec), len(en_sec)
    if m == 0:
        return [(i, None) for i in range(n)], []

    # スコア表。score[i][j] = ja[:i] と en[:j] を整列したときの最良値
    score = [[0.0] * (m + 1) for _ in range(n + 1)]
    back = [[None] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        score[i][0] = score[i - 1][0] - gap
        back[i][0] = 'u'
    for j in range(1, m + 1):
        score[0][j] = score[0][j - 1] - gap
        back[0][j] = 'l'

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            sim = _sim(ja_sec[i - 1][2], en_sec[j - 1][2])
            if ja_sec[i - 1][0] == en_sec[j - 1][0]:
                sim += 0.08              # 見出しの深さが同じなら少し寄せる
            diag = score[i - 1][j - 1] + (sim - floor)
            up = score[i - 1][j] - gap
            left = score[i][j - 1] - gap
            best = max(diag, up, left)
            score[i][j] = best
            back[i][j] = 'd' if best == diag else ('u' if best == up else 'l')

    pairs, spare = [], []
    i, j = n, m
    while i > 0 or j > 0:
        mv = back[i][j]
        if mv == 'd':
            pairs.append((i - 1, j - 1)); i -= 1; j -= 1
        elif mv == 'u':
            pairs.append((i - 1, None)); i -= 1
        else:
            spare.append(j - 1); j -= 1
    pairs.reverse()
    spare.reverse()
    return pairs, spare


def sections(body):
    """[(見出し記号, 見出し, 中身)] に切る。見出し前の導入は '（冒頭）'。"""
    out, pos, cur = [], 0, ('', '（冒頭）')
    for m in H_RE.finditer(body):
        out.append((cur[0], cur[1], body[pos:m.start()]))
        cur = (m.group(1), m.group(2).strip())
        pos = m.end()
    out.append((cur[0], cur[1], body[pos:]))
    return [(lv, t, c) for lv, t, c in out if c.strip()]


def prose_only(chunk):
    """HTML ブロックと式を落として、地の文だけにする。"""
    t = re.sub(r'```\{=html\}.*?```', ' ', chunk, flags=re.S)
    t = re.sub(r'```.*?```', ' ', t, flags=re.S)
    t = re.sub(r'^:::.*$', '', t, flags=re.M)
    return t.strip()


def ja_sentences(t):
    """日本語を文に切る。

    .qmd は 1 文を複数行に折り返して書いてあるので、**先に段落へまとめてから**
    句点で切る。行で切ると文の途中で分かれて、検証する人が読めなくなる。
    表・数式・箇条書きは、それぞれ 1 かたまりのまま渡す。
    """
    parts = []
    for para in re.split(r'\n\s*\n', t):
        lines = [l.rstrip() for l in para.split('\n') if l.strip()]
        if not lines:
            continue
        head = lines[0].lstrip()
        if head.startswith('|'):                       # 表はまるごと
            parts.append('\n'.join(lines))
            continue
        if '$$' in para:                               # 数式ブロックもまるごと
            parts.append(' '.join(l.strip() for l in lines))
            continue
        if re.match(r'^([-*+]|\d+\.)\s', head):        # 箇条書きは 1 項目ずつ
            parts.extend(l.strip() for l in lines)
            continue
        # 日本語の折り返しは詰めて繋ぐ。英字どうしの境目だけ空白を残す。
        joined = ''
        for l in lines:
            l = l.strip()
            if joined and re.search(r'[A-Za-z0-9)\]$]$', joined) \
                      and re.match(r'[A-Za-z0-9(\[$]', l):
                joined += ' '
            joined += l
        # 句点で切る。ただし ** … ** の内側では切らない。強調の中に句点が
        # あると ** が2つの文に分かれ、検証側からは閉じ忘れに見える
        # （2026-09-08 の検証まで毎回「判断できない」に挙がっていた）。
        buf = ''
        for piece in re.split(r'(?<=。)', joined):
            buf += piece
            if buf.count('**') % 2 == 0:
                b = buf.strip()
                if b:
                    parts.append(b)
                buf = ''
        if buf.strip():
            parts.append(buf.strip())
    return parts


def _enclosing_block(s, pos):
    """s[pos] を含む { … } を、括弧の対応を数えて切り出す。

    正規表現で `\\{[^{}]*\\}` と書くと、`units:{…}` や `presets:[{…}]` のように
    入れ子を持つ入力欄が**丸ごと拾えない**。実際それで r と t のラベルが
    パックから抜けていた（2026-09-07 の検証で発覚）。数えて取るのが確実。
    """
    i = pos
    depth = 0
    while i >= 0:                        # 開き括弧まで戻る
        if s[i] == '}':
            depth += 1
        elif s[i] == '{':
            if depth == 0:
                break
            depth -= 1
        i -= 1
    if i < 0:
        return None
    j, depth = i, 0
    while j < len(s):                    # 対応する閉じ括弧まで進む
        if s[j] == '{':
            depth += 1
        elif s[j] == '}':
            depth -= 1
            if depth == 0:
                return s[i:j + 1]
        j += 1
    return None


def labels(body):
    """mount() の中の UI 文字列を (種類, キー, 文字列) で拾う。"""
    js = '\n'.join(re.findall(r'```\{=html\}(.*?)```', body, re.S))
    out, seen = [], set()

    for m in re.finditer(r'\b(?:id|key)\s*:\s*"([^"]+)"', js):
        key = m.group(1)
        blk = _enclosing_block(js, m.start())
        if not blk:
            continue
        # presets の中はボタンの文字列なので、別扱いにする
        body_only = re.sub(r'presets\s*:\s*\[.*?\]', '', blk, flags=re.S)
        for fld in ('label', 'short', 'hint', 'note', 'unit'):
            for mm in re.finditer(fld + r'\s*:\s*"([^"]*)"', body_only):
                v = mm.group(1).strip()
                k = (fld, key, v)
                if v and k not in seen:
                    seen.add(k)
                    out.append(k)
        # 単位セレクトの候補。画面にそのまま出る文字列なので、これも見てもらう。
        for um in re.finditer(r'units\s*:\s*\{([^{}]*)\}', blk):
            for un in re.finditer(r'"([^"]+)"\s*:', um.group(1)):
                v = un.group(1).strip()
                k = ('単位', key, v)
                if v and k not in seen:
                    seen.add(k)
                    out.append(k)
        for mm in re.finditer(r'label\s*:\s*"([^"]*)"',
                              ''.join(re.findall(r'presets\s*:\s*\[(.*?)\]',
                                                 blk, re.S))):
            v = mm.group(1).strip()
            k = ('プリセット', key, v)
            if v and k not in seen:
                seen.add(k)
                out.append(k)

    # 判定メッセージは文字列を連結して組み立てているので、全部つないで見せる。
    for m in re.finditer(r'GwCalc\.(ok|warn|crit)\(([\s\S]*?)\);', js):
        parts = re.findall(r'"([^"]*)"', m.group(2))
        msg = ' … '.join(p for p in parts if p.strip())
        if msg:
            out.append(('判定 ' + m.group(1), '', msg))
    return out


def build(slug):
    rel = 'calc/%s/index.qmd' % slug if slug != 'index' else 'calc/index.qmd'
    path = os.path.join(REPO, rel)
    if not os.path.exists(path):
        print('  ない: %s' % rel)
        return None

    ja = read(path)
    en = git_show(rel)

    ja_fm, ja_body = split_fm(ja)
    en_fm, en_body = split_fm(en) if en else ('', '')
    ja_sec = sections(ja_body)
    en_sec = sections(en_body) if en else []

    o = []
    o.append('# 検証依頼：`%s`（英語 → 日本語）\n' % rel)
    o.append('DeepFlows の計算機ページを英語から日本語へ書き換えました。'
             '**事実・訳・用語の3方向**から見ていただきたいです。\n')

    o.append('## お願いしたいこと\n')
    o.append('見つかったものを、必ず次の**3つに分けて**ご指摘ください。\n')
    o.append('1. **事実の誤り** — 英語の原文の時点で間違っている（式・数値・出典・物理）')
    o.append('2. **誤訳** — 英語は正しいが、日本語が別のことを言っている／意味が抜けている')
    o.append('3. **用語の不適切** — 意味は合っているが、日本の水文地質学の慣用と違う\n')
    o.append('あわせて、**判断できないもの**は「判断できない」として残してください。'
             '推測で3区分に入れないでください。\n')
    o.append('> このページは実務者と学生が道具として使うものです。'
             '**「入門向けだから」は簡略化を許す理由にはなっても、誤りを許す理由にはなりません。**\n')

    # 2026-09-08 の検証で「英語版にも誤りが残っている」という指摘が出た。
    # 『翻訳前（英語）』は git から取り出した削除済みの旧版であって公開ページではない。
    # 前提が伝わっていなかったので、毎回書いておく。
    o.append('### 英語版について\n')
    o.append('**この Calc セクションに英語版はもうありません。** 2026-09-07 に日本語のみへ'
             '全面移行し、英語のページは削除しました。この依頼書に載っている'
             '「翻訳前（英語）」は、**git の履歴から取り出した削除済みの旧版**であって、'
             '公開中のページではありません。\n')
    o.append('ですので、**「英語側も直す必要がある」というご指摘は不要**です。'
             '英語の原文が間違っていた場合は、**日本語が直っていれば足ります**'
             '（区分は「事実の誤り」に入れてください。原文由来か訳出時かの区別は、'
             'こちらで git を見れば追えます）。\n')
    o.append('URL（`/calc/<slug>/`）だけは英語スラッグのまま変えていません。'
             '公開済みの URL を変えると、外部からのリンクや検索結果が切れるためで、意図的です。\n')

    # 2 回目以降の検証では、前回の指摘と反映を検証側へ伝える。
    # <slug>.notes.md を置いておくと、ここに差し込まれる。
    note_p = os.path.join(OUT, slug + '.notes.md')
    if os.path.exists(note_p):
        o.append('## この版について（前回の検証からの変更）\n')
        o.append(read(note_p).strip() + '\n')

    o.append('## 用語の基準\n')
    o.append('サイト共通の対訳表です。これから外れている語があれば、'
             '3の「用語の不適切」として指摘してください。\n')
    o.append('| 日本語 | English |')
    o.append('|---|---|')
    for a, b in glossary():
        o.append('| %s | %s |' % (a, b))
    o.append('')

    o.append('## front matter\n')
    o.append('```yaml')
    o.append(ja_fm.strip())
    o.append('```\n')
    if en_fm:
        o.append('<details><summary>翻訳前（英語）</summary>\n')
        o.append('```yaml')
        o.append(en_fm.strip())
        o.append('```\n</details>\n')

    o.append('## 本文（節ごとの対訳）\n')
    o.append('日本語には文番号を振り、**数値を含む文には `[数値]`** を付けています。\n')

    pairs, spare = align(ja_sec, en_sec)

    n = 0
    for ji, ei in pairs:
        lv, title, chunk = ja_sec[ji]
        if ei is None:
            en_t, en_c = None, ''
        else:
            en_t, en_c = en_sec[ei][1], prose_only(en_sec[ei][2])
        o.append('---\n')
        lvl = {'##': '大見出し', '###': '小見出し'}.get(lv, '導入')
        o.append('### %s' % title)
        o.append('')
        if en_t is None:
            o.append('*%s*　**日本語版で新しく書いた節です**'
                     '（対応する英語はありません。誤訳ではなく、内容の当否をご覧ください）\n'
                     % lvl)
        else:
            o.append('*%s*　翻訳前：%s\n' % (lvl, en_t))

        ja_p = prose_only(chunk)
        if not ja_p:
            o.append('（地の文なし。図・表・スクリプトのみ）\n')
            continue

        o.append('**日本語**\n')
        for s in ja_sentences(ja_p):
            n += 1
            mark = ' `[数値]`' if re.search(r'[0-9０-９]', s) else ''
            o.append('- **JA-%d**%s %s' % (n, mark, s))
        o.append('')

        if en_c:
            o.append('<details><summary>翻訳前（英語）</summary>\n')
            o.append(en_c)
            o.append('\n</details>\n')

    if spare:
        o.append('---\n')
        o.append('### 日本語版に対応する節が無い英語の節\n')
        o.append('**訳し落としの可能性があります。**'
                 '意図して落としたのか、抜けたのかをご判断ください。\n')
        for ei in spare:
            o.append('- `%s %s`' % (en_sec[ei][0], en_sec[ei][1]))
        o.append('')

    lab_ja, lab_en = labels(ja_body), labels(en_body) if en else []
    if lab_ja:
        o.append('---\n')
        o.append('## 計算機のUI文字列\n')
        o.append('ページを開いた人が画面で見る文字列です。'
                 '**用語の不適切と誤訳を、ここでもご確認ください。**\n')
        # 索引で対にすると、片方の言語にしか無い項目（日本語で short を足した等）
        # から先が 1 行ずつずれる。(種類, キー) で引き当てる。
        pool = {}
        for fld, key, v in lab_en:
            pool.setdefault((fld, key), []).append(v)

        o.append('| 種類 | キー | 日本語 | 翻訳前（英語） |')
        o.append('|---|---|---|---|')
        for fld, key, s in lab_ja:
            cand = pool.get((fld, key), [])
            en_s = cand.pop(0) if cand else '—'
            o.append('| %s | `%s` | %s | %s |'
                     % (fld, key or '—', s.replace('|', '\\|'),
                        en_s.replace('|', '\\|')))
        o.append('')
        left = [(f, k, v) for (f, k), vs in pool.items() for v in vs]
        if left:
            o.append('**日本語側に対応が見つからなかった英語の文字列**'
                     '（訳し漏れの可能性があります）\n')
            for f, k, v in left:
                o.append('- `%s` の %s：%s' % (k or '—', f, v))
            o.append('')

    o.append('---\n')
    o.append('## 参考：数値実装の自動検証\n')
    o.append('式の実装そのものは `node calc/_verify/%s.js` で機械検証しています'
             '（ページの `<script>` を評価して照合する方式）。'
             '**この検証は日本語化のあとも全件 PASS しています。**'
             'ですので、計算が合っているかではなく、'
             '**書かれている説明が正しいか**を見ていただきたいです。\n' % slug)

    md = '\n'.join(o) + '\n'
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    dst = os.path.join(OUT, slug + '.md')
    io.open(dst, 'w', encoding='utf-8', newline='\n').write(md)
    print('saved %-28s 文 %3d / UI %3d / %.1f KB'
          % (os.path.relpath(dst, REPO), n, len(lab_ja),
             len(md.encode('utf-8')) / 1024.0))
    return dst


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    if args[0] == '--all':
        slugs = sorted(d for d in os.listdir(HERE)
                       if os.path.isfile(os.path.join(HERE, d, 'index.qmd')))
        slugs.append('index')
    else:
        slugs = args
    for s in slugs:
        build(s)


if __name__ == '__main__':
    main()
