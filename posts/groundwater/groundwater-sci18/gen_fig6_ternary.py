# -*- coding: utf-8 -*-
"""
Sci18 fig6 : Cl - SO4 - HCO3 ternary diagram (Giggenbach 1991).
  Weight basis (mg/L), as in the original and as used by Rafiq et al. (2024).
  Data, all from published papers:
    - Quaternary volcanic area, Hokkaido: Shigeno (2011), Bull. Geol. Surv.
      Japan 62(3/4), 143-176, Table 3
    - Shiraoi area deep waters (same table), for contrast
    - Ain Al-Harrah, Saudi Arabia: Rafiq et al. (2024) ACS Omega 9, 24807,
      Table 2
Companion of the Na-K-Mg diagram used in #16.
Output: fig6_ternary.png
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import Polygon

rcParams['font.family'] = 'Times New Roman'
rcParams['mathtext.fontset'] = 'stix'
rcParams['axes.linewidth'] = 1.2

S3 = np.sqrt(3.0) / 2.0
V_CL = np.array([0.0, 0.0])          # bottom-left
V_HCO3 = np.array([1.0, 0.0])        # bottom-right
V_SO4 = np.array([0.5, S3])          # top


def tern(cl, so4, hco3):
    cl = np.asarray(cl, float)
    so4 = np.asarray(so4, float)
    hco3 = np.asarray(hco3, float)
    tot = cl + so4 + hco3
    f_cl, f_so4, f_hco3 = cl / tot, so4 / tot, hco3 / tot
    x = f_cl * V_CL[0] + f_hco3 * V_HCO3[0] + f_so4 * V_SO4[0]
    y = f_so4 * V_SO4[1]
    return x, y


# ------------------------------------------------------------------ data
# (label, marker, colour, [(Cl, SO4, HCO3), ...])
SETS = [
    ('Noboribetsu  (Shigeno 2011)', 'o', '#b2182b',
     [(2942.9, 48.6, 132.4), (6155.3, 42.0, 48.8), (5850.4, 144.0, 4.6)]),
    ('Kitayuzawa', 's', '#d6604d',
     [(173.0, 233.9, 45.8), (177.3, 235.4, 32.7)]),
    ('Karurusu', 'D', '#7b5aa6',
     [(52.1, 202.7, 157.1)]),
    ('Kawamata', '^', '#4a3480',
     [(7.1, 1073.4, 10.7)]),
    ('NW shore of Lake Shikotsu', 'v', '#1a7a5e',
     [(356.3, 260.1, 349.3), (282.6, 227.6, 254.8)]),
    ('Shiraoi area, deep waters', 'h', '#8a8a8a',
     [(950.3, 2.9, 225.8), (147.2, 0.0, 1373.0),
      (416.7, 0.5, 381.4), (397.2, 40.5, 197.4)]),
    ('Ain Al-Harrah, Saudi Arabia\n(Rafiq et al. 2024)', 'P', '#2166ac',
     [(538.52, 433.39, 71.06), (472.76, 376.71, 64.48),
      (486.96, 387.89, 89.99), (557.76, 436.70, 89.04),
      (581.95, 455.79, 84.40)]),
]

fig, ax = plt.subplots(figsize=(7.869, 7.049))
ax.set_aspect('equal')
ax.axis('off')

tri = np.array([V_CL, V_HCO3, V_SO4, V_CL])
ax.fill(tri[:, 0], tri[:, 1], color='#f8f9fa', zorder=0)

# ------------------------------------------------------------ corner fields
def corner(apex, a, b, frac, colour, alpha):
    """triangle occupying the corner at `apex`, up to `frac` along both edges"""
    p1 = apex + (a - apex) * frac
    p2 = apex + (b - apex) * frac
    ax.add_patch(Polygon([apex, p1, p2], facecolor=colour, edgecolor='none',
                         alpha=alpha, zorder=1))


corner(V_SO4, V_CL, V_HCO3, 0.42, '#c9b7e0', 0.45)
corner(V_CL, V_SO4, V_HCO3, 0.34, '#f0c0b8', 0.50)
corner(V_HCO3, V_SO4, V_CL, 0.34, '#bfe0d2', 0.50)

ax.text(0.500, 0.620, 'volcanic /\nsteam-heated', ha='center',
        va='center', fontsize=11.8, color='#5b4a8a', style='italic',
        linespacing=1.35, zorder=3)
ax.text(0.150, 0.108, 'mature waters', ha='left', va='center', fontsize=12.2,
        color='#9c3535', style='italic', zorder=3)
ax.text(0.850, 0.108, 'peripheral waters', ha='right', va='center',
        fontsize=12.2, color='#15654e', style='italic', zorder=3)
ax.text(0.645, 0.330, 'mixing and dilution', ha='center', va='center',
        fontsize=11.8, color='#9a9a9a', style='italic', zorder=3)

# ------------------------------------------------------------ grid + border
for f in (0.2, 0.4, 0.6, 0.8):
    for (A, B, C) in ((V_CL, V_SO4, V_HCO3), (V_SO4, V_HCO3, V_CL),
                      (V_HCO3, V_CL, V_SO4)):
        p = A + (B - A) * f
        q = A + (C - A) * f
        ax.plot([p[0], q[0]], [p[1], q[1]], color='#dcdcdc', lw=0.7, zorder=2)
ax.plot(tri[:, 0], tri[:, 1], color='#2b2b2b', lw=1.6, zorder=6)

# ------------------------------------------------------------------ data
for lab, mk, col, pts in SETS:
    cl = [p[0] for p in pts]
    so4 = [p[1] for p in pts]
    hco3 = [p[2] for p in pts]
    x, y = tern(cl, so4, hco3)
    ax.plot(x, y, mk, ms=11, mfc=col, mec='#2b2b2b', mew=0.9, ls='none',
            alpha=0.92, label=lab, zorder=8)

# ------------------------------------------------------------------ labels
ax.text(V_SO4[0], V_SO4[1] + 0.040, r'SO$_4^{2-}$', ha='center', va='bottom',
        fontsize=17)
ax.text(V_CL[0] - 0.030, V_CL[1] - 0.028, r'Cl$^{-}$', ha='center', va='top',
        fontsize=17)
ax.text(V_HCO3[0] + 0.030, V_HCO3[1] - 0.028, r'HCO$_3^{-}$', ha='center',
        va='top', fontsize=17)

leg = ax.legend(loc='upper left', bbox_to_anchor=(0.64, 0.99), frameon=True,
                fontsize=11.4, handletextpad=0.5, borderpad=0.8,
                labelspacing=0.75)
leg.get_frame().set_edgecolor('#cccccc')
leg.get_frame().set_linewidth(0.8)

ax.set_title('Cl–SO$_4$–HCO$_3$ diagram: which volatile the water remembers',
             fontsize=16.4, pad=16)
ax.text(0.5, -0.155, 'weight basis (mg L$^{-1}$), after Giggenbach (1991)',
        ha='center', va='center', fontsize=12.0, color='#888888')

ax.set_xlim(-0.16, 1.74)
ax.set_ylim(-0.20, 0.99)

fig.savefig('fig6_ternary.png', dpi=244, bbox_inches='tight',
            facecolor='white')
print('saved fig6_ternary.png')
