# -*- coding: utf-8 -*-
"""
#12 図生成スクリプト（地下水科学入門 #12 — 熊本の高フッ素地下水を PHREEQC で再現）
CLAUDE.md 準拠：.qmd に {python} を直書きせず、ここで PNG を事前生成して静的参照する。

データ出所：PHREEQC (WATEQ4F.dat) 実行結果
  A_si_check.sel / B_exchange.sel / C_fluorite.sel  (D:\\Hityu\\GROUNDWATER_proj\\Sci12)
  値は本スクリプトに転記（再現可能・出所コメント付き）。
図1 SI照合 / 図2 陽イオン交換 / 図3 蛍石の頭打ち。英語ラベル・Times New Roman・#11と統一。
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 12,
    "axes.linewidth": 0.9,
    "axes.edgecolor": "#333333",
    "savefig.dpi": 150,
    "figure.dpi": 150,
})

COL_PHREEQC = "#2c6fbb"   # PHREEQC (this study)
COL_PAPER   = "#e08a1e"   # Hossain et al. 2016
COL_CA      = "#c0392b"   # Ca
COL_NA      = "#2c6fbb"   # Na
COL_PH      = "#6a6a6a"   # pH
COL_SI      = "#2c6fbb"
COL_F       = "#c0392b"

# =====================================================================
# 図1: SI 照合 (PHREEQC vs Hossain et al. 2016, Table 1)
# =====================================================================
# A_si_check.sel より
minerals = ["Calcite", "Fluorite", "Fluorapatite"]
si_phreeqc = {"1st": [-0.419, -1.810, 4.816], "2nd": [-0.417, -2.006, 4.839]}
si_paper   = {"1st": [-0.69, -2.19, 2.42],   "2nd": [-0.57, -2.26, 1.77]}

fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.4), sharey=True)
x = np.arange(len(minerals))
w = 0.38
for ax, aq, title in zip(axes, ["1st", "2nd"],
                         ["First (shallow) aquifer", "Second (deep) aquifer"]):
    ax.bar(x - w/2, si_phreeqc[aq], w, label="PHREEQC (this study)",
           color=COL_PHREEQC, edgecolor="#1b3f6b", linewidth=0.6)
    ax.bar(x + w/2, si_paper[aq], w, label="Hossain et al. (2016)",
           color=COL_PAPER, edgecolor="#8a5410", linewidth=0.6)
    ax.axhline(0, color="#333333", lw=1.0)
    ax.text(0.02, 0.02, "SI = 0  (saturation)", transform=ax.transAxes,
            fontsize=9, color="#333333", va="bottom")
    ax.set_xticks(x)
    ax.set_xticklabels(minerals, rotation=12)
    ax.set_title(title, fontsize=12)
    ax.grid(axis="y", ls=":", lw=0.6, color="#bbbbbb")
    ax.set_axisbelow(True)
axes[0].set_ylabel("Saturation Index  (SI)")
axes[0].set_ylim(-3.2, 6.6)
axes[0].legend(loc="upper left", fontsize=9.5, frameon=False)
# 注記：fluorapatite の絶対値はDB依存（符号=過飽和は一致）。棒の上の空白に配置。
for ax, aq in zip(axes, ["1st", "2nd"]):
    top = max(si_phreeqc[aq][2], si_paper[aq][2])
    ax.text(2, top + 0.35,
            "Fluorapatite: supersaturated in both\n"
            "(sign agrees; magnitude is DB-dependent)",
            fontsize=8.4, color="#555555", ha="center", va="bottom")
fig.suptitle("Saturation indices: PHREEQC reproduction vs. reported values",
             fontsize=13, y=1.0)
fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig("fig1_si_check.png", bbox_inches="tight")
plt.close(fig)
print("saved fig1_si_check.png")

# =====================================================================
# 図2: 陽イオン交換 Ca-HCO3 -> Na-HCO3 (B_exchange.sel)
# =====================================================================
# 初期(解析値) + 交換5点。Ca,Na は mmol/L。
Ca = np.array([1.400, 1.1525, 0.90906, 0.67153, 0.44402, 0.23784])
Na = np.array([0.300, 0.79498, 1.2819, 1.7570, 2.2120, 2.6244])
pH = np.array([7.300, 7.30246, 7.30494, 7.30743, 7.30989, 7.31218])
naca = Na / Ca
ca_removed = 1.400 - Ca   # 交換で除去された Ca (mmol) = 進行度

fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.4))

# 左：Ca と Na の推移
axL = axes[0]
axL.plot(ca_removed, Ca, "o-", color=COL_CA, lw=2, ms=6, label="Ca$^{2+}$")
axL.plot(ca_removed, Na, "s-", color=COL_NA, lw=2, ms=6, label="Na$^{+}$")
axL.set_xlabel("Ca$^{2+}$ removed by exchange  (mmol L$^{-1}$)")
axL.set_ylabel("Concentration  (mmol L$^{-1}$)")
axL.set_title("Cations swap: Ca$^{2+}$ down, Na$^{+}$ up")
axL.grid(ls=":", lw=0.6, color="#cccccc")
axL.legend(loc="center right", fontsize=10, frameon=False)
axL.set_axisbelow(True)

# 右：Na/Ca(対数) と pH
axR = axes[1]
l1, = axR.plot(ca_removed, naca, "^-", color="#7b3fa0", lw=2, ms=6,
               label="Na/Ca (molar)")
axR.set_yscale("log")
axR.set_xlabel("Ca$^{2+}$ removed by exchange  (mmol L$^{-1}$)")
axR.set_ylabel("Na/Ca ratio  (molar, log)", color="#7b3fa0")
axR.tick_params(axis="y", labelcolor="#7b3fa0")
axR.set_title("Na/Ca rises steeply — but pH stays flat")
axR.grid(ls=":", lw=0.6, color="#cccccc")
axR.set_axisbelow(True)
axpH = axR.twinx()
l2, = axpH.plot(ca_removed, pH, "o--", color=COL_PH, lw=1.6, ms=5, label="pH")
axpH.set_ylabel("pH", color=COL_PH)
axpH.tick_params(axis="y", labelcolor=COL_PH)
axpH.set_ylim(6.8, 7.8)
axR.legend(handles=[l1, l2], loc="upper left", fontsize=9.5, frameon=False)
axR.text(0.97, 0.06,
         "exchange changes water TYPE\n(Ca-HCO$_3$ → Na-HCO$_3$),\nnot pH",
         transform=axR.transAxes, fontsize=8.4, color="#555555",
         ha="right", va="bottom")

fig.suptitle("Cation exchange drives Ca-HCO$_3$ toward Na-HCO$_3$ water",
             fontsize=13, y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig("fig2_exchange.png", bbox_inches="tight")
plt.close(fig)
print("saved fig2_exchange.png")

# =====================================================================
# 図3: 蛍石(CaF2)による F の頭打ち (C_fluorite.sel)
# =====================================================================
Ca_c   = np.array([0.2, 0.7, 1.2, 2.2, 4.2, 6.2, 8.2, 10.2, 12.2])   # mmol/L
si_fl  = np.array([-1.4845, -0.9580, -0.7412, -0.5101, -0.2839,
                   -0.1601, -0.0777, -0.0172, 0.0000])
Ftot   = np.array([80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 77.296])  # µmol/L
Fmg    = Ftot * 18.998 / 1000.0   # mg/L

fig, ax = plt.subplots(figsize=(7.4, 4.7))

# 現実の Na-HCO3 水（低Ca）帯を陰影
ax.axvspan(0.1, 1.0, color="#eaf2fb", zorder=0)
ax.text(0.30, -0.52, "real high-F\nNa-HCO$_3$ waters\n(low Ca)",
        fontsize=8.6, color="#2c6fbb", ha="center", va="center")

# 左軸：SI fluorite
ax.plot(Ca_c, si_fl, "o-", color=COL_SI, lw=2, ms=6, label="SI fluorite")
ax.axhline(0, color="#333333", lw=1.0, ls="-")
ax.text(0.12, 0.05, "SI = 0  (fluorite saturation)", fontsize=9,
        color="#333333", va="bottom")
ax.set_xscale("log")
ax.set_xlabel("Ca$^{2+}$ in solution  (mmol L$^{-1}$, log)")
ax.set_ylabel("SI fluorite  (CaF$_2$)", color=COL_SI)
ax.tick_params(axis="y", labelcolor=COL_SI)
ax.set_ylim(-1.75, 0.6)
ax.grid(ls=":", lw=0.6, color="#cccccc")
ax.set_axisbelow(True)

# 右軸：全フッ素 (mg/L)
axF = ax.twinx()
axF.plot(Ca_c, Fmg, "s--", color=COL_F, lw=1.8, ms=5, label="total F")
axF.set_ylabel("Total dissolved F  (mg L$^{-1}$)", color=COL_F)
axF.tick_params(axis="y", labelcolor=COL_F)
axF.set_ylim(1.35, 1.60)

# 頭打ちポイント注記（SI=0 線の上側の空白へ）
ax.annotate("fluorite saturates →\nCaF$_2$ precipitates, F capped",
            xy=(12.2, 0.0), xytext=(2.2, 0.40),
            fontsize=8.8, color="#555555", ha="center", va="center",
            arrowprops=dict(arrowstyle="->", color="#888888", lw=0.9,
                            connectionstyle="arc3,rad=0.25"))

lines = ax.get_lines()[:1] + axF.get_lines()[:1]
ax.legend(lines, ["SI fluorite", "total F"], loc="lower right",
          fontsize=10, frameon=False)
ax.set_title("Only at very high Ca does fluorite cap fluoride\n"
             "— at the low Ca of Na-HCO$_3$ waters, it never does",
             fontsize=12, pad=12)
fig.tight_layout()
fig.savefig("fig3_fluorite.png", bbox_inches="tight")
plt.close(fig)
print("saved fig3_fluorite.png")

print("done.")
