# -*- coding: utf-8 -*-
"""
Sci17 fig4 : Coseismic steps — the sign of the step tells the sign of the strain
  (a) the well sits in a zone of coseismic extension  -> level drops
  (b) the well sits in a zone of coseismic compression -> level rises
Steps are computed from dh = -W_eps * d(eps) with W_eps = 7e5 m
(7 mm per 1e-8 strain) and |d(eps)| = 1e-7, a plausible near-field
coseismic strain step for an M~8 event (cf. Shibata et al., 2010).
Time series are synthetic; the M2 tide is superimposed.
Output: fig4_coseismic.png
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.family'] = 'Times New Roman'
rcParams['mathtext.fontset'] = 'stix'
rcParams['axes.linewidth'] = 1.1

C_LEVEL = '#1f3b73'
C_EVENT = '#cb4335'

W_EPS = 7.0e5           # m per unit strain
T_M2 = 12.4206          # h
EPS_STEP = 1.0e-7       # volumetric strain step

t = np.arange(-36, 60, 1.0 / 6.0)                 # 10-minute sampling, hours
tide = 14.0 * np.sin(2 * np.pi * t / T_M2)
rng = np.random.default_rng(3)
noise = rng.normal(0, 0.6, t.size)
trend = -0.05 * t                                  # slow recession

cases = [
    ('(a) Coseismic extension', +EPS_STEP, '#2166ac'),
    ('(b) Coseismic compression', -EPS_STEP, '#b2182b'),
]

fig, axes = plt.subplots(1, 2, figsize=(12.4, 4.5), sharey=True)
fig.subplots_adjust(wspace=0.10, bottom=0.15, top=0.86, left=0.075, right=0.985)

for ax, (title, deps, col) in zip(axes, cases):
    dh = -W_EPS * deps * 1000.0                    # mm
    # the step decays by 25% over ~30 h (partial poroelastic drainage)
    decay = np.where(t >= 0, 1.0 - 0.25 * (1.0 - np.exp(-t / 30.0)), 0.0)
    level = tide + trend + dh * decay + noise

    ax.plot(t, level, color=C_LEVEL, lw=1.4)
    ax.axvline(0, color=C_EVENT, lw=1.8, ls='--')
    ax.text(-1.4, 108, 'Earthquake', color=C_EVENT, fontsize=14.3,
            rotation=90, va='top', ha='right')

    ax.annotate('', xy=(26, dh), xytext=(26, 0),
                arrowprops=dict(arrowstyle='<->', color=col, lw=1.5))
    ax.text(28.5, -0.62 * dh,
            r'$\Delta h=%+.0f$ mm' % dh + '\n' + r'$\Delta\varepsilon=%+.0f\times10^{-8}$' % (deps * 1e8),
            fontsize=14.3, color=col, va='center')
    ax.axhline(0, color='#999999', lw=0.8, ls=':')

    ax.set_xlim(-36, 60)
    ax.set_xlabel('Hours from the earthquake', fontsize=15.0)
    ax.set_title(title, fontsize=16.2, pad=8, color=col)
    ax.tick_params(labelsize=13.7)
    ax.grid(alpha=0.2, lw=0.7)

axes[0].set_ylabel('Groundwater level (mm)', fontsize=15.0)
axes[0].set_ylim(-115, 115)
axes[0].text(-34, -108, 'the aquifer is stretched;\npore pressure falls',
             fontsize=13.7, color='#333333')
axes[1].text(-34, -108, 'the aquifer is squeezed;\npore pressure rises',
             fontsize=13.7, color='#333333')

fig.suptitle(r'A step in the record is a step in the strain:  $\Delta h=-W_{\varepsilon}\,\Delta\varepsilon$',
             fontsize=17.6, y=0.975)
fig.savefig('fig4_coseismic.png', dpi=200, bbox_inches='tight')
print('saved fig4_coseismic.png')
