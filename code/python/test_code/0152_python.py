# From: Unrecognized Dialectical Fractal Framework
# Date: 2025-10-06T22:56:45.532000
# Context: I understand you want to run a Stern-Gerlach simulation to test the Dialectic Archestructure (DA) framework’s predicted ~30% deviation from the Born rule in outcome probabilities (P(↑)) for a spin-1/2...

import numpy as np
from qutip import Qobj, entropy_vn, tensor, ket, bra
import scipy.stats as stats

# Parameters
N_TRIALS = 50
N_TIMESTEPS = 100
POLARIZATION = 0.2
APPARATUS_DB_DZ_DA = 0.5
APPARATUS_DB_DZ_BORN = 1.5
ARCH_THRESHOLD_I = 0.5
ARCH_THRESHOLD_POS = 0.35
C_EMERGENT_SCALE = 12
COUPLING_FACTOR = 0.1
COHERENCE_DECAY = 0.95
MUTATION_RATE = 0.1
BASELINE_MUTATION_PROB = 0.1
TENSION_ALPHA = 5.0
np.random.seed(42)

class System:
    def __init__(self, polarization=0.2):
        self.rho = Qobj([[0.5 + polarization/2, 0], [0, 0.5 - polarization/2]])
        self.S = Qobj([[self.rho[0,0], 0], [0, self.rho[1,1]]])
        self.R = Qobj([[0, self.rho[0,1]], [self.rho[1,0], 0]])
        self.surplus = 0.0
        self.tension = 0.0
        self.mutation_count = 0

class SimulationResults:
    def __init__(self):
        self.surplus_history = []
        self.tension_history = []
        self.mutation_events = []
        self.arch_log = []
        self.phase_transitions = []
        self.mutation_tension_correlation = 0.0
        self.phase1_mutation_rate = 0.0
        self.phase2_mutation_rate = 0.0
        self.prob_up = []

def calculate_positioning(system, apparatus_dBdz):
    S_sys = abs(system.rho.expect(ket('0')*bra('0') - ket('1')*bra('1')))
    S_app = apparatus_dBdz
    return abs(S_sys - S_app) / (S_sys + S_app + 1e-10)

def calculate_c_emergent(rho_sys, rho_app, rho_joint, scale=12):
    H_sys = entropy_vn(rho_sys)
    H_app = entropy_vn(rho_app)
    H_joint = entropy_vn(rho_joint)
    return scale * max(0, H_sys + H_app - H_joint)

def calculate_tension(system):
    norm_S = np.linalg.norm(system.S.full())
    norm_R = np.linalg.norm(system.R.full())
    return abs(norm_S - norm_R) / (norm_S + norm_R + 1e-10)

def calculate_mutation_probability(tension, baseline_rate=0.1):
    alpha = 5.0
    return baseline_rate * (1 + alpha * tension**2)

def mutate_with_tension(system):
    tension = calculate_tension(system)
    mutation_prob = calculate_mutation_probability(tension)
    if np.random.random() < mutation_prob:
        off_diag = np.random.uniform(-0.01, 0.01)
        system.rho = Qobj(system.rho.full() + [[0, off_diag], [off_diag.conjugate(), 0]])
        system.rho = system.rho / system.rho.tr()
        system.S = Qobj([[system.rho[0,0], 0], [0, system.rho[1,1]]])
        system.R = Qobj([[0, system.rho[0,1]], [self.rho[1,0], 0]])
        system.mutation_count += 1
        return True, tension
    return False, tension

def calculate_p_up(system, c_emergent, arch_formed):
    base_p = system.rho[0,0].real
    if arch_formed:
        return base_p * (1 + 0.5 * c_emergent)
    return base_p

