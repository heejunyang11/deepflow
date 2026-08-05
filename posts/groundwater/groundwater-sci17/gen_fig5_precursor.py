# -*- coding: utf-8 -*-
"""
Sci17 fig5 : The precursor — a log-periodic approach to a critical point
  Usu volcano, 2000 eruption (Shibata, Matsumoto & Akita, 2003, GRL)

The curve is the published log-periodic model
    f(t) = A + B (tc - t)^m { 1 + C cos[ w ln(tc - t) + psi] }
evaluated with the *fitted* exponents of the paper, m = 0.694, w = 7.96,
over the reported period P2 (14 Dec 1999 06:00 - 28 Mar 2000 00:00).
The amplitude is scaled to the reported tensional strain of ~7e-6 read
through the tidal sensitivity of 7 mm per 1e-8 strain (~4.9 m of drawdown).
This is a reconstruction of the model, not the observed record.
Output: fig5_precursor.png
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.family'] = 'Times New Roman'
rcParams['mathtext.fontset'] = 'stix'
rcParams['axes.linewidth'] = 1.1

C_LEVEL = '#1f3b73'
C_MODEL = '#cb4335'
C_P2 = '#f0ad4e'

# day 0 = 1 Dec 1999
D_P2, D_TC, D_ERUPT, D_END = 13.0, 118.0, 121.55, 126.0
M, W = 0.694, 7.96                      # critical exponents (fitted, GRL 2003)
DROP = 4.9                              # m, from ~7e-6 strain x 7 mm / 1e-8
B = DROP / (D_TC - D_P2) ** M

rng = np.random.default_rng(2003)


def logperiodic(t, C=0.085, psi=1.15):
    tau = np.clip(D_TC - t, 1e-6, None)
    return -DROP + B * tau ** M * (1 + C * np.cos(W * np.log(tau) + psi))


t1 = np.arange(0, D_P2, 1 / 24)
t2 = np.arange(D_P2, D_TC - 0.02, 1 / 24)
t3 = np.arange(D_TC, D_END, 1 / 24)

l1 = 0.0 + rng.normal(0, 0.035, t1.size)
l2 = logperiodic(t2) + rng.normal(0, 0.030, t2.size)
l3 = (-DROP - 1.6 * (1 - np.exp(-(t3 - D_TC) / 2.2))
      + rng.normal(0, 0.13, t3.size))

fig, axes = plt.subplots(1, 2, figsize=(12.6, 4.7),
                         gridspec_kw={'width_ratios': [1.5, 1]})
fig.subplots_adjust(wspace=0.24, bottom=0.15, top=0.86, left=0.07, right=0.985)

# --------------------------------------------------------- (a) whole record
ax = axes[0]
ax.axvspan(D_P2, D_TC, color=C_P2, alpha=0.13, zorder=0)
ax.plot(t1, l1, color='#7f8c8d', lw=1.2)
ax.plot(t2, l2, color=C_LEVEL, lw=1.3)
ax.plot(t3, l3, color='#7f8c8d', lw=1.2)
ax.plot(t2, logperiodic(t2, C=0.0), color=C_MODEL, lw=2.0, ls='--',
        label=r'power-law envelope  $(t_c-t)^{m}$,  $m=0.694$')

ax.axvline(D_TC, color=C_MODEL, lw=1.6, ls='-')
ax.axvline(D_ERUPT, color='#8e44ad', lw=1.6, ls=':')
ax.text(D_TC - 1.6, -6.5, 'rock failure  28 Mar', color=C_MODEL,
        fontsize=13.0, rotation=90, va='bottom', ha='right')
ax.text(D_ERUPT + 1.4, -6.5, 'eruption  31 Mar', color='#8e44ad',
        fontsize=13.0, rotation=90, va='bottom', ha='left')

for x, lab in [(6, 'P1'), (65, 'P2'), (122, 'P3')]:
    ax.text(x, 0.55, lab, fontsize=15.6, ha='center', color='#444444')

ax.set_xlim(0, D_END)
ax.set_ylim(-7.0, 1.0)
ax.set_xticks([0, 31, 62, 91, 121])
ax.set_xticklabels(['1 Dec', '1 Jan', '1 Feb', '1 Mar', '31 Mar'])
ax.set_xlabel('1999 – 2000', fontsize=15.0)
ax.set_ylabel('Residual groundwater level (m)', fontsize=15.0)
ax.set_title('(a) Three months of decline before the eruption',
             fontsize=16.2, pad=8)
ax.legend(loc='lower left', fontsize=13.0, framealpha=0.92)
ax.tick_params(labelsize=13.7)
ax.grid(alpha=0.2, lw=0.7)
ax.annotate(r'$\approx 7\times10^{-6}$ of tensional strain',
            xy=(95, -3.6), xytext=(28, -5.2), fontsize=13.7, color='#333333',
            arrowprops=dict(arrowstyle='->', color='#666666', lw=0.9))

# ------------------------------------------------------------- (b) the zoom
ax = axes[1]
sel = t2 > D_TC - 26
resid = l2[sel] - logperiodic(t2[sel], C=0.0)
ax.plot(t2[sel], resid, color=C_LEVEL, lw=1.4)
ax.plot(t2[sel], logperiodic(t2[sel]) - logperiodic(t2[sel], C=0.0),
        color=C_MODEL, lw=1.8, alpha=0.85,
        label=r'$\cos[\,\omega\ln(t_c-t)+\psi\,]$,  $\omega=7.96$')
ax.axhline(0, color='#999999', lw=0.8, ls=':')
ax.axvline(D_TC, color=C_MODEL, lw=1.6)
ax.axvspan(D_TC - 2.11 / 24, D_TC + 2.11 / 24, color=C_MODEL, alpha=0.25)

ax.set_xlim(D_TC - 26, D_TC + 1.2)
ax.set_ylim(-0.55, 0.55)
ax.set_xticks([D_TC - 24, D_TC - 16, D_TC - 8, D_TC])
ax.set_xticklabels(['24', '16', '8', '0'])
ax.set_xlabel(r'Days before the failure point $t_c$', fontsize=15.0)
ax.set_ylabel('Oscillation about the envelope (m)', fontsize=15.0)
ax.set_title('(b) The oscillation speeds up towards $t_c$',
             fontsize=16.2, pad=8)
ax.legend(loc='upper left', fontsize=12.3, framealpha=0.92)
ax.tick_params(labelsize=13.7)
ax.grid(alpha=0.2, lw=0.7)
ax.text(D_TC - 25, -0.47,
        'predicted  $t_c$ = 28 Mar 00:18 $\\pm$ 2:11\nfirst large earthquake = 00:23',
        fontsize=13.0, color='#333333')

fig.suptitle('A well approaching a critical point:  Usu volcano, 2000',
             fontsize=17.6, y=0.975)
fig.savefig('fig5_precursor.png', dpi=200, bbox_inches='tight')
print('saved fig5_precursor.png')
