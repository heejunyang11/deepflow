/* ---------------------------------------------------------------------------
 * calc/_verify/reference-et.js — ページに実装した compute() を、独立に書いた
 * Python 実装（scratchpad/et_ref.py）の値および教科書の既知値と突き合わせる。
 *
 *   node calc/_verify/reference-et.js
 *
 * DOM をスタブ化し、.qmd の <script> をそのまま評価して config を捕まえる。
 * 「実装をテストする」ことが要点で、式を書き写して照合するのでは意味がない。
 * 期待値は同じ式を2度別々に（JS と Python で）書いて一致した値である。
 * ------------------------------------------------------------------------- */

const fs = require("fs");
const path = require("path");
const ROOT = path.join(__dirname, "..");   // = calc/

const TOOL  = "reference-et";

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
let checks = 0;

function near(label, got, want, tol) {
  checks++;
  tol = tol || 1e-3;
  const ok = Math.abs(got - want) <= Math.abs(want) * tol;
  if (!ok) failed++;
  console.log(
    (ok ? "  PASS  " : "  FAIL  ") + label.padEnd(30) +
    " got " + String(Number(got).toPrecision(6)).padStart(14) +
    "   want " + String(Number(want).toPrecision(6)).padStart(14)
  );
}

function state(label, v, want) {
  checks++;
  const got = cfg.check(cfg.compute(v, null)).state;
  const ok = got === want;
  if (!ok) failed++;
  console.log((ok ? "  PASS  " : "  FAIL  ") + label.padEnd(28) + " -> " + got);
}

function say(label, cond) {
  checks++;
  if (!cond) failed++;
  console.log((cond ? "  PASS  " : "  FAIL  ") + label);
}

/* 入力の組み立て。compute は SI 正規化済みの値を受け取る規約なので、
   風速は m/s、標高は m、気温は ℃ のまま渡してよい。 */
function inp(lat, J, z, Tmax, Tmin, RH, u2, n) {
  return { lat, J, z, Tmax, Tmin, RH, u2, n };
}

const DEF  = inp(35.0, 196, 50,  30.0, 20.0, 60.0, 1.8, 8.0);   // ページ既定値
const NAHA = inp(26.2, 196, 28,  32.0, 27.0, 78.0, 3.5, 7.0);   // 本文の例題
const ARID = inp(33.0, 196, 300, 40.0, 22.0, 20.0, 4.0, 11.0);  // 移流卓越
const EQ   = inp(0.0,   81,  0,  20.0, 20.0, 50.0, 2.0, 6.0);   // 恒等式の確認用

console.log("\n[1] ページ既定値");
let d = cfg.compute(DEF, null);
near("ET0 Penman–Monteith", d.pm,   5.08198);
near("ET0 Hargreaves",      d.hs,   5.18193);
near("ET0 Priestley–Taylor", d.pt,  5.07004);
near("ET0 Turc",            d.turc, 4.62450);
near("ET0 Makkink",         d.mk,   4.25695);
near("手法間のばらつき %",       d.spread, 18.2010);
near("Ra",                  d.Ra,  40.78362);
near("N（日長）",              d.N,   14.13050);
near("Rn",                  d.Rn,  13.35764);

console.log("\n[2] 物理的な恒等式（教科書値と一致するか）");
// solve-for が無いツールなので、逆算の代わりに独立に検証できる量を確かめる。
let e = cfg.compute(EQ, null);
near("es at 20℃ (FAO-56 Table 2.3)", e.es, 2.338281);   // 2.338 kPa
near("Δ at 20℃ (FAO-56 Table 2.4)",  e.D,  0.144740);   // 0.145 kPa/℃
near("γ at 海面 (P=101.3 kPa)",       e.gamma, 0.067364); // 0.0673 kPa/℃
near("赤道の日長は 12 h",              e.N,  12.0, 1e-9);
near("Ra（赤道・春分近傍）",            e.Ra, 37.803690);
near("ea = RH × es",                 e.ea, 0.50 * e.es, 1e-12);
say ("VPD = es − ea が正",            e.vpd > 0);

