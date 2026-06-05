"""
darcy_model.py — 地下水科学入門 #3 用のFloPyモデル実行・作図スクリプト

MODFLOW 6 を使用して1次元ダルシーモデルを構築・実行し、
水頭分布の図（darcy_head_distribution.png）を生成します。

使い方:
  python darcy_model.py

事前準備:
  - pip install flopy matplotlib numpy
  - mf6.exe をパスに通すか、下のパスを修正してください。
"""

import flopy
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ===========================================================
# デザインシステム（#1, #2 のスタイルと統一）
# ===========================================================
BG_COLOR    = '#F5F5F5'  # Slightly grayish background for the figure
AXES_COLOR  = '#FCFCFC'  # Almost white/very light gray for the plot area
TEXT_COLOR  = '#222222'  # Dark gray for text
TITLE_COLOR = '#111111'  # Almost black for titles
BLUE_MAIN   = '#1E64C8'  # Classic scientific blue
BLUE_DARK   = '#144285'  # Dark blue
ORANGE      = '#D95F02'  # Classic scientific orange
GRID_COLOR  = '#E0E0E0'  # Light gray for grid
SPINE_COLOR = '#555555'  # Gray for axes border

plt.rcParams.update({
    'font.family': 'Times New Roman',
    'axes.unicode_minus': False,
    'figure.facecolor': BG_COLOR,
    'axes.facecolor': AXES_COLOR,
    'text.color': TEXT_COLOR,
    'axes.labelcolor': TEXT_COLOR,
    'xtick.color': TEXT_COLOR,
    'ytick.color': TEXT_COLOR,
})

# ===========================================================
# 1. MODFLOW 6 モデルの構築
# ===========================================================
name = "darcy_1d"
ws = Path("./model_ws").resolve()
ws.mkdir(exist_ok=True)

# MODFLOW 6 実行ファイルのパス（環境に合わせて修正）
mf6_exe = r"D:\Hityu\Code_ex\mf6.exe"

sim = flopy.mf6.MFSimulation(sim_name=name, sim_ws=str(ws), exe_name=mf6_exe)

# 時間設定（定常流: 1応力期, 1タイムステップ）
tdis = flopy.mf6.ModflowTdis(sim, time_units="DAYS", perioddata=[(1.0, 1, 1.0)])

# ソルバー
ims = flopy.mf6.ModflowIms(sim, complexity="SIMPLE")

# 地下水流動モデル（GWF）
gwf = flopy.mf6.ModflowGwf(sim, modelname=name, save_flows=True)

# 空間離散化（DIS）: 1層, 1行, 10列
Lx = 100.0
nlay, nrow, ncol = 1, 1, 10
delr = Lx / ncol   # セル幅 = 10 m
delc = 10.0
top  = 15.0
botm = 0.0

dis = flopy.mf6.ModflowGwfdis(
    gwf,
    nlay=nlay, nrow=nrow, ncol=ncol,
    delr=delr, delc=delc,
    top=top, botm=botm,
)

# 透水係数（NPF）
k = 10.0
npf = flopy.mf6.ModflowGwfnpf(gwf, k=k)

# 初期条件（IC）
ic = flopy.mf6.ModflowGwfic(gwf, strt=10.0)

# 境界条件（CHD: 固定水頭）
chd_spd = [[(0, 0, 0), 10.0], [(0, 0, ncol - 1), 5.0]]
chd = flopy.mf6.ModflowGwfchd(gwf, stress_period_data=chd_spd, save_flows=True)

# 出力制御（OC）
oc = flopy.mf6.ModflowGwfoc(
    gwf,
    head_filerecord=f"{name}.hds",
    budget_filerecord=f"{name}.cbc",
    saverecord=[("HEAD", "ALL"), ("BUDGET", "ALL")],
)

# ===========================================================
# 2. モデル実行
# ===========================================================
sim.write_simulation()
success, buff = sim.run_simulation()

if not success:
    raise RuntimeError(
        "MODFLOW 6 の実行に失敗しました。mf6.exe の配置を確認してください。"
    )

