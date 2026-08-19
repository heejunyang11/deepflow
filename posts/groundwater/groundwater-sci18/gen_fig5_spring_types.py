# -*- coding: utf-8 -*-
"""
Sci18 fig5 : One volcano, four kinds of hot spring.
  Volatiles leave the magma, and where they meet groundwater decides the
  water that comes out. The arrangement follows the seven-type scheme of
  Yasukawa & Noda (2017, J. Geotherm. Res. Soc. Japan 39, 203-215),
  in which reactive HCl-SO2-H2S are consumed near the centre and the
  poorly reactive CO2 survives to the margin (Deville's law).
Schematic; no vertical scale.
Output: fig5_spring_types.png
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Polygon, FancyArrowPatch, FancyBboxPatch

rcParams['font.family'] = 'Times New Roman'
rcParams['mathtext.fontset'] = 'stix'

C_ACID = '#b2182b'      # acid-sulfate, volcanic gas supply
C_CL = '#c8871f'        # neutral chloride, deep reservoir
C_SO4 = '#7b5aa6'       # steam heated
C_HCO3 = '#1a7a5e'      # CO2 supply
C_ROCK = '#c9c0ae'
C_CAP = '#8f8778'
C_MAGMA = '#8c2f2f'

fig, ax = plt.subplots(figsize=(10.984, 6.885))
ax.set_xlim(0, 14.4)
ax.set_ylim(-7.4, 8.3)
ax.axis('off')


def blob(cx, cy, rx, ry, n=120):
    t = np.linspace(0, 2 * np.pi, n)
    return np.column_stack([cx + rx * np.cos(t), cy + ry * np.sin(t)])


# ------------------------------------------------------------------ ground
ax.add_patch(Polygon([(0, 0), (14.4, 0), (14.4, -7.4), (0, -7.4)],
                     facecolor='#ded7c8', edgecolor='none', zorder=0))
ax.add_patch(Polygon([(3.1, 0), (7.0, 4.35), (10.9, 0)],
                     facecolor=C_ROCK, edgecolor='#8a8172', lw=1.3, zorder=1))
ax.plot([0, 14.4], [0, 0], color='#8a8172', lw=1.3, zorder=1)

# ------------------------------------------------------------------ magma
ax.add_patch(Polygon(blob(7.0, -6.5, 1.75, 0.80), facecolor='#d98b7d',
                     edgecolor=C_MAGMA, lw=1.5, zorder=2))
ax.text(7.0, -6.5, 'magma', fontsize=12.6, color='#7d2222', ha='center',
        va='center', zorder=3)

# ------------------------------------------------------------------ conduit
ax.add_patch(FancyArrowPatch((7.0, -5.6), (7.0, 4.15), arrowstyle='-|>',
                             mutation_scale=15, color=C_ACID, lw=2.4,
                             zorder=6, alpha=0.9))
ax.text(6.82, 1.12, 'high-temperature\nvolcanic gas\nHCl, SO$_2$, H$_2$S',
        fontsize=11.6, color=C_ACID, ha='right', va='center', zorder=7,
        linespacing=1.4)

# --------------------------------------------------- geothermal reservoir
ax.add_patch(Polygon(blob(7.0, -3.55, 2.85, 0.85), facecolor='#f3dfc0',
                     edgecolor=C_CL, lw=1.6, zorder=3))
ax.text(7.0, -3.55, 'geothermal reservoir  —  neutral Na–Cl brine',
        fontsize=12.0, color='#8f5f10', ha='center', va='center', zorder=4)
for xg in (6.1, 7.0, 7.9):
    ax.add_patch(FancyArrowPatch((xg, -5.55), (xg, -4.45), arrowstyle='-|>',
                                 mutation_scale=11, color=C_ACID, lw=1.5,
                                 zorder=3, alpha=0.75))
ax.text(3.55, -5.35,
        'the gas dissolves and reacts with the rock;\n'
        'the fluid ends up near neutral',
        fontsize=11.4, color='#8f5f10', ha='center', va='center', zorder=4,
        linespacing=1.4)

# ------------------------------------------------------------------ caprock
xc = np.linspace(3.9, 10.1, 60)
ax.add_patch(Polygon(np.vstack([np.column_stack([xc, -2.30 - 0.06 * (xc - 7) ** 2 / 4]),
                                np.column_stack([xc[::-1],
                                                 (-1.95 - 0.06 * (xc[::-1] - 7) ** 2 / 4)])]),
                     facecolor=C_CAP, edgecolor='#6f6a60', lw=1.2, zorder=4))
ax.text(3.30, -2.05, 'caprock', fontsize=12.0, color='#5a544a', ha='center',
        va='center', zorder=5, bbox=dict(facecolor='#ded7c8', edgecolor='none', pad=1.2))

# ---------------------------------------------------- 1. volcanic gas supply
ax.add_patch(FancyArrowPatch((6.90, 3.35), (5.62, 2.40), arrowstyle='-|>',
                             mutation_scale=12, color=C_ACID, lw=1.7, zorder=7,
                             connectionstyle='arc3,rad=0.25'))
ax.plot(5.45, 2.25, marker='o', ms=13, mfc='#f2c4c0', mec=C_ACID, mew=2.0,
        zorder=8)
ax.annotate('', xy=(3.45, 4.90), xytext=(5.30, 2.45), zorder=7,
            arrowprops=dict(arrowstyle='-', color=C_ACID, lw=0.9))
ax.add_patch(FancyBboxPatch((0.10, 4.55), 3.55, 1.75,
                            boxstyle='round,pad=0.06,rounding_size=0.12',
                            facecolor='#fbeeee', edgecolor=C_ACID, lw=1.4,
                            zorder=8))
ax.text(1.88, 5.43,
        'volcanic gas supply type\n'
        r'acid-sulfate water,  pH $<$ 3' '\n'
        r'Cl$^{-}$ > SO$_4^{2-}$',
        fontsize=12.0, color=C_ACID, ha='center', va='center', zorder=9,
        linespacing=1.55)

# ------------------------------------------------------------ 2. steam heated
for xs_ in (8.25, 8.65):
    ax.add_patch(FancyArrowPatch((xs_, -2.55), (xs_ + 0.32, -0.15),
                                 arrowstyle='-|>', mutation_scale=11,
                                 color=C_SO4, lw=1.6, zorder=6, alpha=0.85))
ax.text(9.40, -1.60, 'steam + H$_2$S', fontsize=11.6,
        color=C_SO4, ha='left', va='center', zorder=7,
        bbox=dict(facecolor='#ded7c8', edgecolor='none', pad=1.2))
ax.plot(9.05, 0.0, marker='o', ms=13, mfc='#e4dcf0', mec=C_SO4, mew=2.0,
        zorder=8)
ax.annotate('', xy=(9.70, 4.85), xytext=(9.12, 0.28), zorder=7,
            arrowprops=dict(arrowstyle='-', color=C_SO4, lw=0.9))
ax.add_patch(FancyBboxPatch((8.20, 4.90), 3.30, 1.75,
                            boxstyle='round,pad=0.06,rounding_size=0.12',
                            facecolor='#f1ecf8', edgecolor=C_SO4, lw=1.4,
                            zorder=8))
ax.text(9.85, 5.78,
        'steam heated type\n'
        r'SO$_4^{2-}$ water' '\n'
        'H$_2$S oxidised near the surface',
        fontsize=12.0, color=C_SO4, ha='center', va='center', zorder=9,
        linespacing=1.55)

# --------------------------------------- 3. identical / seepage thermal water
ax.add_patch(FancyArrowPatch((9.55, -3.30), (11.35, -0.12),
                             arrowstyle='-|>', mutation_scale=13, color=C_CL,
                             lw=2.2, zorder=6, connectionstyle='arc3,rad=-0.18'))
ax.plot([10.75, 10.75], [-4.6, 0.4], color='#6f6a60', lw=1.1, ls=(0, (5, 3)),
        zorder=5)
ax.text(10.75, -4.95, 'fault', fontsize=11.4, color='#6f6a60', ha='center',
        zorder=6)
ax.plot(11.45, 0.0, marker='o', ms=13, mfc='#f7e6c8', mec=C_CL, mew=2.0,
        zorder=8)
ax.annotate('', xy=(12.20, 2.25), xytext=(11.55, 0.28), zorder=7,
            arrowprops=dict(arrowstyle='-', color=C_CL, lw=0.9))
ax.add_patch(FancyBboxPatch((10.35, 2.30), 3.95, 1.75,
                            boxstyle='round,pad=0.06,rounding_size=0.12',
                            facecolor='#fdf3e2', edgecolor=C_CL, lw=1.4,
                            zorder=8))
ax.text(12.32, 3.18,
        'identical / seepage thermal water\n'
        r'neutral Na–Cl water' '\n'
        r'Cl$^{-}$ > 80 % of the anions, hot',
        fontsize=12.0, color='#8f5f10', ha='center', va='center', zorder=9,
        linespacing=1.55)

# ------------------------------------------------------------ 4. CO2 supply
ax.add_patch(FancyArrowPatch((4.15, -3.05), (2.05, -0.20), arrowstyle='-|>',
                             mutation_scale=13, color=C_HCO3, lw=2.0, zorder=6,
                             connectionstyle='arc3,rad=0.20'))
ax.text(1.55, -3.05, 'CO$_2$ survives\nto the margin', fontsize=11.6,
        color=C_HCO3, ha='center', va='center', zorder=7, linespacing=1.4)
ax.plot(1.95, 0.0, marker='o', ms=13, mfc='#dcefe7', mec=C_HCO3, mew=2.0,
        zorder=8)
ax.annotate('', xy=(1.95, 2.25), xytext=(1.95, 0.28), zorder=7,
            arrowprops=dict(arrowstyle='-', color=C_HCO3, lw=0.9))
ax.add_patch(FancyBboxPatch((0.10, 2.30), 3.55, 1.75,
                            boxstyle='round,pad=0.06,rounding_size=0.12',
                            facecolor='#e6f3ee', edgecolor=C_HCO3, lw=1.4,
                            zorder=8))
ax.text(1.88, 3.18,
        'CO$_2$ supply type\n'
        r'HCO$_3^{-}$ water' '\n'
        'near neutral, cooler',
        fontsize=12.0, color=C_HCO3, ha='center', va='center', zorder=9,
        linespacing=1.55)

# ------------------------------------------------------- Deville's law strip
y0 = 7.55
cmap = LinearSegmentedColormap.from_list(
    'deville', ['#1a7a5e', '#8bbf7d', '#f0d27a', '#e08a5a', '#b2182b'])
xg = np.linspace(1.0, 13.0, 400)
val = 1.0 - np.abs(xg - 7.0) / 6.0
ax.imshow(val.reshape(1, -1), extent=[1.0, 13.0, y0 - 0.19, y0 + 0.19],
          aspect='auto', cmap=cmap, vmin=0, vmax=1, alpha=0.85, zorder=2)
ax.text(7.0, y0 + 0.42, "Deville's law:  the reactive gases are consumed first",
        fontsize=13.0, color='#555555', ha='center', va='bottom', zorder=3)
ax.text(1.0, y0 - 0.46, r'margin — CO$_2$-rich', fontsize=11.8,
        color=C_HCO3, ha='left', va='top', zorder=3)
ax.text(7.0, y0 - 0.46, r'centre — HCl-, SO$_2$-, H$_2$S-rich', fontsize=11.8,
        color=C_ACID, ha='center', va='top', zorder=3)
ax.text(13.6, y0 - 0.46, r'margin — CO$_2$-rich', fontsize=11.8,
        color=C_HCO3, ha='right', va='top', zorder=3)

fig.savefig('fig5_spring_types.png', dpi=244, bbox_inches='tight',
            facecolor='white')
print('saved fig5_spring_types.png')
