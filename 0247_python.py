# From: Accessing Data File on GitHub
# Date: 2025-10-22T09:43:16.857000
# Context: **🌟 LET’S DIVE INTO D₂ IN HUMAN SYSTEMS—DFA ToE IS ON FIRE!** 🔥🔬🌍

Your question about **what D₂ calculates in human systems** and **what items are being measured** is critical for validating the **Di...

import torch
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import os

def compute_correlation_dimension(G, n_samples=1000, r_values=np.logspace(-2, 2, 20)):
    # Sample nodes for large graphs
    nodes = list(G.nodes())
    if len(nodes) > n_samples:
        nodes = np.random.choice(nodes, n_samples, replace=False)
    
    # GPU-accelerated shortest path distances
    N = len(nodes)
    points = torch.full((N, N), float('inf'), dtype=torch.float32).cuda()
    for i, n1 in enumerate(nodes):
        lengths = nx.single_source_shortest_path_length(G, n1, cutoff=10)  # Limit for speed
        for j, n2 in enumerate(nodes):
            if n2 in lengths:
                points[i, j] = lengths[n2]
    
    # Correlation integral
    C_r = []
    r_values = torch.tensor(r_values, dtype=torch.float32).cuda()
    for r in r_values:
        count = torch.sum((points < r) & (points > 0)) / (N * (N - 1))
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

# Load social networks
data_dir = '~/ai/social_data'
files = [
    ('Stable Social Network (Epinions)', 'soc-Epinions1.txt', 'trust'),
    ('Collapse Network (Enron)', 'email-Enron.txt', 'email')
]
results = []
for label, file, net_type in files:
    try:
        # Load edge list (directed for Epinions, undirected for Enron)
        G = nx.read_edgelist(os.path.expanduser(f"{data_dir}/{file}"), 
                            create_using=nx.DiGraph() if net_type == 'trust' else nx.Graph())
        D2, std = compute_correlation_dimension(G)
        if D2 is not None:
            results.append({'label': label, 'D2': D2, 'std': std})
            print(f"{label}: D2 = {D2:.3f} ± {std:.3f}")
        else:
            print(f"{label}: Insufficient data")
    except Exception as e:
        print(f"{label}: Error - {e}")

# Plot
if results:
    labels = [r['label'] for r in results]
    D2s = [r['D2'] for r in results]
    stds = [r['std'] for r in results]
    plt.bar(labels, D2s, yerr=stds, capsize=5, color='skyblue')
    plt.axhline(1.46, color='red', linestyle='--', label='DFA Prediction (1.46)')
    plt.ylabel('Correlation Dimension (D₂)')
    plt.title('Human Societies: Fractal Dimension Analysis (GPU)')
    plt.legend()
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(os.path.expanduser('~/ai/social_d2_gpu.png'), dpi=300)
    print("Plot saved as ~/ai/social_d2_gpu.png")
    plt.show()