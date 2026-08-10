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

if (checks === 0) {
  console.log("\n" + TOOL + ": 検証がまだ 1 件も書かれていない。TODO を埋めること。");
  process.exit(1);
}
console.log("\n" + (failed === 0
  ? TOOL + ": " + checks + " 件すべて一致した。"
  : TOOL + ": " + checks + " 件中 " + failed + " 件が不一致。"));
process.exit(failed === 0 ? 0 : 1);
