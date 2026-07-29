# -*- coding: utf-8 -*-
"""
#13 図生成スクリプト（地下水科学入門 #13 — 酸化還元と熊本のヒ素）
CLAUDE.md 準拠：.qmd に {python} を直書きせず、PNG を事前生成して静的参照。

データ出所：PHREEQC (WATEQ4F.dat) 実行結果（D:\\Hityu\\GROUNDWATER_proj\\Sci13）
  A_as_speciation.sel  -> 図2（As化学種 vs pe/Eh）
  B_redox_ladder.sel   -> 図1（レドックスの梯子）※収束した 0-3 mmol を使用
  C_as_release.sel     -> 図3（Fe酸化物の還元的溶解でAs放出）※Cの再実行後に追加
英語ラベル・Times New Roman・#11/#12と統一。
"""

import numpy as np
import matplotlib.pyplot as plt

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

C_O2  = "#1f77b4"
C_NO3 = "#2ca02c"
C_MN  = "#9467bd"
C_FE  = "#c0392b"
C_SO4 = "#e08a1e"
C_HS  = "#8c564b"
C_PE  = "#222222"

# =====================================================================
# 図1: レドックスの梯子 (B_redox_ladder.sel, 収束域 0-3 mmol CH2O)
# =====================================================================
# CH2O 添加量 (mmol)
x = np.array([0, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0, 2.5, 3.0])
pe = np.array([14.04, 14.05, 13.98, 12.59, 12.50, 12.37, -0.71, -5.80, -5.89, -5.96, -5.89])
# 濃度 (mmol/L)  ※.sel の mol/kgw を ×1000
O2  = np.array([0.50, 0.30, 0.10, 0.0002, 0.0001, 0.00003, 0, 0, 0, 0, 0])
NO3 = np.array([0.50, 0.50, 0.50, 0.38, 0.22, 0.06, 0, 0, 0, 0, 0])
Mn  = np.array([0, 0, 0, 0, 0, 0, 0.050, 0.050, 0.050, 0.050, 0.050])
Fe2 = np.array([0, 0, 0, 0, 0, 0, 0.40, 1.50, 1.72, 1.95, 2.00])
SO4 = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 0.88, 0.65, 0.42, 0.18])
HS  = np.array([0, 0, 0, 0, 0, 0, 0, 0.119, 0.351, 0.580, 0.817])

fig, (axU, axL) = plt.subplots(2, 1, figsize=(8.4, 7.4), sharex=True,
                               gridspec_kw={"height_ratios": [1, 1.5]})

# Fe 還元ゾーン(=As 放出)を陰影
for ax in (axU, axL):
    ax.axvspan(0.9, 3.05, color="#fbeaea", zorder=0)

# 上：pe
axU.plot(x, pe, "o-", color=C_PE, lw=2, ms=6)
axU.set_ylabel("pe  (electron availability)")
axU.set_title("The redox sequence — electron acceptors are used in order",
              fontsize=13)
axU.grid(ls=":", lw=0.6, color="#cccccc"); axU.set_axisbelow(True)
# 高peプラトー=好気呼吸+脱窒。下段の各曲線(O2,NO3)と対応することを明記
axU.text(0.42, 9.0, "high pe:\nO$_2$ & NO$_3^-$ present\n(see lower panel)",
         fontsize=11, color="#444", ha="center", va="center")
axU.annotate("pe crashes once\nO$_2$ & NO$_3^-$ are used up",
             xy=(1.0, -0.7), xytext=(1.95, 7.0), fontsize=11.5, color="#444",
             ha="center", arrowprops=dict(arrowstyle="->", color="#999", lw=1.0))

