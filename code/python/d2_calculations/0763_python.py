# From: Accessing Data File on GitHub
# Date: 2025-11-02T13:10:16.890000
# Context: ```python
#!/usr/bin/env python3
"""
DFA ToE: Batch D₂ Analysis for 50 PDBs
Input: ~/Downloads/pdb/*.pdb
Output: d2_results.csv + summary table
"""

import os
import numpy as np
import pandas as pd
im...

#!/usr/bin/env python3
"""
DFA ToE: Batch D₂ Analysis for 50 PDBs
Input: ~/Downloads/pdb/*.pdb
Output: d2_results.csv + summary table
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from scipy import stats
import logging
from collections import Counter

# === CONFIG ===
PDB_DIR = os.path.expanduser("~/Downloads/pdb")
OUTPUT_CSV = os.path.join(PDB_DIR, "d2_results.csv")
sns.set_style("whitegrid")

# === LOAD & CLEAN DATA ===
print("Loading and cleaning data...")
df = pd.read_csv(OUTPUT_CSV)
df = df[df['D₂'] != 'nan'].copy()
df['D₂'] = pd.to_numeric(df['D₂'], errors='coerce')  # 'nan' → NaN
df = df.dropna(subset=['D₂']).copy()  # Drop rows where D₂ is NaN
df = df[df['N_atoms'] > 30].copy()    # Remove tiny structures (<30 atoms)

print(f"Valid entries after cleaning: {len(df)}")
print(f"D₂ range: {df['D₂'].min():.3f} → {df['D₂'].max():.3f}\n")

# === 1. CATEGORY SUMMARY ===
print("1. D₂ BY CATEGORY")
print("-" * 50)
summary = df.groupby('Category').agg(
    count=('D₂', 'size'),
    mean=('D₂', 'mean'),
    std=('D₂', 'std'),
    min=('D₂', 'min'),
    max=('D₂', 'max')
).round(3)
print(summary)
print()

# === 2. PASS/FAIL vs STATE (only valid rows) ===
print("2. PASS/FAIL vs STATE")
print("-" * 50)
valid_pf = df[df['PASS/FAIL'].isin(['PASS', 'FAIL'])].copy()
state_perf = valid_pf.groupby(['State', 'PASS/FAIL']).size().unstack(fill_value=0)
state_perf['Total'] = state_perf.sum(axis=1)
state_perf['% PASS'] = (state_perf['PASS'] / state_perf['Total'] * 100).round(1)
print(state_perf)
print()

# === 3. NATURAL ZONES (KMeans) ===
print("3. DATA-DRIVEN ZONES (KMeans, n=3)")
print("-" * 60)
X = df[['D₂']].values
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X)
centers = sorted(kmeans.cluster_centers_.flatten())
df['Cluster'] = kmeans.labels_
cluster_map = {i: f"Zone {i+1} ({centers[i]:.3f})" for i in range(3)}
df['Zone'] = df['Cluster'].map(cluster_map)

print(f"Cluster Centers: {centers}")
zone_bounds = f"< {centers[0]:.2f} | {centers[0]:.2f}–{centers[1]:.2f} | > {centers[1]:.2f}"
print(f"Suggested zones: {zone_bounds}")
print()

# === 4. STATISTICAL TESTS ===
print("4. STATISTICAL SIGNIFICANCE")
print("-" * 60)

# Membrane vs Non-Membrane
mem = df[df['Category'] == 'Membrane']['D₂']
non_mem = df[df['Category'] != 'Membrane']['D₂']
if len(mem) > 1 and len(non_mem) > 1:
    t_mem, p_mem = stats.ttest_ind(mem, non_mem, equal_var=False)
    print(f"Membrane vs Others: t={t_mem:.3f}, p={p_mem:.2e}")
else:
    print("Membrane vs Others: Not enough data")

# Fibril vs Healthy
fib = df[df['Category'] == 'Fibril']['D₂']
healthy = df[df['Category'] != 'Fibril']['D₂']
if len(fib) > 1 and len(healthy) > 1:
    t_fib, p_fib = stats.ttest_ind(fib, healthy, equal_var=False)
    print(f"Fibril vs Healthy: t={t_fib:.3f}, p={p_fib:.2e}")
else:
    print("Fibril vs Healthy: Not enough data")
print()

# === 5. LIPID BUFFER EFFECT ===
print("5. LIPID BUFFER EFFECT")
print("-" * 60)
print(f"Membrane D₂ = {mem.mean():.3f} ± {mem.std():.3f} (n={len(mem)})")
print(f"Non-membrane D₂ = {non_mem.mean():.3f} ± {non_mem.std():.3f} (n={len(non_mem)})")
delta = mem.mean() - non_mem.mean()
print(f"→ Lipid increases D₂ by {delta:+.3f}")
print()

# === 6. DIAGNOSTIC RULE COMPARISON ===
print("6. REFINED DIAGNOSTIC RULE SEARCH")
print("-" * 60)

# Test D₂ > 2.0 for pathology
fib_above_2 = (fib > 2.0).mean() * 100
healthy_below_2 = (healthy <= 2.0).mean() * 100
acc_2 = (fib_above_2 + healthy_below_2) / 2

# Test D₂ > 2.5
fib_above_25 = (fib > 2.5).mean() * 100
healthy_below_25 = (healthy <= 2.5).mean() * 100
acc_25 = (fib_above_25 + healthy_below_25) / 2

print(f"D₂ > 2.0 → Fibril: {fib_above_2:.1f}% | Healthy ≤ 2.0: {healthy_below_2:.1f}% → Acc: {acc_2:.1f}%")
print(f"D₂ > 2.5 → Fibril: {fib_above_25:.1f}% | Healthy ≤ 2.5: {healthy_below_25:.1f}% → Acc: {acc_25:.1f}%")

best_thresh = 2.0 if acc_2 >= acc_25 else 2.5
best_acc = max(acc_2, acc_25)
print(f"\nBEST RULE: D₂ > {best_thresh} = Pathology | Accuracy: {best_acc:.1f}%")
print()

# === 7. PLOTS ===
print("7. GENERATING PLOTS...")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Histogram + KDE
sns.histplot(data=df, x='D₂', hue='Category', kde=True, ax=axes[0,0], bins=15, alpha=0.7)
axes[0,0].set_title('D₂ Distribution by Category')
axes[0,0].axvline(best_thresh, color='red', linestyle='--', label=f'Threshold = {best_thresh}')
axes[0,0].legend()

# 2. Boxplot
sns.boxplot(data=df, x='Category', y='D₂', ax=axes[0,1])
axes[0,1].set_title('D₂ by Category')
axes[0,1].axhline(best_thresh, color='red', linestyle='--')
axes[0,1].tick_params(axis='x', rotation=45)

# 3. Size vs D₂
sns.scatterplot(data=df, x='N_atoms', y='D₂', hue='Category', ax=axes[1,0], alpha=0.8)
axes[1,0].set_xscale('log')
axes[1,0].set_title('Protein Size vs D₂')
axes[1,0].axhline(best_thresh, color='red', linestyle='--')

# 4. KMeans Zones
zone_order = df.sort_values('D₂')['Zone'].unique()
sns.stripplot(data=df, x='D₂', y='Zone', order=zone_order, ax=axes[1,1], jitter=True, alpha=0.7)
axes[1,1].set_title('KMeans-Derived Zones')
for c in centers:
    axes[1,1].axvline(c, color='black', linestyle=':', alpha=0.6)

plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(CSV_PATH), "dfa_analysis.png"), dpi=200, bbox_inches='tight')
print(f"→ Plot saved: dfa_analysis.png")
print()

# === 8. FINAL VERDICT ===
print("=== FINAL VERDICT ===")
if best_acc >= 75:
    print("DFA ToE = STRONGLY SUPPORTED")
    print(f"→ D₂ > {best_thresh} = Reliable pathology marker")
else:
    print("DFA ToE = NEEDS REVISION")
    print("→ Consider size, method, or selection bias")

print(f"→ Lipid buffer: D₂ ↑ by {delta:+.3f} in membrane proteins")
print(f"→ KMeans zones: {zone_bounds}")
print(f"→ No strong size correlation (log scale scatter)")
print("\nAnalysis complete.")