# From: Unrecognized Dialectical Fractal Framework
# Date: 2025-10-06T21:15:50.568000
# Context: This looks like a solid, thoughtful extension of the bridging framework we've been developing—taking the abstract Dialectic Archestructure (DA) from simulation to testable biology. I'll treat "What ab...

import numpy as np

def s_r_tension(S, R):
    norm_S = np.linalg.norm(S)
    norm_R = np.linalg.norm(R)
    if norm_S + norm_R == 0:
        return 0  # Edge case for zero-activity cells
    return abs(norm_S - norm_R) / (norm_S + norm_R)