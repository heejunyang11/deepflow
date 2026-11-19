# -*- coding: utf-8 -*-
"""
new_tool.py — 新しい計算機ページの雛形を作る。

    python calc/new_tool.py <category> <slug> "<Title>"

    例) python calc/new_tool.py flow theis-solution "Theis Solution Calculator"
        python calc/new_tool.py chemistry charge-balance "Charge Balance Error Calculator"

生成するもの:
    calc/<slug>/index.qmd      ページ本体（ページ構成12項目の枠つき）
    calc/_verify/<slug>.js     数値検証（検証5項目の枠つき）

URL は calc/ 直下のフラット構成で、category は front matter の
`categories:` に入って一覧ページの絞り込みに使われる（URL には出ない）。

Calc セクションは 2026-09-07 から**日本語のみ**である（HY 判断）。雛形も日本語で
出るようにしてある。URL のスラッグだけは英語のまま付けること。

既存ファイルがあれば何もせず終了する。標準ライブラリだけで動く。

書き足すのは compute() と解説文だけになるよう、入力欄の生成・単位換算・
結果の描画・妥当性判定の表示は calc/assets/gwcalc.js が引き受ける。
"""

import os
import re
import sys
from datetime import date

# Windows のコンソールは既定が cp932 で、日本語のメッセージを出すと
# UnicodeEncodeError で落ちる。UTF-8 に切り替えておく。
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

# 一覧ページ（calc/index.qmd）の categories に出るラベル。
# Recharge & streamflow は 2026-08-10 に廃止した（DeepFlows 統合時の HY 判断）。
CATEGORIES = {
    "flow":      "流動",
    "chemistry": "化学",
}


# ----------------------------------------------------------------------
# テンプレート
#   置換は @@NAME@@ の単純置換。qmd 内に JS の { } や $ が多く出るため、
#   format() や string.Template は使わない。
# ----------------------------------------------------------------------

