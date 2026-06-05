import numpy as np
import matplotlib.pyplot as plt

# ===========================================================
# デザインシステム (Scientific Clean Style)
# ===========================================================
BG_COLOR    = '#F5F5F5'  
AXES_COLOR  = '#FCFCFC'  
TEXT_COLOR  = '#222222'  
TITLE_COLOR = '#111111'  
BLUE_MAIN   = '#1E64C8'  
ORANGE      = '#D95F02'  
GRID_COLOR  = '#E0E0E0'  

plt.rcParams.update({
    'font.family': 'Times New Roman',
    'axes.unicode_minus': False,
    'figure.facecolor': BG_COLOR,
    'axes.facecolor': AXES_COLOR,
    'text.color': TEXT_COLOR,
})

# 変水位透水試験のパラメータ
h0 = 1.0        # 初期水位 (m)
L = 0.1         # 試料の長さ (m)
A = np.pi * (0.05)**2   # 試料の断面積 (半径5cm)
a = np.pi * (0.005)**2  # スタンドパイプの断面積 (半径0.5cm)

# 透水係数 K (m/s)
K_sand = 1e-4   # 砂 (透水性が高い)
K_silt = 1e-7   # シルト (透水性が低い)

# 時間 t (0 〜 600秒 = 10分)
t = np.linspace(0, 600, 200)

# 水位低下の計算式 h(t) = h0 * exp(- (K*A)/(a*L) * t)
def falling_head(K, t):
    alpha = (K * A) / (a * L)
    return h0 * np.exp(-alpha * t)

h_sand = falling_head(K_sand, t)
h_silt = falling_head(K_silt, t)

fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(t, h_sand, color=ORANGE, lw=3, label=f'Sand ($K = {K_sand}$ m/s)')
ax.plot(t, h_silt, color=BLUE_MAIN, lw=3, label=f'Silt ($K = {K_silt}$ m/s)')

ax.set_title('Falling-Head Permeability Test (Transient Flow)', fontsize=16, color=TITLE_COLOR, pad=15, weight='bold')
ax.set_xlabel('Time (seconds)', fontsize=14)
ax.set_ylabel('Water Head $h$ (m)', fontsize=14)
ax.set_xlim(0, 600)
ax.set_ylim(0, 1.05)
ax.grid(True, linestyle='--', color=GRID_COLOR)

ax.legend(fontsize=12, frameon=True, facecolor=AXES_COLOR, edgecolor=GRID_COLOR)

plt.tight_layout()
plt.savefig('falling_head_test.png', dpi=300, bbox_inches='tight', facecolor=BG_COLOR)
plt.close()

print("[OK] Saved falling_head_test.png")
