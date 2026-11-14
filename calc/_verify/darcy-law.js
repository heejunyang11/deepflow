/* ---------------------------------------------------------------------------
 * _verify/darcy-law.js — ページに実装した compute() を、そのページに載せた
 * 例題の数値と突き合わせる。
 *
 *   node _verify/darcy-law.js
 *
 * DOM をスタブ化し、.qmd の <script> をそのまま評価して config を捕まえる。
 * 「実装をテストする」ことが要点で、式を書き写して照合するのでは意味がない。
 * 新しいツールを作るときはこのファイルを雛形にすること。
 * ------------------------------------------------------------------------- */

const fs = require("fs");
const path = require("path");
const ROOT = path.join(__dirname, "..");

const TOOL  = "darcy-law";

global.window = global;
require(path.join(ROOT, "assets/gwcalc.js"));

/* ---- mount をスタブ化して config を捕まえる ---- */

let cfg = null;
GwCalc.mount = function (sel, c) {
  cfg = c;
  return { fields: { K: { unit: {}, input: {} } }, setTarget() {}, update() {} };
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
eval(qmd.match(/<script>([\s\S]*?)<\/script>/)[1]);

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
  const r = cfg.compute(v, "Q");
  const got = cfg.check(r).state;
  const ok = got === want;
  if (!ok) failed++;
  console.log((ok ? "  PASS  " : "  FAIL  ") + label.padEnd(24) +
              " Re=" + r.Re.toPrecision(4).padStart(10) + "  → " + got);
}

console.log("\n[1] ページ既定値  K=1e-4 m/s, Δh=0.5 m, L=1 m, A=0.01 m², n=0.30, d=0.5 mm");
let r = cfg.compute({ K: 1e-4, dh: 0.5, L: 1.0, A: 0.01, Q: 0, n: 0.30, d: 5e-4 }, "Q");
near("i  (–)",      r.i,          0.5);
near("Q  (m³/s)",   r.Q,          5e-7);
near("Q  (m³/day)", r.Q * 86400,  0.0432);
near("q  (m/s)",    r.q,          5e-5);
near("v  (m/s)",    r.v,          1.666667e-4);
near("Re (–)",      r.Re,         0.025);

console.log("\n[2] 逆算 K：Q=5e-7 m³/s から K が戻るか");
r = cfg.compute({ K: 0, dh: 0.5, L: 1.0, A: 0.01, Q: 5e-7, n: 0.30, d: 5e-4 }, "K");
near("K  (m/s)",    r.K,          1e-4);

console.log("\n[3] 逆算 Δh：Q と K から Δh が戻るか");
r = cfg.compute({ K: 1e-4, dh: 0, L: 1.0, A: 0.01, Q: 5e-7, n: 0.30, d: 5e-4 }, "dh");
near("Δh (m)",      r.dh,         0.5);

console.log("\n[4] ページ掲載の例題  K=3e-4, A=1000 m², Δh=1.6 m, L=800 m, n=0.28");
r = cfg.compute({ K: 3e-4, dh: 1.6, L: 800, A: 1000, Q: 0, n: 0.28, d: 5e-4 }, "Q");
near("i  (–)",       r.i,          2.0e-3);
near("Q  (m³/s)",    r.Q,          6.0e-4);
near("Q  (m³/day)",  r.Q * 86400,  51.84);
near("q  (m/s)",     r.q,          6.0e-7);
near("v  (m/day)",   r.v * 86400,  0.185143, 2e-3);
near("t  (days)",    r.t,          4320,     2e-3);
near("t  (years)",   r.t / 365.25, 11.83,    3e-3);

/* 例題の締めで「ダルシー流束を使うと何年になるか」を本文に書いている。
   2026-09-07 の第三者検証で、そこが 33 年（誤り）のまま公開されていたことが
   分かった。正しくは 42 年で、実流速との比 1/n = 3.57 とも合う。
   本文の主張を機械で押さえておく。 */
var t_wrong = 800 / (r.q * 86400);              // 間隙率で割り忘れた場合の日数
near("誤用時 t (days)",  t_wrong,           15432,  2e-3);
near("誤用時 t (years)", t_wrong / 365.25,  42.25,  3e-3);
near("誤用/正解の比",    t_wrong / r.t,     1 / 0.28, 3e-3);