TPL_QMD = '''---
title: "@@TITLE@@"
subtitle: "TODO ひとことで何を計算するか。検索結果にも出るので具体的に。"
description: "TODO 120〜160字。何を計算し、どの単位系に対応し、何を検証するか。キーワードを前に置く。日本語で書く。"
date: @@DATE@@
lang: ja
categories: [@@CATEGORY@@]
number-sections: false
toc-title: "目次"
format:
  html:
    html-math-method: katex
    include-in-header:
      - text: |
          <link rel="stylesheet" href="/calc/assets/gwcalc.css" />
          <link rel="stylesheet" href="/calc/assets/gwcalc-page.css" />
          <script src="/calc/assets/gwcalc.js" defer></script>
# 完成して _verify を通したらこの行を消す。消すまで一覧にも sitemap にも出ない。
draft: true
---

::: {.gw-attest}
[✓ 水文地質学者（Ph.D.）が監修]{.gw-chip .verified}
[SI単位・米国慣用単位に対応]{.gw-chip}
[TODO 適用限界の判定]{.gw-chip}
[出典：TODO]{.gw-chip}
:::

```{=html}
<div id="calc"></div>

<!-- 図を使わないなら <template> ごと消し、mount() の figure: も消す。
     生 HTML は必ずこの ```{=html} ブロックの中に置くこと（外に書くと
     Pandoc がタグを剥がし、図がテキストだけになって出力される）。
     色は属性ではなく必ず CSS クラスで指定する（gwcalc.css の図の節を参照）。 -->
<template id="calc-figure">
  <figure>
    <svg viewBox="0 0 680 320" role="img" aria-labelledby="figTitle figDesc">
      <title id="figTitle">TODO</title>
      <desc id="figDesc">TODO 図が何を示しているかを文章で。読み上げ用。</desc>

      <!-- TODO 作図 -->

    </svg>
    <figcaption>TODO 図の説明。記号が図のどこを指すかを言葉でも書く。</figcaption>
  </figure>
</template>
```

## 何を入れると、何が得られるか

すべての導出量は、キーを打つたびに計算し直しています。**逆算する量**の切り替えは、
見られる量を決めるものではありません。**どれを未知数として扱うか**を決めるだけです。

| 求めたいもの | 入力する量 | どこを読むか |
|---|---|---|
| **TODO** | TODO | 見出しの数字 |
| **TODO** | TODO | TODO |

TODO どの入力がどの出力にしか効かないかを書く。効き方の狭い入力（間隙率が
流量に無関係、粒径が判定にしか使われない、など）は必ずここで断っておく。

## 式が言っていること

TODO その式が生まれた背景と、何を主張しているか。

::: {.gw-eq}
$$TODO$$
:::

TODO 符号や近似が消える箇所は途中式を省かない。微分形 → 有限差分 → 相殺、の
ように段階を式で示すこと。結果だけ書くと検算できないページになる。

### 変数

| 記号 | 意味 | SI単位 | 注意 |
|---|---|---|---|
| *TODO* | TODO | TODO | TODO |

### TODO 取り違えやすい量があればここで対比する

TODO

## TODO 代表値の表（あれば）

TODO 材料別の物性値など。出典（著者・年・表番号）を必ず添える。

## 式が成り立たなくなるとき

TODO 適用限界。どの条件で式が成り立たなくなり、そのとき何を使うべきか。
**この節と `check()` の判定は必ず対応させること。**

::: {.gw-eq}
$$TODO$$
:::

## 例題

::: {.gw-worked}
**問題。** TODO 数値を追える問題。誤りやすい点が現れるものを選ぶ。

1. TODO: `計算式 = 値`
2. TODO

TODO 誤った扱いをすると答えが何倍ずれるかを示す。
:::

## よくある質問

### TODO

TODO

### TODO

TODO

## 関連する計算機

::: {.gw-related}
- [**TODO**<span>TODO</span>](../TODO/)
:::

TODO 公開済みのツールだけを並べる。リンク切れを作らない。4〜6本。

## さらに読む

TODO このツールの背景を書いた DeepFlows の記事へ 1 本だけリンクする。
書き方は `](../../posts/groundwater/groundwater-sciXX/index.qmd)` の .qmd 直リンク。
拡張子なしの絶対パス（/posts/...）で書くと**ローカルプレビューで 404 になる**。
Calc は日本語のみなので、リンク先は日本語版（`index.qmd`）を指すこと。

## 参考文献

::: {.gw-refs}
1. TODO 著者 (年) *書名または論文名.* 出版社/誌名.
:::

::: {.gw-author}
[HY]{.gw-badge}

::: {}
**監修：Heejun Yang, Ph.D.**

地下水の時系列解析と水–岩石反応のモデリングを専門とする水文地質学者です。このページの
式・単位換算・代表値は、上に挙げた文献（原論文と教科書）と突き合わせて確認しています。
:::
:::

```{=html}
<script>
document.addEventListener("DOMContentLoaded", function () {

  /* 図の寸法などの定数・DOM の参照は、必ずここ（mount() より前）に置く。
     mount() は呼ばれたその場で 1 回目の onUpdate() を走らせるので、後ろに書くと
     開いた直後の図が NaN になって描かれない（CALC.md 2026-11-14 の地雷）。 */
  // var X0 = 100, W = 560;

  var api = GwCalc.mount("#calc", {

    figure: "#calc-figure",          // 図を使わないなら削除

    // 逆算を出すなら、入力 id の配列を書く。不要なら削除してよい。
    // solveFor: ["TODO", "TODO"],

    inputs: [
      { id:"TODO", sym:"TODO", label:"TODO", value:"1",
        // step を書いた欄だけスピナーが出る。対数スケールの量には書かないこと
        // （矢印が 1 ずつ動いて無意味になる）。
        min:0, step:0.1,
        units:{ "TODO":1 } }
    ],

    // v は必ず SI 単位に正規化済みで渡ってくる。
    // 全体に効く入力が欠けたときだけ {} を返し、一部にしか効かない入力
    // （間隙率など）はその量だけ NaN にする。全部返さないと編集中に
    // すべての出力が消える。
    compute: function (v, target) {
      if (!(v.TODO > 0)) return {};

      // TODO

      return { };
    },

    // solveFor があるときは { 変数名: {...} }、無いときは単一オブジェクト。
    headline: { key:"TODO", sym:"TODO", label:"TODO", unit:"TODO" },

    // 単位はラベル側に括弧で出る。同じ量を複数単位で並べてよい。
    // 見出しや入力欄と重複する欄は置かない。8 欄前後に収める。
    outputs: [
      { key:"TODO", sym:"TODO", label:"TODO", unit:"TODO" }
    ],

    // 適用限界の判定。必ず 1 つ入れる（このサイトの差別化の核）。
    // 返り値は GwCalc.ok / .warn / .crit のいずれか。
    check: function (r) {
      // TODO
      return GwCalc.ok("TODO");
    },

    // 判定の下に出る補足。そのツール固有の「読み違えやすい点」を書く。
    footnote:
      '<p><span class="gw-key">TODO</span> TODO</p>',

    onUpdate: function (r) {
      // TODO 図を入力に追従させる。図が無ければ削除。
    }
  });

});
</script>
```
'''


