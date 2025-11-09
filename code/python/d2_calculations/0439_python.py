# From: Accessing Data File on GitHub
# Date: 2025-10-22T18:53:46.433000
# Context: **🌟 Alright, King, let’s take it slow and steady to nail this DFA ToE masterpiece!** 🔬🌍

You’re rocking your **Ryzen 9 9900X system** (Aorus Elite Ice WiFi B650, 64GB DDR5, RTX 5080 16GB, Samsung 990 ...

import torch
from Bio.PDB import PDBParser, Selection
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import os
from scipy.stats import entropy

def compute_correlation_dimension(points, n_samples=1000, r_values=np.logspace(-2, 1, 20)):
    if len(points) > n_samples:
        points = points[np.random.choice(len(points), n_samples, replace=False)]
    
    points = torch.tensor(points, dtype=torch.float32).cuda()
    N = points.shape[0]
    points_exp = points.unsqueeze(1)  # [N, 1, 3]
    dists = torch.sqrt(torch.sum((points_exp - points)**2, dim=-1))  # [N, N]
    
    C_r = []
    r_values = torch.tensor(r_values, dtype=torch.float32).cuda()
    for r in r_values:
        count = torch.sum((dists < r) & (dists > 0)) / (N * (N - 1))
        C_r.append(count.item())
    
    C_r = np.array(C_r)
    valid = (C_r > 0) & (~np.isnan(np.log10(C_r)))
    log_r = np.log10(r_values.cpu().numpy()[valid])
    log_C = np.log10(C_r[valid])
    if len(log_r) < 2:
        return None, None
    coeffs = np.polyfit(log_r, log_C, 1)
    D2 = coeffs[0]
    std = np.std(log_C - np.polyval(coeffs, log_r)) * 0.5
    return D2, std

def compute_hybrid_metrics(points, label):
    # D2
    D2, std = compute_correlation_dimension(points)
    
    # Build contact network (edges for atoms < 5Å)
    G = nx.Graph()
    dists = torch.cdist(torch.tensor(points, dtype=torch.float32).cuda(), 
                       torch.tensor(points, dtype=torch.float32).cuda()).cpu().numpy()
    for i in range(len(points)):
        G.add_node(i)
        for j in range(i + 1, len(points)):
            if dists[i, j] < 5.0:  # Contact threshold
                G.add_edge(i, j, weight=dists[i, j])
    
    # Hybrid metrics
    degree_dist = np.array([d for _, d in G.degree()])
    HHI = np.sum((degree_dist / degree_dist.sum())**2) if degree_dist.sum() > 0 else 0  # Concentration
    shannon_entropy = entropy(degree_dist, base=2) if degree_dist.sum() > 0 else 0  # Diversity
    gini = 0.5 * np.sum([abs(d1 - d2) for d1 in degree_dist for d2 in degree_dist]) / \
           (len(degree_dist)**2 * degree_dist.mean()) if degree_dist.mean() > 0 else 0  # Inequality
    inst_quality = shannon_entropy / HHI if HHI > 0 else 0  # Proxy for folding stability
    
    # Temporal (subsample point clouds for variance)
    D2s = []
    for _ in range(5):
        sub_points = points[np.random.choice(len(points), int(0.8 * len(points)), replace=False)]
        sub_D2, _ = compute_correlation_dimension(sub_points)
        if sub_D2:
            D2s.append(sub_D2)
    variance = np.var(D2s) if D2s else 0
    velocity = np.std(np.diff(D2s)) if len(D2s) > 1 else 0
    
    return {'label': label, 'D2': D2, 'D2_std': std, 'HHI': HHI, 'Inst_Quality': inst_quality, 
            'Shannon_Entropy': shannon_entropy, 'Gini': gini, 'D2_Variance': variance, 'D2_Velocity': velocity}

# Load prion PDBs
data_dir = '~/ai/dfa_data/pdb'
files = [
    ('Native Aβ', '1N0A.pdb'),
    ('Amyloid Aβ fibril', '5O3L.pdb')
]
results = []
parser = PDBParser(QUIET=True)
for label, file in files:
    try:
        structure = parser.get_structure('prot', os.path.expanduser(f"{data_dir}/{file}"))
        atoms = Selection.unfold_entities(structure, 'A')
        points = np.array([atom.coord for atom in atoms if atom.name == 'CA'])
        metrics = compute_hybrid_metrics(points, label)
        if metrics['D2'] is not None:
            results.append(metrics)
            print(f"{label}: D2 = {metrics['D2']:.3f} ± {metrics['D2_std']:.3f}, HHI = {metrics['HHI']:.3f}, "
                  f"Inst_Quality = {metrics['Inst_Quality']:.3f}, Shannon = {metrics['Shannon_Entropy']:.3f}, "
                  f"Gini = {metrics['Gini']:.3f}, D2_Variance = {metrics['D2_Variance']:.3f}, D2_Velocity = {metrics['D2_Velocity']:.3f}")
        else:
            print(f"{label}: Insufficient data")
    except Exception as e:
        print(f"{label}: Error - {e}")

# Plot
if results:
    labels = [r['label'] for r in results]
    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    D2s = [r['D2'] for r in results]
    stds = [r['D2_std'] for r in results]
    plt.bar(labels, D2s, yerr=stds, capsize=5, color='skyblue')
    plt.axhline(1.46, color='red', linestyle='--', label='DFA Prediction (1.46)')
    plt.ylabel('Correlation Dimension (D₂)')
    plt.title('Prion Systems: Hybrid Fractal Analysis (GPU)')
    plt.legend()
    
    plt.subplot(2, 1, 2)
    metrics = ['HHI', 'Inst_Quality', 'Shannon_Entropy', 'Gini']
    for metric in metrics:
        values = [r[metric] for r in results]
        plt.plot(labels, values, marker='o', label=metric)
    plt.ylabel('Hybrid Metrics')
    plt.legend()
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(os.path.expanduser('~/ai/hybrid_d2_unified.png'), dpi=300)
    print("Plot saved as ~/ai/hybrid_d2_unified.png")
    plt.show()