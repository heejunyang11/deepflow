# -*- coding: utf-8 -*-
"""
xwt_grinsted.py
Grinsted et al. (2004) の MATLAB "Crosswavelet and Wavelet Coherence Toolbox"
（xwt.m / ar1nv.m / ar1spectrum.m / Torrence-Compo wavelet.m）を
依存ライブラリなしで Python に忠実移植したもの。

- 2017年論文（Yang et al., Tonle Sap）と同じ設定:
    Morlet (k0=6), Dj=1/12, S0=2*dt, MaxScale auto, AR1 赤色雑音 5% 有意, COI, 位相矢印
- 位相→時間ラグ:  timelag = phase * period / (2*pi)   （xwttogetangle.m と同一）

使い方（実データ）:
    Wxy, period, coi, sig95, t = xwt(x, y, dt=1.0)
    plot_xwt(t, period, Wxy, coi, sig95, dt, out="xwt.png")
    lag = phase_to_timelag(Wxy, period, target_period=374)
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm


# ----------------------------------------------------------------------
# Torrence & Compo (1998) Morlet ウェーブレット変換
# ----------------------------------------------------------------------
def wavelet_morlet(Y, dt, pad=1, dj=1 / 12, s0=None, J1=None, k0=6.0):
    Y = np.asarray(Y, float)
    n1 = len(Y)
    if s0 is None:
        s0 = 2 * dt
    if J1 is None:
        J1 = int(round(np.log2(n1 * dt / s0) / dj))

    x = Y - Y.mean()
    if pad:
        base2 = int(np.fix(np.log(n1) / np.log(2) + 0.4999))
        x = np.concatenate([x, np.zeros(2 ** (base2 + 1) - n1)])
    n = len(x)

    # 波数 k [Torrence-Compo Eq.5]
    k = np.arange(1, n // 2 + 1) * (2 * np.pi / (n * dt))
    k = np.concatenate([[0.0], k, -k[(n - 1) // 2 - 1::-1]])

    f = np.fft.fft(x)
    scale = s0 * 2.0 ** (np.arange(J1 + 1) * dj)
    wave = np.zeros((J1 + 1, n), dtype=complex)

    for a1 in range(J1 + 1):
        s = scale[a1]
        expnt = -((s * k - k0) ** 2) / 2.0 * (k > 0)
        norm = np.sqrt(s * k[1]) * (np.pi ** -0.25) * np.sqrt(n)  # 全エネルギー=N
        daughter = norm * np.exp(expnt) * (k > 0)
        wave[a1, :] = np.fft.ifft(f * daughter)

    fourier_factor = (4 * np.pi) / (k0 + np.sqrt(2 + k0 ** 2))
    period = fourier_factor * scale
    coi = fourier_factor / np.sqrt(2)
    coi = coi * dt * np.concatenate([
        [1e-5], np.arange(1, (n1 + 1) // 2), np.arange(n1 // 2 - 1, 0, -1), [1e-5]])

    wave = wave[:, :n1]  # パディング除去
    return wave, period, scale, coi


# ----------------------------------------------------------------------
# AR(1) 推定（ar1nv.m）と赤色雑音スペクトル（ar1spectrum.m）
# ----------------------------------------------------------------------
def ar1nv(x):
    x = np.asarray(x, float)
    N = len(x)
    x = x - x.mean()
    c0 = x @ x / N
    c1 = x[:N - 1] @ x[1:] / (N - 1)
    g = c1 / c0
    a = np.sqrt((1 - g ** 2) * c0)
    return g, a


def ar1spectrum(ar1, period):
    freq = 1.0 / period
    return (1 - ar1 ** 2) / np.abs(1 - ar1 * np.exp(-2j * np.pi * freq)) ** 2


# ----------------------------------------------------------------------
# クロスウェーブレット変換（xwt.m）
# ----------------------------------------------------------------------
def xwt(x, y, dt=1.0, dj=1 / 12, s0=None, J1=None, k0=6.0, max_scale=None):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    n = len(x)
    if s0 is None:
        s0 = 2 * dt
    if J1 is None:
        if max_scale is None:
            max_scale = (n * 0.17) * 2 * dt          # xwt.m の auto MaxScale
        J1 = int(round(np.log2(max_scale / s0) / dj))

    X, period, scale, coix = wavelet_morlet(x, dt, 1, dj, s0, J1, k0)
    Y, period, scale, coiy = wavelet_morlet(y, dt, 1, dj, s0, J1, k0)
    coi = np.minimum(coix, coiy)

    Wxy = X * np.conj(Y)                              # クロス

    # 5% 有意水準（AR1 赤色雑音, V=2, Zv=3.9999）
    sigmax, sigmay = x.std(ddof=1), y.std(ddof=1)
    g1, _ = ar1nv(x)
    g2, _ = ar1nv(y)
    Pkx = ar1spectrum(g1, period / dt)
    Pky = ar1spectrum(g2, period / dt)
    V, Zv = 2.0, 3.9999
    signif = sigmax * sigmay * np.sqrt(Pkx * Pky) * Zv / V
    sig95 = np.abs(Wxy) / signif[:, None]            # >1 で有意
    t = np.arange(n) * dt
    return Wxy, period, scale, coi, sig95, t, (sigmax, sigmay)


# ----------------------------------------------------------------------
# 位相 → 時間ラグ（xwttogetangle.m / WT_timelagfromangle.m）
# ----------------------------------------------------------------------
def phase_to_timelag(Wxy, period, target_period):
    """target_period に最も近い周期帯で、位相角の円周平均から時間ラグを返す。

    符号の約束: 位相 = angle(X*conj(Y)) = (Xの位相) - (Yの位相)。
    xwt(x, y) で x が先行（y が遅れる）なら位相は正・ラグは正になる。
    引数を入れ替える（xwt(y, x)）と符号が反転する（物理結論は同じ）。
    例) 本記事 xwt(川,湖)=+39.7° / Yang et al.(2017) xwt(KL,PK)=-35.9°。
    MATLAB(Grinsted xwt.m)の angle(Wxy) と完全に同符号。
    """
    rowix = int(np.argmin(np.abs(period - target_period)))
    ang = np.angle(Wxy[rowix, :])
    # 円周平均
    mean_theta = np.angle(np.mean(np.exp(1j * ang)))
    timelag = mean_theta * period[rowix] / (2 * np.pi)
    return timelag, mean_theta, period[rowix]


# ----------------------------------------------------------------------
# 描画（2017論文 Fig.4 スタイル）
# ----------------------------------------------------------------------
def plot_xwt(t, period, Wxy, coi, sig95, dt, sigmas, out,
             title="Cross-wavelet transform", t_unit="years", t_scale=365.0,
             arrow_density=(28, 22), cmax=None, cmap="RdBu_r",
             n_levels=24, n_cbar_ticks=7):
    sigmax, sigmay = sigmas
    tt = t / t_scale
    power = np.log2(np.abs(Wxy) / (sigmax * sigmay))     # log2 正規化パワー
    logper = np.log2(period)

    # 色域：狭めにとって青(低)・赤(高)を飽和させ、コントラストを強調する
    if cmax is None:
        cmax = float(np.ceil(np.nanpercentile(np.abs(power), 90)))
        cmax = max(cmax, 3.0)
    print(f"[plot_xwt] power range = [{np.nanmin(power):.1f}, {np.nanmax(power):.1f}], "
          f"cmax(色域) = ±{cmax:.0f}")

    fig, ax = plt.subplots(figsize=(9.6, 5.4))
    norm = TwoSlopeNorm(vmin=-cmax, vcenter=0.0, vmax=cmax)
    levels = np.linspace(-cmax, cmax, n_levels + 1)       # 間隔を広めにとる
    cf = ax.contourf(tt, logper, np.clip(power, -cmax, cmax), levels=levels,
                     cmap=cmap, norm=norm, extend="both")

    # 5% 有意水準コンター（黒・太線）
    ax.contour(tt, logper, sig95, levels=[1], colors="k", linewidths=2)

    # 位相矢印（right=in-phase, left=anti-phase, down=series1 leads series2 by 90deg）
    aWxy = np.angle(Wxy)
    nt, npd = len(t), len(period)
    ti = np.arange(max(nt // arrow_density[0] // 2, 1), nt, max(nt // arrow_density[0], 1))
    pi_ = np.arange(max(npd // arrow_density[1] // 2, 1), npd, max(npd // arrow_density[1], 1))
    Tg, Pg = np.meshgrid(tt[ti], logper[pi_])
    U = np.cos(aWxy[np.ix_(pi_, ti)])
    Vv = -np.sin(aWxy[np.ix_(pi_, ti)])   # y軸反転に合わせ符号反転（画面上の向きをMATLABと一致）
    ax.quiver(Tg, Pg, U, Vv, angles="uv", color="k", scale=26,
              width=0.0032, headwidth=4, headlength=5, alpha=0.85)

    # COI（白半透明で塗りつぶし）
    coi_log = np.log2(np.clip(coi, period.min(), None))
    ax.fill_between(tt, coi_log, logper.max(), color="white", alpha=0.45, zorder=3)
    ax.plot(tt, coi_log, color="k", lw=1.0, ls="--", alpha=0.7, zorder=3)

    # y軸：周期（2のべき乗目盛・反転）
    yt = np.arange(np.floor(logper.min()), np.ceil(logper.max()) + 1)
    ax.set_yticks(yt)
    ax.set_yticklabels([f"{2 ** v:.0f}" for v in yt])
    ax.set_ylim(logper.max(), logper.min())
    ax.set_ylabel("Period (days)", color="#374151")
    ax.set_xlabel(f"Time ({t_unit})", color="#374151")
    ax.set_xlim(tt.min(), tt.max())
    ax.set_title(title, loc="left", color="#374151", fontsize=11, fontweight="bold")

    import matplotlib.ticker as mticker
    cb = fig.colorbar(cf, ax=ax, pad=0.02)
    cb.locator = mticker.MaxNLocator(nbins=n_cbar_ticks, integer=True)
    cb.update_ticks()
    cb.set_label("Cross-wavelet power  $\\log_2(|W^{XY}|/\\sigma_x\\sigma_y)$",
                 color="#374151")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("saved", out)


# ----------------------------------------------------------------------
# 記事図の再生成（合成データ。実データなら x,y,dt を差し替えるだけ）
# ----------------------------------------------------------------------
if __name__ == "__main__":
    import os
    from gen_figs import synth_levels

    t, mr, tsl, lag = synth_levels()
    dt = 1.0
    Wxy, period, scale, coi, sig95, tt, sigmas = xwt(mr, tsl, dt=dt)

    here = os.path.dirname(os.path.abspath(__file__))
    plot_xwt(tt, period, Wxy, coi, sig95, dt, sigmas,
             out=os.path.join(here, "cross_wavelet.png"),
             title="Cross-wavelet transform: Mekong River vs. Tonle Sap Lake")

    lag_days, theta, P = phase_to_timelag(Wxy, period, target_period=365)
    print(f"365-day band: mean phase = {np.degrees(theta):.1f} deg, "
          f"period = {P:.1f} d, time lag = {lag_days:.1f} days")
