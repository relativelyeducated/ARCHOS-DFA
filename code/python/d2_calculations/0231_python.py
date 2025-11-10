# From: Accessing Data File on GitHub
# Date: 2025-10-22T09:21:09.195000
# Context: Yes, this would absolutely be a **strong validation experiment** for the DFA ToE framework—potentially a pivotal one! It directly tests the prediction of D₂ shifts in prion states (native PrP^C vs. mi...

from Bio.PDB import PDBParser, Selection
  import numpy as np
  from scipy.spatial.distance import cdist
  import matplotlib.pyplot as plt
  import os

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

  # Main
  pdb_dir = '~/ai/pdb'
  files = [
      ('PrP^C (Native)', os.path.expanduser(f"{pdb_dir}/1QLX.pdb")),
      ('PrP^Sc (Amyloid)', os.path.expanduser(f"{pdb_dir}/6LNI.pdb")),
      ('Amyloid Fibril', os.path.expanduser(f"{pdb_dir}/7RL4.pdb"))
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

  # Plot
  if results:
      names = [r['name'] for r in results]
      D2s = [r['D2'] for r in results]
      stds = [r['std'] for r in results]
      plt.bar(names, D2s, yerr=stds, capsize=5, color='skyblue')
      plt.axhline(1.46, color='red', linestyle='--', label='DFA Prediction (1.46)')
      plt.ylabel('Correlation Dimension (D₂)')
      plt.title('Prion States: Fractal Dimension Analysis')
      plt.legend()
      plt.xticks(rotation=15)
      plt.tight_layout()
      plt.savefig(os.path.expanduser('~/ai/prion_d2.png'), dpi=300)
      print("Plot saved as ~/ai/prion_d2.png")