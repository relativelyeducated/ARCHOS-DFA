# From: Unrecognized Dialectical Fractal Framework
# Date: 2025-10-12T21:07:41.285000
# Context: # BRIEFING DOCUMENT: ANALYSIS OF ICECUBE HESE 7-YEAR DATA SAMPLE FOR FRACTAL ARCH THEORY VALIDATION

---

## CONTEXT & PURPOSE
On October 12, 2025, at 4:47 PM EDT, you shared a sample of the IceCube H...

import numpy as np
from scipy.spatial.distance import cdist
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

# Sample data from user
energy = np.array([40094.5703125, 98474.578125, 70592.5078125, 184547.453125, 27220.697265625, 21233.8125, 51900.21875, 85419.1640625, 74309.1015625, 86480.1953125, 252038.03125, 1035479.625, 51019.9375, 30255.39453125, 171397.40625, 28886.294921875, 61686.45703125, 1255736.25, 26508.54296875, 195833.46875])
zenith = np.array([1.8270703554153442, 1.4227240085601807, 0.9552649855613708, 0.9126873016356352, 1.2361491916357422, 1.2047853466358633, 2.0946884155273438, 1.2642697095870972, 1.4948956966400146, 0.8667189478874207, 2.0202202796936035, 1.5429260730743408, 0.5677031874656677, 1.1628973484039307, 1.9636365175247192, 1.116873025894165, 0.5592789649963379, 0.42102599143981934, 1.284034013748169, 1.1106257438659668])

# Preprocess
log_e = np.log10(energy)
cos_zenith = np.cos(zenith)
events = np.stack((log_e, cos_zenith), axis=1)

# D₂ Calculation (small sample)
def calculate_D2(events):
    N = len(events)
    if N < 10:
        return np.nan
    distances = cdist(events, events, metric='euclidean')
    r_values = np.logspace(-3, 0, 30)
    C_r = [np.sum(distances < r) / N**2 for r in r_values]
    log_r, log_C = np.log(r_values[:-5]), np.log(C_r[:-5])
    coeffs = np.polyfit(log_r, log_C, 1)
    return coeffs[0]

D2 = calculate_D2(events)
print(f"Sample D₂ = {D2:.2f}")

# Energy-Stratified D₂ (small sample, may be nan)
bins = [energy < 100000, (energy >= 100000) & (energy < 500000), energy >= 500000]
D2_bins = [calculate_D2(events[bin]) if len(events[bin]) > 5 else np.nan for bin in bins]
print(f"Low E D₂: {D2_bins[0]:.2f}, Mid E D₂: {D2_bins[1]:.2f}, High E D₂: {D2_bins[2]:.2f}")

# Angular Correlation
zenith_diff = np.abs(zenith[:, None] - zenith[None, :])
theta_small = zenith_diff[zenith_diff < 0.17]
if len(theta_small) > 5:
    log_theta = np.log10(theta_small + 1e-6)
    coeffs = np.polyfit(log_theta, np.ones_like(log_theta), 1)
    print(f"Angular Slope: {coeffs[0]:.2f} (expected -0.45)")

# Clustering
db = DBSCAN(eps=0.1, min_samples=2).fit(events)
n_clusters = len(np.unique(db.labels_)) - (1 if -1 in db.labels_ else 0)
print(f"Number of Clusters: {n_clusters}")

# Plot
plt.figure(figsize=(8, 6))
plt.scatter(events[:, 0], events[:, 1], alpha=0.5)
plt.xlabel('Log10(Energy)')
plt.ylabel('Cos(Zenith)')
plt.title('IceCube Sample Distribution')
plt.savefig('icecube_sample_distribution.png')
plt.show()