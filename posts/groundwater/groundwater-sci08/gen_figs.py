# -*- coding: utf-8 -*-
"""
地下水科学入門 #8（トンレサップ湖・相互相関／クロスウェーブレット）の図生成スクリプト
- 独立スクリプトでPNGを事前生成し、index.qmd からは静的参照する（CLAUDE.mdルール）
- 学習用の合成（ダミー）データを使用。図中ラベルは文字化け回避のため英語。
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "axes.unicode_minus": False,
    "figure.dpi": 150,
    "savefig.bbox": "tight",
})

# プレミアム配色（sci07を踏襲）
NAVY   = "#1A365D"
BLUE   = "#2563EB"
CYAN   = "#00B4D8"
RED    = "#DC2626"
ORANGE = "#EA580C"
PURPLE = "#7C3AED"
INK    = "#374151"
GRID   = "#CBD5E1"
PANEL  = "#F8F9FA"

YEAR = 365.0


# ----------------------------------------------------------------------
# 共通：合成水位データ（年周期＋半年周期＋短期変動＋ノイズ）
# ----------------------------------------------------------------------
def synth_levels(n_years=11, dt=1.0, seed=8):
    """上流(MR)を基準に、下流の湖(TSL)が時間ラグして減衰する合成水位。"""
    rng = np.random.default_rng(seed)
    n = int(n_years * YEAR)
    t = np.arange(n) * dt

    # 年周期（洪水パルスの本体）＋半年周期
    annual = 4.5 * np.sin(2 * np.pi * t / YEAR - np.pi / 2)
    semi   = 0.8 * np.sin(2 * np.pi * t / (YEAR / 2))
    base   = 5.0

    # 短期変動（非周期）：上流の出水イベント
    short = np.zeros(n)
    for _ in range(60):
        c = rng.integers(0, n)
        w = rng.integers(4, 12)
        amp = rng.uniform(0.5, 2.0)
        short += amp * np.exp(-0.5 * ((t - t[c]) / w) ** 2)

    # 上流メコン川（Kampong Cham 相当）
    mr = base + annual + semi + short + 0.25 * rng.standard_normal(n)

    # 時間ラグして下流の湖へ伝播（約40日遅れ・減衰）
    lag = 40
    def shift(x, k):
        y = np.empty_like(x)
        y[k:] = x[:-k]
        y[:k] = x[0]
        return y
    annual_l = 4.0 * np.sin(2 * np.pi * (t - lag) / YEAR - np.pi / 2)
    semi_l   = 0.5 * np.sin(2 * np.pi * (t - lag) / (YEAR / 2))
    short_l  = 0.35 * shift(short, lag)   # 短期シグナルは湖で弱まる
    tsl = base + annual_l + semi_l + short_l + 0.25 * rng.standard_normal(n)

    return t, mr, tsl, lag


# ----------------------------------------------------------------------
# Fig 1: 洪水パルス（flood pulse）概念図
# ----------------------------------------------------------------------
def fig_flood_pulse(out):
    t, mr, tsl, lag = synth_levels()
    yrs = t / YEAR

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(9.2, 6.0), sharex=True,
        gridspec_kw={"height_ratios": [2.0, 1.2], "hspace": 0.12})

    # (a) 水位の時系列
    ax1.plot(yrs, mr, color=NAVY, lw=1.3, label="Mekong River (upstream)")
    ax1.plot(yrs, tsl, color=RED, lw=1.3, label="Tonle Sap Lake (downstream)")
    ax1.set_ylabel("Water level (m a.s.l.)", color=INK)
    ax1.set_title("(a)  Seasonal water-level fluctuation — the flood pulse",
                  loc="left", color=INK, fontsize=11, fontweight="bold")
    ax1.legend(loc="upper right", framealpha=0.9, fontsize=9)
    ax1.grid(alpha=0.3, color=GRID)
    ax1.set_facecolor(PANEL)

    # (b) 差分（湖 − 川）：負の領域が「逆流」
    diff = tsl - mr
    ax2.axhline(0, color=INK, lw=0.8)
    ax2.fill_between(yrs, diff, 0, where=diff < 0, color=CYAN, alpha=0.6,
                     label="Reverse flow (river → lake)")
    ax2.fill_between(yrs, diff, 0, where=diff >= 0, color=ORANGE, alpha=0.45,
                     label="Normal flow (lake → river)")
    ax2.plot(yrs, diff, color=INK, lw=0.7)
    ax2.set_ylabel("Lake − River (m)", color=INK)
    ax2.set_xlabel("Time (years)", color=INK)
    ax2.set_title("(b)  Water-level difference: sign flips drive the reverse flow",
                  loc="left", color=INK, fontsize=11, fontweight="bold")
    ax2.legend(loc="upper right", framealpha=0.9, fontsize=9, ncol=2)
    ax2.grid(alpha=0.3, color=GRID)
    ax2.set_facecolor(PANEL)
    ax2.set_xlim(0, yrs.max())

    fig.savefig(out)
    plt.close(fig)
    print("saved", out)


# ----------------------------------------------------------------------
# Fig 2: 自己相関（auto-correlation）
# ----------------------------------------------------------------------
def acf(x, maxlag):
    x = x - x.mean()
    n = len(x)
    full = np.correlate(x, x, mode="full") / (np.var(x) * n)
    mid = n - 1
    return full[mid:mid + maxlag + 1]


def fig_autocorrelation(out):
    t, mr, tsl, lag = synth_levels()
    rng = np.random.default_rng(3)
    # 降水：季節性はあるが日々はランダム（周期的記憶を持たない）
    n = len(t)
    rain = np.maximum(0, rng.standard_normal(n) * 6
                      + 5 * (np.sin(2 * np.pi * t / YEAR - np.pi / 2) > 0.3))

    maxlag = int(2.5 * YEAR)
    lags = np.arange(maxlag + 1)
    acf_wl = acf(mr, maxlag)
    acf_rain = acf(rain, maxlag)

    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    ax.axhline(0, color=INK, lw=0.8)
    ax.plot(lags, acf_wl, color=BLUE, lw=1.8, label="Water level (periodic)")
    ax.plot(lags, acf_rain, color=ORANGE, lw=1.3, label="Rainfall (non-periodic)")

    # 1年・2年のピーク位置
    for m in (1, 2):
        ax.axvline(m * YEAR, color=GRID, ls="--", lw=1)
        ax.text(m * YEAR, 0.92, f"{m} yr", color=INK, fontsize=9,
                ha="center", va="top",
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=GRID))

    ax.set_xlabel("Lag (days)", color=INK)
    ax.set_ylabel("Auto-correlation coefficient", color=INK)
    ax.set_title("Auto-correlation: detecting periodicity and 'memory'",
                 loc="left", color=INK, fontsize=11, fontweight="bold")
    ax.legend(loc="upper right", framealpha=0.9, fontsize=9)
    ax.grid(alpha=0.3, color=GRID)
    ax.set_facecolor(PANEL)
    ax.set_xlim(0, maxlag)
    ax.set_ylim(-1.05, 1.05)
    fig.savefig(out)
    plt.close(fig)
    print("saved", out)


# ----------------------------------------------------------------------
# Fig 3: 相互相関（cross-correlation）と時間ラグ
# ----------------------------------------------------------------------
def ccf(x, y, maxlag):
    x = (x - x.mean()) / x.std()
    y = (y - y.mean()) / y.std()
    n = len(x)
    full = np.correlate(y, x, mode="full") / n
    mid = n - 1
    lags = np.arange(-maxlag, maxlag + 1)
    vals = full[mid - maxlag: mid + maxlag + 1]
    return lags, vals


def fig_crosscorrelation(out):
    t, mr, tsl, lag = synth_levels()

    maxlag = 150
    lags, vals = ccf(mr, tsl, maxlag)
    kmax = lags[np.argmax(vals)]

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(9.2, 6.4),
        gridspec_kw={"height_ratios": [1.2, 1.4], "hspace": 0.32})

    # (a) 2系列（最初の3年）を並べて時間差を視覚化
    yrs = t / YEAR
    m = yrs <= 3
    ax1.plot(yrs[m], (mr[m] - mr[m].mean()), color=NAVY, lw=1.3,
             label="Upstream (Mekong River)")
    ax1.plot(yrs[m], (tsl[m] - tsl[m].mean()), color=RED, lw=1.3,
             label="Downstream (Tonle Sap Lake)")
    ax1.set_title("(a)  Two water-level series — the lake peaks later",
                  loc="left", color=INK, fontsize=11, fontweight="bold")
    ax1.set_xlabel("Time (years)", color=INK)
    ax1.set_ylabel("Anomaly (m)", color=INK)
    ax1.legend(loc="upper right", framealpha=0.9, fontsize=9)
    ax1.grid(alpha=0.3, color=GRID)
    ax1.set_facecolor(PANEL)

    # (b) 相互相関関数：ピークの位置＝時間ラグ
    ax2.axhline(0, color=INK, lw=0.8)
    ax2.axvline(0, color=GRID, lw=1)
    ax2.plot(lags, vals, color=PURPLE, lw=1.8)
    ax2.plot([kmax], [vals.max()], "o", color=RED, ms=8, zorder=5)
    ax2.annotate(f"peak at lag = {kmax} days",
                 xy=(kmax, vals.max()), xytext=(kmax + 18, vals.max() - 0.15),
                 color=RED, fontsize=10, fontweight="bold",
                 arrowprops=dict(arrowstyle="->", color=RED))
    ax2.set_title("(b)  Cross-correlation function: the lag is where it peaks",
                  loc="left", color=INK, fontsize=11, fontweight="bold")
    ax2.set_xlabel("Lag (days)   —   positive = lake lags behind river", color=INK)
    ax2.set_ylabel("Cross-correlation", color=INK)
    ax2.grid(alpha=0.3, color=GRID)
    ax2.set_facecolor(PANEL)
    ax2.set_xlim(-maxlag, maxlag)

    fig.savefig(out)
    plt.close(fig)
    print("saved", out)


# ----------------------------------------------------------------------
# Fig 4: クロスウェーブレット変換（自前 Morlet CWT）
# ----------------------------------------------------------------------
def morlet_cwt(x, dt, scales, w0=6.0):
    x = x - x.mean()
    n = len(x)
    xf = np.fft.fft(x)
    k = np.fft.fftfreq(n, d=dt) * 2 * np.pi      # 角周波数
    W = np.empty((len(scales), n), dtype=complex)
    for i, s in enumerate(scales):
        norm = np.sqrt(2 * np.pi * s / dt) * (np.pi ** -0.25)
        daughter = norm * np.exp(-0.5 * (s * k - w0) ** 2) * (k > 0)
        W[i] = np.fft.ifft(xf * daughter)
    return W


def fig_cross_wavelet(out):
    t, mr, tsl, lag = synth_levels()
    dt = 1.0
    n = len(t)
    w0 = 6.0
    # Morlet: period ≈ 1.033 * scale
    fourier_factor = 4 * np.pi / (w0 + np.sqrt(2 + w0 ** 2))
    periods = np.logspace(np.log10(30), np.log10(900), 80)
    scales = periods / fourier_factor

    Wx = morlet_cwt(mr, dt, scales, w0)
    Wy = morlet_cwt(tsl, dt, scales, w0)
    XWT = Wx * np.conj(Wy)
    power = np.abs(XWT)
    phase = np.angle(XWT)

    yrs = t / YEAR
    fig, ax = plt.subplots(figsize=(9.4, 5.2))
    levels = np.linspace(0, np.percentile(power, 99), 60)
    cf = ax.contourf(yrs, periods, power, levels=levels, cmap="turbo", extend="max")
    ax.set_yscale("log")
    ax.set_ylim(periods.max(), periods.min())
    ax.axhline(YEAR, color="white", ls="--", lw=1.2, alpha=0.9)
    ax.text(0.2, YEAR * 0.82, "365-day band", color="white", fontsize=9,
            fontweight="bold")

    # 位相矢印（in-phase=右、X が Y を先導=右やや下）。間引いて描画。
    si, sj = 6, 220
    for ii in range(0, len(periods), si):
        for jj in range(0, n, sj):
            if periods[ii] < 200 or periods[ii] > 700:
                continue
            ang = phase[ii, jj]
            ax.quiver(yrs[jj], periods[ii], np.cos(ang), np.sin(ang),
                      color="white", scale=22, width=0.0035,
                      headwidth=4, alpha=0.9)

    ax.set_xlabel("Time (years)", color=INK)
    ax.set_ylabel("Period (days)", color=INK)
    ax.set_title("Cross-wavelet transform: phase arrows reveal the time-varying lag",
                 loc="left", color=INK, fontsize=11, fontweight="bold")
    cb = fig.colorbar(cf, ax=ax, pad=0.02)
    cb.set_label("Cross-wavelet power", color=INK)
    ax.set_xlim(0, yrs.max())
    fig.savefig(out)
    plt.close(fig)
    print("saved", out)


# ----------------------------------------------------------------------
# Fig 5: 研究位置の模式図（メコン川＋トンレサップ湖）
# ----------------------------------------------------------------------
def fig_study_map(out):
    fig, ax = plt.subplots(figsize=(7.6, 6.2))
    ax.set_facecolor("#EAF2F8")

    # メコン川（縦に流れる）
    river_x = [6.2, 6.0, 5.8, 5.9, 6.1, 6.0]
    river_y = [9.5, 8.0, 6.2, 4.5, 2.8, 1.0]
    ax.plot(river_x, river_y, color=BLUE, lw=6, solid_capstyle="round",
            zorder=1)

    # トンレサップ湖（楕円）
    from matplotlib.patches import Ellipse
    lake = Ellipse((2.6, 6.6), width=2.6, height=4.2, angle=28,
                   facecolor="#2E86C1", edgecolor=NAVY, lw=1.5, zorder=1)
    ax.add_patch(lake)
    ax.text(2.4, 6.7, "Tonle Sap\nLake", color="white", fontsize=11,
            ha="center", va="center", fontweight="bold", zorder=3)

    # トンレサップ川（湖 → 合流点 PPP）
    ax.plot([3.6, 5.0, 5.9], [5.2, 4.5, 4.3], color="#5DADE2", lw=4,
            solid_capstyle="round", zorder=1)
    ax.text(4.5, 4.0, "Tonle Sap River", color=NAVY, fontsize=9,
            rotation=-12, ha="center")

    # 観測点
    stations = {
        "KC (upstream)": (6.05, 8.0),
        "PPP (junction)": (5.9, 4.3),
        "PK (river)": (4.9, 4.55),
        "KL (lake)": (2.9, 7.6),
        "NL (downstream)": (6.05, 1.6),
    }
    for name, (x, y) in stations.items():
        ax.plot(x, y, "o", color=RED, ms=10, mec="white", mew=1.5, zorder=4)
        ax.annotate(name, (x, y), xytext=(x + 0.25, y),
                    fontsize=9, color=INK, va="center", fontweight="bold")

    ax.text(6.05, 9.6, "Mekong River", color=BLUE, fontsize=10,
            rotation=90, ha="center", va="top", fontweight="bold")
    ax.annotate("", xy=(6.0, 1.2), xytext=(6.1, 2.6),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2))
    ax.text(6.7, 2.0, "flow\n(dry season)", color=BLUE, fontsize=8, va="center")

    ax.set_xlim(0.5, 8.5)
    ax.set_ylim(0.3, 10.0)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("Tonle Sap basin (schematic): five water-level stations",
                 loc="left", color=INK, fontsize=11, fontweight="bold")
    for sp in ax.spines.values():
        sp.set_edgecolor(GRID)
    fig.savefig(out)
    plt.close(fig)
    print("saved", out)


# ----------------------------------------------------------------------
# Fig 6: クロスウェーブレット「読み方ガイド」（矢印の意味＋位相→時間）
# ----------------------------------------------------------------------
def fig_arrow_guide(out):
    from matplotlib.patches import Wedge, Circle
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(10.2, 4.7))

    # --- (a) 矢印の向きの意味 ---
    axA.set_xlim(-1.5, 1.5); axA.set_ylim(-1.5, 1.5)
    axA.set_aspect("equal"); axA.axis("off")
    axA.set_title("(a)  What the ARROW DIRECTION means",
                  color=INK, fontsize=11, fontweight="bold", loc="left")
    arr = dict(width=0.025, head_width=0.13, head_length=0.13,
               length_includes_head=True, fc=NAVY, ec=NAVY)
    L = 0.95
    axA.arrow(0, 0,  L, 0, **arr)   # right
    axA.arrow(0, 0, -L, 0, **arr)   # left
    axA.arrow(0, 0, 0, -L, **{**arr, "fc": RED, "ec": RED})    # down
    axA.arrow(0, 0, 0,  L, **{**arr, "fc": CYAN, "ec": CYAN})  # up
    axA.add_patch(Circle((0, 0), 0.07, color=INK, zorder=5))
    axA.text(1.05, 0, "In-phase\n(lag ≈ 0)", va="center", ha="left",
             fontsize=9, color=NAVY, fontweight="bold")
    axA.text(-1.05, 0, "Anti-phase\n(½ period\napart)", va="center", ha="right",
             fontsize=9, color=NAVY, fontweight="bold")
    axA.text(0, -1.08, "River leads Lake\n(¼ period)", va="top", ha="center",
             fontsize=9, color=RED, fontweight="bold")
    axA.text(0, 1.08, "Lake leads River\n(¼ period)", va="bottom", ha="center",
             fontsize=9, color="#0E7490", fontweight="bold")

    # --- (b) 位相角 → 時間ラグ ---
    axB.set_xlim(-1.5, 1.7); axB.set_ylim(-1.5, 1.5)
    axB.set_aspect("equal"); axB.axis("off")
    axB.set_title("(b)  What the ARROW ANGLE gives you",
                  color=INK, fontsize=11, fontweight="bold", loc="left")
    axB.add_patch(Circle((0, 0), 1.0, fill=False, ec=GRID, lw=1.5))
    theta = 36.0
    axB.add_patch(Wedge((0, 0), 1.0, 0, theta, fc=ORANGE, alpha=0.35))
    # 0度（基準）と θ の矢印
    axB.arrow(0, 0, 0.95, 0, **{**arr, "fc": GRID, "ec": GRID})
    th = np.radians(theta)
    axB.arrow(0, 0, 0.95 * np.cos(th), 0.95 * np.sin(th),
              **{**arr, "fc": NAVY, "ec": NAVY})
    axB.text(0.62, 0.16, "θ", fontsize=14, color=NAVY, fontweight="bold")
    axB.text(0, -1.28,
             "One full turn (360°) = one period T\n"
             "θ = 36°  →  36/360 = 1/10 of a cycle\n"
             "time lag = (θ/360) × T",
             ha="center", va="top", fontsize=9.5, color=INK,
             bbox=dict(boxstyle="round,pad=0.4", fc=PANEL, ec=GRID))

    fig.savefig(out)
    plt.close(fig)
    print("saved", out)


if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    fig_arrow_guide(os.path.join(here, "arrow_guide.png"))
    fig_flood_pulse(os.path.join(here, "flood_pulse.png"))
    fig_autocorrelation(os.path.join(here, "autocorrelation.png"))
    fig_crosscorrelation(os.path.join(here, "crosscorrelation.png"))
    # cross_wavelet.png は xwt_grinsted.py（Grinstedツールボックスの忠実移植）で生成する。
    # fig_cross_wavelet(os.path.join(here, "cross_wavelet.png"))
    # 図1（位置図）は論文Fig.1（Ton.png）を使用するため、study_map は生成しない。
    # fig_study_map(os.path.join(here, "study_map.png"))
    print("ALL DONE")
