# -*- coding: utf-8 -*-
"""
#15 fig4 生成: 速度論による"消費ギャップ"の検証（deck K-sweep）
二次粘土(Kaolinite+Montmor-Ca)の析出速度 f_fit を 0.001/0.01/0.1/1.0 で振り、Si(t) と si_Quartz(t) を比較。
上段: DSi(t) と実測帯（Ide 2018: 0.41-1.45, median 0.93）／下段: si_Quartz(t) と石英飽和線。
結論: 実測(高Si・石英過飽和)を再現するには粘土析出が実験室速度より~1000倍遅い必要。データは deck K-sweep 実行値を埋め込み。
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 12, "axes.linewidth": 0.9, "axes.edgecolor": "#333333",
    "savefig.dpi": 150, "figure.dpi": 150,
})

yr = np.array([0.5,1,2,3,5,7,10,15,20,30,40,50,60])
DSi = {
 0.001: np.array([0.155,0.310,0.618,0.891,1.037,0.720,0.467,0.320,0.248,0.179,0.145,0.124,0.110]),
 0.01 : np.array([0.155,0.310,0.594,0.463,0.234,0.176,0.133,0.098,0.080,0.060,0.049,0.043,0.038]),
 0.1  : np.array([0.155,0.310,0.468,0.112,0.075,0.059,0.046,0.035,0.030,0.025,0.025,0.026,0.027]),
 1.0  : np.array([0.155,0.307,0.050,0.035,0.024,0.018,0.014,0.011,0.009,0.007,0.006,0.006,0.006]),
}
siQz = {
 0.001: np.array([0.43,0.73,1.03,1.19,1.25,1.10,0.91,0.74,0.63,0.49,0.40,0.33,0.28]),
 0.01 : np.array([0.43,0.73,1.01,0.90,0.61,0.48,0.36,0.23,0.14,0.01,-0.07,-0.14,-0.19]),
 0.1  : np.array([0.43,0.73,0.91,0.29,0.11,0.01,-0.10,-0.22,-0.29,-0.37,-0.38,-0.36,-0.34]),
 1.0  : np.array([0.43,0.73,-0.07,-0.22,-0.39,-0.50,-0.61,-0.73,-0.81,-0.92,-0.98,-1.01,-1.02]),
}
# 遅い→速い: 青→赤
col = {0.001:"#1f6fb2", 0.01:"#2e8b57", 0.1:"#e08a1e", 1.0:"#c0392b"}
lab = {0.001:"clay rate ×0.001 (slowest)", 0.01:"×0.01", 0.1:"×0.1", 1.0:"×1.0 (fastest)"}
mk  = {0.001:"o", 0.01:"s", 0.1:"^", 1.0:"D"}

# 実測（Ide et al. 2018, Table 1）
OBS_LO, OBS_HI, OBS_MED = 0.41, 1.45, 0.93

fig, (axU, axL) = plt.subplots(2, 1, figsize=(9.2, 8.4), sharex=True,
                               gridspec_kw={"height_ratios":[1.15,1.0]})

# ---------- 上段: DSi(t) ----------
axU.axhspan(OBS_LO, OBS_HI, color="#eaf4ea", zorder=0)
axU.axhline(OBS_MED, color="#4a8a4a", lw=1.3, ls=(0,(6,4)), zorder=1)
axU.text(0.55, OBS_MED+0.03, "observed springs (Ide 2018): median 0.93, range 0.41–1.45",
         fontsize=9.8, color="#3c763d", va="bottom")
for f in [0.001,0.01,0.1,1.0]:
    axU.plot(yr, DSi[f], mk[f]+"-", color=col[f], lw=2.2, ms=6, label=lab[f], zorder=4)
axU.set_xscale("log")
axU.set_ylabel("dissolved silica  DSi  (mmol L$^{-1}$)", fontsize=12.5)
axU.set_ylim(0, 1.55)
axU.grid(ls=":", lw=0.6, color="#cccccc"); axU.set_axisbelow(True)
axU.legend(loc="upper right", fontsize=10.5, frameon=True, framealpha=0.95, edgecolor="#ccc")
# "消費ギャップ" 注記（速い粘土＝Si喪失）
axU.annotate("faster clay → Si is drained\n('consumption gap' opens early)",
             xy=(3, 0.11), xytext=(6, 0.42), fontsize=9.6, color="#a5341f", ha="left",
             arrowprops=dict(arrowstyle="->", color="#c0392b", lw=1.3))
axU.annotate("only the slowest clay reaches\nthe observed DSi band",
             xy=(5, 1.037), xytext=(1.05, 1.30), fontsize=9.6, color="#1f6fb2", ha="left",
             arrowprops=dict(arrowstyle="->", color="#1f6fb2", lw=1.3))
axU.set_title("Kinetic test of the silica 'consumption gap'\n"
              "How fast must clays precipitate to draw silica down?", fontsize=13)

# ---------- 下段: si_Quartz(t) ----------
axL.axhspan(-1.15, 0, color="#fbecea", zorder=0)   # 石英未飽和帯
axL.axhline(0, color="#555", lw=1.4, zorder=2)
axL.text(0.55, 0.04, "quartz saturation (SI = 0)", fontsize=9.8, color="#444", va="bottom")
axL.text(40, -0.9, "quartz UNDERsaturated\n(inconsistent with real springs)",
         fontsize=9.6, color="#a5341f", ha="center", va="center")
for f in [0.001,0.01,0.1,1.0]:
    axL.plot(yr, siQz[f], mk[f]+"-", color=col[f], lw=2.2, ms=6, zorder=4)
axL.set_xscale("log")
axL.set_xlabel("residence time  (years)   —  batch reaction time as a proxy", fontsize=12.5)
axL.set_ylabel("SI(Quartz)", fontsize=12.5)
axL.set_ylim(-1.15, 1.4)
axL.set_xlim(0.5, 60)
axL.grid(ls=":", lw=0.6, color="#cccccc"); axL.set_axisbelow(True)
# 実測は過飽和側にとどまる
axL.annotate("real springs stay quartz-supersaturated\n→ clay precipitation must be strongly inhibited\n(>1000x slower than the lab proxy rate)",
             xy=(20, 0.63), xytext=(1.1, 0.98), fontsize=9.6, color="#1f6fb2", ha="left", va="center",
             arrowprops=dict(arrowstyle="->", color="#1f6fb2", lw=1.3))

fig.tight_layout()
fig.savefig("fig4_kinetic_gap.png", bbox_inches="tight")
plt.close(fig)
print("saved fig4_kinetic_gap.png")
