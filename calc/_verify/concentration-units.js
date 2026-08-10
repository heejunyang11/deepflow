/* ---------------------------------------------------------------------------
 * calc/_verify/concentration-units.js — ページに実装した compute() を、
 * 原子量から手で積み上げた分子量および本文の例題と突き合わせる。
 *
 *   node calc/_verify/concentration-units.js
 *
 * DOM をスタブ化し、.qmd の <script> をそのまま評価して config を捕まえる。
 * 「実装をテストする」ことが要点で、式を書き写して照合するのでは意味がない。
 * ------------------------------------------------------------------------- */

const fs = require("fs");
const path = require("path");
const ROOT = path.join(__dirname, "..");   // = calc/

const TOOL  = "concentration-units";

global.window = global;
require(path.join(ROOT, "assets/gwcalc.js"));

/* ---- mount をスタブ化して config を捕まえる ---- */

let cfg = null;
GwCalc.mount = function (sel, c) {
  cfg = c;
  return { fields: {}, setTarget() {}, update() {} };
};

const stubNode = {
  setAttribute() {}, textContent: "", title: "", dataset: {}, innerHTML: "",
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
let checks = 0;

function near(label, got, want, tol) {
  checks++;
  tol = tol || 1e-3;
  const ok = Math.abs(got - want) <= Math.abs(want) * tol;
  if (!ok) failed++;
  console.log(
    (ok ? "  PASS  " : "  FAIL  ") + label.padEnd(32) +
    " got " + String(Number(got).toPrecision(7)).padStart(14) +
    "   want " + String(Number(want).toPrecision(7)).padStart(14)
  );
}

function say(label, cond) {
  checks++;
  if (!cond) failed++;
  console.log((cond ? "  PASS  " : "  FAIL  ") + label);
}

function state(label, v, target, want) {
  checks++;
  const got = cfg.check(cfg.compute(v, target)).state;
  const ok = got === want;
  if (!ok) failed++;
  console.log((ok ? "  PASS  " : "  FAIL  ") + label.padEnd(30) + " -> " + got);
}

/* v.Cm は kg/m³（= g/L）、v.Cn は mol/m³（= mmol/L）で渡す規約 */
const byMass  = (formula, mgL, z) => ({ formula, Cm: mgL / 1000, Cn: NaN, z });
const byMolar = (formula, mmolL, z) => ({ formula, Cm: NaN, Cn: mmolL, z });

// 原子量から手で積んだ期待値（IUPAC 2021 慣用値）
const M_GYPSUM  = 40.078 + 32.06 + 4 * 15.999 + 2 * (2 * 1.008 + 15.999);  // 172.164
const M_CALCITE = 40.078 + 12.011 + 3 * 15.999;                            // 100.086
const M_DOLO    = 40.078 + 24.305 + 2 * (12.011 + 3 * 15.999);             // 184.399
const M_SO4     = 32.06 + 4 * 15.999;                                      //  96.056
const M_EPSOM   = 24.305 + 32.06 + 4 * 15.999 + 7 * (2 * 1.008 + 15.999);  // 246.466

console.log("\n[1] ページ既定値（石膏 172.164 mg/L・z=2）");
let d = cfg.compute(byMass("CaSO4·2H2O", 172.164, 2), "Cn");
near("分子量 M",            d.M,       M_GYPSUM);
near("モル濃度 mmol/L",      d.Cn,      1.0);
near("当量 meq/L",          d.meq,     2.0);
near("mg/L as CaCO3",      d.asCaCO3, 100.086);
near("当量質量 g/eq",        d.eqMass,  86.082);
near("結晶水 wt%",           d.wH2O,    20.9276);

console.log("\n[2] 逆算（solve-for の往復）");
let a = cfg.compute(byMass("CaSO4·2H2O", 860.325, 2), "Cn");
let b = cfg.compute(byMolar("CaSO4·2H2O", a.Cn, 2), "Cm");
near("mg/L → mmol/L",       a.Cn,      860.325 / M_GYPSUM, 1e-9);
near("mmol/L → mg/L で戻る",  b.Cm * 1000, 860.325,         1e-9);
let c1 = cfg.compute(byMolar("SO4", 5, 2), "Cm");
let c2 = cfg.compute(byMass("SO4", c1.Cm * 1000, 2), "Cn");
near("SO4 の往復（mmol/L）",   c2.Cn,     5,                  1e-9);

console.log("\n[3] ページ掲載の例題（SO4 480 mg/L → 石膏）");
// 期待値は手で積んだ分子量から独立に導く（実装の割り算と突き合わせる意味がある）。
const CN_SO4 = 480 / M_SO4;                       // mmol/L
const TIGHT  = 1e-9;
let s = cfg.compute(byMass("SO4", 480, 2), "Cn");
near("M(SO4)",              s.M,       M_SO4,                       TIGHT);
near("mmol/L",              s.Cn,      CN_SO4,                      TIGHT);
near("meq/L",               s.meq,     CN_SO4 * 2,                  TIGHT);
near("mg/L as CaCO3",       s.asCaCO3, CN_SO4 * 2 * (M_CALCITE / 2), TIGHT);
let g = cfg.compute(byMolar("CaSO4·2H2O", CN_SO4, 2), "Cm");
near("溶けた石膏 mg/L",        g.Cm * 1000, CN_SO4 * M_GYPSUM,         TIGHT);
// 内訳表と同じ計算：Ca は 1 formula unit あたり 1
near("随伴する Ca mg/L",      g.Cn * g.parsed.counts.Ca * 40.078, CN_SO4 * 40.078, TIGHT);
// 本文が丸めて載せている桁と一致するか（ページの数字そのものを守る）
say("本文の 4.997 mmol/L",     s.Cn.toFixed(3) === "4.997");
say("本文の 9.994 meq/L",      s.meq.toFixed(3) === "9.994");
say("本文の 500.1 as CaCO3",   s.asCaCO3.toFixed(1) === "500.1");
say("本文の 860.3 mg/L 石膏",   (g.Cm * 1000).toFixed(1) === "860.3");
say("本文の 200.3 mg/L Ca",    (g.Cn * 40.078).toFixed(1) === "200.3");
// FAQ の硝酸態窒素の換算係数
let mNO3 = cfg.compute(byMolar("NO3", 1, 1), "Cm").M;
let mN   = cfg.compute(byMolar("N", 1, 1), "Cm").M;
near("M(NO3)",              mNO3, 14.007 + 3 * 15.999, TIGHT);
near("NO3/N の換算係数",       mNO3 / mN, (14.007 + 3 * 15.999) / 14.007, TIGHT);
say("本文の 4.427 倍",         (mNO3 / mN).toFixed(3) === "4.427");
say("本文の 44.3 mg/L as NO3", (10 * mNO3 / mN).toFixed(1) === "44.3");

console.log("\n[4] 適用限界の判定の境界");
state("172 mg/L → good",      byMass("CaSO4·2H2O", 172.164, 2), "Cn", "good");
state("5 g/L → warn",         byMass("NaCl", 5000, 1),          "Cn", "warn");
state("40 g/L → crit",        byMass("NaCl", 40000, 1),         "Cn", "crit");
state("式が読めない → crit",     byMass("Xy2O3", 100, 2),          "Cn", "crit");

console.log("\n[5] 不正入力で落ちないか");
say("未知の元素を拒否",      !!cfg.compute(byMass("Xy2O3", 100, 2), "Cn").err);
say("括弧の不一致を拒否",     !!cfg.compute(byMass("Ca(OH2", 100, 2), "Cn").err);
say("空の式を拒否",         !!cfg.compute(byMass("   ", 100, 2), "Cn").err);
say("小文字始まりを拒否",     !!cfg.compute(byMass("caco3", 100, 2), "Cn").err);
// 固溶体表記は「先頭の端成分で代用」せず拒否する（黙って別の鉱物を計算しない）
say("固溶体 (Mg,Fe) を拒否",  !!cfg.compute(byMass("(Mg,Fe)2SiO4", 100, 2), "Cn").err);

// 電荷は当量系の2出力にしか効かない。欠けても分子量と濃度は返し続けること
let noz = cfg.compute(byMass("CaCO3", 100, NaN), "Cn");
say("電荷が空でも M は残る",   isFinite(noz.M));
say("電荷が空でも mmol/L は残る", isFinite(noz.Cn));
say("電荷が空なら meq は NaN", !isFinite(noz.meq));

// 濃度が空でも分子量だけは出す
let noc = cfg.compute({ formula:"CaCO3", Cm:NaN, Cn:NaN, z:2 }, "Cn");
near("濃度が空でも M は出る",   noc.M, M_CALCITE);
say("濃度が空なら Cn は無い",   !isFinite(noc.Cn));

console.log("\n[補] 式の解釈（入れ子・水和・水酸化物）");
near("ドロマイト M",          cfg.compute(byMolar("CaMg(CO3)2", 1, 4), "Cm").M, M_DOLO);
near("エプソマイト M",         cfg.compute(byMolar("MgSO4·7H2O", 1, 2), "Cm").M, M_EPSOM);
near("エプソマイト 結晶水 wt%",  cfg.compute(byMolar("MgSO4·7H2O", 1, 2), "Cm").wH2O, 51.1656);
near("アスタリスク表記も同じ",    cfg.compute(byMolar("MgSO4*7H2O", 1, 2), "Cm").M, M_EPSOM);
// 水酸化物に結晶水を数えないこと（H と O から推定すると 24% になってしまう）
near("Ca(OH)2 の結晶水は 0",   cfg.compute(byMolar("Ca(OH)2", 1, 2), "Cm").wH2O + 1, 1);
near("ハライト M",            cfg.compute(byMolar("NaCl", 1, 1), "Cm").M, 22.990 + 35.45);

if (checks === 0) {
  console.log("\n" + TOOL + ": 検証がまだ 1 件も書かれていない。TODO を埋めること。");
  process.exit(1);
}
console.log("\n" + (failed === 0
  ? TOOL + ": " + checks + " 件すべて一致した。"
  : TOOL + ": " + checks + " 件中 " + failed + " 件が不一致。"));
process.exit(failed === 0 ? 0 : 1);
