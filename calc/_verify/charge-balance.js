/* ---------------------------------------------------------------------------
 * _verify/charge-balance.js — ページに実装した compute() を、そのページに
 * 載せた例題の数値と突き合わせる。
 *
 *   node _verify/charge-balance.js
 * ------------------------------------------------------------------------- */

const fs = require("fs");
const path = require("path");
const ROOT = path.join(__dirname, "..");

const TOOL  = "charge-balance";

global.window = global;
require(path.join(ROOT, "assets/gwcalc.js"));

/* ---- mount をスタブ化して config を捕まえる ---- */

let cfg = null;
GwCalc.mount = function (sel, c) {
  cfg = c;
  return { fields: {}, setTarget() {}, update() {} };
};

const stubNode = {
  setAttribute() {}, textContent: "", title: "", dataset: {}, firstChild: null,
  classList: { add() {}, remove() {} }, addEventListener() {},
  removeChild() {}, appendChild() {}
};
global.document = {
  addEventListener: (ev, fn) => fn(),
  getElementById: () => stubNode,
  querySelector: () => null,
  querySelectorAll: () => [],
  createElementNS: () => stubNode
};

const qmd = fs.readFileSync(path.join(ROOT, TOOL, "index.qmd"), "utf8");
eval(qmd.match(/<script>([\s\S]*?)<\/script>/)[1]);

if (!cfg) { console.error("mount() が呼ばれなかった"); process.exit(1); }

/* ---- 照合 ---- */

let failed = 0;
let checks = 0;

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
  const got = cfg.check(cfg.compute(v)).state;
  const ok = got === want;
  if (!ok) failed++;
  console.log((ok ? "  PASS  " : "  FAIL  ") + label.padEnd(30) + " -> " + got);
}

/* 入力は meq/L で渡す（UI の mg/L 欄は 1/当量重量 を掛けて meq/L にしている）。
   ここでは mg/L から手で換算した値を渡し、換算そのものも照合する。 */
const EQW = { Ca:20.039, Mg:12.153, Na:22.990, K:39.098,
              HCO3:61.016, SO4:48.030, Cl:35.453, NO3:62.004 };

function meq(mgl) {
  const out = {};
  Object.keys(mgl).forEach(function (k) { out[k] = mgl[k] / EQW[k]; });
  return out;
}

// ページ掲載の例題（石灰岩地帯の湧水）
const SPRING = { Ca:65, Mg:8.0, Na:12, K:2.0, HCO3:210, SO4:22, Cl:18, NO3:5.0 };

console.log("\n[1] mg/L → meq/L の換算（当量重量）");
near("Ca  65 mg/L",   meq(SPRING).Ca,   3.24367);
near("Mg  8.0 mg/L",  meq(SPRING).Mg,   0.658277);
near("HCO₃ 210 mg/L", meq(SPRING).HCO3, 3.44174);
near("SO₄ 22 mg/L",   meq(SPRING).SO4,  0.458047);

console.log("\n[2] ページ掲載の例題：釣り合う分析");
(function () {
  const r = cfg.compute(meq(SPRING));
  near("Σ cations (meq/L)", r.cat,  4.475069);
  near("Σ anions  (meq/L)", r.ani,  4.488118);
  near("CBE (%)",           r.cbe, -0.145635);
  near("差 (meq/L)",        r.diff, -0.013049);
})();

console.log("\n[3] 例題の後半：Ca を 85 mg/L と誤記した場合");
(function () {
  const bad = Object.assign({}, SPRING, { Ca: 85 });
  const r = cfg.compute(meq(bad));
  near("Σ cations (meq/L)", r.cat, 5.473117);
  near("CBE (%)",           r.cbe, 9.888330);
  // 不均衡を Ca に換算すると誤記量に近づくが、元の分析自体が -0.013 meq/L
  // ずれているぶんだけ 20.0 mg/L にはならない。本文にもそう書くこと。
  near("不均衡を mg/L に戻す", r.diff * EQW.Ca, 19.7384);
  near("誤記の増分だけなら",   (r.cat - 4.475069) * EQW.Ca, 20.0, 2e-3);
})();

console.log("\n[4] 派生量");
(function () {
  const r = cfg.compute(meq(SPRING));
  near("TDS 計算値 (mg/L)",      r.tds,      342.000);
  near("全硬度 (mg/L as CaCO₃)", r.hardness, 195.254);
  near("イオン強度 (mol/L)",     r.ionic,    6.66159e-3);
})();

console.log("\n[5] 判定の境界");
(function () {
  // Ca を増やして CBE を狙った値に動かす（Cl を減らすと負値になり 0 に丸められる）
  const tweak = (dCa) => meq(Object.assign({}, SPRING, { Ca: 65 + dCa }));
  state("釣り合う（|CBE| < 2 %）",   tweak(0),   "good");
  state("5 % 以内",                  tweak(8),   "good");
  state("5〜10 %（要確認）",         tweak(20),  "warn");
  state("10 % 超（使用不可）",       tweak(30),  "crit");

  // 希薄試料：百分率は大きくても絶対差が小さければ許容する
  const rain = { Ca:0.8, Mg:0.2, Na:1.2, K:0.1, HCO3:1.5, SO4:2.2, Cl:1.8, NO3:1.0 };
  const rr = cfg.compute(meq(rain));
  checks++;
  const st = cfg.check(rr).state;
  const ok = st === "good" && Math.abs(rr.cbe) > 5;
  if (!ok) failed++;
  console.log((ok ? "  PASS  " : "  FAIL  ") +
              "希薄試料は絶対差で判定".padEnd(30) + " -> " + st +
              "  (CBE " + rr.cbe.toFixed(1) + " %, 差 " + rr.diff.toFixed(3) + " meq/L)");
})();

console.log("\n[6] 不正入力で落ちないか");
[ { label: "全部ゼロ",       v: {} },
  { label: "陽イオンのみ",   v: meq({ Ca:65, Mg:8, Na:12, K:2 }) },
  { label: "負の値",         v: { Ca:-5, HCO3:3 } }
].forEach(function (c) {
  checks++;
  try {
    const r = cfg.compute(c.v);
    // 全部ゼロなら空、それ以外は落ちずに数値を返せばよい
    const ok = (c.label === "全部ゼロ") ? !isFinite(r.cbe) : isFinite(r.cbe);
    if (!ok) failed++;
    console.log((ok ? "  PASS  " : "  FAIL  ") + c.label.padEnd(18) +
                (isFinite(r.cbe) ? " CBE = " + r.cbe.toFixed(2) + " %" : " 空の結果を返した"));
  } catch (e) {
    failed++;
    console.log("  FAIL  " + c.label.padEnd(18) + " 例外 " + e.message);
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
