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

/* 2026-11-14 から英語版（index-en.qmd）がある。引数なしで呼ぶと、日英の両ファイルに
   下の [1]〜[8] をそれぞれかけ、最後に [9] 日英の一致を照合する。
   引数にファイル名を渡すと、そのファイルだけを検査する（子プロセスとして使う）。 */
const PAGES = ["index.qmd", "index-en.qmd"];
if (!process.argv[2]) {
  const { spawnSync } = require("child_process");
  let bad = 0;
  PAGES.forEach(function (p) {
    console.log("\n==================== " + p + " ====================");
    const r = spawnSync(process.execPath, [__filename, p], { stdio: "inherit" });
    if (r.status !== 0) bad++;
  });
  console.log("\n==================== [9] 日英の一致 ====================");
  if (require(path.join(__dirname, "charge-balance.parity.js"))() !== 0) bad++;
  console.log("\n" + (bad === 0 ? TOOL + ": 日英とも、すべての検査を通った。"
                                : TOOL + ": " + bad + " 組の検査に不一致がある。"));
  process.exit(bad === 0 ? 0 : 1);
}
const PAGE = process.argv[2];

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

const qmd = fs.readFileSync(path.join(ROOT, TOOL, PAGE), "utf8");
// gwcalc.js の UI 文字列はページの <html lang> で切り替わる。front matter と揃える。
const LANG = (qmd.match(/^lang:\s*(\S+)/m) || [])[1] || "ja";
global.document.documentElement = { lang: LANG };
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

/* [7] 本文が数値で主張していること
   ---------------------------------------------------------------------------
   2026-09-07 の検証で、本文が引き合いに出す数値（darcy-law の「誤用すると 33 年」）が
   検証の網から漏れていたことが分かった。以降、本文が数値で主張したらここに入れる。 */

console.log("\n[7] 本文の主張");
(function () {
  const r = cfg.compute(meq(SPRING));

  // 例題の「HCO3 だけで陰イオン電荷のおよそ 77 %、Ca だけで陽イオン電荷のおよそ 72 %」
  near("HCO₃ が陰イオン電荷に占める割合 (%)", meq(SPRING).HCO3 / r.ani * 100, 76.69, 1e-3);
  near("Ca が陽イオン電荷に占める割合 (%)",   meq(SPRING).Ca  / r.cat * 100, 72.48, 1e-3);

  // 例題の「取り戻した 19.7 mg/L は、誤記の 20.0 mg/L より 0.3 mg/L 足りない。
  //         その 0.3 mg/L は、打ち間違える前からあった -0.013 meq/L そのもの」
  const bad = cfg.compute(meq(Object.assign({}, SPRING, { Ca: 85 })));
  near("取り戻せなかった分 (mg/L)", 20.0 - bad.diff * EQW.Ca,        0.2616, 2e-3);
  near("それは元のずれと同じか",     Math.abs(r.diff) * EQW.Ca,       0.2615, 2e-3);

  // 「0.1 meq/L のずれは、合計 10 meq/L なら 1 %、合計 0.5 meq/L なら 20 %」
  near("希釈の効き方：合計 10 meq/L (%)", 0.1 / 10  * 100,  1, 1e-9);
  near("希釈の効き方：合計 0.5 meq/L (%)", 0.1 / 0.5 * 100, 20, 1e-9);

  // FAQ の「合計 0.3 meq/L で 0.05 meq/L の誤差は 17 %」
  near("雨水の例 (%)", 0.05 / 0.3 * 100, 17, 2e-2);

  // 「当量重量ではなくモル質量で割ると、2価イオンは半分になる」
  near("Ca を M で割ると半分になる", (65 / 40.078) / meq(SPRING).Ca, 0.5, 1e-9);
  near("SO₄ を M で割ると半分になる", (22 / 96.06) / meq(SPRING).SO4, 0.5, 2e-4);

  // 「1 meq/L = 50.04 mg/L as CaCO₃」
  near("硬度の換算係数 (mg/L per meq/L)",
       r.hardness / (meq(SPRING).Ca + meq(SPRING).Mg), 50.04, 1e-9);

  // 判定のしきい値そのもの（±5 %、±2 %、10 %）
  const ok2 = (label, cond) => { checks++; if (!cond) failed++;
    console.log((cond ? "  PASS  " : "  FAIL  ") + label); };
  const st = (cbe) => cfg.check({ cbe: cbe, diff: cbe, ani: 10 }).state;
  ok2("|CBE| = 4.9 % → good",  st(4.9)  === "good");
  ok2("|CBE| = 5.1 % → warn",  st(5.1)  === "warn");
  ok2("|CBE| = 9.9 % → warn",  st(9.9)  === "warn");
  ok2("|CBE| = 10.1 % → crit", st(10.1) === "crit");
})();

/* [8] 第2版で書き足した主張（2026-09-08 の検証を受けて）
   ---------------------------------------------------------------------------
   旧版は「Ca 1 mg が運ぶ電荷は Na の1ミリグラム当量の2倍」と書いていた。
   実際は 0.0499 / 0.0435 = 1.15 倍で、しかも「1ミリグラム当量」は定義上
   ちょうど 1 meq なので比較が成り立たない。2倍が正しいのは mol あたりだけ。
   まさに「質量では比べられない」ことを説明する節だったので、押さえておく。 */

