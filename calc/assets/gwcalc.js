/* ---------------------------------------------------------------------------
 * gwcalc.js — GroundwaterCalc の共通計算機ライブラリ
 *
 * 各ツールページは GwCalc.mount() に「入力の定義・compute 関数・出力の定義」
 * を渡すだけでよい。UI の組み立て・単位換算・数値整形・妥当性判定の表示は
 * すべてここが引き受ける。
 *
 * 使い方の最小形：
 *
 *   GwCalc.mount("#calc", {
 *     inputs: [
 *       { id:"K", sym:"K", label:"Hydraulic conductivity", value:1e-4,
 *         units:{ "m/s":1, "m/day":1.157407e-5 } },
 *       ...
 *     ],
 *     compute: (v, target) => ({ Q: v.K * v.A * v.dh / v.L }),
 *     outputs: [ { key:"Q", sym:"Q", label:"Discharge", unit:"m³/day", scale:86400 } ]
 *   });
 *
 * compute が受け取る v は必ず SI 単位に正規化済みである。返り値のキーを
 * outputs / headline / check / onUpdate が参照する。
 *
 * 入力に type:"text" を指定すると文字列欄になり、その id の値は換算されず
 * 文字列のまま compute へ渡る（化学式のように単位を持たない入力のため）。
 * 単位セレクトは付かない。
 * ------------------------------------------------------------------------- */