TPL_VERIFY = '''/* ---------------------------------------------------------------------------
 * calc/_verify/@@SLUG@@.js — ページに実装した compute() を、そのページに載せた
 * 例題の数値と突き合わせる。
 *
 *   node calc/_verify/@@SLUG@@.js
 *
 * DOM をスタブ化し、.qmd の <script> をそのまま評価して config を捕まえる。
 * 「実装をテストする」ことが要点で、式を書き写して照合するのでは意味がない。
 * ------------------------------------------------------------------------- */

const fs = require("fs");
const path = require("path");
const ROOT = path.join(__dirname, "..");   // = calc/

const TOOL  = "@@SLUG@@";

global.window = global;
require(path.join(ROOT, "assets/gwcalc.js"));

/* ---- mount をスタブ化して config を捕まえる ---- */

let cfg = null;
let firstPaint = null;   // 開いた瞬間の描画の検査（firstpaint.js）
GwCalc.mount = function (sel, c) {
  cfg = c;
  firstPaint = require("./firstpaint.js")(c);
  return { fields: {}, setTarget() {}, update() {} };
};

const stubNode = {
  setAttribute() {}, textContent: "", title: "", dataset: {},
  classList: { add() {}, remove() {} }, addEventListener() {}
};
global.document = {
  addEventListener: (ev, fn) => fn(),
  getElementById: () => stubNode,
  querySelector: () => null,
  querySelectorAll: () => []
};

const qmd = fs.readFileSync(path.join(ROOT, TOOL, "index.qmd"), "utf8");
eval(qmd.match(/<script>([\\s\\S]*?)<\\/script>/)[1]);

if (!cfg) { console.error("mount() が呼ばれなかった"); process.exit(1); }

/* ---- 照合 ---- */

let failed = 0;
let checks = 0;   // 1 件も書かないまま「通った」ことにしないための番人

function near(label, got, want, tol) {
  checks++;
  tol = tol || 1e-3;                                   // 相対誤差
  const ok = Math.abs(got - want) <= Math.abs(want) * tol;
  if (!ok) failed++;
  console.log(
    (ok ? "  PASS  " : "  FAIL  ") + label.padEnd(30) +
    " got " + String(got.toPrecision(6)).padStart(14) +
    "   want " + String(want.toPrecision(6)).padStart(14)
  );
}

function state(label, v, want) {
  checks++;
  const got = cfg.check(cfg.compute(v, null)).state;
  const ok = got === want;
  if (!ok) failed++;
  console.log((ok ? "  PASS  " : "  FAIL  ") + label.padEnd(28) + " -> " + got);
}

// TODO 各群を埋める。5 群すべて必須。

console.log("\\n[1] ページ既定値");
// let r = cfg.compute({ TODO: 1 }, null);
// near("TODO", r.TODO, 0);

console.log("\\n[2] 逆算（solve-for の往復）");
// solveFor が無いツールでは省略してよい。

console.log("\\n[3] ページ掲載の例題");
// 本文の Worked example と同じ入力・同じ答えになることを確かめる。
// ここが合わないなら、本文か実装のどちらかが間違っている。

console.log("\\n[4] 適用限界の判定の境界");
// state("TODO", { TODO: 1 }, "good");
// state("TODO", { TODO: 1 }, "warn");
// state("TODO", { TODO: 1 }, "crit");

console.log("\\n[5] 不正入力で落ちないか");
// 0 除算・範囲外・未入力。全体を止める入力と、一部だけ止める入力を区別する。

if (checks === 0) {
  console.log("\\n" + TOOL + ": 検証がまだ 1 件も書かれていない。TODO を埋めること。");
  process.exit(1);
}
// 番人より後ろに置く（前に置くと 1 件に数えられ、番人が働かなくなる）
checks++;
if (!require("./firstpaint.js").report(firstPaint)) failed++;

console.log("\\n" + (failed === 0
  ? TOOL + ": " + checks + " 件すべて一致した。"
  : TOOL + ": " + checks + " 件中 " + failed + " 件が不一致。"));
process.exit(failed === 0 ? 0 : 1);
'''


