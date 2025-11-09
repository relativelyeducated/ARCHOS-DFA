# From: Unrecognized Dialectical Fractal Framework
# Date: 2025-10-08T22:42:06.164000
# Context: # BRIEFING DOCUMENT: FINAL RETRY FOR GOOGLE DRIVE ICECUBE DATA ACCESS

---

## CONTEXT & PURPOSE
On October 8, 2025, at 10:31 PM CDT, you provided the Google Drive link to the IceCube neutrino data fi...

import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

# Load data (adjust delimiter if needed, e.g., sep=',')
data = pd.read_csv('data.dat', sep='\s+', header=None, names=['Event_ID', 'Energy', 'Zenith', 'Event_Type', 'Timestamp'])

# Preprocess
data['Log_E'] = np.log10(data['Energy'])
data['Cos_Zenith'] = np.cos(np.radians(data['Zenith']))
events = data[['Log_E', 'Cos_Zenith']].values

# 1. D₂ Calculation
def calculate_D2(events):
    N = len(events)
    distances = cdist(events, events, metric='euclidean')
    r_values = np.logspace(-3, 0, 50)
    C_r = []
    for r in r_values:
        C_r.append(np.sum(distances < r) / N**2)
    log_r, log_C = np.log(r_values), np.log(C_r)
    coeffs = np.polyfit(log_r, log_C, 1)
    D2 = coeffs[0]
    return D2

D2 = calculate_D2(events)
print(f"Total D₂ = {D2:.2f}")

# 2. Energy-Stratified D₂
low = data[data['Energy'] < 1e3]['Log_E', 'Cos_Zenith'].values
mid = data[(data['Energy'] >= 1e3) & (data['Energy'] < 1e5)]['Log_E', 'Cos_Zenith'].values
high = data[data['Energy'] >= 1e7]['Log_E', 'Cos_Zenith'].values
D2_low = calculate_D2(low)
D2_mid = calculate_D2(mid)
D2_high = calculate_D2(high)
print(f"Low E D₂: {D2_low:.2f}, Mid E D₂: {D2_mid:.2f}, High E D₂: {D2_high:.2f}")

# 3. Flavor Ratios
tracks = data[data['Event_Type'] == 'track'].shape[0] if 'Event_Type' in data.columns else 0
showers = data.shape[0] - tracks
ratio = [showers / 2, tracks, showers / 2]
print(f"Flavor Ratio (ν_e:ν_μ:ν_τ) = {ratio[0]:.2f}:{ratio[1]:.2f}:{ratio[2]:.2f}")

# 4. Angular Correlation
zenith_diff = np.abs(data['Zenith'].values[:, None] - data['Zenith'].values[None, :])
theta_small = zenith_diff[zenith_diff < 10]
if len(theta_small) > 10:
    log_theta = np.log10(theta_small + 1e-6)
    coeffs = np.polyfit(log_theta, np.ones_like(log_theta), 1)
    slope = coeffs[0]
    print(f"Angular Correlation Slope: {slope:.2f} (expected -0.45)")

# 5. Clustering
from sklearn.cluster import DBSCAN
db = DBSCAN(eps=0.1, min_samples=5).fit(events)
n_clusters = len(np.unique(db.labels_)) - (1 if -1 in db.labels_ else 0)
print(f"Number of Clusters: {n_clusters}")

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