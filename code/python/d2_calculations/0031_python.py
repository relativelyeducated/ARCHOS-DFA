# From: Unrecognized Dialectical Fractal Framework
# Date: 2025-10-08T22:37:48.695000
# Context: # BRIEFING DOCUMENT: ADVANCED TESTING OF FRACTAL ARCH THEORY WITH GOOGLE DRIVE ICECUBE DATA

---

## CONTEXT & PURPOSE
On October 8, 2025, at 10:31 PM CDT, you provided a Google Drive link to the IceC...

import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
from sklearn.cluster import DBSCAN
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

# Load data (adjust path and delimiter if .dat is space-separated)
data = pd.read_csv('data.dat', sep='\s+', header=None, names=['Event_ID', 'Energy', 'Zenith', 'Event_Type', 'Timestamp'])  # Adjust columns as per file

# Preprocess
data['Log_E'] = np.log10(data['Energy'])
data['Cos_Zenith'] = np.cos(np.radians(data['Zenith']))
events = data[['Log_E', 'Cos_Zenith']].values

# 1. D₂ Calculation
def calculate_D2(events, r_max=1.0):
    N = len(events)
    distances = cdist(events, events, metric='euclidean')
    r_values = np.logspace(-3, np.log10(r_max), 50)
    C_r = []
    for r in r_values:
        C_r.append(np.sum(distances < r) / N**2)
    log_r, log_C = np.log(r_values), np.log(C_r)
    coeffs = np.polyfit(log_r, log_C, 1)
    D2 = coeffs[0]
    return D2, np.std(coeffs[0])  # Approximate std

D2, D2_std = calculate_D2(events)
print(f"D₂ = {D2:.2f} ± {D2_std:.2f}")

# 2. Energy-Stratified D₂
bins = [data[data['Energy'] < 1e3], data[(data['Energy'] >= 1e3) & (data['Energy'] < 1e5)], data[data['Energy'] >= 1e7]]
D2_bins = [calculate_D2(bin['Log_E'], bin['Cos_Zenith'].values)[0] for bin in bins]
print(f"Low E D₂: {D2_bins[0]:.2f}, Mid E D₂: {D2_bins[1]:.2f}, High E D₂: {D2_bins[2]:.2f}")

# 3. Flavor Ratios
tracks = data[data['Event_Type'] == 'track'].shape[0]
showers = data[data['Event_Type'] == 'shower'].shape[0]
ratio = [showers / 2, tracks, showers / 2]  # ν_e:ν_μ:ν_τ
print(f"Flavor Ratio (ν_e:ν_μ:ν_τ) = {ratio[0]:.2f}:{ratio[1]:.2f}:{ratio[2]:.2f}")

# 4. Angular Correlation
zenith_diff = np.abs(data['Zenith'].values[:, None] - data['Zenith'].values[None, :])
theta_small = zenith_diff[zenith_diff < 10]
log_theta = np.log10(theta_small + 1e-6)
if len(log_theta) > 10:
    coeffs = np.polyfit(log_theta, np.ones_like(log_theta), 1)  # Flat for no correlation
    print(f"Angular Correlation Slope: {coeffs[0]:.2f} (expected -0.45)")

# 5. Clustering
db = DBSCAN(eps=0.1, min_samples=5).fit(events)
clusters = db.labels_
n_clusters = len(np.unique(clusters)) - (1 if -1 in clusters else 0)
print(f"Number of Clusters: {n_clusters}")

# Plot (optional)
plt.figure(figsize=(8, 6))
plt.scatter(events[:, 0], events[:, 1], alpha=0.5)
plt.xlabel('Log10(Energy)')
plt.ylabel('Cos(Zenith)')
plt.title('IceCube Event Distribution')
plt.savefig('icecube_distribution.png')
plt.show()