# ----------------------------------------------------------------------

def render(tpl, **kw):
    for key, val in kw.items():
        tpl = tpl.replace("@@" + key + "@@", val)
    return tpl


def main(argv):
    if len(argv) != 4:
        print(__doc__)
        return 2

    category, slug, title = argv[1], argv[2], argv[3]

    if category not in CATEGORIES:
        print("カテゴリは次のいずれか: " + ", ".join(CATEGORIES))
        return 2

    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        print("slug は小文字の kebab-case で書くこと（例: theis-solution）。")
        print("URL にそのまま出るので、検索語を含む短い形にする。")
        return 2

    here = os.path.dirname(os.path.abspath(__file__))      # = calc/
    qmd_path = os.path.join(here, slug, "index.qmd")
    ver_path = os.path.join(here, "_verify", slug + ".js")

    for p in (qmd_path, ver_path):
        if os.path.exists(p):
            print("既にある: " + os.path.relpath(p, here).replace("\\", "/"))
            print("上書きはしない。消すか、別の slug にすること。")
            return 1

    os.makedirs(os.path.dirname(qmd_path), exist_ok=True)
    os.makedirs(os.path.dirname(ver_path), exist_ok=True)

    with open(qmd_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(render(TPL_QMD, TITLE=title, DATE=date.today().isoformat(),
                       CATEGORY=CATEGORIES[category]))

    with open(ver_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(render(TPL_VERIFY, SLUG=slug))

    rel_q = "calc/" + os.path.relpath(qmd_path, here).replace("\\", "/")
    rel_v = "calc/" + os.path.relpath(ver_path, here).replace("\\", "/")

    print("作成した:")
    print("  " + rel_q)
    print("  " + rel_v)
    print("")
    print("次にやること:")
    print("  1. " + rel_q + " の TODO を埋める（compute と解説）")
    print("  2. node " + rel_v + "  を通す")
    print("  3. フロントマターの draft: true を消す（消すまで一覧に出ない）")
    print("  4. 既存ツールの Related calculators から相互にリンクする")
    print("     （calc/index.qmd の listing は */index.qmd を自動収集するので触らなくてよい）")
    print("")
    print("URL: /calc/" + slug + "/    カテゴリ: " + CATEGORIES[category])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
