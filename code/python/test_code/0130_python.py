# From: Unrecognized Dialectical Fractal Framework
# Date: 2025-10-06T22:35:12.084000
# Context: Thank you for the enthusiastic feedback! I'm thrilled that the 26.87% P(↑) deviation meets your expectations for publication readiness. Below, I address your requests in a standalone, comprehensive re...

def calculate_p_up(system, c_emergent, arch_formed):
    base_p = system.rho[0,0].real
    if arch_formed:
        return base_p * (1 + 0.5 * c_emergent)
    return base_p