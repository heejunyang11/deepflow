/* ---------------------------------------------------------------------------
 * _verify/theis-solution.js — ページに実装した compute() を、そのページに
 * 載せた例題の数値と突き合わせる。
 *
 *   node _verify/theis-solution.js
 * ------------------------------------------------------------------------- */

const fs = require("fs");
const path = require("path");
const ROOT = path.join(__dirname, "..");

const TOOL  = "theis-solution";

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
eval(qmd.match(/<script>([\s\S]*?)<\/script>/)[1]);

if (!cfg) { console.error("mount() が呼ばれなかった"); process.exit(1); }

/* ---- 照合 ---- */

let failed = 0;
let checks = 0;   // 1 件も書かないまま「通った」ことにしないための番人

function near(label, got, want, tol) {
  checks++;
  tol = tol || 1e-3;
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
  const got = cfg.check(cfg.compute(v, "s")).state;
  const ok = got === want;
  if (!ok) failed++;
  console.log((ok ? "  PASS  " : "  FAIL  ") + label.padEnd(28) + " -> " + got);
}

const BASE = { Q: 0.02, T: 1.2e-2, S: 2.0e-4, r: 50, t: 86400, s: 0 };
const mix = (o) => Object.assign({}, BASE, o);

/* [1] 井戸関数そのもの。ここが狂うと以降すべてが狂う。
       表値は Wenzel (1942) / Freeze & Cherry 付録。compute 経由で逆算して照合する。 */

console.log("\n[1] 井戸関数 W(u) を公表表値と照合（許容 0.1 %）");
[[1e-5, 10.9357], [1e-4, 8.6332], [1e-3, 6.3315], [1e-2, 4.0379],
 [1e-1, 1.8229], [0.5, 0.5598], [1.0, 0.2194], [2.0, 0.04890], [5.0, 0.001148]
].forEach(function (row) {
  // u = r²S/(4Tt) を目標値にする t を逆算して入力する
  const u = row[0];
  const t = BASE.r * BASE.r * BASE.S / (4 * BASE.T * u);
  const r = cfg.compute(mix({ t: t }), "s");
  near("W(u) at u=" + u.toExponential(0), r.Wu, row[1], 1e-3);
});

/* [2] 逆算（solve-for の往復） */

console.log("\n[2] 逆算：s → T → s、s → Q → s で元に戻るか");
(function () {
  const fwd = cfg.compute(mix({}), "s");
  near("順方向 s (m)", fwd.s, 1.12022);

  const backT = cfg.compute(mix({ s: fwd.s }), "T");
  near("s から戻した T (m²/s)", backT.T, 1.2e-2, 2e-3);

  const backQ = cfg.compute(mix({ s: fwd.s }), "Q");
  near("s から戻した Q (m³/s)", backQ.Q, 0.02);
})();

/* [3] ページ掲載の例題。本文と実装のどちらかがずれたらここで落ちる。 */

console.log("\n[3] 例題 (a)  t = 1 day, r = 50 m");
(function () {
  const r = cfg.compute(mix({ t: 86400, r: 50 }), "s");
  near("u",              r.u,     1.20563e-4);
  near("W(u)",           r.Wu,    8.44624);
  near("s  (m)",         r.s,     1.12022);
  near("s  Cooper–Jacob", r.sCJ,  1.12045);
  near("CJ 誤差 (%)",    r.errCJ, 0.0205, 2e-2);
})();

console.log("\n[4] 例題 (b)  t = 30 min, r = 200 m  ← Cooper–Jacob が使えない側");
(function () {
  const r = cfg.compute(mix({ t: 1800, r: 200 }), "s");
  near("u",               r.u,     9.25926e-2);
  near("W(u)",            r.Wu,    1.89282);
  near("s  (m)",          r.s,     0.251043);
  near("s  Cooper–Jacob", r.sCJ,   0.239330);
  near("CJ 誤差 (%)",     r.errCJ, -4.67, 3e-3);
})();

/* [5] 適用限界の判定の境界 */

console.log("\n[5] 判定の境界（u で切り替わる）");
(function () {
  // u = r²S/(4Tt) になる t を逆算して、狙った u をつくる
  const tFor = (u, r) => (r * r * BASE.S) / (4 * BASE.T * u);
  state("u = 0.001  → 良",     mix({ t: tFor(0.001, 50) }), "good");
  // 0.01 < u <= 1 は warn。タイス解そのものは厳密だが、判定行が伝えているのは
  // 「直線近似は使えない」という禁止なので、ok クラスでは色と内容が食い違う
  // （2026-09-08 の検証）。
  state("u = 0.05   → 注意(CJ不可)", mix({ t: tFor(0.05,  50) }), "warn");
  state("u = 2      → 注意",   mix({ t: tFor(2,     50) }), "warn");
  state("u = 8      → 不可",   mix({ t: tFor(8,     50) }), "crit");
})();

console.log("\n[6] 派生量");
(function () {
  const r = cfg.compute(mix({}), "s");
  near("影響半径 R (m)",        r.R,    3415.26);
  near("u=0.01 到達時刻 (h)",   r.t001 / 3600, 0.289352);
})();

/* [7] 不正入力で落ちないか */

