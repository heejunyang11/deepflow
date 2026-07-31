# -*- coding: utf-8 -*-
"""Sci16 fig1 : detailed schematic of a magmatic geothermal system.
Independent redraw conveying the same textbook content as a standard
geothermal-system diagram (cf. Tsutsumi & Ishibashi 2022, Fig.1)."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import Polygon, Ellipse, FancyArrowPatch, Rectangle
from matplotlib.lines import Line2D
rcParams['font.family'] = 'Times New Roman'
rcParams['mathtext.fontset'] = 'stix'

fig, ax = plt.subplots(figsize=(11, 6.8))
x = np.linspace(0, 11, 700)
surf = 2.5 * np.exp(-((x - 3.0) / 1.5) ** 2) + 0.15
def sy(q): return float(np.interp(q, x, surf))

# sky, ground, basement
ax.fill_between(x, surf, 3.7, color='#eef4fb', zorder=0)
ax.fill_between(x, -5, surf, color='#e7dcc6', zorder=1)
ax.fill_between(x, -5, -3.2, color='#cfcfcf', zorder=1)
ax.plot(x, surf, color='#7a6a52', lw=1.4, zorder=3)
ax.plot([0, 11], [-3.2, -3.2], color='#9a9a9a', lw=0.8, zorder=1)
ax.text(0.25, -3.78, 'Basement rock', fontsize=13, color='#666666', style='italic')

# magma chamber
ax.add_patch(Ellipse((5.0, -4.35), 3.9, 1.35, facecolor='#e8791f',
                     edgecolor='#b4560c', lw=1.4, zorder=2))
ax.text(5.0, -4.4, 'Magma (heat source)', ha='center', va='center',
        fontsize=14, color='white', style='italic')
for ang in np.linspace(0.2, np.pi - 0.2, 6):
    x0, y0 = 5.0 + 2.0 * np.cos(ang), -4.35 + 0.72 * np.sin(ang)
    ax.add_patch(FancyArrowPatch((x0, y0), (x0 + 0.34 * np.cos(ang), y0 + 0.34 * np.sin(ang)),
                 arrowstyle='-|>', mutation_scale=9, color='#c0399b', lw=1.3, zorder=2))

# volcanic fluid (orange) rising from magma to reservoir
for xa in [4.4, 5.0, 5.6]:
    ax.add_patch(FancyArrowPatch((xa, -3.5), (xa + 0.08, -2.72),
                 connectionstyle='arc3,rad=0.12', arrowstyle='-|>',
                 mutation_scale=12, color='#e6772e', lw=1.9, zorder=3))
ax.text(3.72, -3.05, 'Volcanic\nfluid', fontsize=15, color='#111111',
        ha='center', fontweight='bold')

# caprock (right end shortened to 6.8 so upflow can pass around it)
ax.add_patch(Polygon([[3.7, -1.05], [6.8, -1.20], [6.8, -1.55], [3.7, -1.40]],
             closed=True, facecolor='#8d8676', edgecolor='#5f5a4d', lw=1.0, zorder=4))
ax.text(4.30, -0.82, 'Caprock', ha='center', fontsize=16, color='#111111',
        fontweight='bold')

# reservoir (stipple)
rng = np.random.default_rng(5)
rx = rng.uniform(3.95, 7.2, 260); ry = rng.uniform(-2.62, -1.62, 260)
ax.scatter(rx, ry, s=6, color='#d94801', alpha=0.72, zorder=4)
ax.text(5.25, -2.10, 'Geothermal reservoir', ha='center', fontsize=16,
        color='#111111', fontweight='bold', zorder=5)

# groundwater flow (blue): steep near the surface, gentle at depth
#   (potential gradient: rapid infiltration then near-horizontal deep flow)
ax.add_patch(FancyArrowPatch((1.95, sy(1.95) - 0.05), (3.95, -2.25),
             connectionstyle='angle3,angleA=-80,angleB=-8', arrowstyle='-|>',
             mutation_scale=13, color='#2f7fc0', lw=1.9, zorder=4))

# heated upflow (red): rises around the RIGHT EDGE of the caprock (no penetration)
ax.add_patch(FancyArrowPatch((6.85, -2.0), (7.15, sy(7.15) + 0.02),
             connectionstyle='arc3,rad=0.32', arrowstyle='-|>',
             mutation_scale=15, color='#c0392b', lw=2.1, zorder=4))

# infiltration arrows on slopes
for xa in [1.3, 1.9, 3.9, 4.5]:
    ax.add_patch(FancyArrowPatch((xa, sy(xa) + 0.55), (xa + 0.12, sy(xa) - 0.12),
                 arrowstyle='-|>', mutation_scale=11, color='#2166ac', lw=1.4, zorder=5))
ax.text(0.90, sy(1.3) + 0.90, 'Infiltration\n(meteoric water)', ha='center',
        fontsize=12, color='#1a4e86')

# rainfall clouds
for cx, cy in [(1.2, 2.75), (6.7, 2.95)]:
    for dx in [-0.34, 0.0, 0.34]:
        ax.add_patch(Ellipse((cx + dx, cy), 0.72, 0.44, facecolor='#c9d6e5',
                     edgecolor='none', zorder=5))
    for dx in np.linspace(-0.4, 0.4, 5):
        ax.plot([cx + dx, cx + dx - 0.1], [cy - 0.32, cy - 0.72],
                color='#7fa8d0', lw=1.0, zorder=5)
ax.text(1.2, 3.35, 'Rainfall', ha='center', fontsize=12, color='#3b6ea5')

# volcanic gas plume from summit
sx, syt = 3.0, sy(3.0)
rng2 = np.random.default_rng(2)
for i in range(75):
    t = i / 75.0
    gx = sx + 0.12 * np.sin(6 * t) + rng2.normal(0, 0.12)
    gy = syt + 0.15 + t * 1.30 + rng2.normal(0, 0.05)
    ax.add_patch(Ellipse((gx, gy), 0.36 - 0.15 * t, 0.30 - 0.11 * t,
                 facecolor='#8c8c8c', alpha=0.22, edgecolor='none', zorder=4))
ax.text(3.95, syt + 1.15, 'Volcanic gas', ha='left', fontsize=12, color='#555555')

# hot spring at the upflow location, with three curved steam plumes
xs = 7.15; ys = sy(xs)
ax.scatter([xs], [ys + 0.02], marker='v', s=95, color='#c0392b', zorder=6)
tt = np.linspace(0, 1, 24)
for i, dx in enumerate([-0.14, 0.0, 0.14]):
    wx = xs + dx + 0.06 * np.sin(4 * np.pi * tt + i)
    wy = ys + 0.10 + tt * 0.62
    ax.plot(wx, wy, color='#bdbdbd', lw=1.3, zorder=6)
ax.text(xs - 0.55, ys + 0.60, 'Hot springs', ha='center', fontsize=13, color='#7b241c')

# geothermal power plant (further right)
px = 9.0; py = sy(px)
ax.add_patch(Rectangle((px - 0.42, py), 0.84, 0.5, facecolor='#d8d8d8',
             edgecolor='#555555', lw=1.0, zorder=6))
ax.add_patch(Rectangle((px + 0.06, py + 0.5), 0.18, 0.34, facecolor='#bbbbbb',
             edgecolor='#555555', lw=0.8, zorder=6))
for dx in [-0.02, 0.06, 0.14]:
    ax.plot([px + 0.06 + dx, px + 0.06 + dx + 0.05], [py + 0.88, py + 1.28],
            color='#cfcfcf', lw=1.2, zorder=6)
ax.text(px - 0.70, py + 0.78, 'Geothermal\npower plant', ha='center', fontsize=12, color='#444444')

# legend (proxy)
handles = [
    Line2D([0], [0], color='#2f7fc0', lw=2.4, label='Groundwater'),
    Line2D([0], [0], color='#c0392b', lw=2.4, label='Hot water'),
    Line2D([0], [0], color='#e6772e', lw=2.4, label='Volcanic fluid'),
    Line2D([0], [0], color='#c0399b', lw=2.4, label='Conductive heat'),
]
leg = ax.legend(handles=handles, loc='upper right', fontsize=12, frameon=True,
                title='Legend', title_fontsize=12.5, borderpad=0.8)
leg.get_frame().set_edgecolor('#cccccc')

ax.set_xlim(0, 11); ax.set_ylim(-5, 4.2); ax.axis('off')
ax.set_title('A Magmatic Geothermal System', fontsize=16, pad=4)
plt.tight_layout()
plt.savefig('fig1_geothermal_system.png', dpi=220, facecolor='white')
print('saved fig1 (revised)')
