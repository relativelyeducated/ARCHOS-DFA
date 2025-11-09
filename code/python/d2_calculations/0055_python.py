# From: Unrecognized Dialectical Fractal Framework
# Date: 2025-10-12T13:42:01.365000
# Context: # BRIEFING DOCUMENT: ACCESSING AND ANALYZING ICECUBE DATA FROM GOOGLE DRIVE FOR FRACTAL ARCH THEORY VALIDATION

---

## CONTEXT & PURPOSE
On October 12, 2025, at 2:41 PM EDT, you indicated that the Ic...

import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

# Load data (adjust path and delimiter: '\s+' for .dat, ',' for CSV)
data = pd.read_csv('data.dat', sep='\s+', header=None, names=['Event_ID', 'Energy', 'Zenith', 'Event_Type', 'Timestamp'])

# Preprocess
data['Log_E'] = np.log10(data['Energy'])
data['Cos_Zenith'] = np.cos(np.radians(data['Zenith']))
events = data[['Log_E', 'Cos_Zenith']].values

# D₂ Calculation
def calculate_D2(events, sample_size=10000):
    N = min(len(events), sample_size)
    sample = events[np.random.choice(len(events), N, replace=False)]
    distances = cdist(sample, sample, metric='euclidean')
    r_values = np.logspace(-3, 0, 50)
    C_r = [np.sum(distances < r) / N**2 for r in r_values]
    log_r, log_C = np.log(r_values[:-10]), np.log(C_r[:-10])
    coeffs = np.polyfit(log_r, log_C, 1)
    return coeffs[0], np.std(coeffs[0])  # D₂, error

D2, D2_std = calculate_D2(events)
print(f"Total D₂ = {D2:.2f} ± {D2_std:.2f}")

# Energy-Stratified D₂
bins = [
    data[data['Energy'] < 1e3][['Log_E', 'Cos_Zenith']].values,
    data[(data['Energy'] >= 1e3) & (data['Energy'] < 1e5)][['Log_E', 'Cos_Zenith']].values,
    data[data['Energy'] >= 1e7][['Log_E', 'Cos_Zenith']].values
]
D2_bins = [calculate_D2(bin)[0] for bin in bins]
print(f"Low E D₂: {D2_bins[0]:.2f}, Mid E D₂: {D2_bins[1]:.2f}, High E D₂: {D2_bins[2]:.2f}")

# Flavor Ratios
if 'Event_Type' in data.columns:
    tracks = data[data['Event_Type'] == 'track'].shape[0]
    showers = data.shape[0] - tracks
    ratio = [showers / 2, tracks, showers / 2]
    print(f"Flavor Ratio (ν_e:ν_μ:ν_τ) = {ratio[0]:.2f}:{ratio[1]:.2f}:{ratio[2]:.2f}")
else:
    print("No Event_Type column; flavor ratio skipped.")

# Angular Correlation
zenith_diff = np.abs(data['Zenith'].values[:, None] - data['Zenith'].values[None, :])
theta_small = zenith_diff[zenith_diff < 10]
if len(theta_small) > 10:
    log_theta = np.log10(theta_small + 1e-6)
    coeffs = np.polyfit(log_theta, np.ones_like(log_theta), 1)
    print(f"Angular Correlation Slope: {coeffs[0]:.2f} (expected -0.45)")

# Clustering
db = DBSCAN(eps=0.1, min_samples=5).fit(events)
n_clusters = len(np.unique(db.labels_)) - (1 if -1 in db.labels_ else 0)
print(f"Number of Clusters: {n_clusters}")

# Temporal Patterns (if Timestamp exists)
if 'Timestamp' in data.columns:
    delta_t = np.diff(data['Timestamp'].values)
    delta_t = delta_t[delta_t > 0]
    if len(delta_t) > 10:
        log_dt = np.log10(delta_t)
        coeffs = np.polyfit(log_dt, np.ones_like(log_dt), 1)
        print(f"Temporal Correlation Slope: {coeffs[0]:.2f} (expected -1.45)")

# Plot
plt.figure(figsize=(8, 6))
plt.scatter(events[:, 0], events[:, 1], alpha=0.5)
plt.xlabel('Log10(Energy)')
plt.ylabel('Cos(Zenith)')
plt.title('IceCube Event Distribution')
plt.savefig('icecube_distribution.png')
plt.show()

# Export sample
data.head(100).to_csv('icecube_sample.csv', index=False)
print("Sample exported to icecube_sample.csv")