# -*- coding: utf-8 -*-
"""
地下水科学入門 #7（南大東島・淡水レンズ）の図生成スクリプト
- 独立スクリプトでPNGを事前生成し、index.qmd からは静的参照する（CLAUDE.mdルール）
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["MS Gothic", "Noto Sans CJK JP", "DejaVu Sans"],
    "axes.unicode_minus": False,
    "figure.dpi": 150,
})

PALETTE = {
    "bg": "#F8F9FA",
    "panel": "#F0F4F8",
    "blue": "#2563EB",
    "red": "#DC2626",
    "ink": "#374151",
    "grid": "#CBD5E1",
    "fresh": "#60A5FA",
    "salt": "#1E3A5F",
}

# 主要5分潮（周期 h）
CONSTITUENTS = {
    "O1": 25.82,   # 主太陰日周潮
    "K1": 23.93,   # 太陰太陽日周潮
    "N2": 12.66,   # 楕円太陰半日周潮
    "M2": 12.42,   # 主太陰半日周潮
    "S2": 12.00,   # 主太陽半日周潮
}
AMP = {"O1": 18, "K1": 22, "N2": 9, "M2": 42, "S2": 16}  # 潮位振幅(cm)相当


# ----------------------------------------------------------------------
# Fig 1: 潮位合成データ → FFT スペクトル（ハンズオンの主役・プレミアム版）
# ----------------------------------------------------------------------
# プレミアム配色
NAVY = "#1A365D"
CYAN = "#00B4D8"
DIURNAL = "#7C3AED"     # 日周潮の帯
SEMIDI = "#EA580C"      # 半日周潮の帯


def fig_tidal_fft(out):
    np.random.seed(7)
    n = 8760            # 1時間 × 8760 = 365日（実データと同じ1年分）
    dt = 1.0            # 1時間サンプリング
    t_idx = np.arange(n)
    date = pd.date_range("2014-01-01", periods=n, freq="h")

    # --- 潮位（海）：5分潮の重ね合わせ ---
    tide = np.zeros(n)
    for name, period in CONSTITUENTS.items():
        phase = np.random.uniform(0, 2 * np.pi)
        tide += AMP[name] * np.sin(2 * np.pi * t_idx / period + phase)
    tide += 2.0 * np.random.randn(n)

    # --- 地下水位：潮位を減衰＆位相遅れさせた応答 ---
    lag = 3                                    # 約3時間遅れ
    gwl = 0.32 * np.roll(tide, lag)            # 振幅比 ~0.3
    gwl += 1.0 * np.random.randn(n)
    gwl_demean = gwl - gwl.mean()
    tide_demean = tide - tide.mean()

    # --- FFT ---
    freq = np.fft.rfftfreq(n, d=dt)            # cycle/hour
    amp_tide = np.abs(np.fft.rfft(tide_demean)) / n * 2
    amp_gwl = np.abs(np.fft.rfft(gwl_demean)) / n * 2

    fig, axes = plt.subplots(2, 1, figsize=(13, 8.5),
                             gridspec_kw={"height_ratios": [1, 1.15]})
    fig.patch.set_facecolor("#FFFFFF")

    # ===== Top: time series (first 14 days) =====
    ax0 = axes[0]
    ax0.set_facecolor("#FBFCFE")
    win = 24 * 14
    ax0.plot(date[:win], tide[:win], lw=1.6, color=NAVY,
             label="Sea tide", alpha=0.9, zorder=3)
    ax0.plot(date[:win], gwl[:win], lw=2.0, color=CYAN,
             label="Groundwater level", alpha=0.95, zorder=4)
    ax0.fill_between(date[:win], gwl[:win], gwl[:win].mean(),
                     color=CYAN, alpha=0.08, zorder=1)
    ax0.set_ylabel("Fluctuation (cm)", fontsize=15, color="#1F2937")
    ax0.set_title("(1) Time series of sea tide and groundwater level (first 14 days)",
                  fontsize=16, fontweight="bold", color=NAVY, loc="left", pad=10)
    leg0 = ax0.legend(fontsize=13, loc="upper right", framealpha=0.95,
                      edgecolor="#E5E7EB")
    leg0.get_frame().set_facecolor("#FFFFFF")
    ax0.grid(True, ls="--", lw=0.5, color="#E5E7EB", zorder=0)
    ax0.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
    ax0.tick_params(labelsize=12.5, colors="#6B7280")
    for s in ["top", "right"]:
        ax0.spines[s].set_visible(False)
    for s in ["left", "bottom"]:
        ax0.spines[s].set_color("#9CA3AF")
    ax0.annotate("Smaller amplitude, ~3 h phase lag",
                 xy=(0.015, 0.06), xycoords="axes fraction",
                 fontsize=13, color="#0E7490", style="italic")

    # ===== Bottom: amplitude spectrum =====
    ax1 = axes[1]
    ax1.set_facecolor("#FBFCFE")
    ymax = max(amp_tide[1:].max(), amp_gwl[1:].max()) * 1.18

    # frequency bands (diurnal / semidiurnal)
    ax1.axvspan(1/26.5, 1/23.0, color=DIURNAL, alpha=0.07, zorder=0)
    ax1.axvspan(1/13.0, 1/11.6, color=SEMIDI, alpha=0.07, zorder=0)

    ax1.plot(freq, amp_tide, lw=1.2, color="#94A3B8",
             label="Sea tide", alpha=0.9, zorder=2)
    ax1.fill_between(freq, amp_gwl, color=CYAN, alpha=0.18, zorder=2)
    ax1.plot(freq, amp_gwl, lw=1.7, color=NAVY,
             label="Groundwater level", alpha=0.95, zorder=3)

    ax1.set_xlim(0, 0.11)
    ax1.set_ylim(0, ymax)
    ax1.set_xlabel("Frequency (cycle / hour)", fontsize=15, color="#1F2937")
    ax1.set_ylabel("Amplitude spectrum", fontsize=15, color="#1F2937")
    ax1.set_title("(2) Amplitude spectrum by FFT: five major tidal constituents",
                  fontsize=16, fontweight="bold", color=NAVY, loc="left", pad=10)
    ax1.grid(True, ls="--", lw=0.5, color="#E5E7EB", zorder=0)
    ax1.tick_params(labelsize=12.5, colors="#6B7280")
    for s in ["top", "right"]:
        ax1.spines[s].set_visible(False)
    for s in ["left", "bottom"]:
        ax1.spines[s].set_color("#9CA3AF")

    # constituent labels (badge above each peak)
    for name, period in CONSTITUENTS.items():
        f = 1.0 / period
        peak = amp_gwl[np.argmin(np.abs(freq - f))]
        ax1.annotate(f"$\\mathrm{{{name[0]}}}_{name[1]}$",
                     xy=(f, peak), xytext=(f, peak + ymax * 0.10),
                     ha="center", fontsize=15, fontweight="bold", color="#B91C1C",
                     bbox=dict(boxstyle="round,pad=0.2", fc="white",
                               ec="#FCA5A5", lw=0.8),
                     arrowprops=dict(arrowstyle="-", color="#FCA5A5", lw=0.8))

    # band labels
    ax1.text(1/24.7, ymax * 0.93, "Diurnal  O₁ · K₁", ha="center",
             fontsize=14, color=DIURNAL, fontweight="bold")
    ax1.text(1/12.3, ymax * 0.93, "Semidiurnal  N₂ · M₂ · S₂", ha="center",
             fontsize=14, color=SEMIDI, fontweight="bold")

    leg1 = ax1.legend(fontsize=13, loc="upper right", framealpha=0.95,
                      edgecolor="#E5E7EB")
    leg1.get_frame().set_facecolor("#FFFFFF")

    plt.tight_layout()
    plt.savefig(out, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print("saved", out)


# ----------------------------------------------------------------------
# Fig 2: 淡水レンズ概念図（Ghyben-Herzberg）
# ----------------------------------------------------------------------
def fig_lens_concept(out):
    fig, ax = plt.subplots(figsize=(11, 6))
    fig.patch.set_facecolor(PALETTE["bg"])
    ax.set_facecolor("#EAF2FB")

    x = np.linspace(0, 10, 400)
    # 島の地表（緩い台地）
    ground = 1.2 - 0.02 * (x - 5) ** 2
    ground = np.clip(ground, 0.2, None)
    sea_level = 0.0

    # 淡水レンズ（地下水面と塩淡境界）
    wt = 0.18 * np.exp(-((x - 5) ** 2) / 14)          # 地下水面(誇張)
    # Ghyben-Herzberg: 境界は水位の約40倍下
    interface = -40 * wt

    # 塩水域
    ax.fill_between(x, interface, -9, color=PALETTE["salt"], alpha=0.85, zorder=1)
    # 淡水レンズ
    ax.fill_between(x, wt, interface, color=PALETTE["fresh"], alpha=0.8, zorder=2)
    # 海
    ax.fill_between(x, sea_level, -9, where=(x < 0.6) | (x > 9.4),
                    color="#3B82F6", alpha=0.5, zorder=0)
    # 地面
    ax.fill_between(x, ground, wt, color="#C7A17A", alpha=0.55, zorder=1)
    ax.plot(x, ground, color="#7C5A37", lw=1.5, zorder=4)

    # ライン
    ax.plot(x, wt, color="#1D4ED8", lw=1.6, zorder=5)
    ax.plot(x, interface, color="#0F2A47", lw=1.6, ls="--", zorder=5)
    ax.axhline(sea_level, color="#1E40AF", lw=1.0, ls=":", alpha=0.7)

    # 注記
    ax.annotate("地下水面", xy=(5, wt.max()), xytext=(6.7, 0.9),
                fontsize=10, color="#1D4ED8",
                arrowprops=dict(arrowstyle="->", color="#1D4ED8"))
    ax.annotate("塩淡境界（遷移帯）", xy=(5, interface.min()), xytext=(5.4, -8.0),
                fontsize=10, color="#0F2A47",
                arrowprops=dict(arrowstyle="->", color="#0F2A47"))
    ax.text(5, interface.min()*0.45, "淡水レンズ", ha="center",
            fontsize=13, color="#0B3D91", fontweight="bold")
    ax.text(1.5, -7.5, "塩水", color="white", fontsize=12, fontweight="bold")
    ax.text(0.1, 0.25, "海", color="#0B3D91", fontsize=11)

    # Ghyben-Herzberg 注記
    ax.text(0.2, -3.2, "Ghyben-Herzberg 関係\n水位 h → 境界深 ≈ 40 h",
            fontsize=9.5, color="#0F2A47",
            bbox=dict(boxstyle="round", fc="white", ec="#93C5FD"))

    ax.set_xlim(0, 10)
    ax.set_ylim(-9, 1.6)
    ax.set_ylabel("標高（模式・縦は誇張）", fontsize=10)
    ax.set_xticks([])
    ax.set_title("淡水レンズの模式断面：塩水の上に浮かぶ「真水の浮き袋」", fontsize=12)
    plt.tight_layout()
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print("saved", out)


if __name__ == "__main__":
    fig_tidal_fft("daito_tidal_fft.png")
    fig_lens_concept("daito_lens_concept.png")
