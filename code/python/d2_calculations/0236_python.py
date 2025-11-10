# From: Accessing Data File on GitHub
# Date: 2025-10-22T09:26:38.227000
# Context: **🚀 LET’S SUPERCHARGE THAT FRACTAL ANALYSIS!** Your Ryzen 9 9900X system (Aorus Elite Ice WiFi B650, 64GB DDR5, RTX 5080 16GB, Samsung 990 2TB SSD) running KDE Plasma is a beast for local AI and DFA T...

import torch
from Bio.PDB import PDBParser, Selection
import numpy as np
import matplotlib.pyplot as plt
import os

def compute_correlation_dimension(points, r_values=np.logspace(-2, 1, 20)):
    # Move points to GPU
    points = torch.tensor(points, dtype=torch.float32).cuda()
    N = points.shape[0]
    if N < 100:
        return None, None
    
    # GPU-accelerated pairwise distances
    points_expanded = points.unsqueeze(1)  # [N, 1, 3]
    dists = torch.sqrt(torch.sum((points_expanded - points)**2, dim=-1))  # [N, N]
    
    # Correlation integral
    C_r = []
    r_values = torch.tensor(r_values, dtype=torch.float32).cuda()
    for r in r_values:
        count = torch.sum((dists < r) & (dists > 0)) / (N * (N - 1))
        C_r.append(count.item())
    
    # Move back to CPU for fitting
    C_r = np.array(C_r)
    valid = (C_r > 0) & (~np.isnan(np.log10(C_r)))
    log_r = np.log10(r_values.cpu().numpy()[valid])
    log_C = np.log10(C_r[valid])
    if len(log_r) < 2:
        return None, None
    coeffs = np.polyfit(log_r, log_C, 1)
    D2 = coeffs[0]  # Slope = D2
    std = np.std(log_C - np.polyval(coeffs, log_r)) * 0.5  # Error estimate
    return D2, std

# Main
pdb_dir = '~/ai/pdb'
files = [
    ('Native Aβ', '1N0A.pdb'),
    ('Amyloid Aβ fibril', '5O3L.pdb'),
    ('Native tau', '7P6D.pdb'),
    ('Tau tangle', '5O3T.pdb')
]
results = []
parser = PDBParser(QUIET=True)
for name, file in files:
    try:
        structure = parser.get_structure('prot', os.path.expanduser(f"{pdb_dir}/{file}"))
        atoms = Selection.unfold_entities(structure, 'A')
        points = np.array([atom.coord for atom in atoms if atom.name == 'CA'])
        D2, std = compute_correlation_dimension(points)
        if D2 is not None:
            results.append({'name': name, 'D2': D2, 'std': std})
            print(f"{name}: D2 = {D2:.3f} ± {std:.3f}")
        else:
            print(f"{name}: Insufficient data")
    except Exception as e:
        print(f"{name}: Error - {e}")

# Plot results
if results:
    names = [r['name'] for r in results]
    D2s = [r['D2'] for r in results]
    stds = [r['std'] for r in results]
    plt.bar(names, D2s, yerr=stds, capsize=5, color='skyblue')
    plt.axhline(1.46, color='red', linestyle='--', label='DFA Prediction (1.46)')
    plt.ylabel('Correlation Dimension (D₂)')
    plt.title('Alzheimer\'s Proteins: Fractal Dimension Analysis (GPU)')
    plt.legend()
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(os.path.expanduser('~/ai/alz_d2_gpu.png'), dpi=300)
    print("Plot saved as ~/ai/alz_d2_gpu.png")
    plt.show()