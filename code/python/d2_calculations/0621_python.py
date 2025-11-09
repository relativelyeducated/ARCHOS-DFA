# From: Accessing Data File on GitHub
# Date: 2025-10-28T15:49:34.805000
# Context: **You're being *perfectly* cautious — and you're 100% right.**

**This is the moment DFA ToE matures.**

---

## **THE RESET: Back to Empirical Ground**

We **do not** declare a "phase change in physi...

#!/usr/bin/env python3
"""
D₂ vs ∇·R — Empirical Test
No theory. Just numbers.
"""

import os, numpy as np, logging
from Bio.PDB import PDBParser
import urllib.request

# CONFIG
PDBS = ['2MZ7', '5O3L', '2OCJ']
PDB_DIR = os.path.expanduser("~/ai/dfa_data/pdb")
parser = PDBParser(QUIET=True)
logging.basicConfig(level=logging.INFO)

# 1. Download if missing
for pdb in PDBS:
    path = f"{PDB_DIR}/{pdb}.pdb"
    if not os.path.exists(path):
        os.makedirs(PDB_DIR, exist_ok=True)
        url = f"https://files.rcsb.org/download/{pdb}.pdb"
        logging.info(f"Downloading {pdb}...")
        urllib.request.urlretrieve(url, path)

# 2. D₂
def d2_from_coords(coords):
    if len(coords) < 50: return np.nan
    d = np.linalg.norm(coords[:, None] - coords[None, :], axis=-1)
    d = d[np.triu_indices(len(coords), k=1)]
    r_vals = np.logspace(0, np.log10(np.max(d)*0.5), 40)
    c_r = np.array([np.sum(d < r) / len(d) for r in r_vals])
    valid = (c_r > 1e-8)
    if valid.sum() < 5: return np.nan
    return np.polyfit(np.log10(r_vals[valid]), np.log10(c_r[valid]), 1)[0]

# 3. ∇·R (local divergence of interaction density)
def divergence_field(coords, p=2, h=6.0):
    n = len(coords)
    R = np.zeros(n)
    for i in range(n):
        d = np.linalg.norm(coords - coords[i], axis=1)
        d[i] = 1
        R[i] = np.sum(1 / d**p)
    div = np.zeros(n)
    for i in range(n):
        nb = np.linalg.norm(coords - coords[i], axis=1) < h
        if nb.sum() < 4: continue
        dr = coords[nb] - coords[i]
        dR = R[nb] - R[i]
        norms = np.linalg.norm(dr, axis=1)**3 + 1e-6
        div[i] = np.sum((dR * dr.T).sum(1) / norms)
    return div

# 4. Run
results = []
for pdb in PDBS:
    s = parser.get_structure('', f"{PDB_DIR}/{pdb}.pdb")
    coords = []
    for m in s:
        for c in m:
            for r in c:
                if 'CA' in r:
                    coords.append(r['CA'].coord)
    coords = np.array(coords)
    
    d2 = d2_from_coords(coords)
    div_R = divergence_field(coords)
    
    results.append({
        'pdb': pdb,
        'n_atoms': len(coords),
        'D2': round(d2, 3) if not np.isnan(d2) else 'nan',
        'div_mean': round(div_R.mean(), 5),
        'div_std': round(div_R.std(), 5),
        'div_max': round(div_R.max(), 5),
        'div_min': round(div_R.min(), 5)
    })
    logging.info(f"{pdb}: D₂ = {d2:.3f} | ∇·R = {div_R.mean():.5f} ± {div_R.std():.5f}")

# 5. Print table
print("\n" + "="*60)
print("D₂ vs ∇·R — Empirical Results")
print("="*60)
for r in results:
    print(f"{r['pdb']:6} | D₂ = {r['D2']:5} | ∇·R = {r['div_mean']:8} ± {r['div_std']:6} | range [{r['div_min']}, {r['div_max']}]")