console.log("\n[3] ページ掲載の例題（那覇 7/15）");
let r = cfg.compute(NAHA, null);
near("es",                  r.es,   4.160060);
near("ea",                  r.ea,   3.244847);
near("Δ",                   r.D,    0.237362);
near("N（日長）",              r.N,   13.487232);
near("Ra",                  r.Ra,  40.179287);
near("Rs",                  r.Rs,  20.471541);
near("Rn",                  r.Rn,  13.715920);
near("ET0 Penman–Monteith", r.pm,   5.120086);
near("ET0 Hargreaves",      r.hs,   3.989424);
near("ET0 Priestley–Taylor", r.pt,  5.498473);
near("ET0 Turc",            r.turc, 4.643893);
near("ET0 Makkink",         r.mk,   4.233600);
near("ばらつき %",             r.spread, 29.472970);
// 本文が主張している「Hargreaves が 22 % 低い」を数値で裏取りする
near("Hargreaves の低さ %",     (1 - r.hs / r.pm) * 100, 22.08, 5e-3);

console.log("\n[4] 適用限界の判定の境界");
state("ばらつき 18 % → good",  DEF,  "good");
state("ばらつき 29 % → warn",  NAHA, "warn");
state("ばらつき 50 % → crit",  ARID, "crit");

console.log("\n[5] 不正入力で落ちないか");
// 全体に効く入力が欠けたときだけ空を返す規約
let miss = cfg.compute(inp(35, 196, 50, 30, 20, NaN, 1.8, 8), null);
say("湿度が空なら全出力を止める", !isFinite(miss.pm) && miss.pm === undefined);

// 風速は Penman–Monteith にしか効かない。欠けても他の4手法は出し続けること
// （ここで {} を返すと、風速欄を編集している最中に全出力が消える）
let nw = cfg.compute(inp(35, 196, 50, 30, 20, 60, NaN, 8), null);
say("風速が空でも PT は残る",     isFinite(nw.pt));
say("風速が空でも Turc は残る",   isFinite(nw.turc));
say("風速が空なら PM だけ NaN",   !isFinite(nw.pm));

// Tmax < Tmin は物理的にありえない。√ の中が負になるので Hargreaves だけ落とす
let rev = cfg.compute(inp(35, 196, 50, 18, 25, 60, 1.8, 8), null);
say("Tmax<Tmin なら HS は NaN",  !isFinite(rev.hs));
say("Tmax<Tmin でも PM は有限",   isFinite(rev.pm));

// 白夜（arccos の定義域外）。丸めて 24 h で頭打ちにしていること
let pol = cfg.compute(inp(80, 172, 0, 10, 2, 70, 2, 12), null);
say("白夜で日長が 24 h に張り付く", Math.abs(pol.N - 24) < 1e-9);
say("白夜でも ET0 が有限",          isFinite(pol.pm));

// 日照が日長を超える入力。Rs/Rso を 1 で頭打ちにしているので Rnl は発散しない
let over = cfg.compute(inp(35, 196, 50, 30, 20, 60, 1.8, 24), null);
say("日照過大でも Rn が有限",       isFinite(over.Rn));

/* [6] 本文が数値で主張していること
   ---------------------------------------------------------------------------
   2026-09-07 の検証（darcy-law の「誤用すると 33 年」）で、本文が引き合いに出す
   数値が検証の網から漏れていたことが分かった。以降、本文が数値で何かを主張したら
   その数値もここに入れる。 */

console.log("\n[6] 本文の主張");
const NAHA_R = cfg.compute(NAHA, null);

// 「地下水と、どうつながるか」の水収支の算術
// P=1200, ETa=950 → R=250。ET が1割低い見積もりだったら R は 155 になり 38 % ずれる。
near("涵養量 R (mm)",              1200 - 950,          250,  1e-12);
near("ET を1割上げた ETa (mm)",     950 * 1.1,          1045,  1e-12);
near("そのときの涵養量 (mm)",       1200 - 950 * 1.1,    155,  1e-9);
near("涵養量の誤差 (%)",           (250 - 155) / 250 * 100, 38, 1e-9);

// 例題の「ハーグリーブスが削った 1.1 mm/日 は年 400 mm ほど」
near("例題 PM − HS (mm/日)",   NAHA_R.pm - NAHA_R.hs,          1.13, 1e-2);
near("その年換算 (mm/年)",     (NAHA_R.pm - NAHA_R.hs) * 365,  400,  4e-2);

// 「10 m の風速はおよそ3割強（1.34倍）高い」 FAO-56 式(47)
near("u10 / u2",  Math.log(67.8 * 10 - 5.42) / 4.87,  1.34, 1e-2);

// 「es 曲線は下に凸なので、平均気温を代入すると es を小さく見積もる」
{
  const flat = cfg.compute(inp(26.2, 196, 28, 29.5, 29.5, 78, 3.5, 7), null);
  say("平均気温で es を出すと小さくなる", flat.es < NAHA_R.es);
}

