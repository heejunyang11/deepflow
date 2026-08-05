# -*- coding: utf-8 -*-
"""
Sci17 fig3 : A well as a strain meter — the tidal calibration
  (a) theoretical M2 volumetric strain vs observed groundwater level (anti-phase)
  (b) the same data as a straight line:  dh = -W_eps * d(eps)
Strain sensitivity W_eps = 7 mm per 1e-8 strain  (= 7e5 m per unit strain),
the value reported for the Usu GSH-1 well (Shibata & Akita, 2001;
quoted in Shibata et al., 2003).  Time series are synthetic.
Output: fig3_strainmeter.png
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.family'] = 'Times New Roman'
rcParams['mathtext.fontset'] = 'stix'
rcParams['axes.linewidth'] = 1.1

C_STRAIN = '#b8860b'
C_LEVEL = '#1f3b73'

W_EPS = 7.0e5          # m per unit strain  (= 7 mm per 1e-8)
T_M2 = 12.4206         # h
EPS_AMP = 2.0e-8       # typical M2 volumetric strain amplitude

t = np.arange(0, 37.3, 1.0 / 6.0)                    # 10-minute sampling
eps = EPS_AMP * np.sin(2 * np.pi * t / T_M2)         # volumetric strain
h = -W_EPS * eps * 1000.0                            # mm
rng = np.random.default_rng(17)
h_obs = h + rng.normal(0, 0.55, h.size)              # observation noise

fig, axes = plt.subplots(1, 2, figsize=(12.2, 4.5),
                         gridspec_kw={'width_ratios': [1.55, 1]})
fig.subplots_adjust(wspace=0.32, bottom=0.15, top=0.88, left=0.07, right=0.975)

# --------------------------------------------------- (a) the two time series
ax = axes[0]
ax.plot(t, eps * 1e8, color=C_STRAIN, lw=1.9,
        label=r'Theoretical M$_2$ volumetric strain')
ax.set_xlabel('Time (hours)', fontsize=15.0)
ax.set_ylabel(r'Volumetric strain  ($\times10^{-8}$)', fontsize=15.0, color=C_STRAIN)
ax.tick_params(axis='y', colors=C_STRAIN, labelsize=13.7)
ax.tick_params(axis='x', labelsize=13.7)
ax.set_xlim(0, 37.3)
ax.set_ylim(-2.6, 2.6)
ax.axhline(0, color='#999999', lw=0.8, ls=':')

ax2 = ax.twinx()
ax2.plot(t, h_obs, color=C_LEVEL, lw=1.7, label='Groundwater level')
ax2.set_ylabel('Groundwater level (mm)', fontsize=15.0, color=C_LEVEL)
ax2.tick_params(axis='y', colors=C_LEVEL, labelsize=13.7)
ax2.set_ylim(-18.2, 18.2)

# mark the anti-phase
ax.annotate('', xy=(T_M2 * 0.25, 2.28), xytext=(T_M2 * 0.75, 2.28),
            arrowprops=dict(arrowstyle='<->', color='#555555', lw=1.0))
ax.text(T_M2 * 0.5, 2.36, 'half a cycle apart', ha='center',
        fontsize=12.3, color='#555555')
ax.text(0.35, -2.35,
        'extension $\\rightarrow$ level falls   |   compression $\\rightarrow$ level rises',
        fontsize=13.7, color='#333333')

lines = ax.get_lines()[:1] + ax2.get_lines()[:1]
ax.legend(lines, [l.get_label() for l in lines], loc='upper right',
          fontsize=13.7, framealpha=0.92)
ax.set_title(r'(a) The tide strains the crust; the well records it',
             fontsize=16.2, pad=8)
ax.grid(alpha=0.2, lw=0.7)

# ------------------------------------------------------ (b) the linear law
ax = axes[1]
ax.plot(eps * 1e8, h_obs, 'o', ms=3.4, color=C_LEVEL, alpha=0.55,
        label='Synthetic record')
xx = np.array([-2.4, 2.4])
ax.plot(xx, -W_EPS * xx * 1e-8 * 1000.0, color='#cb4335', lw=2.0,
        label=r'$\Delta h=-W_{\varepsilon}\,\Delta\varepsilon$')
ax.axhline(0, color='#999999', lw=0.8, ls=':')
ax.axvline(0, color='#999999', lw=0.8, ls=':')
ax.set_xlabel(r'Volumetric strain  $\Delta\varepsilon$  ($\times10^{-8}$)', fontsize=15.0)
ax.set_ylabel(r'Level change  $\Delta h$  (mm)', fontsize=15.0)
ax.set_xlim(-2.6, 2.6)
ax.set_ylim(-18.5, 18.5)
ax.tick_params(labelsize=13.7)
ax.legend(loc='upper right', fontsize=13.7, framealpha=0.92)
ax.set_title('(b) The slope is the strain sensitivity', fontsize=16.2, pad=8)
ax.text(-2.35, -15.5,
        r'slope $=-W_{\varepsilon}=-7$ mm per $10^{-8}$',
        fontsize=14.3, color='#cb4335')
ax.grid(alpha=0.2, lw=0.7)

fig.savefig('fig3_strainmeter.png', dpi=200, bbox_inches='tight')
print('saved fig3_strainmeter.png')