window.GwCalc = (function () {
  "use strict";

  /* ---- 数値整形 -------------------------------------------------------- */

  var SUP = { "-":"⁻", "0":"⁰", "1":"¹", "2":"²", "3":"³", "4":"⁴",
              "5":"⁵", "6":"⁶", "7":"⁷", "8":"⁸", "9":"⁹" };

  function sup(s) {
    return String(s).split("").map(function (c) { return SUP[c] || c; }).join("");
  }

  /** 桁を保った表示用整形。小さい/大きい値は上付き指数にする。 */
  function fmt(x, sig) {
    sig = sig || 3;
    if (x === null || x === undefined || !isFinite(x)) return "—";
    if (x === 0) return "0";
    var abs = Math.abs(x);
    if (abs >= 1e-3 && abs < 1e5) {
      return Number(x.toPrecision(sig)).toLocaleString("en-US", { maximumFractionDigits: 8 });
    }
    var exp = Math.floor(Math.log10(abs));
    var mant = Number((x / Math.pow(10, exp)).toPrecision(sig));
    if (Math.abs(mant) >= 10) { mant /= 10; exp += 1; }
    return mant + "×10" + sup(exp);
  }

  /** 入力欄に書き戻すときの整形（パースし直せる形を保つ）。 */
  function fmtField(x) {
    if (!isFinite(x)) return "";
    var abs = Math.abs(x);
    if (abs !== 0 && (abs < 1e-4 || abs >= 1e6)) return x.toExponential(3);
    return String(Number(x.toPrecision(5)));
  }

  /* ---- check() の戻り値を作るヘルパー ---------------------------------- */

  function ok(text)   { return { state: "good", text: text }; }
  function warn(text) { return { state: "warn", text: text }; }
  function crit(text) { return { state: "crit", text: text }; }

  /* ---- DOM 補助 -------------------------------------------------------- */

  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html !== undefined) n.innerHTML = html;
    return n;
  }

  function symHTML(sym) {
    return sym ? ' <em class="gw-sym">' + sym + "</em>" : "";
  }

  /* ---- 本体 ------------------------------------------------------------ */

  function mount(selector, cfg) {
    var root = typeof selector === "string" ? document.querySelector(selector) : selector;
    if (!root) { console.error("GwCalc: mount target not found:", selector); return; }

    var inputs = cfg.inputs || [];
    var solveFor = cfg.solveFor || null;          // 例: ["Q","K","dh"]
    var target = solveFor ? solveFor[0] : null;   // いま解いている変数
    var fields = {};                              // id -> {input, unit, box}

    root.classList.add("gw-root");

    /* --- 図はパネルの上に全幅で置く（横長の装置図がパネル内では潰れるため） --- */
    if (cfg.figure) {
      var tpl = document.querySelector(cfg.figure);
      if (tpl) {
        var figWrap = el("div", "gw-figure");
        figWrap.appendChild(tpl.content.cloneNode(true));
        root.appendChild(figWrap);
      }
    }

    var panels = el("div", "gw");
    var paneIn = el("div", "gw-pane gw-inputs");
    var paneOut = el("div", "gw-pane gw-stage");
    panels.appendChild(paneIn);
    panels.appendChild(paneOut);
    root.appendChild(panels);

    /* --- solve-for タブ --- */
    if (solveFor) {
      paneIn.appendChild(el("p", "gw-panetitle", "Solve for"));
      var tabs = el("div", "gw-solvefor");
      tabs.setAttribute("role", "group");
      tabs.setAttribute("aria-label", "Quantity to solve for");
      solveFor.forEach(function (id) {
        var def = inputs.filter(function (f) { return f.id === id; })[0] || {};
        var b = el("button", null, (def.short || def.label || id) + symHTML(def.sym));
        b.type = "button";
        b.dataset.solve = id;
        b.setAttribute("aria-pressed", String(id === target));
        b.addEventListener("click", function () { setTarget(id); });
        tabs.appendChild(b);
      });
      paneIn.appendChild(tabs);
    }

    /* --- 入力欄 --- */
    inputs.forEach(function (f) {
      var box = el("div", "gw-field");
      box.dataset.for = f.id;

      var lab = el("label", null, f.label + symHTML(f.sym) +
        (f.hint ? ' <span class="gw-hint">' + f.hint + "</span>" : ""));
      lab.setAttribute("for", "gw-" + f.id);
      box.appendChild(lab);

      // type:"text" の欄は文字列をそのまま compute へ渡す（化学式など）。
      // 単位の概念が無いので単位セレクトは付けない。
      var isText = (f.type === "text");

      var combo = el("div", "gw-combo");
      var inp = el("input");
      inp.id = "gw-" + f.id;
      inp.value = f.value;

      if (isText) {
        inp.type = "text";
        inp.spellcheck = false;
        inp.setAttribute("autocomplete", "off");
        inp.setAttribute("autocapitalize", "off");
      } else {
        inp.type = "number";
        inp.inputMode = "decimal";
        if (f.min !== undefined) inp.min = f.min;
        if (f.max !== undefined) inp.max = f.max;

        // step を指定した欄だけスピナーを出す。step="any" のときブラウザは
        // スピナーを 1 ずつ動かすため、0〜1 の量（間隙率）では min/max に阻まれて
        // 何も起きず、対数スケールの量（K=1e-4）では 1.0001 になって無意味になる。
        if (f.step !== undefined) {
          inp.step = f.step;
        } else {
          inp.step = "any";
          inp.dataset.nospin = "";
        }
      }
      combo.appendChild(inp);

      var sel = el("select");
      sel.setAttribute("aria-label", "Unit for " + f.label);
      if (f.units) {
        Object.keys(f.units).forEach(function (u) {
          var o = el("option", null, u);
          o.value = f.units[u];
          sel.appendChild(o);
        });
      } else {
        sel.appendChild(el("option", null, "–"));
        sel.disabled = true;
      }
      if (!isText) combo.appendChild(sel);
      box.appendChild(combo);
      paneIn.appendChild(box);

      /* プリセット（材料名などから値を入れるボタン） */
      if (f.presets && f.presets.length) {
        var ps = el("div", "gw-presets");
        f.presets.forEach(function (p) {
          var b = el("button", null, p.label);
          b.type = "button";
          b.title = isText
            ? p.label + ": " + p.value
            : p.label + ": " + f.sym + " ≈ " + p.value +
              (f.presetUnit ? " " + f.presetUnit : "");
          b.addEventListener("click", function () {
            if (f.presetUnit && f.units && f.units[f.presetUnit] !== undefined) {
              sel.value = f.units[f.presetUnit];
            }
            inp.value = p.value;
            if (target === f.id && solveFor) setTarget(otherTarget(f.id));
            else update();
          });
          ps.appendChild(b);
        });
        paneIn.appendChild(ps);
      }

      inp.addEventListener("input", function () { if (!inp.readOnly) update(); });
      sel.addEventListener("change", update);

      fields[f.id] = { input: inp, unit: sel, box: box, def: f };
    });

    /* --- 見出しの結果 --- */
    var headline = el("div", "gw-headline");
    var hLab = el("span", "gw-lab");
    var hVal = el("span", "gw-val", "—");
    var hUnit = el("span", "gw-unit");
    headline.appendChild(hLab);
    var hRight = el("span");
    hRight.appendChild(hVal);
    hRight.appendChild(document.createTextNode(" "));
    hRight.appendChild(hUnit);
    headline.appendChild(hRight);
    paneOut.appendChild(headline);

    /* --- 副次的な結果 --- */
    var outs = el("dl", "gw-outs");
    (cfg.outputs || []).forEach(function (o, i) {
      var cell = el("div", "gw-out");
      // 単位はラベル側に括弧で置く。同じ量を別単位で並べたときに区別が付くため。
      // note は「見かけの値か実際の値か」のような、取り違えを防ぐ短い注記。
      cell.appendChild(el("dt", null,
        o.label + symHTML(o.sym) +
        (o.unit ? ' <span class="gw-unit">(' + o.unit + ")</span>" : "") +
        (o.note ? ' <span class="gw-out-note">' + o.note + "</span>" : "")));
      var dd = el("dd", null, "—");
      dd.dataset.slot = String(i);
      cell.appendChild(dd);
      outs.appendChild(cell);
    });
    paneOut.appendChild(outs);

    /* --- 妥当性の判定 --- */
    var verdict = null, vMark = null, vText = null;
    if (cfg.check) {
      verdict = el("div", "gw-verdict");
      vMark = el("span", "gw-mark", "✓");
      vText = el("span");
      verdict.appendChild(vMark);
      verdict.appendChild(vText);
      paneOut.appendChild(verdict);
    }

    /* --- 読み違えを防ぐための補足（判定の下に置く） --- */
    if (cfg.footnote) {
      paneOut.appendChild(el("div", "gw-footnote", cfg.footnote));
    }

    /* --- solve-for の切り替え --- */
    function otherTarget(id) {
      return solveFor.filter(function (t) { return t !== id; })[0];
    }

    function setTarget(id) {
      target = id;
      Array.prototype.forEach.call(root.querySelectorAll(".gw-solvefor button"), function (b) {
        b.setAttribute("aria-pressed", String(b.dataset.solve === id));
      });
      solveFor.forEach(function (t) {
        var f = fields[t];
        if (!f) return;
        var isOut = (t === id);
        f.box.classList.toggle("gw-locked", isOut);
        f.input.readOnly = isOut;
        f.input.tabIndex = isOut ? -1 : 0;
      });
      update();
    }

    /* --- SI 値の取り出し --- */
    function si(id) {
      var f = fields[id];
      if (!f) return NaN;
      // テキスト欄は文字列のまま渡す（単位換算の対象ではない）
      if (f.def && f.def.type === "text") return f.input.value.trim();
      var v = parseFloat(f.input.value);
      if (!isFinite(v)) return NaN;
      var m = f.unit.disabled ? 1 : parseFloat(f.unit.value);
      return v * (isFinite(m) ? m : 1);
    }

    /* --- 再計算 --- */
    function update() {
      var v = {};
      Object.keys(fields).forEach(function (id) { v[id] = si(id); });

      var r;
      try {
        r = cfg.compute(v, target) || {};
      } catch (e) {
        console.error("GwCalc: compute() threw", e);
        r = {};
      }

      /* 解いた変数を入力欄へ書き戻す */
      if (target && fields[target] && isFinite(r[target])) {
        var m = fields[target].unit.disabled ? 1 : parseFloat(fields[target].unit.value);
        fields[target].input.value = fmtField(r[target] / m);
      }

      /* 見出し */
      var hDef = cfg.headline
        ? (target ? cfg.headline[target] : cfg.headline)
        : null;
      if (hDef) {
        hLab.innerHTML = hDef.label + symHTML(hDef.sym);
        var hv = r[hDef.key || target];
        hVal.textContent = fmt(isFinite(hv) ? hv * (hDef.scale || 1) : NaN);
        hUnit.textContent = hDef.unit || "";
      }

      /* 副次的な結果 */
      (cfg.outputs || []).forEach(function (o, i) {
        var dd = outs.querySelector('[data-slot="' + i + '"]');
        if (!dd) return;
        var val = r[o.key];
        var shown = isFinite(val) ? fmt(val * (o.scale || 1), o.sig) : "—";
        dd.textContent = shown;   // 単位は dt 側の括弧に出している
      });

      /* 判定 */
      if (cfg.check && verdict) {
        var res = cfg.check(r, v) || { state: "warn", text: "" };
        verdict.dataset.state = res.state;
        vMark.textContent = { good: "✓", warn: "!", crit: "✕" }[res.state] || "!";
        vText.textContent = res.text;
      }

      /* ページ固有の後処理（図の更新など） */
      if (cfg.onUpdate) {
        try { cfg.onUpdate(r, v, root); }
        catch (e) { console.error("GwCalc: onUpdate() threw", e); }
      }
    }

    if (solveFor) setTarget(target); else update();

    return { update: update, fields: fields, setTarget: setTarget };
  }

  return { mount: mount, fmt: fmt, ok: ok, warn: warn, crit: crit, sup: sup };
})();
