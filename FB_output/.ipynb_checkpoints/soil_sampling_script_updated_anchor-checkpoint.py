import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt

# === Configuration ===
field_width = 160
field_height = 270
n_samples = 100
min_distance = 15  # feet
origin_lat = 40.065500
origin_lon = -88.206420

# === GPS Conversion Functions ===
def feet_to_gps_dms(decimal_degrees, feet_per_deg):
    degrees = int(decimal_degrees)
    remainder = (decimal_degrees - degrees) * 60
    minutes = int(remainder)
    seconds = (remainder - minutes) * 60
    return f"{abs(degrees):02d}-{minutes:02d}-{seconds:05.2f}"

def feet_to_decimal_degrees(offset_ft, feet_per_deg):
    return offset_ft / feet_per_deg

# === Rejection Sampling for Soil Samples ===
np.random.seed(42)
accepted_points = []
attempts = 0

while len(accepted_points) < n_samples and attempts < 10000:
    x = np.random.uniform(0, field_width)
    y = np.random.uniform(0, field_height)
    point = np.array([[x, y]])
    if not accepted_points or cdist(point, np.array(accepted_points)).min() >= min_distance:
        accepted_points.append(point[0])
    attempts += 1

points = np.array(accepted_points)
df = pd.DataFrame({
    "SampleID": [f"S{i+1:03}" for i in range(len(points))],
    "X_ft": points[:, 0].round(2),
    "Y_ft": points[:, 1].round(2)
})

# === Coordinate Transformation ===
df["Decimal_Latitude"] = (
    origin_lat + feet_to_decimal_degrees(df["Y_ft"], 364000)
).round(6)

df["Decimal_Longitude"] = (
    origin_lon + feet_to_decimal_degrees(df["X_ft"], 288200)
).round(6)

df["GPS_Latitude"] = df["Decimal_Latitude"].apply(lambda lat: feet_to_gps_dms(lat, 1))
df["GPS_Longitude"] = df["Decimal_Longitude"].apply(lambda lon: feet_to_gps_dms(abs(lon), 1))
df["PlotID"] = df["SampleID"]

def is_within_plot(x, y, x_size=10, y_size=8):
    col = int(x // x_size)
    row = int(y // y_size)
    if 0 <= col < 16 and 0 <= row < 34:
        return f"p{row * 16 + col + 1:03d}"
    return ""

df["Within_Plot"] = df.apply(lambda r: is_within_plot(r["X_ft"], r["Y_ft"]), axis=1)

df.to_csv("soil_samples_updated_gps_anchor.csv", index=False)

# === Map Generation ===
fig, ax = plt.subplots(figsize=(8, 12))
ax.add_patch(plt.Rectangle((0, df['Y_ft'].min()), field_width, field_height,
                           edgecolor='black', facecolor='lightgrey', lw=1))
ax.scatter(df['X_ft'], df['Y_ft'], c='red', s=30, edgecolors='black', label='Soil Samples')
for i, row in df.iterrows():
    label = f"{row['Decimal_Latitude']:.6f} N\n{abs(row['Decimal_Longitude']):.6f} W"
    ax.text(row['X_ft'], row['Y_ft'], label, fontsize=5, ha='left', va='bottom', rotation=45)
ax.set_xlim(0, 160)
ax.set_ylim(df['Y_ft'].min(), df['Y_ft'].min() + 270)
ax.set_aspect('auto')
ax.set_title("Optimized Soil Sampling Map (Updated GPS Coordinates)")
ax.set_xlabel("X (ft)")
ax.set_ylabel("Y (ft)")
ax.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("soil_sampling_map_updated_anchor.png", dpi=150)
print("✅ Outputs saved: CSV and map image")
