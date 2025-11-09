# From: Accessing Data File on GitHub
# Date: 2025-11-02T13:10:16.890000
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
im...

cd ~/Downloads/pdb
python ~/ai/dfa_v18_analysis.py