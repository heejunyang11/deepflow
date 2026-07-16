# -*- coding: utf-8 -*-
"""
DeepFlows PHREEQC #20 — figure generation.
All numbers are derived from the public Thermoddem database and the already-published
#18 (Satake et al. 2025) reproduction. Figure labels are in English by design.
Run:  python gen_figs.py
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ---- DeepFlows palette ----
AMBER   = "#C8472A"
ORANGE  = "#E07B39"
GOLD     = "#D9A521"
INK     = "#1A1A1A"
GREY    = "#6B6B6B"
TEAL    = "#2C8F7A"
BLUE    = "#034F84"
PAPER   = "#FDFAF6"
CARD    = "#F4F0E7"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 12,
    "axes.edgecolor": "#B9B0A2",
    "axes.linewidth": 1.0,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "savefig.dpi": 150,
})


def _box(ax, x, y, w, h, text, fc, ec, tc=INK, fs=12, weight="bold"):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0.02,rounding_size=0.06",
                 fc=fc, ec=ec, lw=1.6))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=tc, weight=weight, wrap=True)


def _arrow(ax, x0, y0, x1, y1, label=None, color=INK):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1),
                 arrowstyle="-|>", mutation_scale=18, lw=2.0, color=color))
    if label:
        ax.text((x0 + x1) / 2, (y0 + y1) / 2 + 0.06, label, ha="center",
                va="bottom", fontsize=10.5, color=color, style="italic")


# =====================================================================
# 1) thumb.png  — the master map: log K -> dG / SI -> precipitation
# =====================================================================
def fig_thumb():
    fig, ax = plt.subplots(figsize=(9.2, 4.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")
    ax.text(5, 4.6, "One number decides it all:  log K",
            ha="center", fontsize=17, weight="bold", color=INK)

    _box(ax, 0.4, 2.05, 2.1, 1.15, "log K\n(equilibrium\nconstant)", CARD, ORANGE, fs=12.5)
    _box(ax, 3.9, 3.05, 2.5, 1.05, r"$\Delta G^\circ = -2.303RT\,\log K$", "#FFF6EE", AMBER, tc=AMBER, fs=12)
    _box(ax, 3.9, 1.0,  2.5, 1.05, r"$SI = \log(IAP/K)$", "#EEF5F2", TEAL, tc=BLUE, fs=12.5)
    _box(ax, 7.7, 2.05, 2.0, 1.15, "Which mineral\nprecipitates?", CARD, INK, fs=12)

    _arrow(ax, 2.5, 2.9, 3.9, 3.5, "energy (kJ)", AMBER)
    _arrow(ax, 2.5, 2.35, 3.9, 1.5, "saturation", TEAL)
    _arrow(ax, 6.4, 3.5, 7.7, 2.85, color=GREY)
    _arrow(ax, 6.4, 1.5, 7.7, 2.4, color=GREY)

    ax.text(5, 0.25, "PHREEQC does this comparison internally — this article opens the box by hand.",
            ha="center", fontsize=10.5, color=GREY, style="italic")
    fig.tight_layout()
    fig.savefig("thumb.png", bbox_inches="tight")
    plt.close(fig)


# =====================================================================
# 2) fig-si-map.png — how to read an SI value (sign -> 10^SI -> kJ)
# =====================================================================
def fig_si_map():
    fig, ax = plt.subplots(figsize=(9.2, 3.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 4); ax.axis("off")
    ax.text(5, 3.65, "Reading a saturation index (SI)", ha="center",
            fontsize=16, weight="bold", color=INK)

    _box(ax, 0.3, 1.5, 2.4, 1.3,
         "1. SIGN\nSI > 0  precipitate\nSI < 0  dissolve", "#FFF6EE", AMBER, tc=INK, fs=11)
    _box(ax, 3.55, 1.5, 2.6, 1.3,
         r"2. $10^{\,SI}$" + "\nhow many times\naway from equilibrium", "#EEF5F2", TEAL, tc=INK, fs=11)
    _box(ax, 7.0, 1.5, 2.7, 1.3,
         r"3. $2.303RT\cdot SI$" + "\nhow many kJ\n(driving force)", CARD, INK, tc=INK, fs=11)

    _arrow(ax, 2.7, 2.15, 3.55, 2.15, color=GREY)
    _arrow(ax, 6.15, 2.15, 7.0, 2.15, color=GREY)
    ax.text(5, 0.55, "First the sign (out or not) — then the magnitude (how far) — then the energy.",
            ha="center", fontsize=10.5, color=GREY, style="italic")
    fig.tight_layout()
    fig.savefig("fig-si-map.png", bbox_inches="tight")
    plt.close(fig)


# =====================================================================
# 3) fig-satake-si.png — SI time series (public #18 reproduction, 250 C)
# =====================================================================
# (day, si_Saponite(FeMg), si_Montmorillonite(HcMg), si_Saponite(Mg), si_Calcite)
SI = [
(0.100,-1.366,-1.304,-2.813,-1.273),(0.400,-0.019,-0.377,-1.210,-1.046),
(0.700,-0.000,-0.364,-1.187,-0.837),(1.000,0.000,-0.365,-1.187,-0.666),
(1.300,0.000,-0.365,-1.187,-0.525),(1.600,0.000,-0.365,-1.187,-0.407),
(1.900,0.000,-0.365,-1.187,-0.306),(2.200,0.000,-0.365,-1.186,-0.219),
(2.500,0.000,-0.365,-1.186,-0.142),(2.800,0.000,-0.365,-1.186,-0.074),
(3.100,0.000,-0.365,-1.186,-0.012),(3.400,0.000,-0.365,-1.186,0.000),
(4.000,0.000,-0.365,-1.186,0.000),(4.600,0.000,-0.365,-1.186,0.000),
(5.200,0.000,-0.365,-1.186,0.000),(5.800,0.000,-0.365,-1.187,0.000),
(6.400,0.000,-0.365,-1.187,0.000),(6.700,0.000,-0.306,-1.237,0.000),
(7.000,0.000,-0.238,-1.297,0.000),(7.300,0.000,-0.180,-1.347,0.000),
(7.600,0.000,-0.131,-1.390,0.000),(7.900,0.000,-0.088,-1.428,0.000),
(8.200,0.000,-0.049,-1.462,0.000),(8.500,0.000,-0.015,-1.491,0.000),
(8.800,0.000,-0.000,-1.504,0.000),(9.100,0.000,0.000,-1.504,0.000),
(10.0,0.000,0.000,-1.504,0.000),(11.0,0.000,0.000,-1.504,0.000),
(12.0,0.000,0.000,-1.504,0.000),(13.0,0.000,0.000,-1.504,0.000),
(14.0,0.000,0.000,-1.504,0.000),(15.0,0.000,0.000,-1.520,0.000),
]

def fig_satake_si():
    a = np.array(SI)
    day = a[:, 0]
    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    ax.axhline(0, color=INK, lw=1.2, ls="--", alpha=0.7)
    ax.plot(day, a[:, 1], "-", color=TEAL,  lw=2.6, label="Saponite(FeMg)  — wins (has Fe)")
    ax.plot(day, a[:, 2], "-", color=BLUE,  lw=2.6, label="Montmorillonite(HcMg)  — wins (Al available)")
    ax.plot(day, a[:, 4], "-", color=GOLD,  lw=2.2, label="Calcite  — CO$_2$ fixed")
    ax.plot(day, a[:, 3], "-", color=AMBER, lw=2.6, label="Saponite(Mg)  — loses (no Fe)")

    ax.annotate("SI = 0  (saturation line)", xy=(11.5, 0), xytext=(9.0, 0.28),
                fontsize=10.5, color=INK)
    ax.annotate("Saponite(FeMg)\nreaches saturation\n~1.6 d", xy=(1.6, 0), xytext=(2.2, -0.75),
                fontsize=9.5, color=TEAL,
                arrowprops=dict(arrowstyle="->", color=TEAL))
    ax.annotate("Montmorillonite\ntakes over ~9 d", xy=(9.0, 0), xytext=(10.0, -0.55),
                fontsize=9.5, color=BLUE,
                arrowprops=dict(arrowstyle="->", color=BLUE))
    ax.annotate("stays undersaturated  (SI ~ -1.5)\nnever precipitates", xy=(4.5, -1.187),
                xytext=(0.9, -2.7), ha="left", fontsize=9.5, color=AMBER,
                arrowprops=dict(arrowstyle="->", color=AMBER))

    ax.set_xlabel("Reaction time (days)")
    ax.set_ylabel("Saturation index  SI = log(IAP/K)")
    ax.set_title("Basalt–CO$_2$ secondary minerals at 250 °C  (public reproduction of Satake et al., 2025)",
                 fontsize=12.5, weight="bold")
    ax.set_xlim(0, 15.3); ax.set_ylim(-3.0, 0.6)
    ax.legend(loc="lower right", fontsize=10, framealpha=0.95)
    ax.grid(alpha=0.18)
    fig.tight_layout()
    fig.savefig("fig-satake-si.png", bbox_inches="tight")
    plt.close(fig)


# =====================================================================
# 4) fig-zeolite-temp.png — Laumontite<->Wairakite dehydration logK & a(H2O)
# =====================================================================
# (T_C, dehydration logK = si_Wairakite - si_Laumontite at a(H2O)~1)
ZEO = [(25, -2.749), (100, -1.540), (200, -0.387), (250, 0.168)]

def fig_zeolite_temp():
    # Phase diagram: temperature x water activity, with stability fields shaded.
    # The boundary a(H2O) = 10^(logK/2) comes from the dehydration log K, but the
    # reader only needs to locate "the present water" on this map.
    z = np.array(ZEO, dtype=float)
    Tp, Kp = z[:, 0], z[:, 1]                 # computed points (25,100,200,250)
    T = np.linspace(25, 260, 400)
    logK = np.interp(T, Tp, Kp)               # piecewise-linear dehydration logK
    thr = 10 ** (logK / 2.0)                  # boundary: threshold a(H2O)
    Tx = 200 + 50 * (0.387 / (0.387 + 0.168)) # crossover where threshold = 1  (~235 C)
    ymax = 1.08
    thr_c = np.clip(thr, 0, ymax)

    fig, ax = plt.subplots(figsize=(9.2, 5.4))
    # stability fields
    ax.fill_between(T, thr_c, ymax, color=BLUE,   alpha=0.13)   # above boundary: hydrous
    ax.fill_between(T, 0,     thr_c, color=ORANGE, alpha=0.20)  # below boundary: dehydrated
    ax.plot(T, thr_c, color=INK, lw=2.4, zorder=4)             # phase boundary

    # the "present water": dilute groundwater at a(H2O) ~ 1
    ax.axhline(1.0, color=TEAL, lw=2.8, zorder=5)
    ax.text(31, 0.965, "the water in these models:  dilute,  a(H$_2$O) ≈ 1",
            color=TEAL, fontsize=10.5, va="top", weight="bold")

    # computed boundary points (25,100,200 C are <=1)
    for t, k in zip(Tp, Kp):
        a = 10 ** (k / 2)
        if a <= ymax:
            ax.plot(t, a, "o", color=INK, ms=7, zorder=6)
            ax.annotate(f"{a:.2f}", (t, a), textcoords="offset points",
                        xytext=(6, -12), fontsize=9, color=INK)

    # region labels
    ax.text(140, 0.55, "LAUMONTITE  stable\n(more hydrous, ·4H$_2$O)",
            color=BLUE, fontsize=12.5, weight="bold", ha="center")
    ax.text(120, 0.10, "WAIRAKITE  stable  (dehydrated, ·2H$_2$O)",
            color="#A24A1C", fontsize=11.5, weight="bold", ha="center")

    # crossover marker
    ax.axvline(Tx, color=INK, lw=1.3, ls="--", alpha=0.6)
    ax.plot([Tx], [1.0], "o", color="#A24A1C", ms=10, zorder=7)
    ax.annotate(f"~{Tx:.0f} °C : the a≈1 water crosses the line\n"
                f"→ pure water flips to Wairakite\n(matches Liou 1971: ~230 °C)",
                xy=(Tx, 1.0), xytext=(Tx - 6, 0.62), ha="right", fontsize=9.5,
                arrowprops=dict(arrowstyle="->", color=INK))

    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Activity of water   a(H$_2$O)")
    ax.set_title("Which zeolite forms? Find where the water sits on this map",
                 fontsize=13, weight="bold")
    ax.set_xlim(25, 260); ax.set_ylim(0, ymax)
    ax.grid(alpha=0.15)
    fig.tight_layout()
    fig.savefig("fig-zeolite-temp.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig_thumb()
    fig_si_map()
    fig_satake_si()
    fig_zeolite_temp()
    print("saved: thumb.png, fig-si-map.png, fig-satake-si.png, fig-zeolite-temp.png")
