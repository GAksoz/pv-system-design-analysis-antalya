# ============================================================
#  22 kWp PV System — Performance Analysis
#  Antalya, Turkey
#  Author: Gani Aksöz
# ============================================================

# --- LIBRARIES ---
# pandas  : data loading, table operations (Excel, CSV, etc.)
# numpy   : numerical computations
# matplotlib : plotting and visualization
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ============================================================
# 1. DEFINE DATA
#    Source: PVsyst V8.0.20 simulation report — E_Grid column
#    (energy injected into grid, page 4 of the simulation report)
#    In production code you would load this with:
#    df = pd.read_excel("monthly_production.xlsx")
# ============================================================

months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# E_Grid values from PVsyst simulation report (kWh) — verified source of truth
energy_kwh = [1485, 1621, 2472, 2969, 3601, 3866,
              3942, 3550, 3015, 2174, 1605, 1312]

# DataFrame: pandas' core data structure — think of it as a Python spreadsheet
df = pd.DataFrame({
    "Month": months,
    "Energy_kWh": energy_kwh
})

# Add a numeric month index (January=1 ... December=12)
df["Month_Num"] = range(1, 13)

# ============================================================
# 2. KEY CALCULATIONS
#    pandas makes column-level statistics straightforward
# ============================================================

system_kwp        = 22.0    # installed DC capacity
system_area_m2    = 105     # total panel area (m²)
performance_ratio = 84.29   # PVsyst Performance Ratio (%)

total_annual_kwh = df["Energy_kWh"].sum()                        # total yearly output
avg_monthly_kwh  = df["Energy_kWh"].mean()                       # average monthly output
peak_month       = df.loc[df["Energy_kWh"].idxmax(), "Month"]    # highest producing month
lowest_month     = df.loc[df["Energy_kWh"].idxmin(), "Month"]    # lowest producing month
specific_yield   = total_annual_kwh / system_kwp                 # kWh per installed kWp

print("=" * 50)
print("  22 kWp PV SYSTEM — ANNUAL SUMMARY")
print("=" * 50)
print(f"  Total Annual Energy   : {total_annual_kwh:,} kWh")
print(f"  Specific Yield        : {specific_yield:.1f} kWh/kWp")
print(f"  Avg Monthly Output    : {avg_monthly_kwh:.0f} kWh")
print(f"  Peak Month            : {peak_month}")
print(f"  Lowest Month          : {lowest_month}")
print(f"  Performance Ratio     : {performance_ratio}%")
print("=" * 50)

# ============================================================
# 3. VISUALIZATIONS
#    We create a 2x2 subplot dashboard using matplotlib.
#    fig, axes → used when drawing multiple plots at once.
# ============================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 9))
fig.suptitle("22 kWp PV System — Performance Analysis\nAntalya, Turkey",
             fontsize=15, fontweight="bold", y=1.01)
fig.patch.set_facecolor("#F8F9FA")

# Color scheme: blue for peak month, red for lowest, light blue for the rest
colors = [
    "#1565C0" if e == max(energy_kwh) else
    "#EF5350" if e == min(energy_kwh) else
    "#42A5F5"
    for e in energy_kwh
]

# --- CHART 1: Monthly Energy Production (Bar Chart) ---
ax1 = axes[0, 0]
bars = ax1.bar(df["Month"], df["Energy_kWh"], color=colors,
               edgecolor="white", linewidth=0.8)
ax1.set_title("Monthly Energy Production", fontweight="bold", pad=10)
ax1.set_ylabel("Energy (kWh)")
ax1.set_facecolor("#F0F4F8")
ax1.tick_params(axis="x", rotation=45)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

# Annotate each bar with its value
for bar, val in zip(bars, energy_kwh):
    ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 40,
             f"{val:,}", ha="center", va="bottom", fontsize=7.5, color="#333")
ax1.set_ylim(0, max(energy_kwh) * 1.15)

# --- CHART 2: Cumulative Annual Energy (Line Chart) ---
ax2 = axes[0, 1]
cumulative = df["Energy_kWh"].cumsum()    # cumsum → running total across months
ax2.plot(df["Month"], cumulative, color="#1E88E5", linewidth=2.5, marker="o",
         markersize=5, markerfacecolor="white", markeredgewidth=2)
ax2.fill_between(df["Month"], cumulative, alpha=0.12, color="#1E88E5")
ax2.set_title("Cumulative Annual Energy", fontweight="bold", pad=10)
ax2.set_ylabel("Cumulative Energy (kWh)")
ax2.set_facecolor("#F0F4F8")
ax2.tick_params(axis="x", rotation=45)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

