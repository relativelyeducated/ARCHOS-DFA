# From: Unrecognized Dialectical Fractal Framework
# Date: 2025-10-12T15:48:39.340000
# Context: # BRIEFING DOCUMENT: ANALYSIS OF ICECUBE DATA.DAT SAMPLE FOR FRACTAL ARCH THEORY VALIDATION

---

## CONTEXT & PURPOSE
On October 12, 2025, at 4:47 PM EDT, you indicated you obtained data from the "da...

import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

# Load sample data (adjust delimiter if needed, e.g., sep=',' for CSV)
data = pd.read_csv('data.dat', sep='\s+', header=None, names=['Energy', 'Zenith'])

# Preprocess
data['Log_E'] = np.log10(data['Energy'])
data['Cos_Zenith'] = np.cos(data['Zenith'])  # Zenith in radians
events = data[['Log_E', 'Cos_Zenith']].values

# 1. D₂ Calculation
def calculate_D2(events, sample_size=None):
    N = len(events) if sample_size is None else min(len(events), sample_size)
    if N < 10:  # Minimum for meaningful fit
        return np.nan, np.nan
    sample = events[np.random.choice(len(events), N, replace=False)]
    distances = cdist(sample, sample, metric='euclidean')
    r_values = np.logspace(-3, 0, 30)  # Reduced range for small samples
    C_r = [np.sum(distances < r) / N**2 for r in r_values]
    log_r, log_C = np.log(r_values[:-5]), np.log(C_r[:-5])  # Truncate for stability
    coeffs = np.polyfit(log_r, log_C, 1, full=True)
    if coeffs[1][0] > 0.1:  # Check fit quality (residuals)
        return np.nan, np.nan
    return coeffs[0][0], np.std(coeffs[0][0]) / np.sqrt(N)  # D₂, error

D2, D2_std = calculate_D2(events)
print(f"Total D₂ = {D2:.2f} ± {D2_std:.2f}")

# 2. Energy-Stratified D₂
bins = [
    data[data['Energy'] < 1e3][['Log_E', 'Cos_Zenith']].values,
    data[(data['Energy'] >= 1e3) & (data['Energy'] < 1e5)][['Log_E', 'Cos_Zenith']].values,
    data[data['Energy'] >= 1e7][['Log_E', 'Cos_Zenith']].values
]
D2_bins = [calculate_D2(bin)[0] if len(bin) > 10 else np.nan for bin in bins]
print(f"Low E D₂: {D2_bins[0]:.2f}, Mid E D₂: {D2_bins[1]:.2f}, High E D₂: {D2_bins[2]:.2f}")

# 3. Angular Correlation
zenith_diff = np.abs(data['Zenith'].values[:, None] - data['Zenith'].values[None, :])
theta_small = zenith_diff[zenith_diff < 0.17]  # ~10° in radians
if len(theta_small) > 10:
    log_theta = np.log10(theta_small + 1e-6)
    coeffs = np.polyfit(log_theta, np.ones_like(log_theta), 1)
    print(f"Angular Correlation Slope: {coeffs[0]:.2f} (expected -0.45)")

# 4. Clustering
if len(events) > 10:
    db = DBSCAN(eps=0.1, min_samples=5).fit(events)
    n_clusters = len(np.unique(db.labels_)) - (1 if -1 in db.labels_ else 0)
    print(f"Number of Clusters: {n_clusters}")

# Plot
plt.figure(figsize=(8, 6))
plt.scatter(events[:, 0], events[:, 1], alpha=0.5)
plt.xlabel('Log10(Energy)')
plt.ylabel('Cos(Zenith)')
plt.title('IceCube Event Distribution (Sample)')
plt.savefig('icecube_sample_distribution.png')
plt.show()

# Export sample (if not already full dataset)
data.to_csv('icecube_processed_sample.csv', index=False)
print("Sample exported to icecube_processed_sample.csv")