# From: Unrecognized Dialectical Fractal Framework
# Date: 2025-10-12T16:50:01.761000
# Context: # BRIEFING DOCUMENT: ACCESS AND ANALYSIS OF ICECUBE HESE DATA.JSON FROM GITHUB

---

## CONTEXT & PURPOSE
On October 12, 2025, at 4:47 PM EDT, you provided two GitHub raw links to IceCube High Energy ...

import json
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

# Load JSON
with open('HESE_data.json', 'r') as f:
    data = json.load(f)

# Extract to DataFrame
df = pd.json_normalize(data)
df['Log_E'] = np.log10(df['energy'])  # Log energy (TeV)
df['Sin_Dec'] = np.sin(np.radians(df['dec']))  # Sin(dec) for sky coordinate
events = df[['Log_E', 'Sin_Dec']].values

# 1. D₂ Calculation
def calculate_D2(events, sample_size=50):  # Small sample for HESE
    N = min(len(events), sample_size)
    sample = events[np.random.choice(len(events), N, replace=False)]
    distances = cdist(sample, sample, metric='euclidean')
    r_values = np.logspace(-3, 0, 30)  # Reduced for small N
    C_r = [np.sum(distances < r) / N**2 for r in r_values]
    log_r, log_C = np.log(r_values[:-5]), np.log(C_r[:-5])
    coeffs = np.polyfit(log_r, log_C, 1)
    return coeffs[0]

D2 = calculate_D2(events)
print(f"HESE D₂ = {D2:.2f}")

# 2. Energy-Stratified D₂
low = df[df['energy'] < 100][['Log_E', 'Sin_Dec']].values
mid = df[(df['energy'] >= 100) & (df['energy'] < 1000)][['Log_E', 'Sin_Dec']].values
high = df[df['energy'] >= 1000][['Log_E', 'Sin_Dec']].values
D2_low = calculate_D2(low) if len(low) > 10 else np.nan
D2_mid = calculate_D2(mid) if len(mid) > 10 else np.nan
D2_high = calculate_D2(high) if len(high) > 10 else np.nan
print(f"Low E D₂: {D2_low:.2f}, Mid E D₂: {D2_mid:.2f}, High E D₂: {D2_high:.2f}")

# 3. Angular Correlation (using dec)
dec_diff = np.abs(df['dec'].values[:, None] - df['dec'].values[None, :])
theta_small = dec_diff[dec_diff < 10]  # 10° in degrees
if len(theta_small) > 5:
    log_theta = np.log10(theta_small + 1e-6)
    coeffs = np.polyfit(log_theta, np.ones_like(log_theta), 1)
    print(f"Angular Correlation Slope: {coeffs[0]:.2f} (expected -0.45)")

# 4. Clustering
if len(events) > 10:
    db = DBSCAN(eps=0.1, min_samples=2).fit(events)  # Low min_samples for small data
    n_clusters = len(np.unique(db.labels_)) - (1 if -1 in db.labels_ else 0)
    print(f"Number of Clusters: {n_clusters}")

# Plot
plt.figure(figsize=(8, 6))
plt.scatter(events[:, 0], events[:, 1], alpha=0.5)
plt.xlabel('Log10(Energy [TeV])')
plt.ylabel('Sin(Dec)')
plt.title('HESE Event Distribution')
plt.savefig('hese_distribution.png')
plt.show()

# Export sample
df.to_csv('hese_sample.csv', index=False)
print("Sample exported to hese_sample.csv")