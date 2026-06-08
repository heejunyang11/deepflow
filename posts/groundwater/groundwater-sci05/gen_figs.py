import os
import numpy as np
import matplotlib.pyplot as plt

# Create output directories if they don't exist
os.makedirs("d:/Hityu/GROUNDWATER_proj/groundwater-sci05", exist_ok=True)

# Font settings for Japanese support
plt.rcParams['font.family'] = ['Yu Gothic', 'Hiragino Sans', 'Noto Sans CJK JP', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Premium Color Palette
BG_COLOR = '#F8F9FA'
TEXT_COLOR = '#2D3748'
TITLE_COLOR = '#1A365D'
RIVER_COLOR = '#00B4D8'
GW_COLOR = '#0077B6'
AQUIFER_COLOR = '#CBD5E0'
BASEFLOW_COLOR = '#90E0EF'
QUICKFLOW_COLOR = '#F6AD55'
GRID_COLOR = '#E2E8F0'

def draw_gaining_losing_diagrams(lang='ja'):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor(BG_COLOR)

    # Common layout settings
    for ax in axes:
        ax.set_facecolor(BG_COLOR)
        ax.set_xlim(-10, 10)
        ax.set_ylim(-5, 5)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

    # 1. Gaining Stream (得水河川)
    ax = axes[0]
    # Draw aquifer fill
    x_terrain = np.linspace(-10, 10, 100)
    y_terrain = 2 + 0.02 * x_terrain**2  # Muted valley shape
    ax.fill_between(x_terrain, -5, y_terrain, color='#E2E8F0', alpha=0.7, label='Aquifer' if lang=='en' else '帯水層')
    
    # Draw river water body (center)
    river_x = np.linspace(-1.5, 1.5, 50)
    river_y = 2.05 - 0.2 * (river_x)**2
    ax.fill_between(river_x, river_y, 1.5, color=RIVER_COLOR, alpha=0.9, zorder=5)
    ax.plot([-1.5, 1.5], [1.5, 1.5], color='#0077B6', linewidth=2, zorder=6) # River surface

    # Draw groundwater table (Higher than river water level)
    # The water table meets the river at the bank (x = -1.5, y = 1.5 and x = 1.5, y = 1.5)
    x_gw_l = np.linspace(-10, -1.5, 50)
    y_gw_l = 1.5 + 0.03 * (x_gw_l + 1.5)**2
    x_gw_r = np.linspace(1.5, 10, 50)
    y_gw_r = 1.5 + 0.03 * (x_gw_r - 1.5)**2
    ax.plot(x_gw_l, y_gw_l, color=GW_COLOR, linestyle='--', linewidth=2.5, zorder=4)
    ax.plot(x_gw_r, y_gw_r, color=GW_COLOR, linestyle='--', linewidth=2.5, zorder=4)

    # Draw flow arrows (GW -> River)
    ax.annotate("", xy=(-1.0, 1.2), xytext=(-3.0, 1.8),
                arrowprops=dict(arrowstyle="->", color=TITLE_COLOR, lw=2, connectionstyle="arc3,rad=-0.1"))
    ax.annotate("", xy=(1.0, 1.2), xytext=(3.0, 1.8),
                arrowprops=dict(arrowstyle="->", color=TITLE_COLOR, lw=2, connectionstyle="arc3,rad=0.1"))

    # Labels
    if lang == 'ja':
        ax.set_title("得水河川 (Gaining Stream)\n- 地下水位 > 河川水位 -", fontsize=16, fontweight='bold', color=TITLE_COLOR)
        ax.text(-6, 2.5, "地下水面\n(高い)", color=GW_COLOR, fontsize=12, fontweight='bold', ha='center')
        ax.text(0, 0.7, "川へ流入\n(湧出)", color=TITLE_COLOR, fontsize=12, fontweight='bold', ha='center')
        ax.text(0, 2.2, "河川", color='#FFFFFF', fontsize=12, fontweight='bold', ha='center', zorder=7)
    else:
        ax.set_title("Gaining Stream\n- Water Table > River Stage -", fontsize=16, fontweight='bold', color=TITLE_COLOR)
        ax.text(-6, 2.5, "Water Table\n(High)", color=GW_COLOR, fontsize=12, fontweight='bold', ha='center')
        ax.text(0, 0.7, "Inflow from\nGroundwater", color=TITLE_COLOR, fontsize=12, fontweight='bold', ha='center')
        ax.text(0, 2.2, "River", color='#FFFFFF', fontsize=12, fontweight='bold', ha='center', zorder=7)

    # 2. Losing Stream (失水河川)
    ax = axes[1]
    # Draw aquifer fill (flatter terrain for losing stream)
    y_terrain_lose = 1.8 - 0.005 * x_terrain**2
    ax.fill_between(x_terrain, -5, y_terrain_lose, color='#E2E8F0', alpha=0.7)

    # Draw river water body
    ax.fill_between(river_x, river_y, 1.5, color=RIVER_COLOR, alpha=0.9, zorder=5)
    ax.plot([-1.5, 1.5], [1.5, 1.5], color='#0077B6', linewidth=2, zorder=6) # River surface

    # Draw groundwater table (Lower than river water level)
    # The water table is below the riverbed, representing a connected losing stream
    x_gw_l_lose = np.linspace(-10, -1.5, 50)
    y_gw_l_lose = 1.0 - 0.02 * (x_gw_l_lose + 1.5)**2
    x_gw_r_lose = np.linspace(1.5, 10, 50)
    y_gw_r_lose = 1.0 - 0.02 * (x_gw_r_lose - 1.5)**2
    
    # We join them under the river bed smoothly
    x_under = np.linspace(-1.5, 1.5, 20)
    y_under = 1.0 - 0.1 * x_under**2
    
    ax.plot(x_gw_l_lose, y_gw_l_lose, color=GW_COLOR, linestyle='--', linewidth=2.5, zorder=4)
    ax.plot(x_gw_r_lose, y_gw_r_lose, color=GW_COLOR, linestyle='--', linewidth=2.5, zorder=4)
    ax.plot(x_under, y_under, color=GW_COLOR, linestyle='--', linewidth=2.5, zorder=4)

    # Draw flow arrows (River -> GW)
    ax.annotate("", xy=(-3.0, 0.5), xytext=(-0.8, 1.1),
                arrowprops=dict(arrowstyle="->", color=TITLE_COLOR, lw=2, connectionstyle="arc3,rad=-0.1"))
    ax.annotate("", xy=(3.0, 0.5), xytext=(0.8, 1.1),
                arrowprops=dict(arrowstyle="->", color=TITLE_COLOR, lw=2, connectionstyle="arc3,rad=0.1"))

    # Labels
    if lang == 'ja':
        ax.set_title("失水河川 (Losing Stream)\n- 地下水位 < 河川水位 -", fontsize=16, fontweight='bold', color=TITLE_COLOR)
        ax.text(-6, -0.3, "地下水面\n(低い)", color=GW_COLOR, fontsize=12, fontweight='bold', ha='center')
        ax.text(0, -0.5, "地下へ浸透\n(涵養)", color=TITLE_COLOR, fontsize=12, fontweight='bold', ha='center')
        ax.text(0, 2.2, "河川", color='#FFFFFF', fontsize=12, fontweight='bold', ha='center', zorder=7)
    else:
        ax.set_title("Losing Stream\n- Water Table < River Stage -", fontsize=16, fontweight='bold', color=TITLE_COLOR)
        ax.text(-6, -0.3, "Water Table\n(Low)", color=GW_COLOR, fontsize=12, fontweight='bold', ha='center')
        ax.text(0, -0.5, "Outflow to\nGroundwater", color=TITLE_COLOR, fontsize=12, fontweight='bold', ha='center')
        ax.text(0, 2.2, "River", color='#FFFFFF', fontsize=12, fontweight='bold', ha='center', zorder=7)

    plt.suptitle("河川と地下水の水理的関係" if lang=='ja' else "Hydraulic Relationship Between River and Groundwater", 
                 fontsize=20, fontweight='heavy', y=0.98, color=TITLE_COLOR)
    plt.tight_layout()
    
    filename = f"d:/Hityu/GROUNDWATER_proj/groundwater-sci05/fig-gaining-losing{'' if lang=='ja' else '-en'}.png"
    plt.savefig(filename, dpi=150, facecolor=BG_COLOR)
    plt.close()
    print(f"Saved: {filename}")

def run_baseflow_separation(lang='ja'):
    # Generate mock hydrograph data
    np.random.seed(42)
    days = 90
    t = np.arange(days)
    
    # Baseflow: slow seasonal recession
    baseflow_true = 15.0 * np.exp(-t / 120.0) + 5.0 * np.sin(2.0 * np.pi * t / 365.0) + 10.0
    
    # Quickflow: storm events
    quickflow = np.zeros(days)
    storm_days = [15, 45, 70]
    storm_magnitudes = [45.0, 60.0, 35.0]
    
    for sd, mag in zip(storm_days, storm_magnitudes):
        # Exponential rise and fall
        for i in range(days):
            if i >= sd:
                quickflow[i] += mag * np.exp(-(i - sd) / 3.0)
                
    # Total streamflow
    total_flow = baseflow_true + quickflow + np.random.normal(0, 0.5, days)
    total_flow = np.clip(total_flow, 1.0, None)
    
    # Lyne-Hollick Digital Filter
    # Forward-Backward pass for zero phase-shift
    alpha = 0.925
    
    # Pass 1 (Forward)
    q_f = np.zeros(days)
    for i in range(1, days):
        q_f[i] = alpha * q_f[i-1] + 0.5 * (1 + alpha) * (total_flow[i] - total_flow[i-1])
        if q_f[i] < 0:
            q_f[i] = 0
        elif q_f[i] > total_flow[i]:
            q_f[i] = total_flow[i]
            
    # Pass 2 (Backward)
    q_b = np.zeros(days)
    for i in range(days-2, -1, -1):
        q_b[i] = alpha * q_b[i+1] + 0.5 * (1 + alpha) * (total_flow[i] - total_flow[i+1])
        if q_b[i] < 0:
            q_b[i] = 0
        elif q_b[i] > total_flow[i]:
            q_b[i] = total_flow[i]
            
    # Average quickflow
    q_est = 0.5 * (q_f + q_b)
    # Ensure constraint
    q_est = np.clip(q_est, 0, total_flow)
    
    # Estimated Baseflow
    baseflow_est = total_flow - q_est

    # Plot
    fig, ax = plt.subplots(figsize=(12, 6.5))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    # Plot lines
    ax.plot(t, total_flow, color=TITLE_COLOR, linewidth=2, label="総河川流量 $Q(t)$" if lang=='ja' else "Total Streamflow $Q(t)$", zorder=4)
    
    # Area fills
    ax.fill_between(t, 0, baseflow_est, color=BASEFLOW_COLOR, alpha=0.8, label="推定基底流量 (地下水流出)" if lang=='ja' else "Estimated Baseflow (GW Discharge)", zorder=3)
    ax.fill_between(t, baseflow_est, total_flow, color=QUICKFLOW_COLOR, alpha=0.5, label="推定直接流出 (降雨流出)" if lang=='ja' else "Estimated Quickflow (Surface Runoff)", zorder=2)

    # Aesthetics
    ax.set_xlabel("経過日数 (Days)" if lang=='ja' else "Elapsed Days", fontsize=13, fontweight='bold', color=TEXT_COLOR)
    ax.set_ylabel("流量 ($m^3/s$)" if lang=='ja' else "Discharge ($m^3/s$)", fontsize=13, fontweight='bold', color=TEXT_COLOR)
    ax.set_title("ハイドログラフの基底流量分離 (Lyne-Hollick デジタルフィルタ)" if lang=='ja' else "Hydrograph Baseflow Separation (Lyne-Hollick Digital Filter)", 
                 fontsize=18, fontweight='bold', color=TITLE_COLOR, pad=15)
    
    ax.set_xlim(0, days-1)
    ax.set_ylim(0, 100)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CBD5E0')
    ax.spines['bottom'].set_color('#CBD5E0')
    ax.tick_params(colors=TEXT_COLOR, labelsize=11)
    ax.grid(axis='y', alpha=0.4, color=GRID_COLOR, zorder=1, linestyle='--')
    ax.grid(axis='x', alpha=0.4, color=GRID_COLOR, zorder=1, linestyle='--')

    # Legend
    ax.legend(loc="upper right", fontsize=11, frameon=True, facecolor=BG_COLOR, edgecolor='#CBD5E0')

    # Add text annotation
    if lang == 'ja':
        ax.text(20, 75, r"$\alpha = 0.925$ (双方向パス)", fontsize=12, color=TITLE_COLOR, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", fc="#FFFFFF", ec="#CBD5E0", lw=1))
    else:
        ax.text(20, 75, r"$\alpha = 0.925$ (Forward-Backward)", fontsize=12, color=TITLE_COLOR, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", fc="#FFFFFF", ec="#CBD5E0", lw=1))

    plt.tight_layout()
    filename = f"d:/Hityu/GROUNDWATER_proj/groundwater-sci05/fig-baseflow-sep{'' if lang=='ja' else '-en'}.png"
    plt.savefig(filename, dpi=150, facecolor=BG_COLOR)
    plt.close()
    print(f"Saved: {filename}")

if __name__ == "__main__":
    draw_gaining_losing_diagrams('ja')
    draw_gaining_losing_diagrams('en')
    run_baseflow_separation('ja')
    run_baseflow_separation('en')
