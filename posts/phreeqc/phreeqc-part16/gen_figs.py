import os
import numpy as np
import matplotlib.pyplot as plt

# Font settings for Japanese support
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['MS Gothic', 'Meiryo', 'Yu Gothic', 'Hiragino Sans', 'Noto Sans CJK JP']
plt.rcParams['axes.unicode_minus'] = False

# Premium Color Palette
BG_COLOR = '#F8F9FA'
TEXT_COLOR = '#2D3748'
TITLE_COLOR = '#1A365D'
CA_COLOR = '#2B6CB0'  # Blue
SI_COLOR = '#C53030'  # Red
GRID_COLOR = '#E2E8F0'

def run_kinetics_simulation(lang='ja'):
    if lang == 'ja':
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['MS Gothic', 'Meiryo', 'Yu Gothic', 'Hiragino Sans', 'Noto Sans CJK JP']
    else:
        plt.rcParams['font.family'] = 'serif'
        plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']

    # Generate mock kinetics data for Calcite dissolution
    t = np.linspace(0, 10, 200) # 0 to 10 days
    k = 0.6 # rate constant
    
    # Ca concentration (mmol/kgw) approaches 1.5
    Ca_eq = 1.5
    Ca_t = Ca_eq * (1 - np.exp(-k * t))
    
    # SI Calcite approaches 0
    # Simplification: SI ~ log10( (Ca_t/Ca_eq)^2 ) if Ca and CO3 increase together
    # To avoid log(0), we add a small initial concentration
    Ca_t_si = np.clip(Ca_t, 0.01, None)
    SI_t = 2.0 * np.log10(Ca_t_si / Ca_eq)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor(BG_COLOR)
    
    # Common settings
    for ax in axes:
        ax.set_facecolor(BG_COLOR)
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(True)
        for spine in ax.spines.values():
            spine.set_color('black')
            spine.set_linewidth(2)
        ax.tick_params(colors=TEXT_COLOR, labelsize=14)
        ax.grid(alpha=0.4, color=GRID_COLOR, zorder=1, linestyle='--')
        ax.set_xlim(0, 10)
    
    # Plot 1: Ca Concentration
    ax1 = axes[0]
    ax1.plot(t, Ca_t, color=CA_COLOR, linewidth=3, zorder=3)
    ax1.fill_between(t, 0, Ca_t, color=CA_COLOR, alpha=0.1, zorder=2)
    ax1.axhline(Ca_eq, color='#A0AEC0', linestyle='--', linewidth=2, zorder=2)
    
    if lang == 'ja':
        ax1.set_xlabel("経過時間 (Days)", fontsize=18, fontweight='bold', color=TEXT_COLOR)
        ax1.set_ylabel("Ca²⁺ 濃度 (mmol/kgw)", fontsize=18, fontweight='bold', color=TEXT_COLOR)
        ax1.set_title("Calciteの溶解：Ca濃度の時間変化", fontsize=20, fontweight='bold', color=TITLE_COLOR, pad=15)
        ax1.text(6, 1.55, "平衡濃度 (Equilibrium)", color='#718096', fontsize=14, fontweight='bold')
    else:
        ax1.set_xlabel("Elapsed Time (Days)", fontsize=18, fontweight='bold', color=TEXT_COLOR)
        ax1.set_ylabel("Ca²⁺ Concentration (mmol/kgw)", fontsize=18, fontweight='bold', color=TEXT_COLOR)
        ax1.set_title("Calcite Dissolution: Ca Concentration vs Time", fontsize=20, fontweight='bold', color=TITLE_COLOR, pad=15)
        ax1.text(6, 1.55, "Equilibrium", color='#718096', fontsize=14, fontweight='bold')
    
    ax1.set_ylim(0, 2.0)
    
    # Plot 2: Saturation Index
    ax2 = axes[1]
    ax2.plot(t, SI_t, color=SI_COLOR, linewidth=3, zorder=3)
    ax2.fill_between(t, -5, SI_t, color=SI_COLOR, alpha=0.1, zorder=2)
    ax2.axhline(0, color='#A0AEC0', linestyle='--', linewidth=2, zorder=2)
    
    if lang == 'ja':
        ax2.set_xlabel("経過時間 (Days)", fontsize=18, fontweight='bold', color=TEXT_COLOR)
        ax2.set_ylabel("飽和指数 (SI Calcite)", fontsize=18, fontweight='bold', color=TEXT_COLOR)
        ax2.set_title("Calciteの溶解：飽和指数の時間変化", fontsize=20, fontweight='bold', color=TITLE_COLOR, pad=15)
        ax2.text(7, 0.1, "平衡 (SI = 0)", color='#718096', fontsize=14, fontweight='bold')
    else:
        ax2.set_xlabel("Elapsed Time (Days)", fontsize=18, fontweight='bold', color=TEXT_COLOR)
        ax2.set_ylabel("Saturation Index (SI Calcite)", fontsize=18, fontweight='bold', color=TEXT_COLOR)
        ax2.set_title("Calcite Dissolution: Saturation Index vs Time", fontsize=20, fontweight='bold', color=TITLE_COLOR, pad=15)
        ax2.text(7, 0.1, "Equilibrium (SI = 0)", color='#718096', fontsize=14, fontweight='bold')
        
    ax2.set_ylim(-4, 1.0)

    plt.tight_layout(pad=3.0)
    filename = f"d:/Hityu/deepflow/posts/phreeqc/phreeqc-part16/fig-kinetics-calcite{'' if lang=='ja' else '-en'}.png"
    plt.savefig(filename, dpi=150, facecolor=BG_COLOR)
    plt.close()
    print(f"Saved: {filename}")

if __name__ == "__main__":
    run_kinetics_simulation('ja')
    run_kinetics_simulation('en')
