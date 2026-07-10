# -*- coding: utf-8 -*-
"""
地下水科学入門 #9（南大東島・潮汐→透水係数→ラグベース重回帰）の図生成スクリプト
- 独立スクリプトでPNGを事前生成し、index.qmd からは静的参照する（CLAUDE.mdルール）
- 実データ: ../groundwater-sci07/daito.csv （Tide / 92-2=well 922 / Site3=well MD3）
- 図中ラベルは文字化け回避のため英語。
"""
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "axes.unicode_minus": False,
    "figure.dpi": 150,
    "savefig.bbox": "tight",
})

NAVY, BLUE, CYAN = "#1A365D", "#2563EB", "#00B4D8"
RED, ORANGE, PURPLE = "#DC2626", "#EA580C", "#7C3AED"
INK, GRID, PANEL = "#374151", "#CBD5E1", "#F8F9FA"

TAU_H = 12.4206              # M2 周期 [h]
TAU_S = TAU_H * 3600
S_YIELD, B_THICK = 0.1, 300.0   # ケース C1

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, "..", "groundwater-sci07", "daito.csv")

# 論文 Yang et al. (2021) Table 2 : (well, x[m], M2 time lag[h])
WELLS = [("922", 1340, 2.3), ("923", 934, 3.1), ("924", 2304, 3.0),
         ("925", 1346, 2.9), ("928", 1067, 2.5), ("931", 1143, 2.3),
         ("932", 1648, 2.8), ("933", 2001, 3.0), ("935", 2310, 2.9),
         ("936", 1384, 3.0), ("982", 2241, 3.0), ("MD1", 1621, 2.6),
         ("MD2", 250, 1.3), ("MD3", 2367, 2.8), ("MD4", 1196, 2.6)]


# ----------------------------------------------------------------------
def load():
    tide, w922, md3 = [], [], []
    with open(CSV, newline="") as f:
        r = csv.reader(f); next(r)
        for row in r:
            try:
                tide.append(float(row[1])); w922.append(float(row[2])); md3.append(float(row[3]))
            except (ValueError, IndexError):
                pass
    return np.array(tide), np.array(w922), np.array(md3)


def bandpass(x, lo=1/30.0, hi=1/10.0, fs=1.0, order=3):
    """潮汐帯（周期 10〜30 h）だけを取り出す"""
    ny = fs / 2
    b, a = butter(order, [lo/ny, hi/ny], btype="band")
    return filtfilt(b, a, x - np.mean(x))


# 主要5分潮を同時にフィットして相互干渉を除く（FFT単一ビンより厳密）
PERIODS = {"M2": 12.4206, "S2": 12.0000, "N2": 12.6583,
           "K1": 23.9345, "O1": 25.8193}


def harmonic_fit(y):
    """最小二乗調和解析。各分潮の (振幅, 位相) を返す。"""
    n = len(y)
    t = np.arange(n, dtype=float)
    cols = [np.ones(n)]
    for p in PERIODS.values():
        w = 2 * np.pi / p
        cols += [np.cos(w * t), np.sin(w * t)]
    X = np.column_stack(cols)
    beta, *_ = np.linalg.lstsq(X, y - y.mean(), rcond=None)
    out = {}
    for i, k in enumerate(PERIODS):
        a, b = beta[1 + 2*i], beta[2 + 2*i]
        out[k] = (float(np.hypot(a, b)), float(np.arctan2(b, a)))
    return out


def m2_amp_phase(x):
    """M2 分潮の振幅と位相（調和解析による）"""
    return harmonic_fit(x)["M2"]


def m2_component(y, n_pts):
    """フィットした M2 成分を n_pts 時間分だけ再構成する"""
    R, phi = m2_amp_phase(y)
    w = 2 * np.pi / TAU_H
    t = np.arange(n_pts, dtype=float)
    return R * np.cos(w * t - phi)


