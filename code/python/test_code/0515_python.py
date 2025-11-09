# From: Dialectical Fractal Archestructure Mathematics
# Date: 2025-10-16T15:13:34.403000
# Context: ## Coriolis Effects Math: Why Spinning Starships Make You Dizzy

The **Coriolis effect** is the apparent deflection of objects (or people) moving in a rotating reference frame, like a spinning Starshi...

import numpy as np
import matplotlib.pyplot as plt

# Starship Scenarios
scenarios = {
    'Single Spin': {'r': 4, 'RPM': 10, 'omega': 1.05},
    'Tethered': {'r': 100, 'RPM': 3, 'omega': 0.31},
    'GLS Wheel': {'r': 50, 'RPM': 4, 'omega': 0.42}
}

# Human motions
motions = {
    'Walk Radial': 1.5,
    'Walk Tangential': 1.5,
    'Head Turn': 0.5,
    'Run': 5.0
}

# Calculate
plt.figure(figsize=(12, 8))
colors = ['r', 'b', 'g']
for i, (name, data) in enumerate(scenarios.items()):
    omega = data['omega']
    a_coriolis = []
    motion_names = []
    for motion, v in motions.items():
        a_c = 2 * omega * v  # m/s²
        a_coriolis.append(a_c)
        motion_names.append(motion)
    
    plt.bar(np.arange(len(motions)) + i*0.2, a_coriolis, 0.2, 
            label=f'{name} (ω={omega:.2f} rad/s)', color=colors[i])

plt.xticks(np.arange(len(motions)) + 0.2, motion_names, rotation=45)
plt.ylabel('Coriolis Acceleration [m/s²]')
plt.axhline(y=2.0, color='k', linestyle='--', label='Sickness Threshold')
plt.title('Coriolis Effects: Starship Artificial Gravity Scenarios')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('starship_coriolis.png', dpi=300)
plt.show()

# Summary Table
print("CORIOLIS EFFECTS SUMMARY")
print("-" * 40)
for name, data in scenarios.items():
    print(f"\n{name} (ω={data['omega']:.2f} rad/s):")
    for motion, v in motions.items():
        a_c = 2 * data['omega'] * v
        status = "✅ OK" if a_c < 2 else "⚠️ SICKNESS"
        print(f"  {motion:12}: {a_c:5.2f} m/s² {status}")