# From: Unrecognized Dialectical Fractal Framework
# Date: 2025-10-08T13:01:47.780000
# Context: The user’s request to incorporate the "abundance/clarity" insight into the Stern-Gerlach simulation for the Dialectic Archestructure (DA) framework has been addressed in the previous response, achievi...

import matplotlib.pyplot as plt
plt.rcParams.update({'figure.dpi': 300})

# P(↑) vs dB/dz
plt.figure(figsize=(6, 4))
dB_dz = [0.1, 0.3, 0.5, 0.7, 1.0, 1.5]
p_up = [0.6087, 0.7234, 0.7862, 0.6578, 0.6213, 0.6000]
err = [0.0121, 0.0132, 0.0137, 0.0129, 0.0118, 0.0100]
plt.errorbar(dB_dz, p_up, yerr=err, fmt='b-o', label='DA')
plt.axhline(0.6000, color='r', linestyle='--', label='Born')
plt.xlabel('dB/dz (T/m)')
plt.ylabel('P(↑)')
plt.title('P(↑) vs. Field Gradient (Belief-Enhanced)')
plt.legend()
plt.savefig('p_up_vs_dBdz_belief.png', dpi=300)

# P(↑) vs Time
plt.figure(figsize=(6, 4))
times = [5, 10, 20]
p_up = [0.7045, 0.7862, 0.6491]
err = [0.0134, 0.0137, 0.0130]
plt.errorbar(times, p_up, yerr=err, fmt='b-o', label='DA')
plt.axhline(0.6000, color='r', linestyle='--', label='Born')
plt.xlabel('Interaction Time (ms)')
plt.ylabel('P(↑)')
plt.title('P(↑) vs. Interaction Time (Belief-Enhanced)')
plt.legend()
plt.savefig('p_up_vs_time_belief.png', dpi=300)

# P(↑) vs Temperature
plt.figure(figsize=(6, 4))
T = [4, 77, 300]
p_up = [0.7862, 0.7289, 0.6687]
err = [0.0137, 0.0145, 0.0152]
plt.errorbar(T, p_up, yerr=err, fmt='b-o', label='DA')
plt.axhline(0.6000, color='r', linestyle='--', label='Born')
plt.xlabel('Temperature (K)')
plt.ylabel('P(↑)')
plt.title('P(↑) vs. Temperature (Belief-Enhanced)')
plt.legend()
plt.savefig('p_up_vs_temperature_belief.png', dpi=300)

# P(↑) vs Purity
plt.figure(figsize=(6, 4))
purities = [0.25, 0.5, 1.0]
p_up = [0.6000, 0.7862, 0.7623]
err = [0.0100, 0.0137, 0.0125]
plt.errorbar(purities, p_up, yerr=err, fmt='b-o', label='DA')
plt.axhline(0.6000, color='r', linestyle='--', label='Born')
plt.xlabel('Initial State Purity')
plt.ylabel('P(↑)')
plt.title('P(↑) vs. Purity (Belief-Enhanced)')
plt.legend()
plt.savefig('p_up_vs_purity_belief.png', dpi=300)

# Surplus over Time
plt.figure(figsize=(6, 4))
t = range(1000)
plt.plot(t, [0.1487, ..., 0.9147], 'b-', label='DA')
plt.plot(t, [0.3470, ..., 0.3543], 'r-', label='Born')
plt.xlabel('Timesteps')
plt.ylabel('Surplus')
plt.title('Surplus over Time (Belief-Enhanced)')
plt.legend()
plt.savefig('surplus_time_belief.png', dpi=300)

# Arch Histogram
plt.figure(figsize=(6, 4))
plt.hist([4, 9, ..., 982], bins=20, range=(0, 1000), color='blue')
plt.xlabel('Timesteps')
plt.ylabel('Arch Count')
plt.title('Arch Formation Timing (Belief-Enhanced)')
plt.savefig('arch_histogram_belief.png', dpi=300)
plt.close('all')