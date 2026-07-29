# -*- coding: utf-8 -*-
"""
地下水科学入門 #10（時系列解析のまとめ）の図生成スクリプト。
- 独立スクリプトでPNGを事前生成し、index.qmd からは静的参照する（CLAUDE.mdルール）。
- 図中ラベルは文字化け回避のため英語。
- 出力: toolbox_map.png （時系列解析ツールボックスの判断ガイド図／サムネ兼用）
"""
import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "axes.unicode_minus": False,
    "figure.dpi": 150,
    "savefig.bbox": "tight",
})

NAVY, BLUE, CYAN = "#1A365D", "#2563EB", "#00B4D8"
RED, ORANGE, PURPLE = "#DC2626", "#EA580C", "#7C3AED"
INK, GRID, PANEL = "#374151", "#CBD5E1", "#F8F9FA"

HERE = os.path.dirname(os.path.abspath(__file__))

# (question, tool, what it reveals, field case, accent)
ROWS = [
    ("Find the periodicity",   "FFT / Spectral analysis",         "Dominant tidal &\nbarometric periods", "#6 Beppu\n#7 Minami-Daito", CYAN),
    ("Measure the time lag",   "Cross-correlation /\nwavelet",     "Propagation delay\n& phase",           "#8 Tonle Sap",              BLUE),
    ("Get aquifer properties", "Tidal method /\nbarometric eff.",  "Hydraulic conductivity,\ndiffusivity", "#7, #9 Minami-Daito",       PURPLE),
    ("Reproduce & predict",    "Lag-based regression",             "Reconstructed\nwater level",           "#9 Minami-Daito",           ORANGE),
]
COLS = ["The question", "The tool", "What it reveals", "Field case"]

# レイアウト
x0, colw, gap = 0.5, 3.5, 0.35
xs = [x0 + i * (colw + gap) for i in range(4)]
rowh, rgap = 1.55, 0.45
y_top = 8.9
ys = [y_top - r * (rowh + rgap) for r in range(4)]

fig, ax = plt.subplots(figsize=(15, 9))
ax.set_xlim(0, xs[-1] + colw + 0.5)
ax.set_ylim(0, 11.0)
ax.axis("off")

# タイトル
ax.text((xs[0] + xs[-1] + colw) / 2, 10.6,
        "Groundwater Time-Series Toolbox",
        ha="center", va="center", fontsize=22, fontweight="bold", color=NAVY)
ax.text((xs[0] + xs[-1] + colw) / 2, 10.1,
        "One water-level record  →  the hidden properties of the aquifer",
        ha="center", va="center", fontsize=12.5, color=INK, style="italic")

# 列ヘッダー
for cx, title in zip(xs, COLS):
    ax.text(cx + colw / 2, y_top + 0.34, title.upper(),
            ha="center", va="center", fontsize=11.5, fontweight="bold", color=NAVY)

def box(x, y, w, h, text, face, edge, tcolor, fs=12, weight="normal"):
    ax.add_patch(FancyBboxPatch((x, y - h), w, h,
                 boxstyle="round,pad=0.02,rounding_size=0.12",
                 linewidth=1.6, edgecolor=edge, facecolor=face))
    ax.text(x + w / 2, y - h / 2, text, ha="center", va="center",
            fontsize=fs, color=tcolor, fontweight=weight, wrap=True)

for r, (q, tool, reveal, case, accent) in enumerate(ROWS):
    y = ys[r]
    # Q列（濃いアクセント）
    box(xs[0], y, colw, rowh, q, accent, accent, "white", fs=13, weight="bold")
    # tool列（淡色＋アクセント枠）
    box(xs[1], y, colw, rowh, tool, PANEL, accent, INK, fs=12, weight="bold")
    # reveal列
    box(xs[2], y, colw, rowh, reveal, "white", GRID, INK, fs=11.5)
    # case列
    box(xs[3], y, colw, rowh, case, "white", GRID, accent, fs=11.5, weight="bold")
    # 矢印（列間）
    for i in range(3):
        ax.annotate("", xy=(xs[i + 1], y - rowh / 2), xytext=(xs[i] + colw, y - rowh / 2),
                    arrowprops=dict(arrowstyle="-|>", color=accent, lw=1.8))

# フッター
ax.text((xs[0] + xs[-1] + colw) / 2, 0.35,
        "No pumping test required — read the aquifer from existing monitoring data.",
        ha="center", va="center", fontsize=12, color=NAVY, fontweight="bold")

out = os.path.join(HERE, "toolbox_map.png")
fig.savefig(out, facecolor="white")
print("saved:", out)
