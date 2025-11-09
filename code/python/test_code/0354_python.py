# From: Unrecognized Dialectical Fractal Framework
# Date: 2025-10-08T18:49:17.588000
# Context: # BRIEFING DOCUMENT: UNIFYING THE DISCOVERIES IN A SIMULTANEOUS SIMULATION

---

## CONTEXT: What We've Done

We have validated a series of interconnected discoveries through simulations and theoretic...

class SimulationResults:
    pull_history: List[float]
    entropy_gradient_history: List[float]
    arch_log: List[Tuple[int, float]]  # (timestep, gradient_at_arch)
    phase_transitions: List[int]  # timesteps where phase changed
    
    # NEW: Correlation metrics
    entropy_pull_correlation: float  # Pearson R
    phase1_pull_rate: float  # pull per timestep in gradient phase
    phase2_pull_rate: float  # pull per timestep in maintenance phase