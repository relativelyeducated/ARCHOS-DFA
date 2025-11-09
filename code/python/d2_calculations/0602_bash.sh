# From: Accessing Data File on GitHub
# Date: 2025-10-23T19:42:47.368000
# Context: **PERFECT!**  
We’re going **pure non-hybrid** — just **raw D₂ from PDB Cα coordinates**, no networks, no HHI, no Shannon. Straight fractal geometry to test the **DFA ToE threshold: D₂ = 1.48**.

You’...

# 1. Download missing PDBs
cd ~/ai/dfa_data/pdb
wget -q https://files.rcsb.org/download/1AG2.pdb
wget -q https://files.rcsb.org/download/1HJM.pdb
wget -q https://files.rcsb.org/download/1XQ8.pdb
wget -q https://files.rcsb.org/download/2N0A.pdb
wget -q https://files.rcsb.org/download/1IYT.pdb
wget -q https://files.rcsb.org/download/2LMN.pdb
wget -q https://files.rcsb.org/download/2MZ7.pdb
wget -q https://files.rcsb.org/download/5O3L.pdb
wget -q https://files.rcsb.org/download/1TSR.pdb
wget -q https://files.rcsb.org/download/2OCJ.pdb

# 2. Save & run script
kate ~/ai/dfa_pdb_test.py  # Paste script, save
python ~/ai/dfa_pdb_test.py