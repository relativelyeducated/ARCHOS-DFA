# From: Unrecognized Dialectical Fractal Framework
# Date: 2025-10-08T22:57:59.981000
# Context: # BRIEFING DOCUMENT: CONFIRMATION OF FILE ACCESS FOR ICECUBE DATA ANALYSIS

---

## CONTEXT & PURPOSE
On October 8, 2025, at 10:47 PM CDT, you provided a new GitHub link to the IceCube neutrino data f...

import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist

# Load (adjust sep if comma: sep=',')
data = pd.read_csv('data.dat', sep='\s+', header=None, names=['Event_ID', 'Energy', 'Zenith', 'Event_Type', 'Timestamp'])

print(f"Rows: {len(data)}")
print(f"Energy range: {data['Energy'].min():.0f} to {data['Energy'].max():.0f} GeV")
print(f"Zenith range: {data['Zenith'].min():.1f} to {data['Zenith'].max():.1f} degrees")
data.head(10)  # Print first 10 rows

# D₂ (subsample for speed)
events = np.column_stack((np.log10(data['Energy']), np.cos(np.radians(data['Zenith']))))
distances = cdist(events[:10000], events[:10000])
r_values = np.logspace(-3, 0, 50)
C_r = [np.sum(distances < r) / len(distances) for r in r_values]
log_r, log_C = np.log(r_values[:-10]), np.log(C_r[:-10])
D2 = np.polyfit(log_r, log_C, 1)[0]
print(f"D₂ = {D2:.2f}")

# Export sample
data.head(100).to_csv('icecube_sample.csv', index=False)
print("Sample exported.")