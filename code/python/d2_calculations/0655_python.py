# From: Accessing Data File on GitHub
# Date: 2025-11-02T04:31:00.084000
# Context: **PERFECT. LET'S CRUNCH THE 50 PROTEINS.**

Here's the **batch D₂ script** that will process all 50 PDBs and give us the truth:

Save as `~/ai/batch_d2_50.py`:

```python
#!/usr/bin/env python3
"""
DF...

#!/usr/bin/env python3
"""
DFA ToE: 50-Protein Batch D₂ Analysis
No theory. Just numbers.
"""

import os, numpy as np, pandas as pd
from Bio.PDB import PDBParser
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
parser = PDBParser(QUIET=True)

# === CONFIG ===
PDB_DIR = os.path.expanduser("~/Downloads/pdb")
OUTPUT_CSV = "~/ai/dfa_50_results.csv"
# ==============

def compute_d2(pdb_file):
    """Pure D₂ calculation (no hybrids)"""
    try:
        structure = parser.get_structure('', pdb_file)
        coords = []
        for model in structure:
            for chain in model:
                for residue in chain:
                    if 'CA' in residue:
                        coords.append(residue['CA'].coord)
        coords = np.array(coords)
        
        if len(coords) < 50:
            return {'pdb': os.path.basename(pdb_file)[:-4], 'n_atoms': len(coords), 'd2': np.nan, 'r2': np.nan}
        
        # Pairwise distances
        n = len(coords)
        distances = np.linalg.norm(coords[:,None] - coords[None,:], axis=-1)
        triu_distances = distances[np.triu_indices(n, k=1)]
        
        # Correlation integral
        max_d = np.max(triu_distances)
        r_values = np.logspace(np.log10(0.5), np.log10(max_d*0.4), 40)
        c_r = np.array([np.sum(triu_distances < r) / len(triu_distances) for r in r_values])
        
        # Fit (middle 60% to avoid edge effects)
        valid = (c_r > 1e-8) & (r_values > 0)
        if np.sum(valid) < 10:
            return {'pdb': os.path.basename(pdb_file)[:-4], 'n_atoms': len(coords), 'd2': np.nan, 'r2': np.nan}
        
        log_r = np.log10(r_values[valid])
        log_c = np.log10(c_r[valid])
        coeffs = np.polyfit(log_r[10:-10], log_c[10:-10], 1)  # Middle 80%
        d2 = coeffs[0]
        r2 = 1 - np.sum((log_c[10:-10] - np.polyval(coeffs, log_r[10:-10]))**2) / np.sum((log_c[10:-10] - np.mean(log_c[10:-10]))**2)
        
        return {'pdb': os.path.basename(pdb_file)[:-4], 'n_atoms': len(coords), 'd2': d2, 'r2': r2}
    except:
        return {'pdb': os.path.basename(pdb_file)[:-4], 'n_atoms': 0, 'd2': np.nan, 'r2': np.nan}

# === RUN ===
print("Processing 50 PDBs...")
results = []

for pdb_file in os.listdir(PDB_DIR):
    if pdb_file.endswith('.pdb'):
        print(f"Analyzing {pdb_file}...")
        result = compute_d2(os.path.join(PDB_DIR, pdb_file))
        results.append(result)

# === SAVE ===
df = pd.DataFrame(results)
df.to_csv(OUTPUT_CSV, index=False)
print(f"\nResults saved to {OUTPUT_CSV}")

# === SUMMARY ===
valid = df.dropna(subset=['d2'])
print(f"\n{'='*50}")
print(f"DFA ToE 50-PROTEIN VALIDATION")
print(f"{'='*50}")
print(f"Total proteins: {len(df)}")
print(f"Valid D₂: {len(valid)}")
print(f"D₂ range: {valid['d2'].min():.3f} - {valid['d2'].max():.3f}")
print(f"D₂ mean: {valid['d2'].mean():.3f}")
print(f"D₂ std: {valid['d2'].std():.3f}")

# Zone analysis
healthy = valid[valid['n_atoms'] < 300]  # proxy for monomers
fibrils = valid[valid['n_atoms'] > 500]   # proxy for aggregates
print(f"\nHealthy (n<300): {len(healthy)} proteins, mean D₂ = {healthy['d2'].mean():.3f}")
print(f"Fibrils (n>500): {len(fibrils)} proteins, mean D₂ = {fibrils['d2'].mean():.3f}")

print(f"\n{'='*50}")