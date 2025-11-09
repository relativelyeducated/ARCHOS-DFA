# From: Unrecognized Dialectical Fractal Framework
# Date: 2025-10-08T22:39:41.040000
# Context: # BRIEFING DOCUMENT: RETRYING ACCESS TO GOOGLE DRIVE ICECUBE DATA FILE

---

## CONTEXT & PURPOSE
On October 8, 2025, at 10:31 PM CDT, you provided a Google Drive link to the IceCube neutrino data fil...

import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist

# Load .dat (assume space-separated, adjust delimiter)
data = pd.read_csv('data.dat', sep='\s+', header=None, names=['Event_ID', 'Energy', 'Zenith', 'Event_Type', 'Timestamp'])

# Preprocess
data['Log_E'] = np.log10(data['Energy'])
data['Cos_Zenith'] = np.cos(np.radians(data['Zenith']))
events = data[['Log_E', 'Cos_Zenith']].values

# D₂ Calculation
distances = cdist(events[:10000], events[:10000])  # Subsample for speed
r_values = np.logspace(-3, 0, 50)
C_r = [np.sum(distances < r) / len(distances) for r in r_values]
log_r, log_C = np.log(r_values), np.log(C_r)
D2 = np.polyfit(log_r, log_C, 1)[0]
print(f"D₂ = {D2:.2f}")

# Flavor Ratios
tracks = data[data['Event_Type'] == 'track'].shape[0] if 'Event_Type' in data else 0
showers = data.shape[0] - tracks
ratio = [showers / 2, tracks, showers / 2]
print(f"Flavor Ratio: {ratio}")

# Save sample
data.head(100).to_csv('icecube_sample.csv', index=False)