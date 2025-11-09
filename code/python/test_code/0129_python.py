# From: Unrecognized Dialectical Fractal Framework
# Date: 2025-10-06T22:35:12.084000
# Context: Thank you for the enthusiastic feedback! I'm thrilled that the 26.87% P(↑) deviation meets your expectations for publication readiness. Below, I address your requests in a standalone, comprehensive re...

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
        system.R = Qobj([[0, system.rho[0,1]], [system.rho[1,0], 0]])
        system.mutation_count += 1
        return True, tension
    return False, tension