// 「タークの補正は相対湿度 50 % を下回ると効きはじめる」
{
  const t60 = cfg.compute(inp(35, 196, 50, 30, 20, 60, 1.8, 8), null).turc;
  const t50 = cfg.compute(inp(35, 196, 50, 30, 20, 50, 1.8, 8), null).turc;
  const t49 = cfg.compute(inp(35, 196, 50, 30, 20, 49, 1.8, 8), null).turc;
  say("RH = 50 % では補正が掛からない", Math.abs(t50 - t60) < 1e-12);
  near("RH = 49 % での補正倍率", t49 / t50, 1 + 1 / 70, 1e-9);
}

// FAQ の「実測 Rs があるなら n = N(Rs/Ra − 0.25)/0.50 で逆算せよ」
near("日照時間の逆算 (h)",
     NAHA_R.N * (NAHA_R.Rs / NAHA_R.Ra - 0.25) / 0.50, 7.0, 1e-9);

// 「λ は 2.45 MJ/kg（20 ℃）」——マッキンク式から逆に取り出して確かめる
near("蒸発潜熱 λ (MJ/kg)",
     0.65 * NAHA_R.D / (NAHA_R.D + NAHA_R.gamma) * NAHA_R.Rs / NAHA_R.mk,
     2.45, 1e-9);

// 「25 % 未満なら同じことを語り、40 % を超えるともう語っていない」
// check() のしきい値そのものを押さえる（[4] は代表点だけを見ている）
{
  const st = (sp) => cfg.check({ pm: 5, spread: sp }).state;
  say("ばらつき 24.9 % → good", st(24.9) === "good");
  say("ばらつき 25.1 % → warn", st(25.1) === "warn");
  say("ばらつき 39.9 % → warn", st(39.9) === "warn");
  say("ばらつき 40.1 % → crit", st(40.1) === "crit");
}

/* [7] 第2版で書き足した主張（2026-09-08 の検証を受けて）
   ------------------------------------------------------------------------- */

console.log("\n[7] 第2版の主張");
{
  const say2 = (label, cond) => {
    checks++; if (!cond) failed++;
    console.log((cond ? "  PASS  " : "  FAIL  ") + label);
  };

  /* 例題の個別の飽和水蒸気圧。平均（es）だけを検査していたので、
     4.759 / 3.561 という誤った個別値がすり抜けていた。
     Tmax = Tmin にすると es = e°(T) になるので、そこから取り出す。 */
  const e0 = (T) => cfg.compute(inp(26.2, 196, 28, T, T, 78, 3.5, 7), null).es;
  near("e°(32 ℃) (kPa)", e0(32), 4.755, 5e-4);
  near("e°(27 ℃) (kPa)", e0(27), 3.565, 5e-4);
  near("その平均が es",   (e0(32) + e0(27)) / 2, NAHA_R.es, 1e-12);

  /* アルベド：Rns = (1 − 0.23) Rs。本文と例題が 0.77 を掛けていること。 */
  near("Rns / Rs = 1 − α", (NAHA_R.Rn + 2.05) / NAHA_R.Rs, 0.77, 3e-3);
  near("例題の Rns (MJ/m²/日)", 0.77 * NAHA_R.Rs, 15.76, 2e-3);

  /* 例題：マッキンクも 17 % 低い（外れているのは HS だけではない） */
  near("マッキンクの低さ (%)", (1 - NAHA_R.mk / NAHA_R.pm) * 100, 17.3, 5e-3);
  say2("HS のほうが外れている", NAHA_R.hs < NAHA_R.mk);

  /* 「10 m の実測値には 0.75 を掛けてから入れる」FAO-56 式(47) */
  near("u2 / u10", 4.87 / Math.log(67.8 * 10 - 5.42), 0.75, 5e-3);

  /* 極域は両側で頭打ち。極夜（真冬）側が 0 h になること。 */
  const polarNight = cfg.compute(inp(80, 355, 0, -20, -30, 70, 2, 0), null);
  say2("極夜で可照時間が 0 h", Math.abs(polarNight.N) < 1e-9);
  say2("極夜でも Ra が有限",   isFinite(polarNight.Ra));
  const polarDay = cfg.compute(inp(80, 172, 0, 10, 2, 70, 2, 12), null);
  say2("白夜で可照時間が 24 h", Math.abs(polarDay.N - 24) < 1e-9);
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
