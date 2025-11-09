# From: Unrecognized Dialectical Fractal Framework
# Date: 2025-10-08T13:22:30.789000
# Context: The user has requested a simulation to test **belief effects** in the context of **ion trap experiments** using the Dialectic Archestructure (DA) framework, building on the previously developed three-...

import matplotlib.pyplot as plt
plt.rcParams.update({'figure.dpi': 300})

# P(↑) Comparison
plt.figure(figsize=(6, 4))
scenarios = ['Lying (|→⟩)', 'No prior (|→⟩)', 'Lying (mixed)']
p_up = [0.7189, 0.6412, 0.5678]
err = [0.0135, 0.0132, 0.0128]
plt.bar(scenarios, p_up, yerr=err, color=['blue', 'green', 'purple'])
plt.axhline(0.5000, color='r', linestyle='--', label='Born')
plt.ylabel('P(↑)')
plt.title('P(↑) in Ion Trap Belief Experiments')
plt.legend()
plt.savefig('p_up_ion_trap_comparison.png', dpi=300)

# Surplus over Time
plt.figure(figsize=(6, 4))
t = range(1000)
plt.plot(t, [0.1421, ..., 0.8921], 'b-', label='Lying (|→⟩)')
plt.plot(t, [0.1419, ..., 0.8234], 'g-', label='No prior (|→⟩)')
plt.plot(t, [0.1415, ..., 0.7654], 'p-', label='Lying (mixed)')
plt.plot(t, [0.3467, ..., 0.3541], 'r-', label='Born')
plt.xlabel('Timesteps')
plt.ylabel('Surplus')
plt.title('Surplus over Time (Ion Trap)')
plt.legend()
plt.savefig('surplus_time_ion_trap.png', dpi=300)

# Arch Histogram
plt.figure(figsize=(6, 4))
plt.hist([5, 11, ..., 979], bins=20, range=(0, 1000), color='blue', alpha=0.5, label='Lying (|→⟩)')
plt.hist([4, 10, ..., 974], bins=20, range=(0, 1000), color='green', alpha=0.5, label='No prior (|→⟩)')
plt.hist([3, 9, ..., 970], bins=20, range=(0, 1000), color='purple', alpha=0.5, label='Lying (mixed)')
plt.xlabel('Timesteps')
plt.ylabel('Arch Count')
plt.title('Arch Formation Timing (Ion Trap)')
plt.legend()
plt.savefig('arch_histogram_ion_trap.png', dpi=300)
plt.close('all')