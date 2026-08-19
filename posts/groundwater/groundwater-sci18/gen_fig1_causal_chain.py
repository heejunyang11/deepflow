# -*- coding: utf-8 -*-
"""
Sci18 fig1 : The causal chain of this article.
  SiO2 content of the magma
    -> viscosity -> eruption style -> shape of the rock body -> aquifer
    -> rock-forming minerals -> what weathering releases -> water chemistry
    -> volatiles -> hydrothermal chemistry -> hot spring type
Output: fig1_causal_chain.png
"""
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

rcParams['font.family'] = 'Times New Roman'
rcParams['mathtext.fontset'] = 'stix'

C_INK = '#333333'
C_SRC = '#5b4a8a'          # the single source box
C_BR = ['#2166ac', '#1a7a5e', '#b2182b']   # physics / minerals / volatiles
C_FILL = ['#e7eff7', '#e4f0ea', '#f8e8e6']
C_OUT = '#f3f1ec'

fig, ax = plt.subplots(figsize=(10.861, 6.557))
ax.set_xlim(0, 13.25)
ax.set_ylim(0, 8.0)
ax.axis('off')


def box(x, y, w, h, text, fc, ec, fs=12.6, lw=1.3, tc=None, weight='normal'):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle='round,pad=0.045,rounding_size=0.09',
                                facecolor=fc, edgecolor=ec, lw=lw, zorder=3))
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center',
            fontsize=fs, color=tc if tc else C_INK, zorder=4,
            linespacing=1.35, fontweight=weight)


def arrow(x0, y0, x1, y1, col, lw=1.7, rad=0.0):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1),
                                 arrowstyle='-|>', mutation_scale=15,
                                 color=col, lw=lw, zorder=2,
                                 connectionstyle='arc3,rad=%.2f' % rad))


# ------------------------------------------------------------------ source
box(0.15, 3.05, 2.05, 1.30,
    'SiO$_2$ content\nof the magma\n\n45 – 77 wt %',
    '#efeaf7', C_SRC, fs=14.0, lw=2.0, tc=C_SRC, weight='bold')

# ------------------------------------------------------------------ rows
ROW_Y = [5.45, 3.30, 1.15]      # top / middle / bottom band bottom-left y
BH = 1.10                        # box height
XS = [2.69, 5.34, 7.99]          # x of the three chained boxes
BW = 2.32

rows = [
    (0, [r'polymerisation' '\n' r'$\rightarrow$ viscosity',
         'eruption style\n(effusive / explosive)',
         'geometry of the\nvolcanic rock body'],
     'THE VESSEL\naquifer permeability',
     'picks up  #2, #3'),
    (1, ['rock-forming\nminerals',
         'what weathering\nreleases',
         'ions delivered to\nthe groundwater'],
     'THE SOLUTES\nwater chemistry type',
     'picks up  #11, #12'),
    (2, ['dissolved volatiles\nH$_2$O, CO$_2$, SO$_2$, HCl',
         'degassing and\nseparation',
         'chemistry of the\nhydrothermal fluid'],
     'THE SPRING\nhot spring type',
     'picks up  #16'),
]

for i, (k, chain, out, cite) in enumerate(rows):
    y = ROW_Y[i]
    col, fill = C_BR[i], C_FILL[i]
    # from the source into the first box of the row
    arrow(2.20, 3.70, XS[0] - 0.09, y + BH / 2, col, lw=2.0,
          rad=0.0 if i == 1 else (-0.16 if i == 0 else 0.16))
    for j, t in enumerate(chain):
        box(XS[j], y, BW, BH, t, fill, col, fs=12.2)
        if j < len(chain) - 1:
            arrow(XS[j] + BW + 0.09, y + BH / 2, XS[j + 1] - 0.09, y + BH / 2, col)
    arrow(XS[2] + BW + 0.09, y + BH / 2, 10.64, y + BH / 2, col, lw=2.0)
    box(10.64, y, 2.50, BH, out, C_OUT, col, fs=12.6, lw=1.8, tc=col,
        weight='bold')
    ax.text(11.89, y - 0.24, cite, ha='center', va='center',
            fontsize=11.2, color='#8a8a8a', style='italic')

# ------------------------------------------------------------------ titles
ax.text(0.15, 7.62,
        'One number decides three things',
        fontsize=18.5, color=C_INK)
ax.text(0.15, 7.18,
        'How much silica the magma carries fixes the vessel, the solutes and the spring.',
        fontsize=13.2, color='#777777')

ax.text(1.18, 2.62, 'basalt   45–52 %', ha='center', fontsize=11.6, color='#777777')
ax.text(1.18, 2.32, 'andesite  52–63 %', ha='center', fontsize=11.6, color='#777777')
ax.text(1.18, 2.02, 'rhyolite  68–77 %', ha='center', fontsize=11.6, color='#777777')

fig.savefig('fig1_causal_chain.png', dpi=244, bbox_inches='tight',
            facecolor='white')
print('saved fig1_causal_chain.png')
