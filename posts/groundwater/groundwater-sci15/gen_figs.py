# -*- coding: utf-8 -*-
"""
#15 図生成スクリプト（地下水科学入門 #15 — 湧水と滞留時間：水質はどう"熟成"するか）
CLAUDE.md 準拠：.qmd に {python} を直書きせず PNG を事前生成して静的参照。
題材：霧島火山群の湧水（Ide et al. 2018, Chemical Geology 488, 44-55）。
  図1 SI検証     : PHREEQC(llnl.dat) 計算 vs 論文 Table 2 (試料 S-01) の符号照合。
  図2 反応経路   : 一次鉱物の溶解＋二次鉱物の析出で"熟成"を追う（gibbsite→kaolinite→Ca-smectite）。
  図3 活動度図   : 37湧水試料＋反応経路の軌跡を鉱物安定領域に重ねる（論文 Fig 5 の再現）。
データは PHREEQC 実行結果（deck A / deck B）と論文 Table 1/2 の公開値を埋め込み（再現可能・自己完結）。
英語ラベル・Times New Roman・#11–14 と統一。
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

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

C_CALC = "#c0392b"   # 私の計算
C_PAPER = "#2c6fbb"  # 論文値
C_GIB = "#e08a1e"    # gibbsite
C_KAO = "#2e8b57"    # kaolinite
C_SME = "#8e44ad"    # Ca-smectite
C_DSI = "#2c6fbb"
C_PH  = "#c0392b"

# =====================================================================
# 図1: SI 検証 (deck A, 試料 S-01)  ―  PHREEQC 計算 vs 論文 Table 2
# =====================================================================
# 相名（表示用） / 私の計算(A_si_check.sel) / 論文 Table 2 (S-01)
phases = ["Wollas-\ntonite", "Ferro-\nsilite", "Ensta-\ntite", "Anor-\nthite",
          "Albite", "Quartz", "am-\nsilica", "Kaolin-\nite", "Na-\nsmectite", "Ca-\nsmectite"]
si_calc  = [-6.61, -9.22, -4.52, -2.51,  2.19,  1.17, -0.17,  7.47,  7.23,  7.70]
si_paper = [-6.6,  -9.2,  -4.6,  -1.9,   0.0,   1.2,  -0.2,   7.5,   7.3,   7.7 ]

x = np.arange(len(phases)); w = 0.38
fig, ax = plt.subplots(figsize=(10.4, 5.4))
ax.axhline(0, color="#444", lw=1.2, zorder=2)
b1 = ax.bar(x - w/2, si_calc,  w, color=C_CALC,  edgecolor="#333", linewidth=0.6,
            label="This work — PHREEQC (llnl.dat)", zorder=3)
b2 = ax.bar(x + w/2, si_paper, w, color=C_PAPER, edgecolor="#333", linewidth=0.6,
            label="Ide et al. (2018), Table 2 (S-01)", zorder=3)

# 一次/二次の帯
ax.axvspan(-0.5, 4.5, color="#f6efe6", zorder=0)   # primary
ax.axvspan(4.5, 6.5, color="#eef3f7", zorder=0)    # silica
ax.axvspan(6.5, 9.5, color="#eef7f0", zorder=0)    # secondary
ax.text(2.0, 8.6, "primary minerals\n(SI < 0 → dissolve)", ha="center", fontsize=11, color="#8a6d3b")
ax.text(5.5, 8.6, "silica", ha="center", fontsize=11, color="#31708f")
ax.text(8.0, 8.6, "secondary clays\n(SI >> 0 → precipitate)", ha="center", fontsize=11, color="#3c763d")

ax.set_xticks(x); ax.set_xticklabels(phases, fontsize=10.5)
ax.set_ylabel("Saturation Index  (SI)", fontsize=13)
ax.set_ylim(-11, 10.2)
ax.grid(axis="y", ls=":", lw=0.6, color="#cccccc"); ax.set_axisbelow(True)
ax.legend(loc="lower right", fontsize=11, frameon=True, framealpha=0.95, edgecolor="#cccccc")
ax.set_title("Reproducing the saturation indices of a Kirishima spring (S-01)\n"
             "PHREEQC vs the published values — primary minerals dissolve, clays precipitate",
             fontsize=13)
# Albite の注記
ax.annotate("feldspar end-member\n(polymorph difference)", xy=(4.0, 2.2), xytext=(4.0, 5.6),
            fontsize=9, color="#555", ha="center",
            arrowprops=dict(arrowstyle="->", color="#999", lw=1.0))
fig.tight_layout()
fig.savefig("fig1_si_check.png", bbox_inches="tight")
plt.close(fig)
print("saved fig1_si_check.png")

# =====================================================================
# 反応経路データ (deck B: B_reaction_path.sel) を埋め込み
#   反応進行 rxn(mol) をおおよその接触時間の代理として用いる。
# =====================================================================
rxn   = np.array([2e-6, 5e-6, 1e-5, 2e-5, 5e-5, 1e-4, 2e-4, 4e-4, 7e-4, 1e-3, 1.5e-3, 2e-3])
pH_b  = np.array([6.286, 6.322, 6.376, 6.467, 6.661, 6.864, 7.073, 7.286, 7.485, 7.618, 7.772, 7.882])
mSiO2 = np.array([6.879e-6, 1.720e-5, 2.800e-5, 3.519e-5, 8.797e-5, 1.759e-4,
                  2.380e-4, 1.802e-4, 1.376e-4, 1.144e-4, 9.217e-5, 7.896e-5])
mCa   = np.array([2.173e-5, 2.437e-5, 2.876e-5, 3.753e-5, 6.382e-5, 1.075e-4,
                  1.866e-4, 3.310e-4, 5.480e-4, 7.630e-4, 1.115e-3, 1.459e-3])
gib   = np.array([3.357e-6, 8.397e-6, 1.040e-5, 0, 0, 0, 0, 0, 0, 0, 0, 0])
kao   = np.array([0, 0, 3.198e-6, 1.680e-5, 4.200e-5, 8.400e-5,
                  1.272e-4, 1.484e-4, 1.959e-4, 2.504e-4, 3.471e-4, 4.470e-4])
sme   = np.array([0, 0, 0, 0, 0, 0,
                  4.884e-5, 2.247e-4, 4.695e-4, 7.061e-4, 1.093e-3, 1.477e-3])

# =====================================================================
# 図2: 反応経路 = "熟成" (上段: 二次鉱物の三段リレー / 下段: DSi と pH)
# =====================================================================
fig, (axU, axL) = plt.subplots(2, 1, figsize=(9.0, 7.6), sharex=True,
                               gridspec_kw={"height_ratios": [1.25, 1.0]})

# --- 上段: 二次鉱物中の Al 分配率 (100%積み上げ) ―― 三段リレーを明示 ---
al_gib = gib * 1.0
al_kao = kao * 2.0
al_sme = sme * 1.67
al_tot = al_gib + al_kao + al_sme
f_gib = 100 * al_gib / al_tot
f_kao = 100 * al_kao / al_tot
f_sme = 100 * al_sme / al_tot
axU.stackplot(rxn, f_gib, f_kao, f_sme,
              colors=[C_GIB, C_KAO, C_SME], alpha=0.9,
              labels=["Gibbsite  Al(OH)$_3$", "Kaolinite", "Ca-smectite"])
axU.set_xscale("log")
axU.set_ylabel("Al partitioned into\nsecondary minerals  (%)", fontsize=12)
axU.set_ylim(0, 100)
axU.set_xlim(rxn.min(), rxn.max())
axU.text(4.0e-6, 22, "Gibbsite", color="#5a3600", ha="center", fontsize=11, fontweight="bold",
         rotation=90)
axU.text(6.0e-5, 60, "Kaolinite", color="#0f3d22", ha="center", fontsize=12, fontweight="bold")
axU.text(1.15e-3, 60, "Ca-smectite", color="#ffffff", ha="center", fontsize=12, fontweight="bold")
axU.set_title("Weathering 'maturation': secondary minerals hand the baton\n"
              "Gibbsite → Kaolinite → Ca-smectite as reaction proceeds", fontsize=13)

# --- 下段: DSi (mmol) と pH ---
axL.plot(rxn, mSiO2*1e3, "o-", color=C_DSI, lw=2.4, ms=6, label="dissolved silica (DSi)")
axL.set_xscale("log")
axL.set_xlabel("reaction progress  (mol of primary minerals dissolved)  →  longer contact time",
               fontsize=12)
axL.set_ylabel("DSi  (mmol L$^{-1}$)", color=C_DSI, fontsize=12)
axL.tick_params(axis="y", labelcolor=C_DSI)
axL.set_ylim(0, 0.28)
axL.grid(ls=":", lw=0.6, color="#cccccc"); axL.set_axisbelow(True)
# DSi 頭打ちの注記
imax = int(np.argmax(mSiO2))
axL.annotate("DSi peaks then is capped\n(near chalcedony saturation),\nthen taken up by smectite",
             xy=(rxn[imax], mSiO2[imax]*1e3), xytext=(6e-6, 0.205),
             fontsize=9.5, color="#31708f", ha="left", va="center",
             arrowprops=dict(arrowstyle="->", color="#31708f", lw=1.1))
axR = axL.twinx()
axR.plot(rxn, pH_b, "s--", color=C_PH, lw=2.0, ms=6, label="pH")
axR.set_ylabel("pH", color=C_PH, fontsize=12)
axR.tick_params(axis="y", labelcolor=C_PH)
axR.set_ylim(5.8, 8.4)
# 凡例（両軸まとめ）
lines = [Line2D([0],[0], color=C_DSI, marker="o", lw=2.4),
         Line2D([0],[0], color=C_PH, marker="s", ls="--", lw=2.0)]
axL.legend(lines, ["DSi", "pH"], loc="upper right", fontsize=11,
           frameon=True, framealpha=0.95, edgecolor="#ccc")
fig.tight_layout()
fig.savefig("fig2_reaction_path.png", bbox_inches="tight")
plt.close(fig)
print("saved fig2_reaction_path.png")

# =====================================================================
# 37湧水試料 (Ide et al. 2018, Table 1; May 2013)  pH, Ca, DSi(=Si)
#   活動度は希薄近似で濃度で代用（本文で明示）。
# =====================================================================
# (pH, Ca[mmol/L], Si[mmol/L])
samples = [
 (7.1,0.23,0.97),(7.1,0.23,0.95),(7.5,0.24,0.72),(6.6,0.26,0.52),(6.9,0.28,0.61),
 (6.7,0.43,1.34),(6.1,0.16,0.41),(6.7,0.21,1.45),(7.1,0.20,0.86),(7.4,0.45,1.08),
 (7.0,0.44,0.95),(6.8,0.44,1.02),(6.7,0.26,0.76),(7.1,0.44,0.80),(6.9,0.34,0.82),
 (6.9,0.22,0.76),(7.7,2.36,0.90),(6.2,1.84,1.00),(7.0,0.47,0.86),(6.9,0.58,0.86),
 (6.6,0.30,0.74),(7.3,0.16,0.64),(6.4,0.59,1.00),(7.0,0.14,0.59),(5.5,1.50,1.14),
 (6.9,0.56,0.90),(6.6,0.44,0.93),(6.6,0.57,1.01),(6.7,0.94,1.02),(6.8,0.31,0.87),
 (6.3,0.96,1.28),(6.9,0.17,0.96),(7.4,0.29,1.01),(6.1,1.49,1.18),(6.6,0.35,0.90),
 (6.6,0.50,0.99),(6.5,0.40,0.97),
]
s_pH  = np.array([s[0] for s in samples])
s_Ca  = np.array([s[1] for s in samples]) * 1e-3   # mol/L
s_Si  = np.array([s[2] for s in samples]) * 1e-3   # mol/L
s_x = np.log10(s_Si)                # log a(SiO2)  ≈ log[SiO2]
s_y = np.log10(s_Ca) + 2.0 * s_pH   # log(a Ca2+ / a H+^2)

# 反応経路の (x, y)
b_x = np.log10(mSiO2)
b_y = np.log10(mCa) + 2.0 * pH_b
# 各点で「主に析出している二次鉱物」で色分け
b_col = []
for g, k, m in zip(gib, kao, sme):
    if m > k and m > g:      b_col.append(C_SME)
    elif k >= g:             b_col.append(C_KAO)
    else:                    b_col.append(C_GIB)

# 厳密に引ける境界（llnl.dat の logK から導出）
S_GK = -4.35    # Gibbsite | Kaolinite : 垂直線  log aSiO2 = (logK_K - 2 logK_G)/2
C_KA = 19.77    # Kaolinite | Anorthite: 水平線  log(aCa/aH^2) = logK_A - logK_K
# シリカ相の飽和（垂直の参照線）: llnl logK
S_QZ, S_CH, S_AM = -4.00, -3.73, -2.71

# =====================================================================
# 図3: 活動度図 (log(aCa2+/aH+^2) vs log aSiO2)
# =====================================================================
fig, ax = plt.subplots(figsize=(8.8, 7.2))
Y0, Y1 = 6.5, 15.0

# 天然の DSi 窓（石英〜非晶質シリカの間＝準安定過飽和帯）を淡く塗る
ax.axvspan(S_QZ, S_AM, color="#fdf3e7", zorder=0)

# シリカ相の飽和（垂直の参照線）
for xs, lab, cc in [(S_QZ,"quartz","#888"), (S_CH,"chalcedony","#888"), (S_AM,"am-silica","#888")]:
    ax.axvline(xs, color=cc, ls=(0,(6,4)), lw=1.2, zorder=1)
    ax.text(xs, Y1-0.15, lab, rotation=90, va="top", ha="right", fontsize=9.5, color="#666")

# きれいに引ける鉱物境界（Gibbsite|Kaolinite は垂直・実線）
ax.axvline(S_GK, color="#b8860b", lw=1.8, zorder=2)
ax.text(S_GK-0.05, 9.2, "Gibbsite | Kaolinite", rotation=90, va="center", ha="right",
        fontsize=10, color="#b8860b")
# Kaolinite|Anorthite 境界は log(aCa/aH^2)=19.8 と本図の上方 → 矢印で示す
ax.annotate("↑ Anorthite field\n(log $a$Ca/$a$H$^2$ > 19.8)",
            xy=(-5.05, Y1-0.15), xytext=(-5.05, Y1-1.25),
            fontsize=9.3, color="#7a5230", ha="left", va="top",
            arrowprops=dict(arrowstyle="->", color="#7a5230", lw=1.2))

# 領域ラベル
ax.text(-4.62, 8.9, "Gibbsite\nfield", ha="center", fontsize=11, color=C_GIB, style="italic")
ax.text(-3.85, 7.1, "Kaolinite / Ca-smectite field", ha="center", fontsize=11,
        color=C_KAO, style="italic")

# 反応経路（軌跡）
ax.plot(b_x, b_y, "-", color="#555", lw=1.6, zorder=3, alpha=0.8)
ax.scatter(b_x, b_y, c=b_col, s=70, edgecolor="#222", linewidth=0.7, zorder=5)
ax.annotate("", xy=(b_x[7], b_y[7]), xytext=(b_x[3], b_y[3]),
            arrowprops=dict(arrowstyle="->", color="#555", lw=1.6))
ax.text(b_x[0]+0.03, b_y[0]-0.35, "equilibrium reaction\npath (deck B)", fontsize=9.5,
        color="#555", ha="left", va="top")

# 37湧水試料
ax.scatter(s_x, s_y, marker="*", s=150, c="#c0392b", edgecolor="#5a1414",
           linewidth=0.6, zorder=6)

# 速度論ギャップの注記（path と springs の横ずれ＝Si過飽和）
ax.annotate("natural springs stay silica-supersaturated\n"
            "(quartz & chalcedony oversaturated, am-silica under)\n"
            "→ higher DSi than the equilibrium path",
            xy=(-3.1, 12.75), xytext=(-3.75, 14.4),
            fontsize=9.3, color="#8a4b08", ha="center", va="center",
            arrowprops=dict(arrowstyle="->", color="#c07a2a", lw=1.4))

ax.set_xlabel("log $a$(SiO$_2$,aq)   (≈ log[DSi])", fontsize=13)
ax.set_ylabel("log ( $a$Ca$^{2+}$ / $a$H$^{+2}$ )", fontsize=13)
ax.set_xlim(-5.2, -2.5)
ax.set_ylim(Y0, Y1)
ax.grid(ls=":", lw=0.6, color="#dddddd"); ax.set_axisbelow(True)

leg_el = [
    Line2D([0],[0], marker="*", color="none", markerfacecolor="#c0392b",
           markeredgecolor="#5a1414", markersize=14, label="Kirishima springs (n=37)"),
    Line2D([0],[0], marker="o", color="none", markerfacecolor=C_GIB, markeredgecolor="#222",
           markersize=9, label="path: gibbsite ppt."),
    Line2D([0],[0], marker="o", color="none", markerfacecolor=C_KAO, markeredgecolor="#222",
           markersize=9, label="path: kaolinite ppt."),
    Line2D([0],[0], marker="o", color="none", markerfacecolor=C_SME, markeredgecolor="#222",
           markersize=9, label="path: Ca-smectite ppt."),
]
ax.legend(handles=leg_el, loc="lower right", fontsize=10.0, frameon=True,
          framealpha=0.95, edgecolor="#ccc")
ax.set_title("Where the springs sit on the weathering diagram\n"
             "Springs plot in the kaolinite / Ca-smectite region; "
             "the path evolves gibbsite→kaolinite→smectite", fontsize=12.5)
fig.tight_layout()
fig.savefig("fig3_activity_diagram.png", bbox_inches="tight")
plt.close(fig)
print("saved fig3_activity_diagram.png")

print("done (fig1, fig2, fig3).")
