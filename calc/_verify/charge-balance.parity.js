/* ---------------------------------------------------------------------------
 * _verify/charge-balance.parity.js — イオンバランス計算機の日英2ファイルの一致を照合する。
 *
 * charge-balance.js から呼ばれる（単独でも node で動く）。2026-11-14 に英語版
 * index-en.qmd を足したときに書いた。翻訳は人が読むものだが、次の点は機械で守れる。
 *
 *   ① 計算の実装（ION・field・compute）が日英で一字一句同じであること
 *   ② hreflang が両方のファイルに、同じ組で書かれていること
 *   ③ 英語版に日本語が残っていないこと（本文・front matter・画面に出る文字列）
 *   ④ 本文に出てくる数値が日英で同じであること（訳すときの書き写し誤りを拾う）
 *   ⑤ 式・表・見出し・参考文献の数と中身が対応していること
 *   ⑥ リンク先のファイルが実在すること
 *
 * 数値は機械が守り、言葉は人が読む——この分担は CALC.md の 2026-09-07 の記録と同じ。
 * ------------------------------------------------------------------------- */

const fs = require("fs");
const path = require("path");

module.exports = function parity() {
  const DIR = path.join(__dirname, "..", "charge-balance");
  // 改行は LF に揃える（Windows の作業ツリーでは git の autocrlf で CRLF になっている）
  const read = (f) => fs.readFileSync(path.join(DIR, f), "utf8").replace(/\r\n/g, "\n");
  const ja = read("index.qmd");
  const en = read("index-en.qmd");

  let checks = 0, failed = 0;
  const say = (label, cond, detail) => {
    checks++; if (!cond) failed++;
    console.log((cond ? "  PASS  " : "  FAIL  ") + label + (detail ? "\n          " + detail : ""));
  };

  const CJK = /[぀-ヿ一-鿿！-｠]/;
  const script = (s) => s.match(/<script>([\s\S]*?)<\/script>/)[1];
  const stripComments = (s) => s.replace(/\/\*[\s\S]*?\*\//g, "").replace(/\/\/[^\n]*/g, "");
  const frontMatter = (s) => s.match(/^---\n([\s\S]*?)\n---/)[1];
  // 本文 = front matter・計算機の HTML ブロック（図）・<script> を除いた部分
  const body = (s) => s.replace(/^---\n[\s\S]*?\n---/, "")
                       .replace(/```\{=html\}[\s\S]*?```/g, "");

  /* ① 計算の実装 ------------------------------------------------------- */
  console.log("\n  ① 計算の実装");
  const calcPart = (s) => {
    const js = stripComments(script(s));
    return js.slice(js.indexOf("var ION"), js.indexOf("headline:")).replace(/\s+/g, " ");
  };
  say("ION・field・compute が日英で同一", calcPart(ja) === calcPart(en));
  const drawPart = (s) => {
    const js = stripComments(script(s));
    return js.slice(js.indexOf("var X0"), js.indexOf("$(\"gapLabel\").textContent"))
             .replace(/\s+/g, " ");
  };
  say("図の描画（drawBars）が日英で同一（ラベル文字列を除く）", drawPart(ja) === drawPart(en));
  const thresholds = (s) => (stripComments(script(s)).match(/check:[\s\S]*?footnote:/)[0]
                              .match(/(?:<=?|>=?)\s*[\d.]+/g) || []).join(" ");
  say("判定のしきい値が日英で同一: " + thresholds(en),
      thresholds(ja) === thresholds(en), "ja: " + thresholds(ja));

  /* ② hreflang -------------------------------------------------------- */
  console.log("\n  ② hreflang");
  const HJ = '<link rel="alternate" hreflang="ja" href="https://deepflows.net/calc/charge-balance/" />';
  const HE = '<link rel="alternate" hreflang="en" href="https://deepflows.net/calc/charge-balance/index-en" />';
  [["index.qmd", ja], ["index-en.qmd", en]].forEach(function (p) {
    say(p[0] + " に ja・en の両方がある", p[1].includes(HJ) && p[1].includes(HE));
    say(p[0] + " の hreflang に .html が付いていない", !/hreflang[^>]*\.html/.test(p[1]));
  });
  say("日本語版は lang: ja", /^lang:\s*ja\s*$/m.test(ja));
  say("英語版は lang: en",   /^lang:\s*en\s*$/m.test(en));

  /* ③ 英語版に日本語が残っていないか ------------------------------------ */
  console.log("\n  ③ 英語版に日本語が残っていないか");
  const leftovers = (label, s) => {
    const lines = s.split("\n").filter((l) => CJK.test(l));
    say(label + "：日本語の行 " + lines.length + " 件", lines.length === 0,
        lines.slice(0, 5).map((l) => l.trim().slice(0, 70)).join("\n          "));
  };
  leftovers("front matter", frontMatter(en));
  leftovers("本文", body(en));
  const htmlBlocks = (en.match(/```\{=html\}[\s\S]*?```/g) || [])
                       .map((b) => b.replace(/<script>[\s\S]*?<\/script>/, "")).join("\n");
  leftovers("図（SVG の title・desc・figcaption）", htmlBlocks);
  leftovers("<script> のコード（コメントを除く）", stripComments(script(en)));

  /* ④ 本文の数値 ------------------------------------------------------- */
  console.log("\n  ④ 本文に出てくる数値");
  // 数字の列を取り出す。全角の符号・空白の違いは揃える。
  const nums = (s) => (body(s).replace(/−/g, "-").replace(/＋/g, "+")
                         .match(/[-+]?\d+(?:\.\d+)?/g) || [])
                       .map((x) => x.replace(/^\+/, ""));
  const bag = (arr) => arr.reduce((m, x) => (m[x] = (m[x] || 0) + 1, m), {});
  const nj = bag(nums(ja)), ne = bag(nums(en));
  /* 言語の書き方の違いで生じる差。ここに足すときは理由を必ず書く。
     - 日本語の「8イオン」「1リットル」「2本の棒」は英語で eight / litre / two と綴る
     - 「PHREEQCをゼロから始める #2」の 2 は日英どちらにもある（差にならない） */
  const ALLOWED = {
    "8": "「8イオン」→ eight ions",
    "1": "「1リットルあたり」→ per litre",
    "2": "「2本の棒」「2つの合計」→ two",
    "3": "「3つの量」→ Three quantities",
    "4": "「陽イオン4つ」→ the four cations",
    "10": "「およそ10倍」→ a factor of ten"
  };
  const keys = Array.from(new Set(Object.keys(nj).concat(Object.keys(ne))));
  const diffs = keys.filter((k) => (nj[k] || 0) !== (ne[k] || 0))
                    .map((k) => ({ k: k, ja: nj[k] || 0, en: ne[k] || 0 }));
  const unexplained = diffs.filter((d) => !(d.k in ALLOWED) || d.en > d.ja);
  diffs.forEach(function (d) {
    console.log("          " + (d.k in ALLOWED && d.en <= d.ja ? "（許容）" : "（要確認）") +
                " " + d.k.padStart(8) + "  ja " + d.ja + " / en " + d.en +
                (d.k in ALLOWED ? "  … " + ALLOWED[d.k] : ""));
  });
  say("本文の数値が日英で一致（言語の書き方による差を除く）。数値の種類 " + keys.length,
      unexplained.length === 0);

  /* ⑤ 構成の対応 ------------------------------------------------------- */
  console.log("\n  ⑤ 構成の対応");
  const count = (s, re) => (body(s).match(re) || []).length;
  say("## 見出しの数", count(ja, /^## /gm) === count(en, /^## /gm),
      "ja " + count(ja, /^## /gm) + " / en " + count(en, /^## /gm));
  say("### 見出しの数", count(ja, /^### /gm) === count(en, /^### /gm),
      "ja " + count(ja, /^### /gm) + " / en " + count(en, /^### /gm));
  say("表の行の数", count(ja, /^\|/gm) === count(en, /^\|/gm),
      "ja " + count(ja, /^\|/gm) + " / en " + count(en, /^\|/gm));
  // 式：\text{…} の中（言葉）を除けば同じ式であること
  const eqs = (s) => (body(s).match(/\$\$[\s\S]*?\$\$/g) || [])
                       .map((e) => e.replace(/\\text\{[^}]*\}/g, "\\text{}").replace(/\s+/g, ""));
  const ej = eqs(ja), ee = eqs(en);
  say("式の数（" + ee.length + "）", ej.length === ee.length);
  ej.forEach(function (e, i) {
    say("式 " + (i + 1) + " が同じ形", e === ee[i], "ja " + e + "\n          en " + ee[i]);
  });
  // 例題のインラインコード（計算の途中値）は一字一句同じであるべき（Σ のあとの語を除く）
  const codes = (s) => (body(s).match(/`[^`]+`/g) || [])
                         .map((c) => c.replace(/Σ\s*\S+/g, "Σ"));
  say("例題の計算行（`…`）が日英で同一（" + codes(en).length + " 個）",
      JSON.stringify(codes(ja)) === JSON.stringify(codes(en)),
      "ja " + codes(ja).join(" | ") + "\n          en " + codes(en).join(" | "));
  const refs = (s) => s.match(/::: \{\.gw-refs\}([\s\S]*?):::/)[1].trim();
  say("参考文献が日英で同一", refs(ja) === refs(en));
  const chips = (s) => (s.match(/::: \{\.gw-attest\}([\s\S]*?):::/)[1].match(/\{\.gw-chip/g) || []).length;
  say("信頼の表示（チップ）の数", chips(ja) === chips(en));

  /* ⑥ リンク先 ---------------------------------------------------------- */
  console.log("\n  ⑥ リンク先");
  const links = (s) => (body(s).match(/\]\(([^)]+)\)/g) || []).map((l) => l.slice(2, -1));
  links(en).forEach(function (l) {
    if (/^https?:/.test(l)) return;
    let p = path.join(DIR, l);
    if (l.endsWith("/")) p = path.join(p, "index.qmd");
    say("英語版のリンク " + l, fs.existsSync(p));
    say("  拡張子 .html を手書きしていない", !/\.html$/.test(l));
  });
  const enRead = links(en).filter((l) => /posts\//.test(l));
  say("英語版の「Read further」は英語の記事（-en）を指す",
      enRead.length > 0 && enRead.every((l) => /index-en\.qmd$/.test(l)), enRead.join(", "));

  console.log("\n  日英の一致: " + checks + " 件中 " + (checks - failed) + " 件が一致。");
  return failed;
};

if (require.main === module) process.exit(module.exports() === 0 ? 0 : 1);
