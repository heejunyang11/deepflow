import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# フォント設定
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans"],
    "axes.unicode_minus": False,
    "figure.dpi": 150,
})

# ---- 実データの読み込み ----
df = pd.read_csv("BP.csv", parse_dates=["Date"], index_col="Date")

# データの抽出
t = df.index
gwl_ow1 = df["OW1"]
gwl_ow2 = df["OW2"]
baro = df["Baro"]

# Figure
fig, axes = plt.subplots(2, 1, figsize=(13, 7), sharex=True)
fig.patch.set_facecolor("#F8F9FA")

# 上：地下水位
ax1 = axes[0]
ax1.set_facecolor("#F0F4F8")
ax1.plot(t, gwl_ow1, lw=0.8, color="#2563EB", label="OW 1", alpha=0.9)
ax1.plot(t, gwl_ow2, lw=0.8, color="#DC2626", label="OW 2", alpha=0.9)
ax1.set_ylabel("Groundwater Level (m a.s.l.)", fontsize=10)
ax1.legend(fontsize=9, loc="upper right")
ax1.grid(True, ls="--", lw=0.4, color="#CBD5E1")
ax1.set_title("Unconfined Groundwater Level in Southern Beppu (2017-2018)", fontsize=12)

# 下：気圧
ax2 = axes[1]
ax2.set_facecolor("#F0F4F8")
ax2.plot(t, baro, lw=0.8, color="#374151", label="Barometric Pressure", alpha=0.85)
ax2.set_ylabel("Pressure (hPa)", fontsize=10)
ax2.set_xlabel("Date", fontsize=10)
ax2.legend(fontsize=9, loc="upper right")
ax2.grid(True, ls="--", lw=0.4, color="#CBD5E1")
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d\n%Y"))

plt.tight_layout()
plt.savefig("beppu_gwl_overview-en2.png", bbox_inches="tight")
print("Saved real data plot to beppu_gwl_overview-en2.png")
