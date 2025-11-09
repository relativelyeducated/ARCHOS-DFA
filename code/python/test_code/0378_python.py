# From: Unrecognized Dialectical Fractal Framework
# Date: 2025-10-08T18:49:17.588000
# Context: # BRIEFING DOCUMENT: UNIFYING THE DISCOVERIES IN A SIMULTANEOUS SIMULATION

---

## CONTEXT: What We've Done

We have validated a series of interconnected discoveries through simulations and theoretic...

class SimulationResults:
    surplus_history: List[float]
    tension_history: List[float]
    mutation_events: List[Tuple[int, float]]  # (timestep, tension_at_mutation)
    arch_log: List[ArchEvent]
    phase_transitions: List[int]  # timesteps where phase changed
    
    # NEW: Correlation metrics
    mutation_tension_correlation: float  # Pearson R
    phase1_mutation_rate: float  # mutations per timestep in positioning phase
    phase2_mutation_rate: float  # mutations per timestep in maintenance phase