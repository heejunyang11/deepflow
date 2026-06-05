"""
well_scale_plot.py
Generates a plot to visually explain the "Scale Gap" and Peaceman's Equivalent Well Radius.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# ===========================================================
# デザインシステム (Scientific Clean Style)
# ===========================================================
BG_COLOR    = '#F5F5F5'  
AXES_COLOR  = '#FCFCFC'  
TEXT_COLOR  = '#222222'  
TITLE_COLOR = '#111111'  
BLUE_MAIN   = '#1E64C8'  
BLUE_DARK   = '#144285'  
ORANGE      = '#D95F02'  
GRID_COLOR  = '#E0E0E0'  
SPINE_COLOR = '#555555'  

plt.rcParams.update({
    'font.family': 'Times New Roman',
    'axes.unicode_minus': False,
    'figure.facecolor': BG_COLOR,
    'axes.facecolor': AXES_COLOR,
    'text.color': TEXT_COLOR,
})

fig, ax = plt.subplots(figsize=(8, 8))

# 1セルを 100m x 100m と仮定
dx = 100.0
dy = 100.0

# 中心点
cx, cy = 0.0, 0.0

# 1. MODFLOWのセル (四角形)
rect = patches.Rectangle((cx - dx/2, cy - dy/2), dx, dy, 
                         linewidth=2, edgecolor=BLUE_MAIN, facecolor=BLUE_MAIN, alpha=0.1)
ax.add_patch(rect)
# セルの境界線
ax.plot([cx - dx/2, cx + dx/2, cx + dx/2, cx - dx/2, cx - dx/2],
        [cy - dy/2, cy - dy/2, cy + dy/2, cy + dy/2, cy - dy/2], 
        color=BLUE_MAIN, lw=2.5, linestyle='--', label='MODFLOW Cell (100m x 100m)')

# 2. 実際の井戸 (本来は r=0.15m だが、見えないので少し誇張)
r_w = 0.3 # 描画のために少し大きく
well = patches.Circle((cx, cy), r_w, linewidth=2, edgecolor='black', facecolor='black', zorder=5, label='Actual Well ($r_w$)')
ax.add_patch(well)

# 3. Peacemanの等価井戸半径 (r_e = 0.198 * dx)
r_e = 0.198 * dx
eq_well = patches.Circle((cx, cy), r_e, linewidth=2.5, edgecolor=ORANGE, facecolor='none', linestyle='-', zorder=4, label=r'Equivalent Well Radius ($r_e \approx 0.2 \Delta x$)')
ax.add_patch(eq_well)

# 中心点のマーク
ax.plot(cx, cy, marker='+', color='black', markersize=10, zorder=6)

# 注釈テキスト
ax.annotate(f'MODFLOW Cell\\n$\\Delta x = {int(dx)}$ m', xy=(-dx/2 + 5, dy/2 - 10), fontsize=14, color=BLUE_DARK, weight='bold')
ax.annotate(fr'Equivalent Well Radius\n$r_e \approx {r_e:.1f}$ m', xy=(r_e*0.7, r_e*0.7), xytext=(r_e + 10, r_e + 10),
            fontsize=14, color=ORANGE, weight='bold',
            arrowprops=dict(arrowstyle='->', color=ORANGE, lw=2))
ax.annotate('Actual Well\n(Too small to see!)', xy=(0, 0), xytext=(15, -15),
            fontsize=12, color='black', weight='bold',
            arrowprops=dict(arrowstyle='->', color='black', lw=2))

ax.set_aspect('equal')
ax.set_xlim(-60, 60)
ax.set_ylim(-60, 60)
ax.axis('off') # 枠線と軸メモリを消す

# 凡例
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.1), fontsize=13, frameon=False, ncol=1)

plt.title("The Scale Gap in Well Modeling", fontsize=18, color=TITLE_COLOR, pad=20, weight='bold')
plt.tight_layout()
plt.savefig('well_scale.png', dpi=300, bbox_inches='tight', facecolor=BG_COLOR)
plt.close()

print("[OK] Saved well_scale.png")
