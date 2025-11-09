# From: Accessing Data File on GitHub
# Date: 2025-10-23T19:42:47.368000
# Context: **PERFECT!**  
We’re going **pure non-hybrid** — just **raw D₂ from PDB Cα coordinates**, no networks, no HHI, no Shannon. Straight fractal geometry to test the **DFA ToE threshold: D₂ = 1.48**.

You’...

#!/usr/bin/env python3
"""
PURE NON-HYBRID D₂ TEST FOR DFA ToE
10 PDBs: Healthy vs. Diseased
Threshold: D₂ = 1.48
"""

import numpy as np
from Bio.PDB import PDBParser
import os
import logging

logging.basicConfig(level=logging.INFO)
parser = PDBParser(QUIET=True)

# === CONFIG ===
PDB_DIR = "~/ai/dfa_data/pdb"
TEST_PDBS = {
    '1AG2': 'Healthy Prion',
    '1HJM': 'Diseased Prion',
    '1XQ8': 'Healthy α-syn',
    '2N0A': 'Diseased α-syn',
    '1IYT': 'Healthy Aβ',
    '2LMN': 'Diseased Aβ',
    '2MZ7': 'Healthy Tau',
    '5O3L': 'Diseased Tau',
    '1TSR': 'Healthy p53',
    '2OCJ': 'Diseased p53'
}
THRESHOLD = 1.48
# =============

def get_ca_coords(pdb_file):
    structure = parser.get_structure('', pdb_file)
    coords = []
    for model in structure:
        for chain in model:
            for residue in chain:
                if 'CA' in residue:
                    coords.append(residue['CA'].coord)
    return np.array(coords)

def correlation_integral(coords, r_values):
    n = len(coords)
    distances = np.sqrt(((coords[:, None] - coords[None, :]) ** 2).sum(-1))
    distances = distances[np.triu_indices(n, k=1)]
    return np.array([np.sum(distances < r) / len(distances) for r in r_values])

def fit_d2(r_values, c_r):
    valid = (c_r > 1e-8) & (r_values > 0)
    if sum(valid) < 5: return np.nan
    log_r = np.log10(r_values[valid])
    log_c = np.log10(c_r[valid])
    coeffs = np.polyfit(log_r, log_c, 1)
    return coeffs[0]

def analyze_pdb(pdb_id):
    pdb_file = os.path.expanduser(f"{PDB_DIR}/{pdb_id}.pdb")
    if not os.path.exists(pdb_file):
        logging.error(f"{pdb_id}.pdb not found!")
        return None
    
    coords = get_ca_coords(pdb_file)
    if len(coords) < 50:
        logging.warning(f"{pdb_id}: too few atoms ({len(coords)})")
        return None
    
    max_dist = np.max(np.linalg.norm(coords[:, None] - coords[None, :], axis=-1))
    r_values = np.logspace(0, np.log10(max_dist*0.5), 40)
    c_r = correlation_integral(coords, r_values)
    d2 = fit_d2(r_values, c_r)
    
    state = "DISEASED" if 'Diseased' in TEST_PDBS[pdb_id] else "HEALTHY"
    pred = "FAIL" if (d2 > THRESHOLD and state == "HEALTHY") or (d2 < THRESHOLD and state == "DISEASED") else "PASS"
    
    logging.info(f"{pdb_id}: D₂ = {d2:.3f} | {state} | {pred}")
    return {'id': pdb_id, 'd2': d2, 'state': state, 'pred': pred}

# === RUN ===
results = []
for pdb in TEST_PDBS:
    res = analyze_pdb(pdb)
    if res: results.append(res)

# === SUMMARY ===
correct = sum(1 for r in results if r['pred'] == 'PASS')
logging.info(f"\nVALIDATION: {correct}/10 CORRECT")
logging.info(f"THRESHOLD: D₂ = {THRESHOLD}")