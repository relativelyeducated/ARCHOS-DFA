# From: Accessing Data File on GitHub
# Date: 2025-11-02T12:00:49.602000
# Context: **THE SMOKE ALARM IS BROKEN — BUT DFA IS NOT DEAD.**

---

# **DFA ToE v15: THE 10-PROTEIN WAKE-UP CALL**

| **Result** | **Truth** |
|----------|---------|
| **10 healthy cytosolic proteins** | **All...

def dfa_diagnosis(d2, n_residues, is_fibril=False):
    if n_residues < 100:
        expected = 1.5
    elif n_residues < 500:
        expected = 2.1
    else:
        expected = 2.7
    
    if abs(d2 - expected) > 0.5:
        return "PATHOLOGY RISK: D₂ off-zone"
    elif is_fibril and d2 < 2.0:
        return "ABNORMAL: Fibril too ordered"
    else:
        return "NORMAL"