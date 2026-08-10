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
GwCalc.mount = function (sel, c) {
  cfg = c;
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
  near("s  Cooper–Jacob", r.sCJ,  1.12065);
  near("CJ 誤差 (%)",    r.errCJ, 0.0385, 2e-2);
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
  state("u = 0.05   → 良(CJ不可)", mix({ t: tFor(0.05,  50) }), "good");
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

if (checks === 0) {
  console.log("\n" + TOOL + ": 検証がまだ 1 件も書かれていない。TODO を埋めること。");
  process.exit(1);
}
console.log("\n" + (failed === 0
  ? TOOL + ": " + checks + " 件すべて一致した。"
  : TOOL + ": " + checks + " 件中 " + failed + " 件が不一致。"));
process.exit(failed === 0 ? 0 : 1);