console.log("\n[5] 適用限界の判定");
state("層流 (Re≪1)",        { K: 1e-4, dh: 0.5, L: 1, A: 0.01, Q: 0, n: 0.3, d: 5e-4 }, "good");
state("遷移域 (1<Re<10)",   { K: 1e-2, dh: 0.5, L: 1, A: 0.01, Q: 0, n: 0.3, d: 1e-3 }, "warn");
state("非ダルシー (Re>10)", { K: 1e-1, dh: 1.0, L: 1, A: 0.01, Q: 0, n: 0.3, d: 5e-3 }, "crit");

console.log("\n[6] 全体を止めるべき入力（L と A）だけが Q を止めるか");
[ { label: "L = 0",    v: { K: 1e-4, dh: 0.5, L: 0, A: 0.01, Q: 0, n: 0.3, d: 5e-4 } },
  { label: "A = 0",    v: { K: 1e-4, dh: 0.5, L: 1, A: 0,    Q: 0, n: 0.3, d: 5e-4 } },
  { label: "K 未入力", v: { K: NaN,  dh: 0.5, L: 1, A: 0.01, Q: 0, n: 0.3, d: 5e-4 } }
].forEach(function (c) {
  try {
    const empty = !isFinite(cfg.compute(c.v, "Q").Q);
    if (!empty) failed++;
    console.log((empty ? "  PASS  " : "  FAIL  ") + c.label.padEnd(12) +
                (empty ? " 空の結果を返した" : " 値を返してしまった"));
  } catch (e) {
    failed++;
    console.log("  FAIL  " + c.label.padEnd(12) + " 例外 " + e.message);
  }
});

console.log("\n[7] n と d は自分が効く量だけを止める（編集中に全出力が消えないこと）");
[ { label: "n 未入力", v: { K: 1e-4, dh: 0.5, L: 1, A: 0.01, Q: 0, n: NaN, d: 5e-4 },
    live: ["Q", "i", "q", "Re"], dead: ["v", "t"] },
  { label: "n > 1",    v: { K: 1e-4, dh: 0.5, L: 1, A: 0.01, Q: 0, n: 1.5, d: 5e-4 },
    live: ["Q", "i", "q", "Re"], dead: ["v", "t"] },
  { label: "d 未入力", v: { K: 1e-4, dh: 0.5, L: 1, A: 0.01, Q: 0, n: 0.3, d: NaN },
    live: ["Q", "i", "q", "v", "t"], dead: ["Re"] }
].forEach(function (c) {
  const r = cfg.compute(c.v, "Q");
  const badLive = c.live.filter(function (k) { return !isFinite(r[k]); });
  const badDead = c.dead.filter(function (k) { return isFinite(r[k]); });
  const ok = badLive.length === 0 && badDead.length === 0;
  if (!ok) failed++;
  console.log((ok ? "  PASS  " : "  FAIL  ") + c.label.padEnd(12) +
              " 生存 " + c.live.join(",") + " / 停止 " + c.dead.join(",") +
              (ok ? "" : "   << " + badLive.concat(badDead).join(",") + " が想定と逆"));
});

console.log("\n[8] n を変えると seepage velocity が実際に変わるか");
(function () {
  const base = { K: 1e-4, dh: 0.5, L: 1, A: 0.01, Q: 0, d: 5e-4 };
  const a = cfg.compute(Object.assign({}, base, { n: 0.30 }), "Q");
  const b = cfg.compute(Object.assign({}, base, { n: 0.15 }), "Q");
  near("n=0.30 の v (m/s)",   a.v,       1.666667e-4);
  near("n=0.15 の v (m/s)",   b.v,       3.333333e-4);
  near("比 v(0.15)/v(0.30)",  b.v / a.v, 2.0);
  near("q は n に依存しない", b.q,       a.q);
  near("t も n で変わる",     a.t / b.t, 2.0);
})();

/* [本2] 第2版で書き足した主張
   ---------------------------------------------------------------------------
   2026-09-08 の検証で、遷移域（1 < Re < 10）の警告文が「得られた流量は上限値」
   と固定されていたことが分かった。K を逆算しているときは向きが逆で、真の K は
   得られた値より大きい（慣性損失を透水性の低さとして読むため）。安全側に
   倒したつもりの利用者を、逆側へ外させる文言だった。→ target で言い分ける。 */

