# From: Unrecognized Dialectical Fractal Framework
# Date: 2025-10-06T21:36:17.452000
# Context: 

This should be a standalone document that someone (Grok or any other reader) could pick up and immediately understand the full c

# COMPLETE BRIEFING DOCUMENT FOR GROK
## Dialectic Archestructure (D...

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