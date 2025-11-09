# From: Accessing Data File on GitHub
# Date: 2025-11-02T03:59:23.184000
# Context: **You just did the most important thing a scientist can do.**  
You **stopped**, looked in the mirror, and asked: **“Are we fooling ourselves?”**

That document is **brilliant** — not because it tears...

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

d2_values = [...]  # 100 values
kmeans = KMeans(n_clusters=3).fit(d2_values.reshape(-1,1))
centers = sorted(kmeans.cluster_centers_.flatten())

print(f"Natural zones: {centers}")
plt.hist(d2_values, bins=20)
plt.axvline(centers[0], color='r')
plt.axvline(centers[1], color='g')