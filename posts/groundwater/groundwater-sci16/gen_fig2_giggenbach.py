# -*- coding: utf-8 -*-
"""
Sci16 fig2 : Giggenbach (1988) Na-K-Mg ternary geothermometer (simple, readable)
  - single full-equilibrium curve with temperature ticks (100-340 C)
  - three fields (Fully / Partially equilibrated / Immature waters)
  - data: Shiraoi (Shigeno 2011, 4 districts) + Bugok (Jeong 2022)
All input data are from published papers (JOGMEC-unrelated).
Output: fig2_giggenbach.png
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'Times New Roman'
rcParams['mathtext.fontset'] = 'stix'
rcParams['axes.linewidth'] = 1.2

S3 = np.sqrt(3.0) / 2.0
VK, VMG, VNA = np.array([0, 0]), np.array([1, 0]), np.array([0.5, S3])

def tern(na, k, mg):
    na = np.asarray(na, float); k = np.asarray(k, float); mg = np.asarray(mg, float)
    sNa, sK, sMg = na / 1000.0, k / 100.0, np.sqrt(mg)
    tot = sNa + sK + sMg
    fNa, fK, fMg = sNa / tot, sK / tot, sMg / tot
    x = fK * VK[0] + fMg * VMG[0] + fNa * VNA[0]
    y = fNa * VNA[1]
    return x, y

# full equilibrium curve
T = np.linspace(60, 340, 400)
TK = T + 273.15
Na0 = 10.0 ** (1390.0 / TK - 1.75)
Mg0 = 1.0 / 10.0 ** (14.0 - 4410.0 / TK)
xc, yc = tern(Na0, 1.0, Mg0)

fig, ax = plt.subplots(figsize=(8.4, 7.6))
ax.set_aspect('equal'); ax.axis('off')

tri = np.array([VK, VMG, VNA, VK])
ax.fill(tri[:, 0], tri[:, 1], color='#f7f9fb', zorder=0)
ax.plot(tri[:, 0], tri[:, 1], color='#2b2b2b', lw=1.6, zorder=5)

# --- field labels: "Fully equilibrated waters" ABOVE the curve ---
ax.text(0.545, 0.560, 'Fully equilibrated\nwaters', ha='center', va='center',
        style='italic', fontsize=10.5, color='#34495e', linespacing=1.2)
ax.text(0.405, 0.265, 'Partially equilibrated waters', ha='center',
        style='italic', fontsize=11, color='#7f8c8d')
ax.text(0.405, 0.130, 'Immature waters', ha='center',
        style='italic', fontsize=11.5, color='#95a5a6')

# full equilibrium curve
ax.plot(xc, yc, color='#1f3b73', lw=2.6, zorder=6,
        label='Full equilibrium (Giggenbach 1988)')

# temperature ticks on the curve
for tt in [100, 140, 180, 220, 260, 300, 340]:
    tk = tt + 273.15
    na = 10.0 ** (1390.0 / tk - 1.75); mg = 1.0 / 10.0 ** (14.0 - 4410.0 / tk)
    xt, yt = tern(na, 1.0, mg)
    ax.plot(xt, yt, 'o', ms=6.5, mfc='white', mec='#1f3b73', mew=1.6, zorder=7)
    ax.text(xt - 0.028, yt + 0.006, f'{tt}', fontsize=10.5, color='#1f3b73',
            ha='right', va='center')
ax.text(0.135, 0.44, r'$T\,(^{\circ}\mathrm{C})$', fontsize=12,
        color='#1f3b73', style='italic')

# --- data ---
shiraoi = {
    'a  Kojohama (W)':  (1150.0, 50.6, 1.8, '#B2182B'),
    'C  Kitayoshiwara': (402.5, 22.5, 0.3, '#E6784B'),
    'E  Ishiyama (C)':  (625.0, 50.0, 0.4, '#D6604D'),
    'G  Shadai (E)':    (540.0, 45.5, 3.4, '#F1A340'),
}
for lab, (na, k, mg, col) in shiraoi.items():
    x, y = tern(na, k, mg)
    ax.plot(x, y, 'o', ms=12, mfc=col, mec='#4d0f14', mew=1.1,
            zorder=9, label='Shiraoi ' + lab)

bugok = [(93.2,3.58,0.12),(88.7,3.43,0.08),(96.7,3.81,0.38),(78.7,2.92,0.02),
         (74.2,2.13,1.93),(66.7,2.00,0.03),(83.7,2.94,0.01),(89.5,3.04,0.03),
         (91.1,3.02,0.06),(65.2,0.81,1.07),(75.6,2.69,0.22)]
bx, by = tern([b[0] for b in bugok], [b[1] for b in bugok], [b[2] for b in bugok])
ax.plot(bx, by, 'D', ms=8, mfc='#2166AC', mec='#0b2e52', mew=0.9,
        alpha=0.9, zorder=8, label='Bugok, Korea (Jeong 2022)')

# vertex labels
ax.text(VNA[0], VNA[1] + 0.045, r'$\mathrm{Na}/1000$', ha='center', va='bottom', fontsize=15)
ax.text(VK[0] - 0.035, VK[1] - 0.028, r'$\mathrm{K}/100$', ha='center', va='top', fontsize=15)
ax.text(VMG[0] + 0.035, VMG[1] - 0.028, r'$\sqrt{\mathrm{Mg}}$', ha='center', va='top', fontsize=15)

leg = ax.legend(loc='upper left', bbox_to_anchor=(0.60, 1.00), frameon=True,
                fontsize=10.5, handletextpad=0.4, borderpad=0.8)
leg.get_frame().set_edgecolor('#cccccc'); leg.get_frame().set_linewidth(0.8)

ax.set_title('Na–K–Mg Geothermometer (Giggenbach Diagram)', fontsize=16, pad=14)
ax.set_xlim(-0.16, 1.30); ax.set_ylim(-0.12, 0.98)

plt.tight_layout()
plt.savefig('fig2_giggenbach.png', dpi=220, bbox_inches='tight', facecolor='white')
print('saved fig2_giggenbach.png (simple, Fully-label above curve)')
