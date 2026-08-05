# -*- coding: utf-8 -*-
"""
Sci17 fig2 : What volumetric strain is, and why a well can feel it
  (a) one block of confined aquifer, undeformed / stretched / squeezed
      -> pore volume -> pore pressure -> water level in the standpipe
  (b) the quadrantal pattern of coseismic dilatation around a fault,
      and which way the level moves in each quadrant (schematic).
Output: fig2_strain.png
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import Rectangle, Ellipse, FancyArrow
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

rcParams['font.family'] = 'Times New Roman'
rcParams['mathtext.fontset'] = 'stix'
rcParams['axes.linewidth'] = 1.1

C_EXT = '#2166ac'      # extension  -> level falls
C_COM = '#b2182b'      # compression -> level rises
C_ROCK = '#d9d3c7'
C_WATER = '#4292c6'
C_INK = '#333333'

fig = plt.figure(figsize=(9.8, 10.6))
gs = fig.add_gridspec(2, 1, height_ratios=[0.60, 1.0], hspace=0.10,
                      left=0.045, right=0.965, bottom=0.045, top=0.945)

# ============================================================ (a) the block
ax = fig.add_subplot(gs[0])
ax.set_xlim(0, 5.45)
ax.set_ylim(-0.92, 2.94)
ax.axis('off')

Y0, HB, HC = 0.40, 0.62, 0.11          # block bottom, block height, cap height
TOP = Y0 + HB + HC                     # top of the confining layer
PIPE = 1.98                            # top of the standpipe
REF = 1.70                             # reference water level

cases = [
    (0.22, 1.00, 1.00, REF, 'Undeformed', r'$\Delta\varepsilon=0$', C_INK, None),
    (1.72, 1.14, 1.18, 1.42, 'Extension', r'$\Delta\varepsilon>0$', C_EXT, 'out'),
    (3.72, 0.88, 0.82, 1.90, 'Compression', r'$\Delta\varepsilon<0$', C_COM, 'in'),
]

for x0, wblk, pore, wlev, name, sym, col, pull in cases:
    ax.add_patch(Rectangle((x0, Y0), wblk, HB, facecolor=C_ROCK,
                           edgecolor='#8a8172', lw=1.3, zorder=2))
    for iy, yy in enumerate([Y0 + 0.15, Y0 + 0.31, Y0 + 0.47]):
        n = 4
        for ix in range(n):
            xx = x0 + wblk * (ix + 0.5 + 0.5 * (iy % 2)) / (n + 0.5)
            if xx > x0 + wblk - 0.07:
                continue
            ax.add_patch(Ellipse((xx, yy), 0.105 * pore, 0.072 * pore,
                                 facecolor=C_WATER, edgecolor='none',
                                 alpha=0.9, zorder=3))
    ax.add_patch(Rectangle((x0, Y0 + HB), wblk, HC, facecolor='#9c9384',
                           edgecolor='#7d7466', lw=1.0, zorder=2))

    xc = x0 + wblk / 2
    ax.add_patch(Rectangle((xc - 0.05, TOP), 0.10, PIPE - TOP, facecolor='white',
                           edgecolor='#555555', lw=1.2, zorder=4))
    ax.add_patch(Rectangle((xc - 0.05, TOP), 0.10, wlev - TOP,
                           facecolor=C_WATER, edgecolor='none', zorder=5))
    ax.plot([xc - 0.05, xc + 0.05], [wlev, wlev], color=col, lw=2.4, zorder=6)

    ax.text(xc, 0.21, name, ha='center', fontsize=16.2, color=col)
    ax.text(xc, -0.05, sym, ha='center', fontsize=16.2, color=col)

    # strain arrows, well clear of the neighbouring block
    if pull == 'out':
        ax.annotate('', xy=(x0 - 0.24, Y0 + 0.31), xytext=(x0 - 0.06, Y0 + 0.31),
                    arrowprops=dict(arrowstyle='->', color=col, lw=2.0))
        ax.annotate('', xy=(x0 + wblk + 0.24, Y0 + 0.31),
                    xytext=(x0 + wblk + 0.06, Y0 + 0.31),
                    arrowprops=dict(arrowstyle='->', color=col, lw=2.0))
    elif pull == 'in':
        ax.annotate('', xy=(x0 - 0.06, Y0 + 0.31), xytext=(x0 - 0.24, Y0 + 0.31),
                    arrowprops=dict(arrowstyle='->', color=col, lw=2.0))
        ax.annotate('', xy=(x0 + wblk + 0.06, Y0 + 0.31),
                    xytext=(x0 + wblk + 0.24, Y0 + 0.31),
                    arrowprops=dict(arrowstyle='->', color=col, lw=2.0))

# reference level across all three
ax.plot([0.30, 4.66], [REF, REF], color='#999999', lw=0.9, ls=':', zorder=1)
ax.text(1.05, REF + 0.05, 'reference level', fontsize=12.3, color='#777777',
        va='bottom')

# level-change arrows and their labels, offset clear of the standpipe
ax.annotate('', xy=(2.44, 1.44), xytext=(2.44, REF - 0.02), zorder=7,
            arrowprops=dict(arrowstyle='->', color=C_EXT, lw=1.7))
ax.text(2.52, 1.56, 'level falls', fontsize=13.7, color=C_EXT, va='center')
ax.annotate('', xy=(4.31, 1.88), xytext=(4.31, REF + 0.02), zorder=7,
            arrowprops=dict(arrowstyle='->', color=C_COM, lw=1.7))
ax.text(4.39, 1.82, 'level rises', fontsize=13.7, color=C_COM, va='center')

ax.text(0.10, 2.76,
        r'$\Delta\varepsilon=\dfrac{\Delta V}{V}$ — the fractional change in volume, '
        'a pure number.',
        fontsize=16.2, color=C_INK)
ax.text(0.10, 2.34,
        r'$10^{-8}$ of strain stretches a block of rock 1 km long by 0.01 mm.',
        fontsize=14.3, color='#777777')
ax.text(0.10, -0.40,
        'Stretch the rock and its pores open: the same water now fills\n'
        'a larger space, so the pressure — and the level — falls.',
        fontsize=13.7, color='#555555', va='top', linespacing=1.6)
ax.set_title('(a) Strain the rock, and the pore water answers',
             fontsize=16.9, pad=6)

# ========================================================= (b) the quadrants
ax = fig.add_subplot(gs[1])
n = 420
g = np.linspace(-1, 1, n)
X, Y = np.meshgrid(g, g)
R = np.hypot(X, Y)
TH = np.arctan2(Y, X)
E = -np.sin(2 * TH) * np.exp(-(R / 0.55) ** 2)

cmap = LinearSegmentedColormap.from_list(
    'strain', [C_COM, '#e8e6e3', C_EXT])
cf = ax.contourf(X, Y, E, levels=np.linspace(-1, 1, 21),
                 cmap=cmap, norm=TwoSlopeNorm(0, -1, 1))

# the fault
ax.plot([-0.62, 0.62], [0, 0], color='#111111', lw=2.6, solid_capstyle='round',
        zorder=5)
ax.annotate('', xy=(0.30, 0.075), xytext=(-0.05, 0.075),
            arrowprops=dict(arrowstyle='->', color='#111111', lw=1.6))
ax.annotate('', xy=(-0.30, -0.075), xytext=(0.05, -0.075),
            arrowprops=dict(arrowstyle='->', color='#111111', lw=1.6))
ax.text(0.0, 0.16, 'fault', fontsize=14.3, ha='center', color='#111111')

# two wells
for (wx, wy), col, lab, dy in [((-0.42, 0.42), C_EXT, 'level falls', -0.14),
                               ((0.42, 0.42), C_COM, 'level rises', 0.14)]:
    ax.plot(wx, wy, marker='o', ms=9, mfc='white', mec=col, mew=2.2, zorder=6)
    ax.annotate('', xy=(wx, wy + dy), xytext=(wx, wy),
                arrowprops=dict(arrowstyle='->', color=col, lw=2.0))
    ax.text(wx, wy + (0.20 if dy > 0 else -0.30), lab, ha='center',
            fontsize=13.7, color=col)

ax.text(-0.93, 0.86, 'extension', fontsize=14.3, color=C_EXT)
ax.text(0.93, 0.86, 'compression', fontsize=14.3, color=C_COM, ha='right')
ax.text(-0.93, -0.92, 'compression', fontsize=14.3, color=C_COM)
ax.text(0.93, -0.92, 'extension', fontsize=14.3, color=C_EXT, ha='right')

ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])
ax.set_title('(b) Where the well sits decides the sign', fontsize=16.9, pad=6)

cb = fig.colorbar(cf, ax=ax, orientation='horizontal', fraction=0.052,
                  pad=0.045, ticks=[-1, 0, 1])
cb.ax.set_xticklabels(['compression', '0', 'extension'], fontsize=13.0)
cb.set_label(r'coseismic volumetric strain $\Delta\varepsilon$  (schematic)',
             fontsize=13.7)
cb.outline.set_linewidth(0.8)

fig.savefig('fig2_strain.png', dpi=200, bbox_inches='tight')
print('saved fig2_strain.png')
