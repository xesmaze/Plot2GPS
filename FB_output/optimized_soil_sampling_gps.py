
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
import re

# === Configuration ===
field_width = 160
field_height = 270
n_samples = 100
min_distance = 15  # Minimum separation in feet between samples
# Chang ethe following to update the sample coordinates
gps_input = "40-06-54"  # Format: XX-YY-ZZ

# === GPS Conversion ===
def gps_to_feet(gps_str):
    match = re.match(r'^(\d+)[\s\-:]+(\d+)[\s\-:]+(\d+)$', gps_str.strip())
    if not match:
        raise ValueError("GPS input must be in 'xx-yy-zz' format")
    degrees, minutes, seconds = map(int, match.groups())
    decimal_deg = degrees + minutes / 60 + seconds / 3600
    return decimal_deg * 364000

def shift_coordinates(df, gps_y_feet):
    df['Y_ft'] += gps_y_feet
    return df.round(2)

# === Rejection Sampling ===
np.random.seed(None)
accepted_points = []
attempts = 0
max_attempts = 10000

while len(accepted_points) < n_samples and attempts < max_attempts:
    x = np.random.uniform(0, field_width)
    y = np.random.uniform(0, field_height)
    point = np.array([[x, y]])
    if not accepted_points:
        accepted_points.append(point[0])
    else:
        distances = cdist(point, np.array(accepted_points))
        if distances.min() >= min_distance:
            accepted_points.append(point[0])
    attempts += 1

# === Save to CSV ===
points = np.array(accepted_points)
df_samples = pd.DataFrame({
    "SampleID": [f"S{i+1:03}" for i in range(len(points))],
    "X_ft": points[:, 0].round(2),
    "Y_ft": points[:, 1].round(2)
})

gps_y_feet = gps_to_feet(gps_input)
df_shifted = shift_coordinates(df_samples, gps_y_feet)

# Export
df_shifted.to_csv("optimized_soil_samples_gps_aligned.csv", index=False)
print("✅ Saved: optimized_soil_samples_gps_aligned.csv")