console.log("\n[7] 不正入力で落ちないか");
[ { label: "S = 0",    v: mix({ S: 0 }),    target: "s" },
  { label: "r = 0",    v: mix({ r: 0 }),    target: "s" },
  { label: "t = 0",    v: mix({ t: 0 }),    target: "s" },
  { label: "T 未入力", v: mix({ T: NaN }),  target: "s" },
  { label: "T を解く際に s=0", v: mix({ s: 0 }), target: "T" }
].forEach(function (c) {
  checks++;
  try {
    const r = cfg.compute(c.v, c.target);
    const empty = !isFinite(r.s) || !isFinite(r.T);
    if (!empty) failed++;
    console.log((empty ? "  PASS  " : "  FAIL  ") + c.label.padEnd(22) +
                (empty ? " 空の結果を返した" : " 値を返してしまった"));
  } catch (e) {
    failed++;
    console.log("  FAIL  " + c.label.padEnd(22) + " 例外 " + e.message);
  }
});

/* [8] 本文が数値で主張していること
   ---------------------------------------------------------------------------
   日本語版で「u と Cooper–Jacob 誤差」の対応表を本文に載せた。表の数字は
   ページの実装から取ったものなので、実装が変わったら表も直す必要がある。
   2026-09-07 の検証で、英語版の「u = 0.01 で誤差およそ 1 %」が誤り
   （実際は 0.2 %）だと分かった経緯があるため、本文の主張を機械で押さえる。 */
console.log("\n[8] 本文の対応表：u と Cooper–Jacob の誤差");
{
  const Q = 0.020, T = 1.2e-2, S = 2.0e-4, r = 50;
  const errAt = (u) => cfg.compute(
    { Q, T, S, r, t: r * r * S / (4 * T * u), s: 0 }, "s").errCJ;

  [[0.01, -0.201], [0.03, -0.944], [0.05, -1.926],
   [0.1, -5.250], [0.2, -15.42]].forEach(([u, want]) => {
    near("u = " + u + " の誤差 (%)", errAt(u), want, 5e-3);
  });

  // 「1 % に達するのは u ≈ 0.03」という本文の主張
  let lo = 0.001, hi = 0.2;
  for (let i = 0; i < 80; i++) {
    const mid = Math.sqrt(lo * hi);
    (Math.abs(errAt(mid)) < 1.0) ? (lo = mid) : (hi = mid);
  }
  near("|誤差| = 1 % となる u", Math.sqrt(lo * hi), 0.0313, 2e-2);

  /* 例題 (a) の「クーパー・ヤコブでは 1.120 m、誤差 +0.02 %」。
     2026-09-07 の検証で、実装が 2.303 をリテラルで掛けていたため
     ln10 との差 0.018 % が誤差に混ざり、掲載値が 1.121 m / 0.04 % に
     なっていたことが分かった。自然対数で評価するよう直した結果を押さえる。 */
  const a = cfg.compute({ Q, T, S, r: 50, t: 86400, s: 0 }, "s");
  near("例題(a) C–J の s (m)",   a.sCJ,   1.12045, 1e-4);
  near("例題(a) C–J の誤差 (%)", a.errCJ, 0.0205, 2e-2);
}

/* [9] 第2版で書き足した主張（2026-09-08 の検証を受けて）
   ------------------------------------------------------------------------- */

console.log("\n[9] 第2版の主張");
{
  const say2 = (label, cond) => {
    checks++; if (!cond) failed++;
    console.log((cond ? "  PASS  " : "  FAIL  ") + label);
  };

  /* 影響半径は揚水量に依らない——「R は影響の範囲ではない」という節の根拠。
     表の「入れるもの」から Q を外したので、実装がそれを裏づけているか押さえる。 */
  const r1  = cfg.compute(mix({ Q: 0.02 }), "s");
  const r10 = cfg.compute(mix({ Q: 0.20 }), "s");
  say2("R は Q を 10 倍しても変わらない", Math.abs(r10.R - r1.R) < 1e-9);
  near("R (m)", r1.R, 3415.26);
  // 一方 s は Q に比例する（R だけが動かないことの対照）
  near("s は Q に比例する", r10.s / r1.s, 10, 1e-9);

  /* 例題 (a) の「誤差 +0.02 % は実寸で 0.2 mm」 */
  const a = cfg.compute(mix({ t: 86400, r: 50 }), "s");
  near("例題(a) の差 (mm)", (a.sCJ - a.s) * 1000, 0.2, 0.2);
  say2("差は 1 mm 未満", Math.abs(a.sCJ - a.s) * 1000 < 1.0);

  /* 誤差表の注記：慣用の 2.25 ではなく厳密な 4e^(-γ) = 2.2458 を使うと
     u = 0.01 での誤差は -0.25 % になる。実装ではなく本文の但し書きの検算。 */
  const u = 0.01;
  const t = BASE.r * BASE.r * BASE.S / (4 * BASE.T * u);
  const W = cfg.compute(mix({ t: t }), "s").Wu;
  const errWith = (C) => (Math.log(C / (4 * u)) / W - 1) * 100;
  near("2.25 での誤差 (%)",   errWith(2.25),   -0.201, 5e-3);
  near("2.2458 での誤差 (%)", errWith(2.2458), -0.25,  2e-2);
  near("4e^(-γ) の値",        4 * Math.exp(-0.5772156649), 2.2458, 1e-4);
}

if (checks === 0) {
  console.log("\n" + TOOL + ": 検証がまだ 1 件も書かれていない。TODO を埋めること。");
  process.exit(1);
}
// 番人より後ろに置く（前に置くと 1 件に数えられ、番人が働かなくなる）
checks++;
if (!require("./firstpaint.js").report(firstPaint)) failed++;

console.log("\n" + (failed === 0
  ? TOOL + ": " + checks + " 件すべて一致した。"
  : TOOL + ": " + checks + " 件中 " + failed + " 件が不一致。"));
process.exit(failed === 0 ? 0 : 1);
