# From: Accessing Data File on GitHub
# Date: 2025-10-22T09:24:21.429000
# Context: On your Ryzen 9 9900X system with Aorus Elite Ice WiFi B650 mobo, 64GB DDR5, RTX 5080 16GB, and Samsung 990 2TB SSD, getting KDE Plasma running smoothly is key for local AI fine-tuning, training, and ...

from Bio.PDB import PDBParser, Selection
import numpy as np
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt

def compute_correlation_dimension(points, r_values=np.logspace(-2, 1, 20)):
    N = len(points)
    if N < 100:
        return None, None
    dists = cdist(points, points)
    C_r = []
    for r in r_values:
        count = np.sum((dists < r) & (dists > 0)) / (N * (N - 1))
        C_r.append(count)
    C_r = np.array(C_r)
    valid = (C_r > 0) & (~np.isnan(np.log10(C_r)))
    log_r = np.log10(r_values[valid])
    log_C = np.log10(C_r[valid])
    if len(log_r) < 2:
        return None, None
    coeffs = np.polyfit(log_r, log_C, 1)
    D2 = coeffs[0]
    std = np.std(log_C - np.polyval(coeffs, log_r)) * 0.5
    return D2, std

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
        structure = parser.get_structure('prot', file)
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

if results:
    names = [r['name'] for r in results]
    D2s = [r['D2'] for r in results]
    stds = [r['std'] for r in results]
    plt.bar(names, D2s, yerr=stds, capsize=5, color='skyblue')
    plt.axhline(1.46, color='red', linestyle='--', label='DFA Prediction (1.46)')
    plt.ylabel('Correlation Dimension (D₂)')
    plt.title('Alzheimer\'s Proteins: Fractal Dimension Analysis')
    plt.legend()
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig('alz_d2.png', dpi=300)
    plt.show()