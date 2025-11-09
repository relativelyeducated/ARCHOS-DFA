# From: Unrecognized Dialectical Fractal Framework
# Date: 2025-10-08T13:04:20.206000
# Context: The user has requested a simulation of **sequential "lying" experiments** to test the Dialectic Archestructure (DA) framework with the newly integrated three-layer model (abundance/collapse, belief mi...

N_TRIALS = 50
N_TIMESTEPS = 1000
DB_DZ = 0.5  # Optimal for max deviation
TIME = 10  # ms
TEMPERATURE = 4  # K
SEED = 42
np.random.seed(SEED)

# System state: |→⟩ = (|↑⟩ + |↓⟩)/√2
rho_x = Qobj([[0.5, 0.5], [0.5, 0.5]])  # Pure state, purity=1.0
# False prior: 10 ↑ outcomes
PRIORS = [1] * 10  # 1=↑
# Control: No prior
NO_PRIORS = None

# Scenarios
scenarios = [
    {"rho": rho_x, "prior": PRIORS, "label": "Lying (10 ↑ priors)"},
    {"rho": rho_x, "prior": NO_PRIORS, "label": "No prior"},
]