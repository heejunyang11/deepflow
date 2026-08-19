# -*- coding: utf-8 -*-
"""
Sci18 fig3 : The vessel that the magma built.
  (a) schematic section of a volcanic pile: lava flows with clinker and
      columnar joints, non-welded and welded pyroclastic flow deposits,
      a lava dome and a lahar deposit; the water table and the spring line.
  (b) hydraulic conductivity of the same units, on one logarithmic axis.
      Ranges are orders of magnitude from standard tables
      (Freeze & Cherry 1979 Table 2.2; Fetter 2001), not measurements
      from any single volcano.
Output: fig3_volcanic_aquifer.png
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import Polygon, Rectangle, FancyArrowPatch

rcParams['font.family'] = 'Times New Roman'
rcParams['mathtext.fontset'] = 'stix'
rcParams['axes.linewidth'] = 1.1

C_INK = '#333333'
C_HI = '#1a7a5e'        # permeable
C_LO = '#8c6d3f'        # tight
C_MID = '#c8871f'
C_WATER = '#2f7ec2'

fig = plt.figure(figsize=(11.69, 5.246))
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.10], wspace=0.45,
                      left=0.030, right=0.985, bottom=0.10, top=0.88)

# ============================================================== (a) the section
ax = fig.add_subplot(gs[0])
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.6)
ax.axis('off')

# basement
ax.add_patch(Rectangle((0.2, 0.35), 9.6, 0.75, facecolor='#b9b2a4',
                       edgecolor='#8a8172', lw=1.1))
ax.text(5.0, 0.72, 'basement', fontsize=11.6, color='#6d6455', ha='center',
        va='center')

# non-welded pyroclastic flow deposit (the big aquifer)
ax.add_patch(Rectangle((0.2, 1.10), 9.6, 1.05, facecolor='#f0e2c4',
                       edgecolor=C_HI, lw=1.4))
for x in np.arange(0.5, 9.7, 0.42):
    ax.plot([x, x + 0.16], [1.35, 1.55], color='#cbb98f', lw=0.8)
ax.text(2.6, 1.62, 'non-welded pyroclastic flow deposit',
        fontsize=11.8, color='#8a6c1f', ha='left', va='center')

# welded tuff (the tight one)
ax.add_patch(Rectangle((0.2, 2.15), 9.6, 0.52, facecolor='#c3b7a0',
                       edgecolor=C_LO, lw=1.4))
ax.text(2.6, 2.41, 'welded tuff', fontsize=11.8, color='#6d5326',
        ha='left', va='center')

# lava flow with clinker top and base
ax.add_patch(Rectangle((0.2, 2.67), 9.6, 0.92, facecolor='#a8a297',
                       edgecolor='#6f6a60', lw=1.3))
for yy in (2.74, 3.46):
    ax.add_patch(Rectangle((0.2, yy), 9.6, 0.13, facecolor='#e0d3ae',
                           edgecolor='none'))
for x in np.arange(0.45, 9.8, 0.34):          # columnar joints
    ax.plot([x, x], [2.88, 3.44], color='#6f6a60', lw=0.7, alpha=0.8)
ax.text(2.6, 3.13, 'lava flow — columnar joints', fontsize=11.8,
        color='#4f4a42', ha='left', va='center')
ax.annotate('clinker — the permeable\ntop and base of a lava flow',
            xy=(1.70, 3.52), xytext=(1.70, 4.72), fontsize=11.2,
            color='#8a6c1f', ha='left', va='center', linespacing=1.4,
            arrowprops=dict(arrowstyle='-', color='#8a6c1f', lw=1.0))

# lahar deposit
ax.add_patch(Polygon([(0.2, 3.59), (6.2, 3.59), (5.4, 4.10), (0.2, 4.10)],
                     facecolor='#b0a693', edgecolor=C_LO, lw=1.3))
ax.text(2.0, 3.86, 'lahar deposit', fontsize=11.6, color='#6d5326',
        ha='center', va='center')

# lava dome
ax.add_patch(Polygon([(6.3, 3.59), (7.2, 5.15), (8.4, 5.30), (9.4, 3.59)],
                     facecolor='#9b9187', edgecolor=C_LO, lw=1.4))
ax.text(7.85, 4.35, 'lava dome', fontsize=11.6, color='#3f3a34',
        ha='center', va='center')

# water table and springs
xw = np.linspace(0.2, 9.8, 200)
yw = 1.72 + 0.34 * (xw / 9.8) ** 1.5
ax.plot(xw, yw, color=C_WATER, lw=2.0, zorder=6)
ax.plot(0.55, yw[7], marker='v', ms=9, color=C_WATER, zorder=7)
ax.text(6.3, 2.02, 'water table', fontsize=11.6, color=C_WATER, va='bottom')
ax.add_patch(FancyArrowPatch((0.55, 1.68), (0.22, 1.30), arrowstyle='-|>',
                             mutation_scale=13, color=C_WATER, lw=1.8,
                             zorder=7))
ax.text(0.75, 1.22, 'spring line', fontsize=11.8, color=C_WATER,
        ha='left', va='center', zorder=7)

ax.text(0.0, 6.20, '(a)  what the eruptions stacked up', fontsize=15.4,
        color=C_INK, ha='left', va='center')
ax.text(0.0, 5.78,
        'welding, jointing and weathering decide the permeability —\n'
        'not the chemistry of the rock',
        fontsize=11.8, color='#777777', ha='left', va='top', linespacing=1.5)

# ================================================= (b) hydraulic conductivity
ax = fig.add_subplot(gs[1])

units = [
    ('clean sand  (for scale)',            1e-6, 1e-2, '#9aa3ad'),
    ('silt, clay  (for scale)',            1e-11, 1e-8, '#9aa3ad'),
    ('lava dome, massive andesite',        1e-11, 1e-8, C_LO),
    ('lahar / debris-flow deposit',        1e-9, 1e-6, C_LO),
    ('welded tuff  (unfractured)',         1e-10, 1e-7, C_LO),
    ('welded tuff  (fractured)',           1e-7, 1e-4, C_MID),
    ('non-welded pyroclastic flow',        1e-6, 1e-4, C_HI),
    ('basalt lava flow  (jointed)',        1e-6, 1e-2, C_HI),
]

ypos = np.arange(len(units))[::-1]
for y, (lab, lo, hi, col) in zip(ypos, units):
    ax.plot([np.log10(lo), np.log10(hi)], [y, y], color=col, lw=11,
            solid_capstyle='butt', alpha=0.85, zorder=3)
    ax.plot([np.log10(lo), np.log10(hi)], [y, y], color=col, lw=11,
            solid_capstyle='butt', alpha=0.0, zorder=3)

ax.set_yticks(ypos)
ax.set_yticklabels([u[0] for u in units], fontsize=12.2)
ax.set_ylim(-0.8, len(units) - 0.2)

ax.set_xlim(-12.2, -1.2)
ax.set_xticks(range(-12, -1))
ax.set_xticklabels([r'$10^{%d}$' % e for e in range(-12, -1)], fontsize=12.0)
ax.set_xlabel(r'hydraulic conductivity  $K$  (m s$^{-1}$)', fontsize=13.4)
ax.grid(axis='x', color='#dddddd', lw=0.8, zorder=0)
ax.set_axisbelow(True)
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)

ax.axhline(5.5, color='#bbbbbb', lw=0.9, ls=(0, (4, 3)))
ax.text(-1.35, 5.60, 'reference materials', fontsize=11.2,
        color='#999999', va='bottom', ha='right')
ax.text(-1.35, 5.32, 'volcanic units', fontsize=11.2,
        color='#999999', va='top', ha='right')

ax.set_title('(b)  ten orders of magnitude inside one volcano',
             fontsize=15.4, pad=12, loc='left')

fig.savefig('fig3_volcanic_aquifer.png', dpi=244, bbox_inches='tight',
            facecolor='white')
print('saved fig3_volcanic_aquifer.png')