# Run Simulation
da_results_list = []
born_results_list = []
for trial in range(N_TRIALS):
    da_results = SimulationResults()
    born_results = SimulationResults()
    da_system = System(POLARIZATION)
    born_system = System(POLARIZATION)
    rho_app = Qobj([[1, 0], [0, 0]])  # |ready⟩
    H_initial = entropy_vn(da_system.rho)

    for t in range(N_TIMESTEPS):
        # DA
        pos = calculate_positioning(da_system, APPARATUS_DB_DZ_DA)
        rho_joint = tensor(da_system.rho, rho_app)  # Simplified
        c_emergent = calculate_c_emergent(da_system.rho, rho_app, rho_joint, C_EMERGENT_SCALE)
        arch_formed = (0.5 < c_emergent/H_initial < 1.5) and (ARCH_THRESHOLD_POS < pos < 0.7)
        da_system.surplus += 0.1 * c_emergent if arch_formed else 0
        p_up_da = calculate_p_up(da_system, c_emergent, arch_formed)
        mutation_occ, tension = mutate_with_tension(da_system)
        
        da_results.surplus_history.append(da_system.surplus)
        da_results.tension_history.append(tension)
        if mutation_occ:
            da_results.mutation_events.append((t, tension))
        if arch_formed:
            da_results.arch_log.append(t)
        da_results.prob_up.append(p_up_da)
        
        # Born
        born_system = mutate_with_tension(born_system)[0]  # Constant rate
        born_fitness = abs(born_system.rho.expect(ket('0')*bra('0') - ket('1')*bra('1')))
        coherence = born_fitness / (born_fitness + 1)
        born_results.surplus_history.append(3 * coherence)
        born_results.prob_up.append(born_system.rho[0,0].real)

    # Phase Detection
    tension_mean_early = np.mean(da_results.tension_history[:10])
    eq_time = next((t for t, tens in enumerate(da_results.tension_history) if tens < tension_mean_early), N_TIMESTEPS)
    da_results.phase_transitions.append(eq_time)
    phase1_mut = len([e for e, _ in da_results.mutation_events if e < eq_time]) / eq_time
    phase2_mut = len([e for e, _ in da_results.mutation_events if e >= eq_time]) / (N_TIMESTEPS - eq_time)
    da_results.phase1_mutation_rate = phase1_mut
    da_results.phase2_mutation_rate = phase2_mut
    corr, p_val = stats.pearsonr([t for _, t in da_results.mutation_events] + [0] * (N_TIMESTEPS - len(da_results.mutation_events)), 
                                 da_results.tension_history + [0] * (len(da_results.mutation_events) - N_TIMESTEPS))
    da_results.mutation_tension_correlation = corr
    da_results_list.append(da_results)
    born_results_list.append(born_results)

# Aggregate Results
da_surplus = np.mean([r.surplus_history[-1] for r in da_results_list])
da_surplus_std = np.std([r.surplus_history[-1] for r in da_results_list])
born_surplus = np.mean([r.surplus_history[-1] for r in born_results_list])
born_surplus_std = np.std([r.surplus_history[-1] for r in born_results_list])
da_p_up = np.mean([r.prob_up[-1] for r in da_results_list])
da_p_up_std = np.std([r.prob_up[-1] for r in da_results_list])
born_p_up = np.mean([r.prob_up[-1] for r in born_results_list])
born_p_up_std = np.std([r.prob_up[-1] for r in born_results_list])
arch_mean = np.mean([len(r.arch_log) for r in da_results_list])
arch_std = np.std([len(r.arch_log) for r in da_results_list])
corr_mean = np.mean([r.mutation_tension_correlation for r in da_results_list])
phase1_mean = np.mean([r.phase1_mutation_rate for r in da_results_list])
phase2_mean = np.mean([r.phase2_mutation_rate for r in da_results_list])
eq_time_mean = np.mean([r.phase_transitions[0] for r in da_results_list])

# Report
print("=== SURPLUS PRESERVATION ===")
print(f"DA mean: {da_surplus:.4f} ± {da_surplus_std:.4f}")
print(f"Born mean: {born_surplus:.4f} ± {born_surplus_std:.4f}")
print(f"Ratio: {da_surplus/born_surplus:.3f}x")
print(f"t-test p-value: {stats.ttest_ind([r.surplus_history[-1] for r in da_results_list], [r.surplus_history[-1] for r in born_results_list])[1]:.4f}")
print("\n=== ARCH FORMATION ===")
print(f"Mean arches: {arch_mean:.2f} ± {arch_std:.2f}")
print(f"Range: {min(len(r.arch_log) for r in da_results_list)} - {max(len(r.arch_log) for r in da_results_list)}")
print("\n=== MUTATION-TENSION CORRELATION ===")
print(f"Mean correlation (Pearson R): {corr_mean:.3f}")
print(f"p-value: {p_val:.4f}")
print(f"Phase 1 mutation rate: {phase1_mean:.4f}")
print(f"Phase 2 mutation rate: {phase2_mean:.4f}")
print(f"Phase ratio: {phase1_mean/phase2_mean:.2f}x")
print("\n=== TEMPORAL DYNAMICS ===")
print(f"Mean time to equilibrium: {eq_time_mean:.1f} timesteps")
print(f"Surplus trajectory: [t=0,10,25,50,75,99]")
print(f"  DA: {[np.mean([r.surplus_history[i] for r in da_results_list]) for i in [0,10,25,50,75,99]]}")
print(f"  Born: {[np.mean([r.surplus_history[i] for r in born_results_list]) for i in [0,10,25,50,75,99]]}")
print("\n=== OUTCOME PROBABILITIES ===")
print(f"DA mean P(↑): {da_p_up:.4f} ± {da_p_up_std:.4f}")
print(f"Born mean P(↑): {born_p_up:.4f} ± {born_p_up_std:.4f}")
print(f"Difference: {100*(da_p_up - born_p_up):.2f}%")
print(f"t-test p-value: {stats.ttest_ind([r.prob_up[-1] for r in da_results_list], [r.prob_up[-1] for r in born_results_list])[1]:.4f}")