# -*- coding: utf-8 -*-
"""
Sci17 fig6 : After the shaking — permeability enhancement in the shallow crust
  Loma Prieta, 1989 (Rojstaczer, Wolf & Michel, 1995, Nature 373:237-239)

(a) Excess stream flow from the paper's darcian model,
        v(t) = (4 k rho g w / eta L) * SUM (-1)^n/(2n+1)
                * exp[-(2n+1)^2 pi^2 c t / (4 L^2)]
    for the two hydraulic diffusivities reported, c = 200 and 260 cm2/s.
    The flow-path length L is not given in the paper; L = 500 m is assumed
    here so that the decay spans the observed few months.
(b) The same model seen from the hillside: discharge up, water table down.
    A compression source cannot produce both; a permeability increase can.
Output: fig6_permeability.png
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.family'] = 'Times New Roman'
rcParams['mathtext.fontset'] = 'stix'
rcParams['axes.linewidth'] = 1.1

C_FLOW = '#1f3b73'
C_TABLE = '#b8860b'
C_EVENT = '#cb4335'

L = 500.0                       # m, assumed flow-path length
N = np.arange(0, 80)[:, None]


def flux(t_days, c_m2s):
    tt = np.clip(t_days, 0, None) * 86400.0
    e = np.exp(-((2 * N + 1) ** 2) * np.pi ** 2 * c_m2s * tt[None, :] / (4 * L ** 2))
    return (((-1.0) ** N / (2 * N + 1)) * e).sum(axis=0) / (np.pi / 4)


def head(t_days, c_m2s):
    tt = np.clip(t_days, 0, None) * 86400.0
    e = np.exp(-((2 * N + 1) ** 2) * np.pi ** 2 * c_m2s * tt[None, :] / (4 * L ** 2))
    return ((8 / np.pi ** 2) / (2 * N + 1) ** 2 * e).sum(axis=0)


t = np.linspace(-15, 150, 1800)
fig, axes = plt.subplots(1, 2, figsize=(12.4, 4.6))
fig.subplots_adjust(wspace=0.30, bottom=0.15, top=0.86, left=0.07, right=0.925)

# ------------------------------------------------- (a) excess flow and decay
ax = axes[0]
for c_cm2, col, ls in [(260.0, '#2166ac', '-'), (200.0, '#6baed6', '--')]:
    v = flux(t, c_cm2 * 1e-4)
    ax.plot(t, np.where(t < 0, 0.0, v), color=col, lw=2.0, ls=ls,
            label=r'$c=%d$ cm$^2$ s$^{-1}$' % c_cm2)
ax.axvline(0, color=C_EVENT, lw=1.8, ls='--')
ax.text(-2.0, 1.02, 'Loma Prieta,  17 Oct 1989', color=C_EVENT, fontsize=13.7,
        rotation=90, va='top', ha='right')
ax.set_xlim(-15, 150)
ax.set_ylim(-0.03, 1.10)
ax.set_xlabel('Days from the earthquake', fontsize=15.0)
ax.set_ylabel('Excess stream flow (normalised)', fontsize=15.0)
ax.set_title('(a) The pulse decays as a darcian drainage', fontsize=16.2, pad=8)
ax.legend(loc='upper right', fontsize=13.7, framealpha=0.92)
ax.tick_params(labelsize=13.7)
ax.grid(alpha=0.2, lw=0.7)
ax.text(6, 0.26,
        'peak excess flow\n920 L s$^{-1}$  San Lorenzo R.\n690 L s$^{-1}$  Pescadero Ck.',
        fontsize=12.5, color='#333333', va='top')

# --------------------------------------- (b) discharge up, water table down
ax = axes[1]
c = 220.0 * 1e-4
base = np.where(t < 0, 1.0, 1.0 + 9.0 * flux(t, c))
wt = np.where(t < 0, 1.0, np.clip(head(t, c), 1e-3, None))

ax.plot(t, base, color=C_FLOW, lw=2.2, label='Discharge to the stream')
ax.plot(t, wt, color=C_TABLE, lw=2.2, label='Water stored in the hillside')
ax.axvline(0, color=C_EVENT, lw=1.8, ls='--')
ax.axhline(1.0, color='#999999', lw=0.9, ls=':')
ax.set_yscale('log')
ax.set_xlim(-15, 150)
ax.set_ylim(0.02, 30)
ax.set_yticks([0.03, 0.1, 0.3, 1, 3, 10])
ax.set_yticklabels(['0.03', '0.1', '0.3', '1', '3', '10'])
ax.set_xlabel('Days from the earthquake', fontsize=15.0)
ax.set_ylabel('Relative to the pre-seismic value', fontsize=15.0)
ax.tick_params(labelsize=13.7)
ax.grid(alpha=0.2, lw=0.7, which='both')
ax.legend(loc='lower left', fontsize=13.7, framealpha=0.92)

ax.annotate('up by one order', xy=(6, 9.4), xytext=(30, 17),
            fontsize=13.7, color=C_FLOW,
            arrowprops=dict(arrowstyle='->', color=C_FLOW, lw=1.0))
ax.annotate('down, and staying down', xy=(104, 0.105), xytext=(83, 0.42),
            fontsize=13.7, color=C_TABLE, ha='center',
            arrowprops=dict(arrowstyle='->', color=C_TABLE, lw=1.0))
ax.set_title('(b) One cause, two opposite signs', fontsize=16.2, pad=8)

fig.suptitle('The earthquake did not squeeze the crust — it opened it',
             fontsize=17.6, y=0.975)
fig.savefig('fig6_permeability.png', dpi=200, bbox_inches='tight')
print('saved fig6_permeability.png')