def K_from_lag(x_m, lag_h):
    """Ferris(1952): 位相ラグ → 水理拡散係数 D=T/S → 透水係数 K"""
    theta = 2 * np.pi * lag_h / TAU_H
    D = np.pi * x_m ** 2 / (TAU_S * theta ** 2)
    T = D * S_YIELD
    return D, T, T / B_THICK


# ----------------------------------------------------------------------
# Fig 1: 潮位と2井の水位（潮汐帯）
# ----------------------------------------------------------------------
def fig_two_wells(out, tide, w922, md3):
    """M2 分潮成分（調和解析で抽出）を重ねて、減衰と遅れを見る"""
    n = 24 * 3                                   # 3日分
    ct, c9, c3 = m2_component(tide, n), m2_component(w922, n), m2_component(md3, n)
    A9 = m2_amp_phase(w922)[0]
    A3 = m2_amp_phase(md3)[0]
    t = np.arange(n) / 24.0

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9.8, 6.4), sharex=True,
                                   gridspec_kw={"height_ratios": [1.25, 1],
                                                "hspace": 0.16})
    ax1.plot(t, ct, color=NAVY, lw=2.2, label="Sea level  (M$_2$, amp. 0.543 m)")
    ax1.axhline(0, color=INK, lw=0.7)
    ax1.set_ylabel("M$_2$ tide (m)", color=INK)
    ax1.set_title("The tide propagates inland: attenuated and delayed  (M$_2$ constituent)",
                  loc="left", color=INK, fontsize=11, fontweight="bold")
    ax1.legend(loc="upper right", fontsize=9, framealpha=0.9)
    ax1.grid(alpha=0.3, color=GRID); ax1.set_facecolor(PANEL)

    ax2.plot(t, c9, color=ORANGE, lw=2.0,
             label=f"Well 922   (1,340 m)   amp. {A9:.4f} m")
    ax2.plot(t, c3, color=RED, lw=2.0,
             label=f"Well MD3  (2,367 m — farthest)   amp. {A3:.4f} m")
    ax2.axhline(0, color=INK, lw=0.7)
    ax2.set_xlabel("Time (days)", color=INK)
    ax2.set_ylabel("Groundwater, M$_2$ (m)", color=INK)
    ax2.legend(loc="upper right", fontsize=9, framealpha=0.9)
    ax2.grid(alpha=0.3, color=GRID); ax2.set_facecolor(PANEL)
    ax2.set_xlim(0, t.max())
    ax2.text(0.012, 0.04,
             "MD3 lies 1.8x farther from the coast, yet its M$_2$ amplitude is LARGER\n"
             "and its peak arrives only slightly later  →  far more permeable ground",
             transform=ax2.transAxes, fontsize=8.6, color=INK, va="bottom",
             bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=GRID, alpha=0.92))
    fig.savefig(out); plt.close(fig); print("saved", out)