# ===========================================================
# 3. 水頭分布の可視化
# ===========================================================
head = gwf.output.head().get_data()
x_centers = np.linspace(delr / 2, Lx - delr / 2, ncol)

fig, ax = plt.subplots(figsize=(10, 5))

# MODFLOW Head（セル中心）
ax.plot(
    x_centers, head[0, 0, :],
    marker='o', color=BLUE_MAIN, markersize=6,
    linestyle='-', linewidth=2.0, zorder=5,
    label='MODFLOW Head (Cell Center)'
)

# 解析解（カラム端のx=0～100の全域）
x_analytic = np.array([0, Lx])
h_analytic  = np.array([10, 5])
ax.plot(
    x_analytic, h_analytic,
    color=ORANGE, linestyle='-', linewidth=2.0,
    label='Analytical Solution (Boundary Based)', zorder=4
)

# セル中心の境界位置を示す縦破線
for xv in [delr / 2, Lx - delr / 2]:
    ax.axvline(x=xv, color='#888888', linestyle='--', alpha=0.7, linewidth=1.8)

# 境界面の位置を示す矢印（空間離散化誤差の可視化）
ax.annotate(
    '', xy=(5, 4.4), xytext=(0, 4.4),
    arrowprops=dict(arrowstyle='<->', color=TEXT_COLOR, lw=1.2),
)
ax.text(2.5, 4.5, 'Δx/2', ha='center', va='bottom', fontsize=11,
        color=TEXT_COLOR, fontweight='bold')

ax.annotate(
    '', xy=(100, 4.4), xytext=(95, 4.4),
    arrowprops=dict(arrowstyle='<->', color=TEXT_COLOR, lw=1.2),
)
ax.text(97.5, 4.5, 'Δx/2', ha='center', va='bottom', fontsize=11,
        color=TEXT_COLOR, fontweight='bold')

# 軸・タイトル設定
ax.set_title(
    'Head Distribution in 1D Darcy Model: MODFLOW vs. Analytical Solution',
    fontsize=15, color=TITLE_COLOR, pad=12
)
ax.set_xlabel('Distance x [m]', fontsize=13, labelpad=8)
ax.set_ylabel('Head h [m]', fontsize=13, labelpad=8)
ax.set_xlim(-5, 105)
ax.set_ylim(4.0, 11.0)

ax.legend(fontsize=11, facecolor='white', framealpha=1.0,
          edgecolor='#CCCCCC', loc='upper right')

# クリーンなグリッド線（点線）
ax.grid(axis='both', alpha=0.6, color=GRID_COLOR, linestyle=':', linewidth=1.7, zorder=0)

# スパイン（枠線）を全周表示し、色と太さを設定
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_color(SPINE_COLOR)
    spine.set_linewidth(1.8)

ax.tick_params(labelsize=11, color=SPINE_COLOR, direction='out')

plt.tight_layout()
plt.savefig('darcy_head_distribution.png', dpi=300, bbox_inches='tight',
            facecolor=BG_COLOR)
plt.close()
print("[OK] Saved darcy_head_distribution.png")

# ===========================================================
# 4. 流量バランスの確認
# ===========================================================
cbc = gwf.output.budget()
chd_flux = cbc.get_data(text='CHD', totim=1.0)[0]

q_in  = chd_flux[chd_flux['q'] > 0]['q'].sum()
q_out = chd_flux[chd_flux['q'] < 0]['q'].sum()

print(f"\n--- Flow Budget ---")
print(f"CHD Inflow:   {q_in:+.4f} m^3/day")
print(f"CHD Outflow:  {q_out:+.4f} m^3/day")
print(f"Mass balance: {abs(q_in + q_out):.2e} m^3/day")

# セル中心ベースの比流量
q_cell = -k * (head[0, 0, -1] - head[0, 0, 0]) / ((ncol - 1) * delr)
print(f"\nSpecific discharge (cell-center basis): {q_cell:.4f} m/day")
print(f"Specific discharge (analytical, 100m):  0.5000 m/day")
print(f"Discretization error: {abs(q_cell - 0.5)/0.5*100:.1f}%")
