# From: Unrecognized Dialectical Fractal Framework
# Date: 2025-10-08T13:22:30.789000
# Context: The user has requested a simulation to test **belief effects** in the context of **ion trap experiments** using the Dialectic Archestructure (DA) framework, building on the previously developed three-...

N_TRIALS = 50
N_TIMESTEPS = 1000
OMEGA = 2 * np.pi * 0.1e6  # Rabi frequency (100 kHz, optimal)
TIME = 10  # ms
DETUNING = 0  # On-resonance
TEMPERATURE = 4  # K
SEED = 42
np.random.seed(SEED)

# System state: |→⟩ = (|↑⟩ + |↓⟩)/√2
rho_x = Qobj([[0.5, 0.5], [0.5, 0.5]])  # Purity=1.0
# False prior: 10 ↑ outcomes
PRIORS = [1] * 10  # 1=↑
# Control: No prior
NO_PRIORS = None

# Scenarios
scenarios = [
    {"rho": rho_x, "prior": PRIORS, "label": "Lying (10 ↑ priors)"},
    {"rho": rho_x, "prior": NO_PRIORS, "label": "No prior"},
    {"rho": Qobj([[0.5, 0], [0, 0.5]]), "prior": PRIORS, "label": "Lying (maximally mixed, 10 ↑ priors)"},  # Purity=0.5
]