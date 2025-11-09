# From: Unrecognized Dialectical Fractal Framework
# Date: 2025-10-12T21:16:26.081000
# Context: # BRIEFING DOCUMENT: UPDATED ANALYSIS OF ICECUBE HESE 7-YEAR DATA SAMPLE FOR FRACTAL ARCH THEORY VALIDATION

---

## CONTEXT & PURPOSE
On October 12, 2025, at 10:15 PM EDT, you provided an expanded sa...

import numpy as np
from scipy.spatial.distance import cdist
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

# Updated sample data from user
energy = np.array([40094.5703125, 98474.578125, 70592.5078125, 184547.453125, 27220.697265625, 21233.8125, 
                   51900.21875, 85419.1640625, 74309.1015625, 86480.1953125, 252038.03125, 1035479.625, 
                   51019.9375, 30255.39453125, 171397.40625, 28886.294921875, 61686.45703125, 1255736.25, 
                   26508.54296875, 195833.46875, 86080.4453125, 27899.150390625, 31755.53125, 186558.625, 
                   52423.89453125, 45565.3984375, 27931.66796875, 107340.828125, 31077.705078125, 333548.5, 
                   37420.3125, 1799984.125, 23609.314453125, 23908.265625, 186010.953125, 88198.453125, 
                   175380.359375, 85167.0703125, 32440.328125, 71842.3125, 409560.3125, 134221.28125, 
                   66663.140625, 102178.703125, 51387.0859375, 19914.587890625, 59696.09765625, 122203.265625, 
                   42366.98046875, 98337.875, 118801.9296875, 50258.1015625, 121114.0859375, 86322.9140625, 
                   66750.6484375, 39222.53515625, 79398.8671875, 154762.21875, 54265.30078125, 88021.875, 
                   60255.66796875, 33291.375, 78055.796875, 148418.296875, 125109.1015625, 35785.56640625, 
                   51696.421875, 140879.828125, 77529.8203125, 102387.4609375, 147270.875, 49665.76171875, 
                   618922.8125])

zenith = np.array([1.8270703554153442, 1.4227240085601807, 0.9552649855613708, 0.9126873016357422, 
                   1.2361491918563843, 1.2047853469848633, 2.0946884155273438, 1.2642697095870972, 
                   1.4948956966400146, 0.8667189478874207, 2.0202202796936035, 1.5429260730743408, 
                   0.5677031874656677, 1.1628973484039307, 1.9636365175247192, 1.116873025894165, 
                   0.5592789649963379, 0.42102599143981934, 1.284034013748169, 1.1106257438659668, 
                   2.938802719116211, 1.4657127857208252, 1.4951144456863403, 2.0677058696746826, 
                   1.3677444458007812, 0.35190701484680176, 2.2445640563964844, 0.06610847264528275, 
                   2.524462938308716, 1.6727001667022705, 2.1044046878814697, 0.5554018616676331, 
                   1.6721534729003906, 1.9257616996765137, 1.8349400758743286, 1.3661432266235352, 
                   1.0529940128326416, 1.6673823595046997, 1.0599446296691895, 1.5989704132080078, 
                   0.055354710668325424, 1.3480594158172607, 2.523169994354248, 1.1925050020217896, 
                   1.0685871839523315, 2.538329601287842, 2.7537858486175537, 0.5483760833740234, 
                   1.793353796005249, 0.8602895140647888, 1.0339771509170532, 1.5574061870574951, 
                   1.5571563243865967, 0.9718018770217896, 1.0978033542633057, 0.9923081994056702, 
                   2.614529609680176])

# Preprocess
log_e = np.log10(energy / 1000)  # Convert to TeV and log scale
cos_zenith = np.cos(zenith)
events = np.stack((log_e, cos_zenith), axis=1)

# D₂ Calculation
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

# Energy-Stratified D₂
bins = [energy < 100000, (energy >= 100000) & (energy < 500000), energy >= 500000]
D2_bins = [calculate_D2(events[bin]) if len(events[bin]) > 10 else np.nan for bin in bins]
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
plt.xlabel('Log10(Energy [TeV])')
plt.ylabel('Cos(Zenith)')
plt.title('IceCube HESE 75-Event Sample Distribution')
plt.savefig('icecube_hese_75_distribution.png')
plt.show()