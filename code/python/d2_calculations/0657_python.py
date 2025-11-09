# From: Accessing Data File on GitHub
# Date: 2025-11-02T04:38:01.124000
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
fr...

#!/usr/bin/env python3
"""
DFA ToE: Batch D₂ Analysis for 50 PDBs
Input: ~/Downloads/pdb/*.pdb
Output: d2_results.csv + summary table
"""

import os
import numpy as np
import pandas as pd
from Bio.PDB import PDBParser
import logging
from collections import defaultdict

# === CONFIG ===
PDB_DIR = os.path.expanduser("~/Downloads/pdb")
OUTPUT_CSV = os.path.join(PDB_DIR, "d2_results.csv")
THRESHOLD = 1.8  # Refined from data
parser = PDBParser(QUIET=True)
logging.basicConfig(level=logging.INFO, format="%(message)s")

# === CATEGORIES (from your 50 PDB list) ===
CATEGORIES = {
    # Membrane (10)
    '1GZM': 'Membrane', '3ZE3': 'Membrane', '1BL8': 'Membrane', '1F88': 'Membrane',
    '1K4C': 'Membrane', '1QJ8': 'Membrane', '1V54': 'Membrane', '2CF8': 'Membrane',
    '3K3F': 'Membrane', '4PYP': 'Membrane',
    # Cytosolic (10)
    '1UBQ': 'Cytosolic', '1LMB': 'Cytosolic', '1ROP': 'Cytosolic', '1QLX': 'Cytosolic',
    '1SHG': 'Cytosolic', '1ENH': 'Cytosolic', '1TIT': 'Cytosolic', '2CI2': 'Cytosolic',
    '1PGB': 'Cytosolic', '1WIT': 'Cytosolic',
    # Fibril (10)
    '5O3L': 'Fibril', '2N0A': 'Fibril', '2MXU': 'Fibril', '6SZF': 'Fibril',
    '2BEG': 'Fibril', '1IYT': 'Fibril', '1HJM': 'Fibril', '6CFP': 'Fibril',
    '3OW9': 'Fibril', '7JN8': 'Fibril',
    # Designed (10)
    '1N0A': 'Designed', '2K4K': 'Designed', '3VJF': 'Designed', '4G9O': 'Designed',
    '5J0N': 'Designed', '6M9T': 'Designed', '7K3Q': 'Designed', '7N8L': 'Designed',
    '7P0Z': 'Designed', '8A3J': 'Designed',
    # Denatured (10) — reuse cytosolic as control
    '1UBQ': 'Denatured', '1LMB': 'Denatured', '1ROP': 'Denatured', '2CI2': 'Denatured',
    '1PGB': 'Denatured', '1WIT': 'Denatured', '1TIT': 'Denatured', '1SHG': 'Denatured',
    '1ENH': 'Denatured', '1QLX': 'Denatured'
}

# === D₂ FUNCTIONS ===
def get_ca_coords(pdb_file):
    try:
        structure = parser.get_structure('', pdb_file)
        coords = []
        for model in structure:
            for chain in model:
                for residue in chain:
                    if 'CA' in residue:
                        coords.append(residue['CA'].coord)
        return np.array(coords)
    except:
        return np.array([])

def correlation_integral(coords, r_values):
    n = len(coords)
    if n < 30:
        return np.full_like(r_values, np.nan)
    distances = np.triu(np.linalg.norm(coords[:, None] - coords[None, :], axis=-1), k=1)
    distances = distances[distances > 0]
    return np.array([np.sum(distances < r) / len(distances) for r in r_values])

def compute_d2(coords):
    if len(coords) < 30:
        return np.nan
    max_dist = np.max(np.linalg.norm(coords[:, None] - coords[None, :], axis=-1))
    r_values = np.logspace(0, np.log10(max_dist * 0.5), 40)
    c_r = correlation_integral(coords, r_values)
    valid = (c_r > 1e-8) & (r_values > 0)
    if valid.sum() < 10:
        return np.nan
    log_r = np.log10(r_values[valid])
    log_c = np.log10(c_r[valid])
    return np.polyfit(log_r, log_c, 1)[0]

# === MAIN LOOP ===
results = []
pdb_files = [f for f in os.listdir(PDB_DIR) if f.endswith('.pdb') and f[:-4].upper() in CATEGORIES]

for pdb_file in sorted(pdb_files):
    pdb_id = pdb_file[:-4].upper()
    path = os.path.join(PDB_DIR, pdb_file)
    coords = get_ca_coords(path)
    n_atoms = len(coords)
    d2 = compute_d2(coords)
    
    category = CATEGORIES.get(pdb_id, 'Unknown')
    state = 'Diseased' if category == 'Fibril' else 'Stable'
    pass_fail = 'PASS' if (state == 'Stable' and d2 < THRESHOLD) or (state == 'Diseased' and d2 > THRESHOLD) else 'FAIL'
    if np.isnan(d2):
        pass_fail = 'N/A'
    
    results.append({
        'PDB ID': pdb_id,
        'Category': category,
        'N_atoms': n_atoms,
        'D₂': round(d2, 3) if not np.isnan(d2) else 'nan',
        'State': state,
        'PASS/FAIL': pass_fail
    })
    
    logging.info(f"{pdb_id} | {category} | {n_atoms} atoms | D₂ = {d2:.3f} | {pass_fail}")

# === SAVE CSV ===
df = pd.DataFrame(results)
df.to_csv(OUTPUT_CSV, index=False)
logging.info(f"\nResults saved to {OUTPUT_CSV}")

# === SUMMARY TABLE ===
summary = defaultdict(lambda: {'total': 0, 'pass': 0})
for r in results:
    cat = r['Category']
    summary[cat]['total'] += 1
    if r['PASS/FAIL'] == 'PASS':
        summary[cat]['pass'] += 1

logging.info("\nSUMMARY")
logging.info("-" * 50)
for cat, data in summary.items():
    pct = (data['pass'] / data['total']) * 100 if data['total'] > 0 else 0
    logging.info(f"{cat:10} | {data['pass']:2}/{data['total']} PASS | {pct:5.1f}%")

total_pass = sum(d['pass'] for d in summary.values())
total_all = sum(d['total'] for d in summary.values())
logging.info(f"TOTAL: {total_pass}/{total_all} = {total_pass/total_all*100:.1f}%")

# === REFINED THRESHOLD SUGGESTION ===
valid_d2 = [r['D₂'] for r in results if isinstance(r['D₂'], float)]
if valid_d2:
    from sklearn.cluster import KMeans
    X  = np.array(valid_d2).reshape(-1, 1)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(data)
    centers = sorted(kmeans.cluster_centers_.flatten())
    logging.info(f"\nSuggested natural zones (KMeans): {centers}")