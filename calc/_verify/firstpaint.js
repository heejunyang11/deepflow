/* ---------------------------------------------------------------------------
 * _verify/firstpaint.js — 「ページを開いた瞬間」の描画を再現する。
 *
 * 本物の GwCalc.mount() は、呼ばれたその場で 1 回目の compute() と onUpdate() を
 * 走らせる。ページの <script> のうち mount() より後ろに書いた var は、その時点では
 * まだ undefined である。図の寸法の定数をそこに置くと、開いた直後の図だけが NaN で
 * 描かれない（数字を 1 つ変えると直るので、気づきにくい）。
 *
 * 2026-11-14、イオンバランス・ダルシー・タイスの 3 ページで実際に起きていた。
 * それまでの _verify は mount() をスタブにして config を捕まえるだけで、onUpdate() は
 * スクリプトを最後まで評価した「後」に呼んでいたため、この不具合を再現できなかった。
 *
 * 使い方（各 _verify/<slug>.js の mount スタブの中で、config を捕まえた直後に）:
 *   firstPaint = require("./firstpaint.js")(c);
 * 戻り値は問題の一覧（空なら問題なし）。
 * ------------------------------------------------------------------------- */

module.exports = function firstPaint(c) {
  const bad = [];
  const flag = (where, v) => {
    if (/NaN|undefined|Infinity/.test(String(v))) bad.push(where + " = " + v);
  };

  // 図が触る DOM の代わり。数値でない値が書きこまれたら記録する。
  const node = {
    setAttribute(k, v) { flag("setAttribute(" + k + ")", v); },
    getAttribute() { return ""; },
    title: "", dataset: {}, firstChild: null, style: {},
    classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
    addEventListener() {}, removeChild() {}, appendChild() {}, insertBefore() {},
    querySelector() { return node; }, querySelectorAll() { return []; }
  };
  Object.defineProperty(node, "textContent", {
    get() { return ""; }, set(v) { flag("textContent", v); }
  });
  Object.defineProperty(node, "innerHTML", {
    get() { return ""; }, set(v) { flag("innerHTML", v); }
  });

  // 本物の mount と同じ既定値：各入力の value を、最初の単位で SI に直す
  const v = {};
  (c.inputs || []).forEach(function (f) {
    if (f.type === "text") { v[f.id] = String(f.value).trim(); return; }
    const u = f.units ? f.units[Object.keys(f.units)[0]] : 1;
    v[f.id] = parseFloat(f.value) * (isFinite(u) ? u : 1);
  });
  const target = c.solveFor ? c.solveFor[0] : undefined;

  const doc = global.document;
  const saved = { g: doc.getElementById, n: doc.createElementNS, e: doc.createElement };
  doc.getElementById = () => node;
  doc.createElementNS = () => node;
  doc.createElement = () => node;
  try {
    const r = c.compute(v, target) || {};
    if (c.onUpdate) c.onUpdate(r, v, node);
  } catch (e) {
    bad.push("例外: " + e.message);
  } finally {
    doc.getElementById = saved.g;
    doc.createElementNS = saved.n;
    doc.createElement = saved.e;
  }
  return bad;
};

/* 各 _verify の末尾で呼ぶ照合。checks / failed を増やすための値を返す。 */
module.exports.report = function (problems) {
  const ok = problems !== null && problems.length === 0;
  console.log("\n[0] ページを開いた瞬間の描画（mount() の中で 1 回目の onUpdate）");
  console.log((ok ? "  PASS  " : "  FAIL  ") + "図に NaN・undefined が書きこまれず、例外も出ない" +
              (problems === null ? "\n          mount() の中で検査が走らなかった" :
               problems.slice(0, 6).map((p) => "\n          " +
                 (p.length > 110 ? p.slice(0, 110) + "…" : p)).join("")));
  return ok;
};