# 下：各化学種
axL.plot(x, O2,  "o-", color=C_O2,  lw=1.8, ms=5, label="O$_2$")
axL.plot(x, NO3, "s-", color=C_NO3, lw=1.8, ms=5, label="NO$_3^-$")
axL.plot(x, Mn,  "^-", color=C_MN,  lw=1.8, ms=5, label="Mn$^{2+}$ (from MnO$_2$)")
axL.plot(x, Fe2, "D-", color=C_FE,  lw=2.2, ms=6, label="Fe$^{2+}$ (from Fe(OH)$_3$)")
axL.plot(x, SO4, "v-", color=C_SO4, lw=1.8, ms=5, label="SO$_4^{2-}$")
axL.plot(x, HS,  "P-", color=C_HS,  lw=1.8, ms=5, label="H$_2$S / HS$^-$")
axL.set_xlabel("Organic matter added, CH$_2$O  (mmol L$^{-1}$) — reaction progress →")
axL.set_ylabel("Concentration  (mmol L$^{-1}$)")
axL.grid(ls=":", lw=0.6, color="#cccccc"); axL.set_axisbelow(True)
axL.legend(loc="upper left", fontsize=10, frameon=False, ncol=1)
axL.text(2.25, 1.28, "Fe reduction zone\n= As released", fontsize=13,
         color=C_FE, ha="center", va="center", fontweight="bold")

fig.tight_layout()
fig.savefig("fig1_redox_ladder.png", bbox_inches="tight")
plt.close(fig)
print("saved fig1_redox_ladder.png")

# =====================================================================
# 図2: ヒ素の化学種は pe(≒Eh) で決まる (A_as_speciation.sel)
# =====================================================================
peA   = np.array([12, 10, 8, 6, 4, 2, 0, -2, -4])
As3   = np.array([8.27e-34, 8.28e-30, 8.28e-26, 8.28e-22, 8.28e-18,
                  8.27e-14, 8.26e-10, 7.29e-7, 8.00e-7])
As5   = np.array([8.00e-7, 8.00e-7, 8.00e-7, 8.00e-7, 8.00e-7,
                  8.00e-7, 7.99e-7, 7.05e-8, 7.74e-12])
Fe2v  = np.array([1.48e-15, 1.48e-13, 1.48e-11, 1.48e-9, 1.46e-7,
                  5.60e-6, 8.95e-6, 9.00e-6, 9.00e-6])
Fe3v  = np.array([9.00e-6, 9.00e-6, 9.00e-6, 9.00e-6, 8.85e-6,
                  3.40e-6, 5.43e-8, 5.46e-10, 5.46e-12])
fAs3 = As3 / (As3 + As5)          # As(III) 分率
fFe2 = Fe2v / (Fe2v + Fe3v)       # Fe(II) 分率

fig, ax = plt.subplots(figsize=(8.2, 5.0))

# 中間ゾーン：鉄は還元済みだが As はまだ砒酸 As(V)＝「鉄が先」の証拠
ax.axvspan(1.7, -1.0, color="#fde7d6", zorder=0)
ax.text(0.35, 0.40, "Fe already reduced,\nbut As still\narsenate As(V)",
        fontsize=9.5, color="#8a5410", ha="center", va="center")
# 完全還元側
ax.axvspan(-1.0, -4.8, color="#eaf2fb", zorder=0)
ax.text(-3.1, 0.24, "fully reducing\n(As → arsenite)",
        fontsize=9.5, color="#2c6fbb", ha="center")

# Fe(II) を上位zorderで(Fe≥As を視覚化) → As が Fe の上に見える誤読を防ぐ
ax.plot(peA, fFe2, "s-", color=C_O2, lw=2.6, ms=6, zorder=5,
        label="Fe(II) fraction  (iron reduced first)")
ax.plot(peA, fAs3, "o-", color=C_FE, lw=2.6, ms=6, zorder=4,
        label="As(III) fraction  (arsenite, later)")

# 交代点の縦線
ax.axvline(1.7,  color=C_O2, lw=1.0, ls="--", zorder=1)
ax.axvline(-1.0, color=C_FE, lw=1.0, ls="--", zorder=1)

# 直接ラベル（色で対応づけ：Feは高pe側、Asは低pe側）
ax.text(3.3, 0.60, "Fe(II)", fontsize=12.5, color=C_O2, ha="center", fontweight="bold")
ax.text(-2.5, 0.60, "As(III)", fontsize=12.5, color=C_FE, ha="center", fontweight="bold")

ax.axhline(0.5, color="#bbb", lw=0.8, ls=":")
ax.set_xlabel("pe  (oxidizing →  large;  reducing →  small)")
ax.set_ylabel("Fraction of reduced species")
ax.set_xlim(12.8, -4.8)      # 酸化的(左)→還元的(右)
ax.set_ylim(-0.03, 1.08)
ax.grid(ls=":", lw=0.6, color="#cccccc"); ax.set_axisbelow(True)
ax.legend(loc="center left", fontsize=10.5, frameon=False)

