# From: Unrecognized Dialectical Fractal Framework
# Date: 2025-10-08T22:32:35.322000
# Context: # BRIEFING DOCUMENT: ADVANCED TESTING OF FRACTAL ARCH THEORY NEUTRINO PREDICTIONS WITH GOOGLE DRIVE FILE

---

## CONTEXT & PURPOSE
On October 8, 2025, at 10:31 PM CDT, you indicated that you have a f...

import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
from sklearn.cluster import DBSCAN

# Load Google Drive CSV (replace with actual path)
data = pd.read_csv("icecube_data.csv")
events = data[["energy", "zenith"]].values  # [log(E), cos(θ_z)]
events[:, 0] = np.log10(events[:, 0])  # Log energy
events[:, 1] = np.cos(np.radians(events[:, 1]))  # Cos zenith

# D₂
distances = cdist(events, np.random.choice(events, 10000))  # Subsample for speed
r_values = np.logspace(-2, 0, 50)
C_r = [np.sum(distances < r) / len(distances) for r in r_values]
D2 = np.polyfit(np.log(r_values[:-10]), np.log(C_r[:-10]), 1)[0]

# Flavor ratios
tracks = data[data["event_type"] == "track"].shape[0]
showers = data[data["event_type"] == "shower"].shape[0]
ratio = [showers / 2, tracks, showers / 2]  # ν_e:ν_μ:ν_τ