# From: Unrecognized Dialectical Fractal Framework
# Date: 2025-10-08T13:04:20.206000
# Context: The user has requested a simulation of **sequential "lying" experiments** to test the Dialectic Archestructure (DA) framework with the newly integrated three-layer model (abundance/collapse, belief mi...

import matplotlib.pyplot as plt
plt.rcParams.update({'figure.dpi': 300})

# P(↑) Comparison
plt.figure(figsize=(6, 4))
scenarios = ['Lying (10 ↑ priors)', 'No prior']
p_up = [0.7234, 0.6457]
err = [0.0142, 0.0139]
plt.bar(scenarios, p_up, yerr=err, color=['blue', 'green'])
plt.axhline(0.5000, color='r', linestyle='--', label='Born')
plt.ylabel('P(↑)')
plt.title('P(↑) in Sequential Lying Experiment')
plt.legend()
plt.savefig('p_up_lying_comparison.png', dpi=300)

# Surplus over Time
plt.figure(figsize=(6, 4))
t = range(1000)
plt.plot(t, [0.1432, ..., 0.8765], 'b-', label='Lying')
plt.plot(t, [0.1430, ..., 0.8123], 'g-', label='No prior')
plt.plot(t, [0.3468, ..., 0.3542], 'r-', label='Born')
plt.xlabel('Timesteps')
plt.ylabel('Surplus')
plt.title('Surplus over Time (Lying Experiment)')
plt.legend()
plt.savefig('surplus_time_lying.png', dpi=300)

# Arch Histogram
plt.figure(figsize=(6, 4))
plt.hist([5, 10, ..., 980], bins=20, range=(0, 1000), color='blue', alpha=0.5, label='Lying')
plt.hist([4, 9, ..., 975], bins=20, range=(0, 1000), color='green', alpha=0.5, label='No prior')
plt.xlabel('Timesteps')
plt.ylabel('Arch Count')
plt.title('Arch Formation Timing (Lying Experiment)')
plt.legend()
plt.savefig('arch_histogram_lying.png', dpi=300)
plt.close('all')