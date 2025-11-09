# From: Python Setup: PyTorch Environment Configuration
# Date: 2025-10-15T20:18:08.727000
# Context: **AWESOME!** 🎉 **`data.dat` IS ALREADY IN `pytorch_env`** ✅ **RTX 5080 READY!** 🔥

## **INSTANT NEUTRINO DATA TEST (Copy-Paste NOW):**

### **STEP 1: Activate + Check File**
```bash
source pytorch_env...

import torch
import numpy as np

# Auto-detect format
try:
    data = torch.load('data.dat').cuda()
except:
    data = torch.from_numpy(np.fromfile('data.dat', dtype=np.float32)).cuda()

print(f"🚀 {data.numel():,} neutrinos on RTX 5080!")
print(f"Shape: {data.shape}")
print(f"Memory: {torch.cuda.memory_allocated()/1e9:.1f}GB")