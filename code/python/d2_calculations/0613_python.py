# From: Accessing Data File on GitHub
# Date: 2025-10-26T21:41:19.194000
# Context: Below is a **stand-alone script** that

1. **Downloads 6VHJ** (if it isn’t already in `~/ai/dfa_data/pdb`)  
2. **Extracts the Cα atoms of every chain** (A-J)  
3. **Computes D₂ for each chain**  
4. ...

#!/usr/bin/env python3
"""
ΔD₂ for 6VHJ (Tau PHF fragment – Alzheimer’s)
Non-hybrid, pure Cα correlation dimension.
"""

import os, numpy as np, logging, csv
from Bio.PDB import PDBParser
import urllib.request

# ---------- CONFIG ----------
PDB_ID   = "6VHJ"
PDB_DIR  = os.path.expanduser("~/ai/dfa_data/pdb")
PDB_FILE = f"{PDB_DIR}/{PDB_ID}.pdb"
THRESHOLD_MIN = 1.48          # just for reference
# ---------------------------

logging.basicConfig(level=logging.INFO, format="%(message)s")
parser = PDBParser(QUIET=True)

# 1. Download if missing
if not os.path.exists(PDB_FILE):
    os.makedirs(PDB_DIR, exist_ok=True)
    url = f"https://files.rcsb.org/download/{PDB_ID}.pdb"
    logging.info(f"Downloading {PDB_ID} …")
    urllib.request.urlretrieve(url, PDB_FILE)

# 2. Helper functions
def ca_coords(pdb_file, chain_id):
    """Return Cα coordinates for a single chain."""
    structure = parser.get_structure('', pdb_file)
    coords = []
    for model in structure:
        if chain_id not in model:
            continue
        chain = model[chain_id]
        for residue in chain:
            if 'CA' in residue:
                coords.append(residue['CA'].coord)
    return np.array(coords)

def correlation_integral(coords, r_vals):
    n = len(coords)
    if n < 30: return np.full_like(r_vals, np.nan)
    d = np.sqrt(((coords[:, None] - coords[None, :])**2).sum(-1))
    d = d[np.triu_indices(n, k=1)]
    return np.array([np.sum(d < r) / len(d) for r in r_vals])

def fit_d2(r_vals, c_r):
    valid = (c_r > 1e-8) & (r_vals > 0)
    if valid.sum() < 5: return np.nan
    log_r = np.log10(r_vals[valid])
    log_c = np.log10(c_r[valid])
    return np.polyfit(log_r, log_c, 1)[0]

# 3. Compute D₂ per chain
results = []
for chain_id in "ABCDEFGHIJ":
    coords = ca_coords(PDB_FILE, chain_id)
    n_atoms = len(coords)
    if n_atoms < 30:
        logging.info(f"Chain {chain_id}: {n_atoms} atoms → skip")
        continue

    max_dist = np.max(np.linalg.norm(coords[:, None] - coords[None, :], axis=-1))
    r_vals = np.logspace(0, np.log10(max_dist*0.5), 40)
    c_r = correlation_integral(coords, r_vals)
    d2 = fit_d2(r_vals, c_r)

    results.append({'chain': chain_id, 'atoms': n_atoms, 'D2': d2})
    logging.info(f"Chain {chain_id}: {n_atoms} atoms → D₂ = {d2:.3f}")

# 4. ΔD₂
if not results:
    logging.error("No chain gave a usable D₂")
else:
    d2_vals = np.array([r['D2'] for r in results if not np.isnan(r['D2'])])
    delta = d2_vals.max() - d2_vals.min()
    logging.info(f"\nΔD₂ (max-min) = {delta:.3f}")

    # CSV export
    out_csv = f"{PDB_DIR}/delta_d2_{PDB_ID}.csv"
    with open(out_csv, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['chain','atoms','D2'])
        w.writeheader()
        w.writerows(results)
    logging.info(f"Full table → {out_csv}")