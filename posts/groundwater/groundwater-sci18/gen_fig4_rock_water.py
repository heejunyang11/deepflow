# -*- coding: utf-8 -*-
"""
Sci18 fig4 : What each magma type leaves in the water (PHREEQC).
  Reads the SELECTED_OUTPUT of phreeqc_sci18_rock_water.pqi, in which a
  mineral assemblage representing basalt / andesite / rhyolite is titrated
  into CO2-charged pure water (P_CO2 = 10^-2 atm, 25 C, llnl.dat).
  (a) the water after 2.5 mmol of rock has dissolved, mg/L, log axis
  (b) how much CO2 each rock takes out of the gas phase on the way

Input decks and .sel files live in D:\\Hityu\\GROUNDWATER_proj\\Sci18\\.
Output: fig4_rock_water.png
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.family'] = 'Times New Roman'
rcParams['mathtext.fontset'] = 'stix'
rcParams['axes.linewidth'] = 1.1

SEL_DIR = r'D:\Hityu\GROUNDWATER_proj\Sci18'

# fixed order, fixed colour - never cycled (basalt -> andesite -> rhyolite)
ROCKS = [('Basalt', 'out_basalt.sel', '#1a5b8a'),
         ('Andesite', 'out_andesite.sel', '#c8871f'),
         ('Rhyolite', 'out_rhyolite.sel', '#9e3b52')]

MW = {'Ca': 40.078, 'Mg': 24.305, 'Na': 22.990, 'K': 39.098,
      'Si': 60.084, 'F': 18.998, 'Alk': 61.017}     # Si reported as SiO2


def read_sel(path):
    with open(path) as fh:
        head = fh.readline().split()
        rows = [[float(v) for v in ln.split()] for ln in fh if ln.strip()]
    return head, np.array(rows)


data = {}
for name, fn, col in ROCKS:
    head, arr = read_sel(os.path.join(SEL_DIR, fn))
    data[name] = {h: arr[:, i] for i, h in enumerate(head)}
    data[name]['_col'] = col

fig = plt.figure(figsize=(10.820, 4.836))
gs = fig.add_gridspec(1, 2, width_ratios=[1.35, 1.0], wspace=0.24,
                      left=0.055, right=0.985, bottom=0.13, top=0.86)

# ================================================== (a) the resulting water
ax = fig.add_subplot(gs[0])

species = [('Ca', r'Ca$^{2+}$'), ('Mg', r'Mg$^{2+}$'), ('Na', r'Na$^{+}$'),
           ('K', r'K$^{+}$'), ('Alk', r'HCO$_3^{-}$'), ('Si', r'SiO$_2$'),
           ('F', r'F$^{-}$')]
FLOOR = 0.02          # mg/L, so that "absent" is visible as a stub

x = np.arange(len(species))
w = 0.26
for k, (name, fn, col) in enumerate(ROCKS):
    d = data[name]
    vals = []
    for key, _ in species:
        c = d[key][-1] * MW[key] * 1000.0
        vals.append(max(c, FLOOR))
    bars = ax.bar(x + (k - 1) * w, vals, width=w, color=col, alpha=0.9,
                  edgecolor='white', lw=0.8, label=name, zorder=3)
    for xi, (v, (key, _)) in zip(x + (k - 1) * w, zip(vals, species)):
        raw = d[key][-1] * MW[key] * 1000.0
        txt = '–' if raw < FLOOR else ('%.2f' % raw if raw < 10 else '%.0f' % raw)
        ax.text(xi, v * 1.16, txt, ha='center', va='bottom', fontsize=10.2,
                color=col, zorder=4)

ax.set_yscale('log')
ax.set_ylim(FLOOR * 0.55, 1.5e3)
ax.set_xticks(x)
ax.set_xticklabels([s[1] for s in species], fontsize=14.0)
ax.set_ylabel(r'concentration (mg L$^{-1}$)', fontsize=13.4)
ax.grid(axis='y', color='#e2e2e2', lw=0.8, zorder=0)
ax.set_axisbelow(True)
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
ax.legend(fontsize=12.4, frameon=False, loc='upper right', ncol=3,
          columnspacing=1.4)
ax.set_title('(a)  the water after 2.5 mmol of rock has dissolved',
             fontsize=15.2, pad=10, loc='left')

# ================================================== (b) CO2 taken from the gas
ax = fig.add_subplot(gs[1])

for name, fn, col in ROCKS:
    d = data[name]
    rock = d['step'] * 1.0e-4 * 1000.0            # mmol of rock per kg water
    co2 = (10.0 - d['CO2(g)']) * 1000.0           # mmol of CO2 consumed
    ax.plot(rock, co2, color=col, lw=2.6, label=name, zorder=3)
    ax.plot(rock[-1], co2[-1], 'o', ms=7, mfc='white', mec=col, mew=2.0,
            zorder=4)
    ax.text(rock[-1] + 0.06, co2[-1], '%.1f' % co2[-1], fontsize=11.4,
            color=col, va='center')

ax.set_xlabel(r'rock dissolved  (mmol kg$_{\rm w}^{-1}$)', fontsize=13.4)
ax.set_ylabel(r'CO$_2$ taken from the gas phase  (mmol kg$_{\rm w}^{-1}$)',
              fontsize=13.0)
ax.set_xlim(0, 2.95)
ax.set_ylim(0, 7.4)
ax.tick_params(labelsize=12.0)
ax.grid(color='#e2e2e2', lw=0.8, zorder=0)
ax.set_axisbelow(True)
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
ax.legend(fontsize=12.4, frameon=False, loc='upper left')
ax.set_title('(b)  basalt is the hungriest for CO$_2$',
             fontsize=15.2, pad=10, loc='left')

fig.savefig('fig4_rock_water.png', dpi=244, bbox_inches='tight',
            facecolor='white')
print('saved fig4_rock_water.png')