console.log("\n[本2] 遷移域の警告は、解いている量で向きが変わる");
{
  // Re ≈ 5 になる条件をつくる。Re = ρ q d / μ, q = K i。
  //   d = 5e-3 m, q = 1e-3 m/s → Re = 1000*1e-3*5e-3/1e-3 = 5
  const V = { K: 1e-3, dh: 1.0, L: 1.0, A: 0.01, Q: 1e-5, n: 0.30, d: 5e-3 };

  const say2 = (label, cond) => {
    checks++; if (!cond) failed++;
    console.log((cond ? "  PASS  " : "  FAIL  ") + label);
  };

  const forQ  = cfg.check(cfg.compute(V, "Q"));
  const forK  = cfg.check(cfg.compute(V, "K"));
  const forDh = cfg.check(cfg.compute(V, "dh"));

  say2("Q を解くと遷移域の warn",  forQ.state  === "warn");
  say2("K を解くと遷移域の warn",  forK.state  === "warn");
  say2("Δh を解くと遷移域の warn", forDh.state === "warn");

  say2("Q のときだけ「上限値」",
       /Q は上限値/.test(forQ.text) &&
       !/上限値/.test(forK.text) && !/上限値/.test(forDh.text));
  say2("K のときは「下限値」",  /K は下限値/.test(forK.text));
  say2("Δh のときは「下限値」", /Δh は下限値/.test(forDh.text));

  // target を返さない実装に戻したら、ここが落ちる
  say2("compute が target を返す", cfg.compute(V, "K").target === "K");
}

/* 本文が引き合いに出す代表値が、同じページの表の値と一致しているか。
   本文だけ直して表を直し忘れる（あるいはその逆）を防ぐ。「13桁」「ほぼ全域」は
   Freeze & Cherry の主張なので、こちらで桁を数え直さず、引いている端の値が
   表と揃っていることだけを押さえる（2026-09-08 の検証を受けて追加）。 */
console.log("\n[本2] 本文の代表値は、同じページの表と一致するか");
{
  const src = fs.readFileSync(path.join(ROOT, TOOL, "index.qmd"), "utf8").split(String.fromCharCode(13)).join("");
  const flat = src.replace(/\n\s*/g, "");
  const row = (name) => {
    const m = new RegExp("<td>" + name + "[^<]*</td><td align=\"right\">([^<]*)</td>").exec(flat);
    return m ? m[1].trim() : "";
  };
  const say3 = (label, cond) => {
    checks++; if (!cond) failed++;
    console.log((cond ? "  PASS  " : "  FAIL  ") + label);
  };
  say3("表の礫の上限は 10\u207b\u00b9 m/s",
       row("\u792b").split("\u2013").pop().trim() === "10\u207b\u00b9");
  say3("表の粗砂の上限は 10\u207b\u00b2 m/s",
       row("\u7c97\u7802").split("\u2013").pop().trim() === "10\u207b\u00b2");
  say3("表の海成粘土の下限は 10\u207b\u00b9\u00b3 m/s",
       row("\u6d77\u6210\u7c98\u571f").split("\u2013")[0].trim() === "10\u207b\u00b9\u00b3");
  say3("\u672c\u6587\u304c\u792b 10\u207b\u00b9 \u3068\u7c98\u571f 10\u207b\u00b9\u00b3 \u3092\u5f15\u3044\u3066\u3044\u308b",
       src.indexOf("\u4e0a\u7aef\uff08\u792b\uff09\u306f\n10\u207b\u00b9 m/s") >= 0 &&
       src.indexOf("10\u207b\u00b9\u00b3 m/s \u3067\u3059") >= 0);
  say3("\u672c\u6587\u304c\u7c97\u7802\u306e\u4e0a\u9650 10\u207b\u00b2 \u3092\u5f15\u3044\u3066\u3044\u308b",
       src.indexOf("\u7c97\u7802\uff08\u4e0a\u9650 10\u207b\u00b2 m/s\uff09") >= 0);
}

if (checks === 0) {
  console.log("\n" + TOOL + ": 検証がまだ 1 件も書かれていない。TODO を埋めること。");
  process.exit(1);
}
console.log("\n" + (failed === 0
  ? TOOL + ": " + checks + " 件すべて一致した。"
  : TOOL + ": " + checks + " 件中 " + failed + " 件が不一致。"));
process.exit(failed === 0 ? 0 : 1);
