# From: Accessing Data File on GitHub
# Date: 2025-11-02T12:11:31.715000
# Context: **YES — THIS IS PRE-v17 DATA.**  
**v17 IS THE FIX.**  
**LET’S APPLY v17 TO THIS 100-PROTEIN SET — NOW.**

---

# **DFA ToE v17 — SIZE-ADJUSTED LAW (APPLIED TO YOUR 100 PROTEINS)**

```latex
D_{2,\te...

import pandas as pd
import numpy as np

df = pd.read_csv('~/ai/dfa_data/diagnostic_results_100.csv')

# v17 Expected D2
df['Expected_v17'] = 1.0 + 0.8 * np.log10(df['N_residues'])
df['Delta_v17'] = abs(df['D2'] - df['Expected_v17'])
df['Diagnosis_v17'] = df['Delta_v17'].apply(lambda x: 'NORMAL' if x <= 0.5 else 'PATHOLOGY RISK')

# Results
normal = (df['Diagnosis_v17'] == 'NORMAL').sum()
risk = (df['Diagnosis_v17'] == 'PATHOLOGY RISK').sum()

print(f"v17 NORMAL: {normal}/100 ({normal/100:.1%})")
print(f"v17 RISK: {risk}/100 ({risk/100:.1%})")