# 副軸：Eh(mV) = 59.2 * pe (25C)
axT = ax.twiny()
axT.set_xlim(59.2 * 12.8, 59.2 * -4.8)
axT.set_xlabel("Eh  (mV, SHE)   [$E_h \\approx 59.2 \\times$ pe]")

ax.set_title("Iron is reduced first, arsenic second\n"
             "(As(V) arsenate → As(III) arsenite; pH = 8, PHREEQC / WATEQ4F)",
             fontsize=12, pad=26)
fig.tight_layout()
fig.savefig("fig2_as_speciation.png", bbox_inches="tight")
plt.close(fig)
print("saved fig2_as_speciation.png")

# =====================================================================
# 図3: Fe酸化物の還元的溶解が収着 As を解き放つ (C_as_release.sel)
# =====================================================================
xc      = np.array([0, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.3, 1.6, 2.0])   # CH2O mmol
As_mol  = np.array([3.72e-8, 1.36e-6, 4.51e-6, 4.64e-6, 4.77e-6,
                    4.90e-6, 5.00e-6, 5.00e-6, 5.00e-6, 5.00e-6])
As_ugL  = As_mol * 74.9216e6           # µg/L
FeOH3   = np.array([1.001, 0.604, 0.363, 0.320, 0.248,
                    0.155, 0.0, 0.0, 0.0, 0.0])                 # mmol 残存

fig, ax = plt.subplots(figsize=(7.6, 4.8))

# 左軸：溶存 As (µg/L, log)
ax.plot(xc, As_ugL, "o-", color=C_FE, lw=2.4, ms=7, label="dissolved As")
ax.set_yscale("log")
ax.set_xlabel("Organic matter added, CH$_2$O  (mmol L$^{-1}$) — reduction proceeds →")
ax.set_ylabel("Dissolved As  (µg L$^{-1}$, log)", color=C_FE)
ax.tick_params(axis="y", labelcolor=C_FE)
ax.set_ylim(1, 800)
ax.grid(ls=":", lw=0.6, color="#cccccc"); ax.set_axisbelow(True)

# 飲料水基準 10 µg/L
ax.axhline(10, color="#333", lw=1.0, ls="--")
ax.text(1.98, 12, "WHO / Japan limit 10 µg L$^{-1}$", fontsize=10.5,
        color="#333", ha="right", va="bottom")

# 右軸：Fe(OH)3 残存 (mmol)
axF = ax.twinx()
axF.plot(xc, FeOH3, "s--", color=C_O2, lw=1.8, ms=5, label="Fe(OH)$_3$ remaining")
axF.set_ylabel("Fe(OH)$_3$ (ferrihydrite) remaining  (mmol L$^{-1}$)", color=C_O2)
axF.tick_params(axis="y", labelcolor=C_O2)
axF.set_ylim(-0.05, 1.1)

# 注記
ax.annotate("initially: As sorbed on Hfo\n(low dissolved As)",
            xy=(0.0, 2.8), xytext=(0.55, 1.5), fontsize=11, color="#555",
            ha="center", va="center",
            arrowprops=dict(arrowstyle="->", color="#999", lw=1.0))
ax.text(1.15, 55, "Fe(OH)$_3$ reductively dissolves\n→ sorbed As released",
        fontsize=12, color=C_FE, ha="center", va="center", fontweight="bold")

# 凡例(両軸)
l1 = ax.get_lines()[0]; l2 = axF.get_lines()[0]
ax.legend([l1, l2], ["dissolved As", "Fe(OH)$_3$ remaining"],
          loc="lower right", bbox_to_anchor=(1.0, 0.14), fontsize=11, frameon=False)

ax.set_title("Reductive dissolution of iron oxide releases sorbed arsenic\n"
             "(concept demo, Hfo surface complexation, PHREEQC / WATEQ4F)",
             fontsize=12, pad=10)
fig.tight_layout()
fig.savefig("fig3_as_release.png", bbox_inches="tight")
plt.close(fig)
print("saved fig3_as_release.png")

print("done (fig1, fig2, fig3).")
