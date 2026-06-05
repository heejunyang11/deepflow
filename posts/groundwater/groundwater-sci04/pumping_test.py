"""
pumping_test.py
Generates the plots for DeepFlows Groundwater Series #4 (Pumping Tests).
Uses the Theis well function to show:
1. Cone of Depression (Drawdown vs Distance)
2. Cooper-Jacob Method (Drawdown vs Time on Semi-log plot)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import exp1

# ===========================================================
# デザインシステム (Scientific Clean Style)
# ===========================================================
BG_COLOR    = '#F5F5F5'  # Slightly grayish background for the figure
AXES_COLOR  = '#FCFCFC'  # Almost white/very light gray for the plot area
TEXT_COLOR  = '#222222'  # Dark gray for text
TITLE_COLOR = '#111111'  # Almost black for titles
BLUE_MAIN   = '#1E64C8'  # Classic scientific blue
BLUE_DARK   = '#144285'  # Dark blue
ORANGE      = '#D95F02'  # Classic scientific orange
GRID_COLOR  = '#E0E0E0'  # Light gray for grid
SPINE_COLOR = '#555555'  # Gray for axes border

plt.rcParams.update({
    'font.family': 'Times New Roman',
    'axes.unicode_minus': False,
    'figure.facecolor': BG_COLOR,
    'axes.facecolor': AXES_COLOR,
    'text.color': TEXT_COLOR,
    'axes.labelcolor': TEXT_COLOR,
    'xtick.color': TEXT_COLOR,
    'ytick.color': TEXT_COLOR,
})

# ===========================================================
# 1. 揚水試験モデルのパラメータ定義
# ===========================================================
Q = 1000.0   # 揚水量 (m3/day)
T = 200.0    # 透水量係数 (m2/day)
S = 0.001    # 貯留係数 (-)

def theis_drawdown(r, t, Q, T, S):
    """Theis公式に基づく水位低下量の計算"""
    u = (r**2 * S) / (4.0 * T * t)
    s = (Q / (4.0 * np.pi * T)) * exp1(u)
    return s

# ===========================================================
# 2. プロット作成
# ===========================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# -----------------------------------------------------------
# [Panel 1] 水位低下錐 (Cone of Depression)
# -----------------------------------------------------------
r_array = np.linspace(0.1, 500, 500) # 距離 0.1m から 500m
t_days = [0.1, 1.0, 10.0]            # 3つの経過時間 (day)

line_styles = ['dotted', 'dashed', 'solid']
alphas = [0.6, 0.8, 1.0]

for t, ls, al in zip(t_days, line_styles, alphas):
    s_spatial = theis_drawdown(r_array, t, Q, T, S)
    ax1.plot(
        r_array, s_spatial,
        color=BLUE_MAIN, linestyle=ls, linewidth=2.0, alpha=al,
        label=f'Time: {t} days'
    )

ax1.set_title('Cone of Depression (Spatial Drawdown)', fontsize=16, color=TITLE_COLOR, pad=12)
ax1.set_xlabel('Distance from well, r [m]', fontsize=14, labelpad=8)
ax1.set_ylabel('Drawdown, s [m]', fontsize=14, labelpad=8)
ax1.set_xlim(0, 500)
ax1.set_ylim(0, 4.0)
ax1.invert_yaxis() # 水位低下なので下向きを正にする直感的な表現

# -----------------------------------------------------------
# [Panel 2] Jacobの直線図法 (Jacob Method)
# -----------------------------------------------------------
# 観測井における架空のデータセットを生成
r_obs = 30.0 # 観測井までの距離 30m
t_times = np.logspace(-3, 1, 50) # 0.001 day to 10 days
s_time = theis_drawdown(r_obs, t_times, Q, T, S)

# ノイズを少し付加して「架空の実測データ」っぽくする
np.random.seed(42)
noise = np.random.normal(0, 0.02, size=len(s_time))
s_noisy = s_time + noise

# 実測データのプロット
ax2.semilogx(
    t_times, s_noisy,
    marker='o', color=BLUE_MAIN, linestyle='None',
    markersize=5, alpha=0.7, label='Observation Data'
)

# Jacob近似直線のフィッティング (u < 0.01 となる後半部分のデータを使用)
# u = r^2 * S / (4 * T * t). u < 0.01 means t > r^2 * S / (0.04 * T)
t_crit = (r_obs**2 * S) / (0.04 * T)
valid_idx = np.where(t_times > t_crit)[0]

if len(valid_idx) > 2:
    # 最小二乗法で直線を当てはめる
    log_t_valid = np.log10(t_times[valid_idx])
    s_valid = s_noisy[valid_idx]
    coeffs = np.polyfit(log_t_valid, s_valid, 1)
    
    # 近似直線をプロット
    t_fit = np.logspace(np.log10(t_crit), 1, 100)
    s_fit = coeffs[0] * np.log10(t_fit) + coeffs[1]
    
    # 直線を延長して t0 (s=0) を求める
    t0 = 10**(-coeffs[1] / coeffs[0])
    t_extrapolate = np.logspace(np.log10(t0), 1, 100)
    s_extrapolate = coeffs[0] * np.log10(t_extrapolate) + coeffs[1]
    
    ax2.semilogx(
        t_extrapolate, s_extrapolate,
        color=ORANGE, linestyle='-', linewidth=2.0, zorder=4,
        label='Jacob Straight-Line Fit'
    )
    
    # t0 の点を強調
    ax2.plot([t0], [0], marker='s', color=TITLE_COLOR, markersize=7, zorder=5)
    ax2.annotate(
        f'$t_0$ = {t0:.3f} d', xy=(t0, 0), xytext=(t0*1.5, -0.3),
        fontsize=12, color=TEXT_COLOR,
        arrowprops=dict(arrowstyle='->', color=TEXT_COLOR, lw=1.2)
    )
    
    # 1対数サイクルあたりの低下量 Δs を注釈
    delta_s = coeffs[0]
    # Estimate T and S using Jacob's formula
    T_est = (2.303 * Q) / (4 * np.pi * delta_s)
    S_est = (2.25 * T_est * t0) / (r_obs**2)
    
    text_str = f"Estimated Parameters:\n$T$ = {T_est:.1f} $\\mathrm{{m^2/d}}$\n$S$ = {S_est:.2e}"
    ax2.text(
        0.05, 0.2, text_str, transform=ax2.transAxes,
        fontsize=12, bbox=dict(facecolor='white', edgecolor=SPINE_COLOR, alpha=0.9, pad=10)
    )

ax2.set_title('Cooper-Jacob Method (Drawdown vs Time)', fontsize=16, color=TITLE_COLOR, pad=12)
ax2.set_xlabel('Time, t [days] (Log Scale)', fontsize=14, labelpad=8)
ax2.set_ylabel('Drawdown, s [m]', fontsize=14, labelpad=8)
ax2.set_xlim(1e-3, 10)
ax2.set_ylim(-0.5, 3.5)
ax2.invert_yaxis()

# ===========================================================
# 共通の修飾 (グリッド、枠線、凡例など)
# ===========================================================
for ax in [ax1, ax2]:
    ax.legend(fontsize=12, facecolor='white', framealpha=1.0, edgecolor='#CCCCCC', loc='lower right' if ax == ax1 else 'upper right')
    ax.grid(axis='both', alpha=0.6, color=GRID_COLOR, linestyle=':', linewidth=1.5, zorder=0)
    # マイナーグリッドも追加 (x軸が対数のため)
    ax.grid(axis='x', which='minor', alpha=0.3, color=GRID_COLOR, linestyle=':', linewidth=1.0, zorder=0)
    
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color(SPINE_COLOR)
        spine.set_linewidth(1.8)
    
    ax.tick_params(labelsize=12, color=SPINE_COLOR, direction='out', which='both')
    ax.tick_params(which='major', length=6, width=1.5)
    ax.tick_params(which='minor', length=4, width=1.0)

plt.tight_layout()
plt.savefig('pumping_test_analysis.png', dpi=300, bbox_inches='tight', facecolor=BG_COLOR)
plt.close()
print("[OK] Saved pumping_test_analysis.png")