# ----------------------------------------------------------------------
# Fig 2: 相互相関（ラグ）と M2 振幅比
# ----------------------------------------------------------------------
def fig_xcorr_amp(out, tide, w922, md3):
    tb = bandpass(tide)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.6, 4.4),
                                   gridspec_kw={"width_ratios": [1.55, 1]})
    maxlag = 12
    for name, y, col in [("Well 922", w922, ORANGE), ("Well MD3", md3, RED)]:
        wb = bandpass(y)
        a = (tb - tb.mean()) / tb.std(); b = (wb - wb.mean()) / wb.std()
        n = len(a)
        full = np.correlate(b, a, mode="full") / n
        mid = n - 1
        lags = np.arange(-maxlag, maxlag + 1)
        vals = full[mid-maxlag: mid+maxlag+1]
        k = lags[np.argmax(vals)]
        ax1.plot(lags, vals, color=col, lw=2.0, label=f"{name}  (peak at {k} h)")
        ax1.plot([k], [vals.max()], "o", color=col, ms=8, zorder=5)

    ax1.axvline(0, color=GRID, lw=1)
    ax1.axhline(0, color=INK, lw=0.7)
    ax1.set_xlabel("Lag (hours)   —   positive = groundwater lags the sea", color=INK)
    ax1.set_ylabel("Cross-correlation", color=INK)
    ax1.set_title("(a)  Cross-correlation gives the time lag",
                  loc="left", color=INK, fontsize=11, fontweight="bold")
    ax1.legend(loc="lower center", fontsize=9, framealpha=0.9)
    ax1.grid(alpha=0.3, color=GRID); ax1.set_facecolor(PANEL)

    # M2 振幅
    At, _ = m2_amp_phase(tide)
    A9, _ = m2_amp_phase(w922)
    A3, _ = m2_amp_phase(md3)
    names = ["Sea\n(tide)", "Well 922\n1,340 m", "Well MD3\n2,367 m"]
    vals = [At, A9, A3]
    cols = [NAVY, ORANGE, RED]
    bars = ax2.bar(names, vals, color=cols, width=0.6)
    for b, v, r in zip(bars, vals, [1.0, A9/At, A3/At]):
        ax2.text(b.get_x()+b.get_width()/2, v+0.006, f"{v:.3f} m\n(A={r:.3f})",
                 ha="center", fontsize=8.5, color=INK, fontweight="bold")
    ax2.set_ylabel("M$_2$ amplitude (m)", color=INK)
    ax2.set_ylim(0, max(vals)*1.35)
    ax2.set_title("(b)  M$_2$ amplitude and tidal efficiency $A$",
                  loc="left", color=INK, fontsize=11, fontweight="bold")
    ax2.grid(alpha=0.3, color=GRID, axis="y"); ax2.set_facecolor(PANEL)

    fig.tight_layout(); fig.savefig(out); plt.close(fig); print("saved", out)


# ----------------------------------------------------------------------
# Fig 3: Ferris 解の概念（振幅の指数減衰・位相の線形遅れ）
# ----------------------------------------------------------------------
def fig_ferris(out):
    D = 100.0
    x = np.linspace(0, 2600, 400)
    decay = np.exp(-x * np.sqrt(np.pi / (D * TAU_S)))
    lag = x * np.sqrt(np.pi / (D * TAU_S)) * TAU_H / (2 * np.pi)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.6, 4.3))
    ax1.plot(x, decay, color=BLUE, lw=2.4)
    ax1.fill_between(x, 0, decay, color=BLUE, alpha=0.12)
    ax1.set_xlabel("Distance from coast  $x$ (m)", color=INK)
    ax1.set_ylabel("Tidal efficiency  $A = h_x/h_0$", color=INK)
    ax1.set_title("(a)  Amplitude decays exponentially", loc="left",
                  color=INK, fontsize=11, fontweight="bold")
    ax1.grid(alpha=0.3, color=GRID); ax1.set_facecolor(PANEL)
    ax1.text(0.45, 0.72, r"$A=\exp\left(-x\sqrt{\pi S/\tau T}\right)$",
             transform=ax1.transAxes, fontsize=12, color=NAVY,
             bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=GRID))

    ax2.plot(x, lag, color=RED, lw=2.4)
    ax2.set_xlabel("Distance from coast  $x$ (m)", color=INK)
    ax2.set_ylabel("Time lag (hours)", color=INK)
    ax2.set_title("(b)  Phase lag grows linearly", loc="left",
                  color=INK, fontsize=11, fontweight="bold")
    ax2.grid(alpha=0.3, color=GRID); ax2.set_facecolor(PANEL)
    ax2.text(0.06, 0.72, r"$\theta = x\sqrt{\pi S/\tau T}$" + "\n" +
             r"$\Rightarrow\ T/S=\pi x^2/(\tau\theta^2)$",
             transform=ax2.transAxes, fontsize=11, color=NAVY,
             bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=GRID))

    fig.suptitle("Ferris (1952): the tide carries the aquifer's fingerprint",
                 color=INK, fontsize=12, fontweight="bold", y=1.02)
    fig.tight_layout(); fig.savefig(out); plt.close(fig); print("saved", out)


