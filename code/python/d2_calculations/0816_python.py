# From: Accessing Data File on GitHub
# Date: 2025-11-02T15:42:38.477000
# Context: **HERE IS THE FULL SCRIPT — `dfa_v23_full_pipeline.py`**  
**Copy-paste → save → run on your Ryzen 9 9900X KDE Plasma system.**

---

```python
#!/usr/bin/env python3
"""
DFA ToE v23 — FULL PIPELINE
H...

N = 441  # tau from CSF
D2 = 3.1  # from Cryo-EM

if D2 - (2.0 + 0.15 * math.log10(N)) > 0.5:
    print("HIGH RISK: Pre-Alzheimer’s")
else:
    print("LOW RISK")