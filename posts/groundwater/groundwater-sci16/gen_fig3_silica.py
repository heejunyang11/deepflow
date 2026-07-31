# -*- coding: utf-8 -*-
"""
Sci16 fig3 : Silica geothermometry as SI vs temperature sweep
  Shiraoi Ishiyama-1 (E) ; data = A_shiraoi_E.sel (PHREEQC, llnl.dat)
  SI=0 crossing of quartz / chalcedony = reservoir temperature.
Output: fig3_silica.png
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.family'] = 'Times New Roman'
rcParams['mathtext.fontset'] = 'stix'
rcParams['axes.linewidth'] = 1.1

# ---- read sel (skip header, drop contamination row where T reverses) ----
rows, last = [], -1e9
with open('A_shiraoi_E.sel') as f:
    next(f)
    for line in f:
        p = line.split()
        if len(p) < 5:
            continue
        t = float(p[0])
        if t < last:
            break
        rows.append([float(x) for x in p[:5]])
        last = t
d = np.array(rows)
T, qz, ch, am, cal = d[:, 0], d[:, 1], d[:, 2], d[:, 3], d[:, 4]

def cross(T, si):
    for i in range(1, len(si)):
        if (si[i-1] > 0) != (si[i] > 0):
            return T[i-1] + (T[i]-T[i-1]) * si[i-1] / (si[i-1]-si[i])
    return None
tqz, tch = cross(T, qz), cross(T, ch)

# ---- figure ----
fig, ax = plt.subplots(figsize=(8.4, 6.1))

# reservoir-T band (between chalcedony and quartz)
ax.axvspan(tch, tqz, color='#2ca25f', alpha=0.10, zorder=0)
ax.axhline(0, color='#555555', lw=1.2, ls='--', zorder=2)

ax.plot(T, qz,  color='#1f3b73', lw=2.5, label='Quartz', zorder=4)
ax.plot(T, ch,  color='#4292c6', lw=2.3, label='Chalcedony', zorder=4)
ax.plot(T, am,  color='#9a9a9a', lw=2.0, label='Amorphous silica', zorder=3)
ax.plot(T, cal, color='#cb4335', lw=2.0, label='Calcite', zorder=3)

# crossing markers + labels
ax.plot(tqz, 0, 'o', ms=10, mfc='white', mec='#1f3b73', mew=2.0, zorder=6)
ax.plot(tch, 0, 'o', ms=10, mfc='white', mec='#4292c6', mew=2.0, zorder=6)
ax.annotate(f'Quartz\n{tqz:.0f} $^{{\\circ}}$C', (tqz, 0), xytext=(tqz+22, -1.35),
            ha='center', fontsize=11, color='#1f3b73',
            arrowprops=dict(arrowstyle='-', color='#1f3b73', lw=0.9))
ax.annotate(f'Chalcedony\n{tch:.0f} $^{{\\circ}}$C', (tch, 0), xytext=(tch-24, -1.9),
            ha='center', fontsize=11, color='#2f6ea5',
            arrowprops=dict(arrowstyle='-', color='#4292c6', lw=0.9))

ax.text((tch+tqz)/2, 2.55, 'Reservoir $T$\n(silica)', ha='center',
        fontsize=11, color='#1e7d4f', style='italic')

# discharge temperature marker
ax.axvline(58.4, color='#e08214', lw=1.3, ls=':', zorder=2)
ax.text(58.4, -2.75, 'discharge\n58 $^{\\circ}$C', ha='center', fontsize=9.5,
        color='#b3600a')

ax.set_xlabel('Temperature ($^{\\circ}$C)', fontsize=13)
ax.set_ylabel('Saturation index   SI = log($Q/K$)', fontsize=13)
ax.set_title('Silica Geothermometry — Shiraoi Ishiyama-1 (Shigeno 2011)',
             fontsize=14, pad=10)
ax.set_xlim(0, 250)
ax.set_ylim(-3, 3)
ax.grid(alpha=0.22)
ax.legend(loc='upper right', fontsize=11, frameon=True, borderpad=0.7)
ax.legend(loc='upper right', fontsize=11).get_frame().set_edgecolor('#cccccc')

plt.tight_layout()
plt.savefig('fig3_silica.png', dpi=220, facecolor='white')
print('saved fig3_silica.png  tqz=%.1f  tch=%.1f' % (tqz, tch))
