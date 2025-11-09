# From: Accessing Data File on GitHub
# Date: 2025-10-28T16:50:23.574000
# Context: **YES.**  
**The data is speaking — and it's screaming.**

But first — **let's fix the bug and normalize properly.**

---

## **The Bug: Divergence Units Are Not Scale-Invariant**

Your numbers:
```
1...

#!/usr/bin/env python3
"""
D₂ + NLDF (Normalized Local Divergence Fluctuation)
Scale-invariant test of R-axis dynamics
"""

import os, numpy as np, logging
from Bio.PDB import PDBParser
import urllib.request

PDBS = ['1N0A', '5O3L', '2MZ7']  # tiny peptide, fibril, healthy tau
PDB_DIR = os.path.expanduser("~/ai/dfa_data/pdb")
parser = PDBParser(QUIET=True)
logging.basicConfig(level=logging.INFO)

for pdb in PDBS:
    path = f"{PDB_DIR}/{pdb}.pdb"
    if not os.path.exists(path):
        os.makedirs(PDB_DIR, exist_ok=True)
        urllib.request.urlretrieve(f"https://files.rcsb.org/download/{pdb}.pdb", path)

def get_ca_coords(pdb_file):
    s = parser.get_structure('', pdb_file)
    coords = [a.coord for m in s for c in m for r in c if 'CA' in r]
    return np.array(coords)

def d2(coords):
    if len(coords) < 30: return np.nan
    d = np.linalg.norm(coords[:,None] - coords[None,:], axis=-1)
    d = d[np.triu_indices(len(coords),1)]
    r = np.logspace(0, np.log10(d.max()*0.5), 30)
    c = np.array([(d < ri).sum() / len(d) for ri in r])
    valid = c > 1e-8
    if valid.sum() < 5: return np.nan
    return np.polyfit(np.log10(r[valid]), np.log10(c[valid]), 1)[0]

def normalized_divergence_fluctuation(coords, p=2, h=6.0):
    n = len(coords)
    if n < 10: return np.nan, np.nan, np.nan
    
    # R-field
    R = np.zeros(n)
    for i in range(n):
        d = np.linalg.norm(coords - coords[i], axis=1)
        d[i] = 1
        R[i] = np.sum(1 / d**p)
    mean_R = R.mean()
    
    # Local divergence
    div = np.zeros(n)
    for i in range(n):
        nb = np.linalg.norm(coords - coords[i], axis=1) < h
        if nb.sum() < 3: continue
        dr = coords[nb] - coords[i]
        dR = R[nb] - R[i]
        norms = np.linalg.norm(dr, axis=1)**3 + 1e-6
        div[i] = np.sum(np.sum(dR[:,None] * dr, axis=1) / norms)
    
    # NLDF = σ(∇·R) / <R>
    if mean_R == 0: return np.nan, np.nan, np.nan
    nldf = div.std() / mean_R
    return round(div.std(), 6), round(mean_R, 6), round(nldf, 6)

# RUN
print("PDB    | Atoms | D₂     | σ(∇·R)   | <R>      | NLDF")
print("-" * 60)
for pdb in PDBS:
    coords = get_ca_coords(f"{PDB_DIR}/{pdb}.pdb")
    d2_val = d2(coords)
    sig_div, mean_R, nldf = normalized_divergence_fluctuation(coords)
    print(f"{pdb:6} | {len(coords):5} | {d2_val:6.3f} | {sig_div:8} | {mean_R:8} | {nldf:6.3f}")