# Annotate the final data point with the total annual output
ax2.annotate(f"{int(cumulative.iloc[-1]):,} kWh",
             xy=(11, cumulative.iloc[-1]),
             xytext=(8, cumulative.iloc[-1] - 3000),
             fontsize=9, color="#1565C0", fontweight="bold",
             arrowprops=dict(arrowstyle="->", color="#1565C0"))

# --- CHART 3: Seasonal Distribution (Pie Chart) ---
ax3 = axes[1, 0]
# Group months into meteorological seasons
seasons = {
    "Winter\n(Dec-Feb)": df.loc[df["Month_Num"].isin([12, 1, 2]),  "Energy_kWh"].sum(),
    "Spring\n(Mar-May)": df.loc[df["Month_Num"].isin([3, 4, 5]),   "Energy_kWh"].sum(),
    "Summer\n(Jun-Aug)": df.loc[df["Month_Num"].isin([6, 7, 8]),   "Energy_kWh"].sum(),
    "Autumn\n(Sep-Nov)": df.loc[df["Month_Num"].isin([9, 10, 11]), "Energy_kWh"].sum(),
}
season_colors = ["#90CAF9", "#A5D6A7", "#FFCC80", "#EF9A9A"]
wedges, texts, autotexts = ax3.pie(
    seasons.values(),
    labels=seasons.keys(),
    colors=season_colors,
    autopct="%1.1f%%",
    startangle=90,
    wedgeprops=dict(edgecolor="white", linewidth=1.5)
)
for at in autotexts:
    at.set_fontsize(9)
    at.set_fontweight("bold")
ax3.set_title("Seasonal Distribution", fontweight="bold", pad=10)

# --- CHART 4: System Summary (Info Panel) ---
ax4 = axes[1, 1]
ax4.set_facecolor("#E3F2FD")
ax4.axis("off")    # turn off axes — we only want to display text
metrics = [
    ("System Size",       f"{system_kwp} kWp"),
    ("Annual Output",     f"{total_annual_kwh:,} kWh"),
    ("Specific Yield",    f"{specific_yield:.0f} kWh/kWp"),
    ("Performance Ratio", f"{performance_ratio}%"),
    ("Peak Month",        peak_month),
    ("Lowest Month",      lowest_month),
    ("Panel Area",        f"{system_area_m2} m²"),
    ("No. of Modules",    "40 × 550 W"),
]
ax4.set_title("System Summary", fontweight="bold", pad=10)
for i, (label, value) in enumerate(metrics):
    y_pos = 0.88 - i * 0.115
    ax4.text(0.05, y_pos, label + ":", fontsize=10, color="#555",
             transform=ax4.transAxes, va="center")
    ax4.text(0.95, y_pos, value, fontsize=10, fontweight="bold",
             color="#1565C0", transform=ax4.transAxes, va="center", ha="right")
    # Draw a thin separator line between rows
    if i < len(metrics) - 1:
        ax4.plot([0.03, 0.97], [y_pos - 0.055, y_pos - 0.055],
                 color="#BBDEFB", linewidth=0.8,
                 transform=ax4.transAxes, clip_on=False)

plt.tight_layout()
plt.savefig("pv_analysis.png", dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
plt.show()
print("\n✓ Chart saved as pv_analysis.png")

# ============================================================
# 4. BASELINE MACHINE LEARNING MODEL (Linear Regression)
#    scikit-learn: the standard Python ML library.
#    We predict monthly energy output from the month number.
#    This is the first ML model type covered in the course —
#    keep this file as a hands-on reference while you learn.
# ============================================================

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# X: input feature (month number), y: target variable (energy output)
X = df[["Month_Num"]]    # must be a 2D array — note the double brackets
y = df["Energy_kWh"]

model = LinearRegression()
model.fit(X, y)           # train the model on our 12 data points

y_pred = model.predict(X)

mae = mean_absolute_error(y, y_pred)
r2  = r2_score(y, y_pred)

print(f"\n  Linear Regression — Baseline Model")
print(f"  Mean Absolute Error  : {mae:.0f} kWh")
print(f"  R² Score             : {r2:.3f}  (1.0 = perfect fit)")
print(f"  Note: A low R² is expected — solar output follows a")
print(f"        sinusoidal pattern, not a linear trend.")
print(f"        As you progress through the course you will learn")
print(f"        better models: polynomial, tree-based, neural nets.")
