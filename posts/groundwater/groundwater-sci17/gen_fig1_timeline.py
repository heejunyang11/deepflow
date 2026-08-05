# -*- coding: utf-8 -*-
"""
Sci17 fig1 : Three faces of a well across an earthquake / eruption timeline
  (a) precursor  - log-periodic decline  (Shibata et al., 2003, Usu 2000)
  (b) coseismic  - step change           (Shibata et al., 2010, Hokkaido)
  (c) postseismic- enhanced discharge    (Rojstaczer et al., 1995, Loma Prieta)
Synthetic / schematic data: the shapes follow the published models,
the absolute values are illustrative.
Output: fig1_timeline.png
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.family'] = 'Times New Roman'
rcParams['mathtext.fontset'] = 'stix'
rcParams['axes.linewidth'] = 1.1

C_LINE = '#1f3b73'
C_EVENT = '#cb4335'
C_BAND = '#cb4335'

fig, axes = plt.subplots(1, 3, figsize=(12.6, 4.0))
fig.subplots_adjust(wspace=0.28, top=0.80, bottom=0.16, left=0.06, right=0.985)

# ---------------------------------------------------------------- (a) before
ax = axes[0]
tc = 105.0                      # critical failure point (day)
t = np.linspace(0, tc - 0.6, 1400)
m, w = 0.694, 7.96              # critical exponents (Shibata et al., 2003)
tau = tc - t
level = -4.9 * (1.0 - (tau / tc) ** m * (1 + 0.09 * np.cos(w * np.log(tau) + 1.2)))

ax.plot(t, level, color=C_LINE, lw=1.6)
ax.axvline(tc, color=C_EVENT, lw=1.8, ls='--')
ax.text(tc - 2.5, 0.72, 'Eruption', color=C_EVENT, fontsize=14.3,
        rotation=90, va='top', ha='right')
ax.set_xlim(0, tc + 6)
ax.set_ylim(-5.6, 0.9)
ax.set_xlabel('Days from the onset of the decline', fontsize=15.0)
ax.set_ylabel('Residual groundwater level (m)', fontsize=15.0)
ax.set_title('(a) Precursor  —  months', fontsize=16.2, pad=8)
ax.annotate('power-law decline with\nself-similar oscillation',
            xy=(62, -2.6), xytext=(14, -4.5), fontsize=13.0, color='#333333',
            arrowprops=dict(arrowstyle='->', color='#666666', lw=0.9))

# --------------------------------------------------------------- (b) during
ax = axes[1]
t = np.linspace(-6, 12, 2200)                    # hours
tide = 14.0 * np.sin(2 * np.pi * t / 12.4206)    # M2 tide, mm
step = np.where(t >= 0, -70.0, 0.0)              # coseismic step, mm
ax.plot(t, tide + step, color=C_LINE, lw=1.5)
ax.axvline(0, color=C_EVENT, lw=1.8, ls='--')
ax.text(-0.7, 40, 'Earthquake', color=C_EVENT, fontsize=14.3,
        rotation=90, va='top', ha='right')
ax.annotate('', xy=(6, -70), xytext=(6, 0),
            arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.2))
ax.text(6.6, -36, r'$\Delta h=-W_{\varepsilon}\,\Delta\varepsilon$',
        fontsize=15.0, color='#333333', va='center')
ax.set_xlim(-6, 12)
ax.set_ylim(-105, 45)
ax.set_xlabel('Hours from the earthquake', fontsize=15.0)
ax.set_ylabel('Groundwater level (mm)', fontsize=15.0)
ax.set_title('(b) Coseismic  —  seconds to minutes', fontsize=16.2, pad=8)

# ---------------------------------------------------------------- (c) after
ax = axes[2]
t = np.linspace(-20, 150, 1700)                  # days
c, L = 0.020, 500.0                              # m2/s, m
tt = np.clip(t, 0, None) * 86400.0
n = np.arange(0, 60)[:, None]
series = ((-1.0) ** n / (2 * n + 1)) * np.exp(
    -((2 * n + 1) ** 2) * np.pi ** 2 * c * tt[None, :] / (4 * L ** 2))
v = series.sum(axis=0) / (np.pi / 4)
flow = np.where(t < 0, 1.0, 1.0 + 9.0 * v)

ax.fill_between(t, 1.0, flow, where=(t >= 0), color=C_BAND, alpha=0.13)
ax.plot(t, flow, color=C_LINE, lw=1.7)
ax.axvline(0, color=C_EVENT, lw=1.8, ls='--')
ax.text(-3.0, 11.2, 'Earthquake', color=C_EVENT, fontsize=14.3,
        rotation=90, va='top', ha='right')
ax.set_xlim(-20, 150)
ax.set_ylim(0, 11.5)
ax.set_xlabel('Days from the earthquake', fontsize=15.0)
ax.set_ylabel('Base flow (pre-seismic $=1$)', fontsize=15.0)
ax.set_title('(c) Postseismic  —  weeks to months', fontsize=16.2, pad=8)
ax.annotate('excess discharge\n($\\sim$10$\\times$ base flow)',
            xy=(18, 6.0), xytext=(52, 8.0), fontsize=13.0, color='#333333',
            arrowprops=dict(arrowstyle='->', color='#666666', lw=0.9))

for ax in axes:
    ax.tick_params(labelsize=13.7)
    ax.grid(alpha=0.22, lw=0.7)

fig.suptitle('Three faces of a well:  strain, shaking, and permeability',
             fontsize=18.2, y=0.965)
fig.savefig('fig1_timeline.png', dpi=200, bbox_inches='tight')
print('saved fig1_timeline.png')
