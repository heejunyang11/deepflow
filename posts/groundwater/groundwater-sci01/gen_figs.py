import matplotlib.pyplot as plt
import numpy as np

# Font settings
plt.rcParams['font.family'] = ['Yu Gothic', 'Hiragino Sans', 'Noto Sans CJK JP', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Global premium colors
BG_COLOR = '#F8F9FA'
TEXT_COLOR = '#2D3748'
TITLE_COLOR = '#1A365D'

# ==========================================
# Figure 1: Water Distribution (Donut Charts)
# ==========================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor(BG_COLOR)
for ax in axes:
    ax.set_facecolor(BG_COLOR)

# Left: Global Water
sizes_total = [97.5, 2.5]
labels_total = ['海水 (97.5%)', '淡水 (2.5%)']
colors_total = ['#1A365D', '#00B4D8']
explode_total = (0, 0.05)

wedges1, texts1 = axes[0].pie(
    sizes_total, explode=explode_total, labels=labels_total, colors=colors_total,
    startangle=90, pctdistance=0.8,
    textprops={'fontsize': 14, 'fontweight': 'bold', 'color': TEXT_COLOR},
    wedgeprops={'width': 0.35, 'edgecolor': BG_COLOR, 'linewidth': 3}
)
axes[0].text(0, 0, '地球上の水\n全体', ha='center', va='center', 
             fontsize=16, fontweight='bold', color=TITLE_COLOR)
axes[0].set_title('地球上の水の分布', fontsize=18, fontweight='bold', pad=20, color=TITLE_COLOR)

# Right: Freshwater
sizes_fresh = [68.7, 30.1, 0.9, 0.3]
labels_fresh = ['氷河・氷床 (68.7%)', '地下水 (30.1%)', 'その他 (0.9%)', '河川・湖沼 (0.3%)']
colors_fresh = ['#89C2D9', '#0077B6', '#48CAE4', '#90E0EF']
explode_fresh = (0.02, 0.02, 0.02, 0.02)

wedges2, texts2 = axes[1].pie(
    sizes_fresh, explode=explode_fresh, colors=colors_fresh,
    startangle=90,
    wedgeprops={'width': 0.35, 'edgecolor': BG_COLOR, 'linewidth': 2}
)
axes[1].text(0, 0, '淡水\n(2.5%)', ha='center', va='center', 
             fontsize=16, fontweight='bold', color=TITLE_COLOR)
axes[1].set_title('淡水の内訳', fontsize=18, fontweight='bold', pad=20, color=TITLE_COLOR)

# Legend instead of overlapping text
axes[1].legend(wedges2, labels_fresh, loc="center left", bbox_to_anchor=(0.95, 0.5),
               fontsize=13, frameon=False, labelcolor=TEXT_COLOR)

plt.suptitle('地球の水資源：地下水は最大の液体淡水貯留庫', 
             fontsize=22, fontweight='heavy', y=1.05, color=TITLE_COLOR)
plt.tight_layout()
plt.savefig('fig-water-distribution.png', dpi=150, bbox_inches='tight', facecolor=BG_COLOR)
plt.close()


# ==========================================
# Figure 2: Water Budget
# ==========================================
P  = 1668
ET = 730
Q  = 800
R  = P - ET - Q

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

categories = ['降水量 P', '蒸発散 ET', '流出量 Q', '涵養量 R\n(推定)']
values = [P, ET, Q, R]
# Modern cohesive colors
colors = ['#00B4D8', '#F6AD55', '#48CAE4', '#0077B6']

bars = ax.bar(categories, values, color=colors, width=0.55,
              edgecolor=BG_COLOR, linewidth=2, zorder=3)

for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
            f'{val} mm', ha='center', va='bottom', 
            fontsize=13, fontweight='bold', color=TITLE_COLOR)

ax.set_ylabel('mm / year', fontsize=13, color=TEXT_COLOR, fontweight='bold')
ax.set_title('日本の年間水収支（概算）\nP = ET + Q + R', 
             fontsize=18, fontweight='bold', color=TITLE_COLOR, pad=20)
ax.set_ylim(0, 2000)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#CBD5E0')
ax.spines['bottom'].set_color('#CBD5E0')
ax.tick_params(colors=TEXT_COLOR, labelsize=12)
ax.grid(axis='y', alpha=0.4, color='#CBD5E0', zorder=0, linestyle='--')

plt.tight_layout()
plt.savefig('fig-water-budget.png', dpi=150, bbox_inches='tight', facecolor=BG_COLOR)
plt.close()


# ==========================================
# Figure 3: Residence Time
# ==========================================
reservoirs = [
    '大気 (水蒸気)', '土壌水', '河川', '湖沼', 
    '海洋', '氷河・氷床', '地下水 (浅層)', '地下水 (深層)'
]
residence_days = [10, 182, 16, 1825, 1095000, 5840000, 36500, 36500000]

fig, ax = plt.subplots(figsize=(11, 7))
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

y_pos = np.arange(len(reservoirs))
# Muted colors for context, vibrant for groundwater
bar_colors = ['#94A3B8'] * 6 + ['#00B4D8', '#1A365D']

bars = ax.barh(y_pos, residence_days, color=bar_colors, 
               edgecolor=BG_COLOR, linewidth=1.5, zorder=3, height=0.6)

labels_text = ['10日', '約半年', '約2週間', '約5年',
               '約3,000年', '約16,000年', '約100年', '約100,000年']

for i, (bar, label) in enumerate(zip(bars, labels_text)):
    # Bold text for groundwater
    weight = 'bold' if i >= 6 else 'normal'
    color = TITLE_COLOR if i >= 6 else TEXT_COLOR
    ax.text(bar.get_width() * 1.15, bar.get_y() + bar.get_height()/2,
            label, va='center', fontsize=12, fontweight=weight, color=color)

ax.set_yticks(y_pos)
ax.set_yticklabels(reservoirs, fontsize=13, color=TEXT_COLOR)
ax.set_xscale('log')
ax.set_xlabel('滞留時間（日）— 対数スケール', fontsize=13, color=TEXT_COLOR, fontweight='bold', labelpad=15)
ax.set_title('水循環における各リザーバーの滞留時間', 
             fontsize=18, fontweight='bold', color=TITLE_COLOR, pad=20)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#CBD5E0')
ax.spines['bottom'].set_color('#CBD5E0')
ax.tick_params(colors=TEXT_COLOR)
ax.grid(axis='x', alpha=0.4, color='#CBD5E0', zorder=0, linestyle='--')

plt.tight_layout()
plt.savefig('fig-residence-time.png', dpi=150, bbox_inches='tight', facecolor=BG_COLOR)
plt.close()

print("Premium figures generated successfully.")
