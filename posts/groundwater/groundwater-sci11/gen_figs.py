# -*- coding: utf-8 -*-
"""
地下水科学入門 #11（地下水質）の図生成スクリプト。
- 独立スクリプトでPNGを事前生成し、index.qmd からは静的参照する（CLAUDE.mdルール）。
- 図中フォントは Times New Roman（serif）・大きめ。ラベルは英語。

出力:
  calcite_evolution.png : 雨水＋土壌CO2が方解石を溶かしてCa-HCO3型へ進化する過程
  piper.png             : Piper（トリリニア）ダイアグラム。Yang et al.(2020) Fig.2 準拠。
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 15, "axes.titlesize": 18, "axes.labelsize": 16,
    "xtick.labelsize": 13, "ytick.labelsize": 13,
    "axes.unicode_minus": False, "figure.dpi": 150, "savefig.bbox": "tight",
})

NAVY, BLUE, CYAN = "#1A365D", "#2563EB", "#00B4D8"
RED, ORANGE, PURPLE, GREEN = "#DC2626", "#EA580C", "#7C3AED", "#059669"
INK, GRID, PANEL = "#374151", "#CBD5E1", "#F8F9FA"
HERE = os.path.dirname(os.path.abspath(__file__))

# ===========================================================================
# 図1: 方解石溶解による水質進化（開放系・pCO2固定・25℃, Appelo & Postma 2005）
# ===========================================================================
KH, K1, K2 = 10**-1.47, 10**-6.35, 10**-10.33
KCAL, KW = 10**-8.48, 10**-14.0
PCO2 = 10**-2.0

def carbonate_species(H):
    hco3 = K1 * (KH * PCO2) / H
    return hco3, K2 * hco3 / H, KW / H

def solve_H(Ca):
    def charge(pH):
        H = 10**(-pH); hco3, co3, oh = carbonate_species(H)
        return 2*Ca + H - (hco3 + 2*co3 + oh)
    return 10**(-brentq(charge, 3.0, 12.0))

def SI_calcite(Ca, H):
    _, co3, _ = carbonate_species(H)
    return np.log10((Ca * co3) / KCAL)

Ca_eq = brentq(lambda Ca: SI_calcite(Ca, solve_H(Ca)), 1e-5, 1e-1)
Ca_arr = np.linspace(1e-4, Ca_eq, 200)
pH_arr, hco3_arr, si_arr = [], [], []
for Ca in Ca_arr:
    H = solve_H(Ca); hco3, co3, oh = carbonate_species(H)
    pH_arr.append(-np.log10(H)); hco3_arr.append(hco3*1000); si_arr.append(SI_calcite(Ca, H))
pH_arr, hco3_arr, si_arr = map(np.array, (pH_arr, hco3_arr, si_arr))
Ca_mmol = Ca_arr * 1000
print(f"[calcite] eq: Ca={Ca_eq*1000:.2f} mmol/L ({Ca_eq*1000*40.08:.0f} mg/L), "
      f"pH={pH_arr[-1]:.2f}, HCO3={hco3_arr[-1]:.2f} mmol/L")

fig, (axA, axB) = plt.subplots(1, 2, figsize=(14, 5.6))
axA.set_facecolor(PANEL)
axA.plot(Ca_mmol, Ca_mmol, color=BLUE, lw=3, label="Ca$^{2+}$")
axA.plot(Ca_mmol, hco3_arr, color=GREEN, lw=3, label="HCO$_3^-$")
axA.set_xlabel("Calcite dissolved  (mmol/L)", color=INK)
axA.set_ylabel("Concentration  (mmol/L)", color=INK)
axA.grid(True, color=GRID, lw=0.6, alpha=0.7)
axA.set_xlim(0, Ca_mmol[-1]*1.02); axA.set_ylim(0, hco3_arr[-1]*1.15)
axpH = axA.twinx()
axpH.plot(Ca_mmol, pH_arr, color=ORANGE, lw=3, ls="--", label="pH")
axpH.set_ylabel("pH", color=ORANGE); axpH.tick_params(axis="y", labelcolor=ORANGE)
axpH.set_ylim(4.5, 8.5)
l1, la1 = axA.get_legend_handles_labels(); l2, la2 = axpH.get_legend_handles_labels()
axA.legend(l1+l2, la1+la2, loc="center right", fontsize=14, framealpha=0.95)
axA.set_title("Rainwater + soil CO$_2$  $\\rightarrow$  dissolving calcite",
              fontweight="bold", color=NAVY, pad=8)
axB.set_facecolor(PANEL)
axB.plot(Ca_mmol, si_arr, color=PURPLE, lw=3.2)
axB.axhline(0, color=RED, lw=1.8, ls=":")
axB.text(Ca_mmol[-1]*0.98, 0.15, "saturation (SI = 0)", ha="right", color=RED,
         fontsize=14, fontweight="bold")
axB.fill_between(Ca_mmol, si_arr, 0, where=(si_arr < 0), color=PURPLE, alpha=0.08)
axB.set_xlabel("Calcite dissolved  (mmol/L)", color=INK)
axB.set_ylabel("Saturation Index (calcite)", color=INK)
axB.grid(True, color=GRID, lw=0.6, alpha=0.7); axB.set_xlim(0, Ca_mmol[-1]*1.02)
axB.set_title("The water evolves toward calcite saturation",
              fontweight="bold", color=NAVY, pad=8)
axB.annotate(f"Ca-HCO$_3$ groundwater\npH {pH_arr[-1]:.1f}, Ca {Ca_mmol[-1]:.1f} mmol/L",
             xy=(Ca_mmol[-1], 0), xytext=(Ca_mmol[-1]*0.5, -1.7), fontsize=13, color=NAVY,
             arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.5))
fig.suptitle("Open system, pCO$_2$ = 10$^{-2}$ atm, 25 $\\degree$C  "
             "(dilute, activities $\\approx$ concentrations)", fontsize=13, color=INK, y=1.02)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "calcite_evolution.png"), facecolor="white")
plt.close(fig)

# ===========================================================================
# 図2: Piper（トリリニア）ダイアグラム  ── Yang et al. (2020) Fig.2 準拠
# ===========================================================================
WATERS = {
    "River":        (7,     1.3, 12,  3,    8,     9,    28,  CYAN,   "o"),
    "Groundwater":  (12,    1.2, 45,  9,    14,    12,   110, GREEN,  "s"),
    "Onsen (Na-Cl)":(545,   35,  44,  8,    848,   160,  90,  RED,    "^"),
    "Seawater":     (10556, 380, 400, 1272, 18980, 2649, 140, PURPLE, "D"),
}
EW = dict(Na=23.0, K=39.1, Ca=20.04, Mg=12.15, Cl=35.45, SO4=48.03, HCO3=61.02)

def meq_pct(na, k, ca, mg, cl, so4, hco3):
    c_na = na/EW["Na"] + k/EW["K"]; c_ca = ca/EW["Ca"]; c_mg = mg/EW["Mg"]
    cs = c_na + c_ca + c_mg
    a_cl = cl/EW["Cl"]; a_so4 = so4/EW["SO4"]; a_hco3 = hco3/EW["HCO3"]; a_s = a_cl + a_so4 + a_hco3
    return (100*c_ca/cs, 100*c_mg/cs, 100*c_na/cs, 100*a_hco3/a_s, 100*a_so4/a_s, 100*a_cl/a_s)

L, G = 100.0, 70.0
H = L*np.sqrt(3)/2
X0 = L + G
M = np.sqrt(3)

def cat_pt(ca, mg, nak):  return (nak/100*L + mg/100*(L/2), mg/100*H)      # Ca(0,0) NaK(L,0) Mg(top)
def an_pt(hco3, so4, cl): return (X0 + cl/100*L + so4/100*(L/2), so4/100*H)  # HCO3(X0,0) Cl Mg->SO4 top

def dia_pt(pc, pa):                 # 陽イオン点から+60°、陰イオン点から-60°の交点（回転なし＝標準）
    xc, yc = pc; xa, ya = pa
    x = (M*xc + M*xa + ya - yc) / (2*M)
    return (x, yc + M*(x - xc))

fig, ax = plt.subplots(figsize=(12.5, 12))
ax.set_aspect("equal"); ax.axis("off")

def _u(v):
    n = np.hypot(v[0], v[1]); return (v[0]/n, v[1]/n)
def _out(P, Q, cen):                # 辺PQの外向き法線（単位）
    d = _u((Q[0]-P[0], Q[1]-P[1])); n = (-d[1], d[0])
    mid = ((P[0]+Q[0])/2, (P[1]+Q[1])/2); c2m = (mid[0]-cen[0], mid[1]-cen[1])
    return n if (n[0]*c2m[0]+n[1]*c2m[1]) > 0 else (-n[0], -n[1])

def edge_axis(P, Q, cen, title, tick0_at_P=True, tdist=13, ldist=34, fs_t=11, fs_l=15):
    """辺PQに沿って0–100目盛＋軸名（外向き）。tick0_at_P: 0%がPか。"""
    n = _out(P, Q, cen)
    for v in (0, 20, 40, 60, 80, 100):
        t = v/100 if tick0_at_P else 1 - v/100
        p = (P[0]+t*(Q[0]-P[0]), P[1]+t*(Q[1]-P[1]))
        ax.plot([p[0], p[0]+n[0]*4], [p[1], p[1]+n[1]*4], color=INK, lw=0.8, zorder=3)
        ax.text(p[0]+n[0]*tdist, p[1]+n[1]*tdist, str(v), ha="center", va="center",
                fontsize=fs_t, color=INK, zorder=3)
    if title:
        mid = ((P[0]+Q[0])/2, (P[1]+Q[1])/2)
        ang = np.degrees(np.arctan2(Q[1]-P[1], Q[0]-P[0]))
        if ang > 90: ang -= 180
        if ang < -90: ang += 180
        ax.text(mid[0]+n[0]*ldist, mid[1]+n[1]*ldist, title, ha="center", va="center",
                fontsize=fs_l, fontweight="bold", color=INK, rotation=ang, rotation_mode="anchor")

def grid_tri(A, B, C):
    for f in (0.2, 0.4, 0.6, 0.8):
        for (P, Q, R, S) in [(A, C, B, C), (A, B, C, B), (B, A, C, A)]:
            p1 = (P[0]+f*(Q[0]-P[0]), P[1]+f*(Q[1]-P[1]))
            p2 = (R[0]+f*(S[0]-R[0]), R[1]+f*(S[1]-R[1]))
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=GRID, lw=0.5, zorder=1)
    ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], color=INK, lw=1.7, zorder=2)

# --- 陽イオン三角 ---  Ca(左下) Mg(頂) NaK(右下)
Aca, Bnk, Cmg = (0, 0), (L, 0), (L/2, H)
cen_cat = ((Aca[0]+Bnk[0]+Cmg[0])/3, (Aca[1]+Bnk[1]+Cmg[1])/3)
grid_tri(Aca, Bnk, Cmg)
edge_axis(Bnk, Aca, cen_cat, "Ca$^{2+}$", tick0_at_P=True)     # 底辺: 右NaK(Ca0)→左Ca(Ca100)? tick0 at Bnk
edge_axis(Aca, Cmg, cen_cat, "Mg$^{2+}$", tick0_at_P=True)     # 左辺: Ca(Mg0)→Mg(100)
edge_axis(Cmg, Bnk, cen_cat, "", tick0_at_P=True)  # 右辺: 目盛のみ（軸名はダイヤ側と共有）

# --- 陰イオン三角 --- HCO3(左下) SO4(頂) Cl(右下)
Ahc, Bcl, Cso = (X0, 0), (X0+L, 0), (X0+L/2, H)
cen_an = ((Ahc[0]+Bcl[0]+Cso[0])/3, (Ahc[1]+Bcl[1]+Cso[1])/3)
grid_tri(Ahc, Bcl, Cso)
edge_axis(Ahc, Bcl, cen_an, "Cl$^-$", tick0_at_P=True)             # 底辺: HCO3(Cl0)→Cl(100)
edge_axis(Cso, Ahc, cen_an, "", tick0_at_P=True)  # 左辺: 目盛のみ（軸名はダイヤ側と共有）
edge_axis(Bcl, Cso, cen_an, "SO$_4^{2-}$", tick0_at_P=True)        # 右辺: Cl(SO4 0)→SO4(100)

# --- ダイヤ（回転なし：左=Ca-HCO3, 右=NaK-Cl, 上=Ca-Cl, 下=NaK-HCO3）---
Dl = dia_pt(cat_pt(100,0,0), an_pt(100,0,0))   # 左  Ca-HCO3
Dr = dia_pt(cat_pt(0,0,100), an_pt(0,0,100))   # 右  NaK-Cl
Dt = dia_pt(cat_pt(100,0,0), an_pt(0,0,100))   # 上  Ca-Cl
Db = dia_pt(cat_pt(0,0,100), an_pt(100,0,0))   # 下  NaK-HCO3
cen_d = ((Dl[0]+Dr[0]+Dt[0]+Db[0])/4, (Dl[1]+Dr[1]+Dt[1]+Db[1])/4)
for f in (0.2, 0.4, 0.6, 0.8):
    ax.plot([Dl[0]+f*(Dt[0]-Dl[0]), Db[0]+f*(Dr[0]-Db[0])],
            [Dl[1]+f*(Dt[1]-Dl[1]), Db[1]+f*(Dr[1]-Db[1])], color=GRID, lw=0.5, zorder=1)
    ax.plot([Dl[0]+f*(Db[0]-Dl[0]), Dt[0]+f*(Dr[0]-Dt[0])],
            [Dl[1]+f*(Db[1]-Dl[1]), Dt[1]+f*(Dr[1]-Dt[1])], color=GRID, lw=0.5, zorder=1)
ax.plot([Dl[0],Dt[0],Dr[0],Db[0],Dl[0]], [Dl[1],Dt[1],Dr[1],Db[1],Dl[1]], color=INK, lw=1.7, zorder=2)
edge_axis(Dl, Dt, cen_d, "SO$_4^{2-}$+Cl$^-$", tick0_at_P=True)
edge_axis(Dt, Dr, cen_d, "Ca$^{2+}$+Mg$^{2+}$", tick0_at_P=True)
edge_axis(Db, Dl, cen_d, "Na$^{+}$+K$^{+}$", tick0_at_P=True)
edge_axis(Dr, Db, cen_d, "HCO$_3^-$+CO$_3^{2-}$", tick0_at_P=True)

# 水質タイプ区分（梁 2021 Fig.2b 準拠）：対辺中点を結ぶ2本でダイヤを4分割
def _mid(P, Q): return ((P[0]+Q[0])/2, (P[1]+Q[1])/2)
M_ul, M_ur = _mid(Dl, Dt), _mid(Dt, Dr)
M_ll, M_lr = _mid(Db, Dl), _mid(Dr, Db)
ax.plot([M_ul[0], M_lr[0]], [M_ul[1], M_lr[1]], color="#9CA3AF", lw=1.1, zorder=2)
ax.plot([M_ur[0], M_ll[0]], [M_ur[1], M_ll[1]], color="#9CA3AF", lw=1.1, zorder=2)
def _toward(V, f): return (V[0]+(cen_d[0]-V[0])*f, V[1]+(cen_d[1]-V[1])*f)
for V, num, f in [(Dr, "I", 0.34), (Dt, "II", 0.34), (Dl, "III", 0.34), (Db, "IV", 0.34)]:
    x, y = _toward(V, f)
    ax.text(x, y, num, ha="center", va="center", fontsize=18, style="italic",
            color=NAVY, zorder=6)
# タイプ凡例
ax.text(0.70, 0.99,
        "I     Na-Cl type\nII    Ca-Mg-SO$_4$ type\nIII   Ca-HCO$_3$ type\nIV    Na-HCO$_3$ type",
        transform=ax.transAxes, ha="left", va="top", fontsize=13, color=INK,
        linespacing=1.5,
        bbox=dict(boxstyle="round,pad=0.5", fc="white", ec=GRID, lw=1.0))

# --- データ点 ＋ 投影ガイド線（ダイヤ＝2三角の交点、を可視化）---
for name, (na, k, ca, mg, cl, so4, hco3, col, mk) in WATERS.items():
    pca, pmg, pnak, phco3, pso4, pcl = meq_pct(na, k, ca, mg, cl, so4, hco3)
    pc = cat_pt(pca, pmg, pnak); pa = an_pt(phco3, pso4, pcl); pd = dia_pt(pc, pa)
    ax.plot([pc[0], pd[0]], [pc[1], pd[1]], color=col, lw=0.9, ls=(0,(4,3)), alpha=0.45, zorder=4)
    ax.plot([pa[0], pd[0]], [pa[1], pd[1]], color=col, lw=0.9, ls=(0,(4,3)), alpha=0.45, zorder=4)
    for (x, y) in (pc, pa, pd):
        ax.scatter([x], [y], s=135, color=col, marker=mk, edgecolor="white",
                   linewidth=1.3, zorder=6, label=name if (x, y) == pd else None)

ax.legend(loc="upper left", fontsize=15, framealpha=0.96, title="Water type", title_fontsize=15)
ax.set_title("Piper (trilinear) diagram — river, groundwater, onsen, seawater",
             fontsize=19, fontweight="bold", color=NAVY, y=1.0, pad=12)
ax.set_ylim(-48, Dt[1]+34)
fig.savefig(os.path.join(HERE, "piper.png"), facecolor="white")
plt.close(fig)
print("saved calcite_evolution.png, piper.png")