console.log("\n[8] 第2版の主張");
{
  const say2 = (label, cond) => {
    checks++; if (!cond) failed++;
    console.log((cond ? "  PASS  " : "  FAIL  ") + label);
  };

  const meqPerMg = (eqw) => 1 / eqw;
  near("Ca 1 mg の当量 (meq)", meqPerMg(EQW.Ca), 0.0499, 5e-3);
  near("Na 1 mg の当量 (meq)", meqPerMg(EQW.Na), 0.0435, 5e-3);
  near("その比（2 倍ではない）", meqPerMg(EQW.Ca) / meqPerMg(EQW.Na), 1.15, 5e-3);
  // 2 倍が成り立つのは mol あたり（電荷数の比）
  near("mol あたりなら 2 倍", 2 / 1, 2, 1e-12);

  /* 「Ca を当量重量ではなくモル質量で割ると、CBE は −22 %」
     合計が 2 倍ずれるのではないことを、実装で示す。 */
  const bad = Object.assign({}, meq(SPRING));
  bad.Ca = 65 / 40.078;                       // 価数を落とした換算
  const rb = cfg.compute(bad);
  near("価数を落としたときの CBE (%)", rb.cbe, -22.3, 5e-3);
  near("そのときの Σ陽イオン (meq/L)", rb.cat, 2.8532, 1e-3);
  say2("合計は 2 倍ずれていない", Math.abs(rb.ani / rb.cat - 2) > 0.3);
  // ずれの大きさは Ca の寄与のちょうど半分
  const r0 = cfg.compute(meq(SPRING));
  near("ずれは Ca の寄与の半分", (r0.cat - rb.cat) / (meq(SPRING).Ca / 2), 1, 1e-9);

  /* 本文に式を出した3つの派生量 */
  near("EC = 100 × Σ陽イオン", r0.ec / r0.cat, 100, 1e-12);
  near("全硬度 = (Ca+Mg) × 50.04",
       r0.hardness / (meq(SPRING).Ca + meq(SPRING).Mg), 50.04, 1e-12);
  // I = ½ Σ m z²（mol/L 基準）。手で積んだ値と照合する。
  const Z = { Ca:2, Mg:2, Na:1, K:1, HCO3:1, SO4:2, Cl:1, NO3:1 };
  let I = 0;
  Object.keys(Z).forEach(function (k) {
    const m = meq(SPRING)[k] / Z[k] / 1000;   // mmol/L → mol/L
    I += m * Z[k] * Z[k];
  });
  near("イオン強度 I (mol/L)", r0.ionic, 0.5 * I, 1e-12);
}

/* [L] 画面に出る文字列の言語（2026-11-14 英語版の追加にあわせて）
   ---------------------------------------------------------------------------
   英語版の判定文・ラベルに日本語が残っていないか、日本語版が英語に化けていないか。
   判定文は状態ごとに組み立てが違うので、すべての分岐を通して確かめる。 */

console.log("\n[L] 画面の文字列の言語（" + LANG + "）");
{
  const CJK = /[぀-ヿ一-鿿！-｠]/;
  const isEn = /^en/.test(LANG);
  const say = (label, cond) => {
    checks++; if (!cond) failed++;
    console.log((cond ? "  PASS  " : "  FAIL  ") + label);
  };
  const right = (s) => isEn ? !CJK.test(s) : CJK.test(s);

  // gwcalc.js の共通文字列（単位セレクトの読み上げ名など）
  const T = GwCalc._ui();
  say("gwcalc.js の単位ラベル: " + T.unitFor("Ca²⁺"), right(T.unitFor("Ca²⁺")));
  say("gwcalc.js の逆算タブ名: " + T.solveFor,       right(T.solveFor));

  // 判定文の全分岐
  const base = meq(SPRING);
  const cases = {
    "入力なし":           {},
    "希薄（絶対差で可）": meq({ Ca:0.8, Mg:0.2, Na:1.2, K:0.1, HCO3:1.5, SO4:2.2, Cl:1.8, NO3:1.0 }),
    "±2 % 以内":          base,
    "2〜5 %":             meq(Object.assign({}, SPRING, { Ca: 73 })),
    "陽イオン過剰 warn":  meq(Object.assign({}, SPRING, { Ca: 85 })),
    "陰イオン過剰 warn":  meq(Object.assign({}, SPRING, { HCO3: 260 })),
    "crit":               meq(Object.assign({}, SPRING, { Ca: 95 }))
  };
  Object.keys(cases).forEach(function (k) {
    const res = cfg.check(cfg.compute(cases[k]));
    say(("判定文「" + k + "」").padEnd(22) + " [" + res.state + "] " +
        res.text.slice(0, 60) + "…", right(res.text));
  });

  // 見出し・出力欄・脚注
  say("見出し: " + cfg.headline.label, right(cfg.headline.label));
  cfg.outputs.forEach(function (o) {
    const s = o.label + (o.note ? " / " + o.note : "");
    say("出力欄: " + s, right(s));
  });
  say("脚注", right(cfg.footnote));

  // 図の寸法線ラベル（drawBars がスタブの textContent に書く）
  cfg.onUpdate(cfg.compute(cases["陽イオン過剰 warn"]));
  say("図の差のラベル: " + stubNode.textContent, right(stubNode.textContent));
}

if (checks === 0) {
  console.log("\n" + TOOL + ": 検証がまだ 1 件も書かれていない。TODO を埋めること。");
  process.exit(1);
}
console.log("\n" + (failed === 0
  ? TOOL + ": " + checks + " 件すべて一致した。"
  : TOOL + ": " + checks + " 件中 " + failed + " 件が不一致。"));
process.exit(failed === 0 ? 0 : 1);
