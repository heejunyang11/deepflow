# -*- coding: utf-8 -*-
"""
#14 図生成スクリプト（地下水科学入門 #14 — 同位体で読む地下水の年齢と涵養源）
CLAUDE.md 準拠：.qmd に {python} を直書きせず PNG を事前生成して静的参照。
#14 は同位体・年代（物理トレーサー）回で PHREEQC 不要。図は関係式＋論文の代表値で構成。
  図1 天水線(GMWL)と高度効果 / 図2 年代トレーサーの大気入力履歴 / 図3 熊本A-A'の85Kr年代×水質。
英語ラベル・Times New Roman・#11–13と統一。※模式的な代表値を含む(本文で明示)。
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

C_LINE = "#2c6fbb"
C_PT   = "#c0392b"
C_EVAP = "#e08a1e"

# =====================================================================
# 図1: 天水線 (GMWL) と高度効果  δD = 8 δ18O + 10
# =====================================================================
fig, ax = plt.subplots(figsize=(8.8, 7.0))

# x=0 / y=0（VSMOW基準）に太い点線
ax.axhline(0, color="#666", lw=1.6, ls=(0, (7, 4)), zorder=1)
ax.axvline(0, color="#666", lw=1.6, ls=(0, (7, 4)), zorder=1)

# --- GMWL 本体 ---
o = np.linspace(-12, 1.5, 120)
ax.plot(o, 8 * o + 10, "-", color=C_LINE, lw=3.0, zorder=3,
        label="GMWL:  δD = 8 δ¹⁸O + 10")

# --- 地下水(=涵養時の降水)は線の上に乗る ---
rech_o = np.array([-6.5, -7.5, -8.5])
rech_d = 8 * rech_o + 10
ax.plot(rech_o, rech_d, "o", color=C_PT, ms=12, zorder=5,
        label="groundwater (plots on the line)")

# --- 高度効果：線の両端に「重い/軽い」を明示（点への細い引出線）---
ax.annotate("lower / warmer /\ncoastal recharge\n(heavier)",
            xy=(rech_o[0], rech_d[0]), xytext=(-4.7, -57),
            fontsize=13, color=C_PT, ha="center", va="center",
            arrowprops=dict(arrowstyle="-", color="#e0a9a0", lw=1.0))
ax.annotate("higher / colder /\ninland recharge\n(lighter)",
            xy=(rech_o[2], rech_d[2]), xytext=(-9.7, -77),
            fontsize=13, color=C_PT, ha="center", va="center",
            arrowprops=dict(arrowstyle="-", color="#e0a9a0", lw=1.0))

# --- 蒸発：上端の涵養点から右上へ外れる（線を離れる）---
ev_o = np.array([-6.5, -5.2, -3.9, -2.8])
ev_d = rech_d[0] + 4.5 * (ev_o - rech_o[0])   # 傾き4.5で分岐
ax.plot(ev_o, ev_d, "s--", color=C_EVAP, lw=2.4, ms=8, zorder=4,
        label="evaporated water (leaves the line)")
ax.annotate("evaporation:\nwater leaves the line\n(slope ≈ 4–5)",
            xy=(ev_o[-1], ev_d[-1]), xytext=(-6.5, -12),
            fontsize=13, color=C_EVAP, ha="center", va="center",
            arrowprops=dict(arrowstyle="->", color=C_EVAP, lw=1.7))

# --- 海水 = VSMOW = 原点 ---
ax.plot(0, 0, "*", color="#222", ms=22, zorder=7)
ax.text(-0.3, -2.5, "seawater\n(VSMOW = 0)", fontsize=12.5, color="#222",
        ha="right", va="top")

# --- 読み方の一言（右下の余白）---
ax.text(-3.1, -78,
        "How to read it:\na water's spot on the line\n= its recharge (elevation,\nclimate). Evaporation pushes\nit off the line, to the right.",
        fontsize=12, color="#333", ha="center", va="center",
        bbox=dict(boxstyle="round,pad=0.45", fc="#f6f6f6", ec="#bbbbbb"))

ax.set_xlabel("δ¹⁸O  (‰, VSMOW)", fontsize=14.5)
ax.set_ylabel("δD  (‰, VSMOW)", fontsize=14.5)
ax.tick_params(axis="both", labelsize=13)
ax.set_xlim(-12, 2)
ax.set_ylim(-92, 16)
ax.grid(ls=":", lw=0.6, color="#cccccc"); ax.set_axisbelow(True)
ax.legend(loc="upper left", fontsize=12, frameon=True, framealpha=0.9,
          edgecolor="#cccccc")
ax.set_title("The meteoric water line (δD vs δ¹⁸O)\n"
             "— where does a water plot, and why?", fontsize=14.5)
fig.tight_layout()
fig.savefig("fig1_gmwl.png", bbox_inches="tight")
plt.close(fig)
print("saved fig1_gmwl.png")

# =====================================================================
# 図2: 年代トレーサーの大気入力履歴 (模式・北半球)
# =====================================================================
fig, ax = plt.subplots(figsize=(8.2, 4.9))
yr = np.linspace(1940, 2020, 400)

# 3H: 1963 ボムピーク(相対) ガウス的減衰
tri = 0.05 + 1.0 * np.exp(-((yr - 1963) / 4.0) ** 2)
tri = np.where(yr < 1952, 0.05, tri)
# CFC-12: シグモイド増加→頭打ち(相対)
cfc = 1.0 / (1 + np.exp(-(yr - 1975) / 8.0))
# 85Kr: ほぼ単調増加(相対)
kr = np.clip((yr - 1950) / (2015 - 1950), 0, 1) ** 0.9
# SF6: 近年に加速増加(相対)
sf6 = np.clip((yr - 1970) / (2015 - 1970), 0, 1) ** 1.8

ax.plot(yr, tri, color="#c0392b", lw=2.2, label="³H (tritium) — bomb peak 1963")
ax.plot(yr, cfc, color="#2c6fbb", lw=2.2, label="CFCs — rise then plateau")
ax.plot(yr, kr,  color="#2e8b57", lw=2.2, label="⁸⁵Kr — steady rise")
ax.plot(yr, sf6, color="#8c564b", lw=2.0, ls="--", label="SF₆ — recent rise")

ax.annotate("³H bomb peak\n(1963)", xy=(1963, 1.0), xytext=(1972, 1.02),
            fontsize=9.5, color="#c0392b",
            arrowprops=dict(arrowstyle="->", color="#c0392b", lw=1.0))
ax.text(1996, 0.20,
        "In cities, CFCs & SF₆ are\ncontaminated (extra sources)\n→ ⁸⁵Kr more reliable",
        fontsize=9, color="#555", ha="center",
        bbox=dict(boxstyle="round,pad=0.3", fc="#f4f4f4", ec="#cccccc"))

ax.set_xlabel("Year")
ax.set_ylabel("Atmospheric level  (relative, schematic)")
ax.set_xlim(1940, 2020)
ax.set_ylim(0, 1.15)
ax.grid(ls=":", lw=0.6, color="#cccccc"); ax.set_axisbelow(True)
ax.legend(loc="upper left", fontsize=9.5, frameon=False)
ax.set_title("Age tracers: each has a known atmospheric history (a clock)\n"
             "(schematic, Northern Hemisphere)", fontsize=12)
fig.tight_layout()
fig.savefig("fig2_tracers.png", bbox_inches="tight")
plt.close(fig)
print("saved fig2_tracers.png")

# =====================================================================
# 図3: 熊本 A–A' の 85Kr 年代 × 水質 (Kagabu 2017)
# =====================================================================
fig, ax = plt.subplots(figsize=(7.8, 4.9))

zones = ["Recharge\narea", "Discharge\narea", "Stagnant\nzone"]
ages  = [16, 36, 55]          # 85Kr 見かけ年代 (yr) ; 停滞域は ≥55(下限)
xpos  = [0, 1, 2]
colors = ["#7fb2e5", "#4a90d9", "#c0392b"]
bars = ax.bar(xpos, ages, width=0.55, color=colors, edgecolor="#333", linewidth=0.7)
ax.set_xticks(xpos); ax.set_xticklabels(zones, fontsize=11)
ax.set_ylabel("⁸⁵Kr apparent age  (years)")
ax.set_ylim(0, 72)
ax.grid(axis="y", ls=":", lw=0.6, color="#cccccc"); ax.set_axisbelow(True)

# 年代ラベル
for x, a, t in zip(xpos, ages, ["≈ 16", "≈ 36", "≥ 55"]):
    ax.text(x, a + 1.5, t, ha="center", fontsize=12, fontweight="bold")

# 停滞域＝高F/高As
ax.annotate("high fluoride (#12)\n& arsenic (#13)\nconcentrate here",
            xy=(2, 55), xytext=(1.15, 60), fontsize=9.6, color="#c0392b",
            ha="center", arrowprops=dict(arrowstyle="->", color="#c0392b", lw=1.1))
# 流れの向き
ax.annotate("groundwater flow  →  older water",
            xy=(2.05, 6), xytext=(-0.05, 6), fontsize=9.5, color="#555",
            ha="left", arrowprops=dict(arrowstyle="->", color="#888", lw=1.2))

ax.set_title("Groundwater gets older along the flow line (Kumamoto A–A′)\n"
             "⁸⁵Kr: recharge ≈16 yr → discharge ≈36 yr → stagnant ≥55 yr "
             "(Kagabu et al. 2017)", fontsize=11.5)
fig.tight_layout()
fig.savefig("fig3_age_flowline.png", bbox_inches="tight")
plt.close(fig)
print("saved fig3_age_flowline.png")

print("done (fig1, fig2, fig3).")
