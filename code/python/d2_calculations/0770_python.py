# From: Accessing Data File on GitHub
# Date: 2025-11-02T14:01:10.428000
# Context: **YES — THAT'S THE ENTIRE FORMULA (DFA v21 — FULL-ATOM ONLY)**

---

### **FULL DFA v21 FORMULA (Copy-Paste Ready)**

```python
import math

def dfa_v21_diagnosis(N_residues, observed_D2):
    # Step ...

import math

def dfa_v21_diagnosis(N_residues, observed_D2):
    # Step 1: Expected D₂
    expected_D2 = 2.8 + 0.15 * math.log10(N_residues)
    
    # Step 2: Deviation
    delta_D2 = abs(observed_D2 - expected_D2)
    
    # Step 3: Diagnosis
    if delta_D2 <= 0.5:
        return "NORMAL"
    else:
        return "PATHOLOGY RISK"

# Example:
print(dfa_v21_diagnosis(500, 3.2))
# → NORMAL