# ----------------------------------------------------------------------
# Fig 4: 距離 vs ラグ（色＝K）と等拡散係数線  ★主役
# ----------------------------------------------------------------------
def fig_k_vs_distance(out):
    xs = np.array([w[1] for w in WELLS], float)
    lags = np.array([w[2] for w in WELLS], float)
    Ks = np.array([K_from_lag(x, l)[2] for x, l in zip(xs, lags)])

    XMAX, YMAX = 2750.0, 3.7
    fig, ax = plt.subplots(figsize=(10.0, 5.8))

    # 等 D 線（Ferris より lag ∝ x、原点を通る直線）。ラベルは必ず軸内に置く。
    for D in (25, 50, 100, 200):
        slope = np.sqrt(np.pi / (D * TAU_S)) * TAU_H / (2 * np.pi)
        x_end = min(YMAX / slope, XMAX)
        ax.plot([0, x_end], [0, slope * x_end], ls="--", lw=1.0,
                color=GRID, zorder=1)
        x_lab = min(YMAX / slope * 0.93, XMAX * 0.95)
        ax.text(x_lab, slope * x_lab, f"D={D}", fontsize=8, color="#94A3B8",
                ha="center", va="bottom", rotation=0,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.8))

    sc = ax.scatter(xs, lags, c=Ks * 1e3, s=170, cmap="YlOrRd",
                    edgecolor=INK, linewidth=0.8, zorder=3,
                    norm=plt.Normalize(0, 70))

    # 重なりやすい井戸だけラベル位置を微調整
    off = {"982": (-20, 9), "924": (16, 9), "935": (22, -3), "MD3": (5, -17),
           "925": (-13, 9), "936": (10, 9), "922": (-16, -14)}
    for w, x, l in WELLS:
        dx, dy = off.get(w, (0, 11))
        ax.annotate(w, (x, l), xytext=(dx, dy), textcoords="offset points",
                    ha="center", fontsize=8, color=INK, zorder=5)

    for w, x, l, col in [("922", 1340, 2.3, "#1D4ED8"), ("MD3", 2367, 2.8, "#B91C1C")]:
        ax.scatter([x], [l], s=330, facecolor="none", edgecolor=col,
                   linewidth=2.4, zorder=4)

    ax.annotate("", xy=(2320, 2.74), xytext=(1390, 2.30),
                arrowprops=dict(arrowstyle="->", color="#B91C1C", lw=1.8,
                                connectionstyle="arc3,rad=-0.28"))
    ax.text(1830, 1.72, "MD3 is 1.8x farther,\nbut its lag grows only +0.5 h\n"
                        r"$\Rightarrow$ $D$ and $K$ are 2.1x higher",
            fontsize=9.5, color="#B91C1C", fontweight="bold", ha="center",
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#FCA5A5"))

    ax.set_xlabel("Shortest distance to coast  $x$ (m)", color=INK)
    ax.set_ylabel("M$_2$ time lag (hours)", color=INK)
    ax.set_title("What matters is the lag RELATIVE to distance — not the lag itself",
                 loc="left", color=INK, fontsize=11.5, fontweight="bold")
    ax.grid(alpha=0.3, color=GRID); ax.set_facecolor(PANEL)
    ax.set_xlim(0, XMAX); ax.set_ylim(0, YMAX)
    cb = fig.colorbar(sc, ax=ax, pad=0.02)
    cb.set_label("Hydraulic conductivity  $K$  ($\\times10^{-3}$ m/s)", color=INK)
    fig.savefig(out); plt.close(fig); print("saved", out)


# ----------------------------------------------------------------------
# Fig 5: ラグベース重回帰（MRA）  ★HYオリジナル手法
# ----------------------------------------------------------------------
def build_design(x, maxlag):
    n = len(x)
    cols = [np.ones(n - maxlag)]
    for m in range(maxlag + 1):
        cols.append(x[maxlag - m: n - m])
    return np.column_stack(cols)


def _aic(X, y):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    rss = float(np.sum((y - X @ beta) ** 2))
    n, k = X.shape
    return n * np.log(rss / n) + 2 * k, beta


def forward_select(lag_cols, y):
    """AIC による前進変数選択（論文の R `step` に相当）。多重共線性を抑える。"""
    n = len(y)
    ones = np.ones((n, 1))
    selected, remaining = [], list(range(len(lag_cols)))
    best_aic, _ = _aic(ones, y)
    while remaining:
        cand = None
        for r in remaining:
            X = np.column_stack([ones] + [lag_cols[i] for i in selected + [r]])
            a, _ = _aic(X, y)
            if a < best_aic - 1e-6 and (cand is None or a < cand[0]):
                cand = (a, r)
        if cand is None:
            break
        best_aic, r = cand
        selected.append(r)
        remaining.remove(r)
    return sorted(selected)


def fig_mra(out, tide, md3):
    tb, mb = bandpass(tide), bandpass(md3)
    n = len(tb)
    split = 24 * 300                       # 前300日で学習、残り65日で検証

    # --- AIC で最大ラグを選ぶ ---
    Ms, aics = list(range(0, 49)), []
    for M in Ms:
        X = build_design(tb, M); y = mb[M:]
        Xtr, ytr = X[:split], y[:split]
        beta, *_ = np.linalg.lstsq(Xtr, ytr, rcond=None)
        rss = np.sum((ytr - Xtr @ beta) ** 2)
        k = X.shape[1]
        aics.append(len(ytr) * np.log(rss / len(ytr)) + 2 * k)
    aics = np.array(aics)
    # AIC は n が大きいためラグを足すほど僅かに下がり続ける（最小値が端に来る）。
    # 実際には約1潮汐周期(12.4h)で改善が頭打ちになる＝帯水層が潮汐を覚えている長さ。
    # よって「肘」かつ物理的に意味のある M=12 h を採用する。
    Mbest = 12

    # --- 候補ラグ 0..Mbest から AIC 前進選択（多重共線性対策）---
    Xall = build_design(tb, Mbest); y = mb[Mbest:]
    lag_cols = [Xall[:, 1 + m] for m in range(Mbest + 1)]
    tr = slice(0, split)
    sel = forward_select([c[tr] for c in lag_cols], y[tr])
    print(f"  MRA: selected lags (h) = {sel}")

    ones = np.ones((len(y), 1))
    X = np.column_stack([ones] + [lag_cols[i] for i in sel])
    Xtr, ytr = X[:split], y[:split]
    Xte, yte = X[split:], y[split:]
    beta, *_ = np.linalg.lstsq(Xtr, ytr, rcond=None)
    pred = Xte @ beta
    ss_res = np.sum((yte - pred) ** 2)
    ss_tot = np.sum((yte - yte.mean()) ** 2)
    # R^2 は観測-計算のピアソン相関の二乗、NSE は Nash–Sutcliffe（別物）
    r2 = np.corrcoef(yte, pred)[0, 1] ** 2
    nse = 1 - ss_res / ss_tot
    rmse = np.sqrt(ss_res / len(yte))
    print(f"  MRA: best maxlag={Mbest} h, R2={r2:.3f}, NSE={nse:.3f}, RMSE={rmse:.4f} m")

    fig = plt.figure(figsize=(10.6, 7.4))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.1], hspace=0.42, wspace=0.26)

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(Ms, aics, "o-", color=PURPLE, lw=1.8, ms=4)
    aic_best = aics[Ms.index(Mbest)]
    ax1.plot([Mbest], [aic_best], "o", color=RED, ms=11, zorder=5)
    ax1.axvline(TAU_H, color=GRID, ls="--", lw=1.2)
    ax1.annotate(f"elbow at {Mbest} h\n= one M$_2$ cycle (12.4 h)",
                 xy=(Mbest, aic_best),
                 xytext=(Mbest + 7, aic_best + (aics.max()-aics.min())*0.26),
                 color=RED, fontsize=9, fontweight="bold",
                 arrowprops=dict(arrowstyle="->", color=RED))
    ax1.set_xlabel("Maximum lag (hours)", color=INK)
    ax1.set_ylabel("AIC", color=INK)
    ax1.set_title("(a)  AIC flattens after one tidal cycle", loc="left",
                  color=INK, fontsize=11, fontweight="bold")
    ax1.grid(alpha=0.3, color=GRID); ax1.set_facecolor(PANEL)

    ax2 = fig.add_subplot(gs[0, 1])
    coef = beta[1:]
    ax2.bar([str(m) for m in sel], coef, color=CYAN, edgecolor=NAVY, lw=0.6, width=0.65)
    ax2.axhline(0, color=INK, lw=0.8)
    ax2.set_xlabel("Selected lag of sea level (hours)", color=INK)
    ax2.set_ylabel("Partial regression coeff. $a_m$", color=INK)
    ax2.set_title(f"(b)  AIC forward selection keeps {len(sel)} lags",
                  loc="left", color=INK, fontsize=11, fontweight="bold")
    ax2.grid(alpha=0.3, color=GRID, axis="y"); ax2.set_facecolor(PANEL)

    ax3 = fig.add_subplot(gs[1, :])
    d = 24 * 6
    tt = np.arange(d) / 24.0
    ax3.plot(tt, yte[:d], "o", color=INK, ms=3.0, alpha=0.6, label="Observed (MD3)")
    ax3.plot(tt, pred[:d], "-", color=RED, lw=2.0, label="Reconstructed by lag-based MRA")
    ax3.set_xlabel("Time (days, validation period — never used for fitting)", color=INK)
    ax3.set_ylabel("Tidal-band groundwater level (m)", color=INK)
    ax3.set_title("(c)  Predicting groundwater level from the sea tide alone",
                  loc="left", color=INK, fontsize=11, fontweight="bold")
    ax3.legend(loc="upper right", fontsize=9, framealpha=0.9)
    ax3.grid(alpha=0.3, color=GRID); ax3.set_facecolor(PANEL)
    ax3.set_xlim(0, tt.max())
    ax3.text(0.012, 0.05, f"$R^2$ = {r2:.3f}    NSE = {nse:.3f}    RMSE = {rmse:.4f} m",
             transform=ax3.transAxes, fontsize=10.5, color=RED, fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=GRID))

    fig.savefig(out); plt.close(fig); print("saved", out)
    return Mbest, r2, nse, rmse


# ----------------------------------------------------------------------
if __name__ == "__main__":
    tide, w922, md3 = load()
    print(f"data: {len(tide)} hours ({len(tide)/24:.0f} days)")
    for name, y in [("922", w922), ("MD3", md3)]:
        A, _ = m2_amp_phase(y); At, _ = m2_amp_phase(tide)
        print(f"  {name}: M2 amp={A:.4f} m, A={A/At:.3f}")

    fig_two_wells(os.path.join(HERE, "two_wells.png"), tide, w922, md3)
    fig_xcorr_amp(os.path.join(HERE, "xcorr_amp.png"), tide, w922, md3)
    fig_ferris(os.path.join(HERE, "ferris.png"))
    fig_k_vs_distance(os.path.join(HERE, "k_vs_distance.png"))
    fig_mra(os.path.join(HERE, "mra.png"), tide, md3)
    print("ALL DONE")
