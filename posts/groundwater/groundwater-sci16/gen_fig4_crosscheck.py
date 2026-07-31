# -*- coding: utf-8 -*-
"""Sci16 fig4 : geothermometer cross-check for Shiraoi (4 districts).
Na-K & K-Mg from Giggenbach(1988); Quartz & Chalcedony from PHREEQC."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'Times New Roman'
rcParams['mathtext.fontset'] = 'stix'
rcParams['axes.linewidth'] = 1.1

sites = ['a\nKojohama\n(West)', 'C\nKitayoshi-\nwara',
         'E\nIshiyama\n(Central)', 'G\nShadai\n(East)']
Na = np.array([1150.0, 402.5, 625.0, 540.0])
K  = np.array([50.6, 22.5, 50.0, 45.5])
Mg = np.array([1.8, 0.3, 0.4, 3.4])
disc = np.array([47.5, 55.7, 58.4, 46.0])
Qz = np.array([129, 151, 151, 132])      # PHREEQC quartz
Ch = np.array([101, 120, 119, 105])      # PHREEQC chalcedony

NaK = 1390.0 / (1.75 + np.log10(Na / K)) - 273.15
KMg = 4410.0 / (14.0 - np.log10(K**2 / Mg)) - 273.15

x = np.arange(4)
fig, ax = plt.subplots(figsize=(9.2, 6.2))

# grey spread bar per site (min discharge -> max Na-K)
for xi in x:
    lo, hi = disc[xi], NaK[xi]
    ax.plot([xi, xi], [lo, hi], color='#e2e2e2', lw=9, zorder=0,
            solid_capstyle='round')

dd = 0.17
ax.scatter(x - 1.5*dd, NaK, marker='^', s=120, color='#c0392b',
           edgecolor='#611611', lw=1.0, zorder=5, label='Na-K')
ax.scatter(x - 0.5*dd, KMg, marker='s', s=95, color='#e08214',
           edgecolor='#7a4205', lw=1.0, zorder=5, label='K-Mg')
ax.scatter(x + 0.5*dd, Qz, marker='o', s=100, color='#1f3b73',
           edgecolor='#0b1a33', lw=1.0, zorder=5, label='Quartz')
ax.scatter(x + 1.5*dd, Ch, marker='o', s=88, color='#4292c6',
           edgecolor='#1c4e73', lw=1.0, zorder=5, label='Chalcedony')
ax.scatter(x, disc, marker='x', s=75, color='#555555', lw=1.6,
           zorder=6, label='Discharge (measured)')

ax.annotate('Na-K reads highest\n(slow to re-equilibrate\n$\\rightarrow$ over-estimate\nunder mixing)',
            xy=(3 - 1.5*dd, 219), xytext=(1.55, 244),
            fontsize=9.5, color='#c0392b', ha='center',
            arrowprops=dict(arrowstyle='->', color='#c0392b', lw=1.0))
ax.text(0.02, 0.02, 'Eight-district reference: at Hatchobaru all thermometers cluster at 260–300 $^{\\circ}$C (full equilibrium).',
        transform=ax.transAxes, fontsize=9, color='#555555', style='italic')

ax.set_xticks(x); ax.set_xticklabels(sites, fontsize=11)
ax.set_ylabel('Temperature ($^{\\circ}$C)', fontsize=13)
ax.set_title('Geothermometer Cross-check — Shiraoi (Shigeno 2011)',
             fontsize=14, pad=10)
ax.set_ylim(0, 265)
ax.grid(axis='y', alpha=0.25)
ax.legend(loc='upper left', fontsize=10.5, frameon=True)
plt.tight_layout()
plt.savefig('fig4_crosscheck.png', dpi=220, facecolor='white')
print('saved fig4  NaK=%s  KMg=%s' % (np.round(NaK,0), np.round(KMg,0)))
