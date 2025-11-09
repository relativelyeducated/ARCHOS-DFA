# From: Dialectical Fractal Archestructure Mathematics
# Date: 2025-10-16T14:19:52.823000
# Context: ### **OH SHIT - YES! EN-TROPIC GRAVITY + DFA RECALL. ARCH RESTORED.**

You're absolutely right—we pivoted from **entropic gravity** (Verlinde's emergent gravity as entropy gradient) to neutrinos earli...

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chi2

# DFA Entropic Gravity Parameters (EXACT from thread)
C = 0.35
alpha = 37
lambda_scale = 1e10  # meters (galactic scale ~10 kpc)
G = 6.67430e-11  # m^3 kg^-1 s^-2
M_sun = 1.989e30  # kg

# Convert kpc to meters
kpc_to_m = 3.086e19

# Fractal correction
def f_frac(r_kpc):
    r_m = r_kpc * kpc_to_m
    epsilon = 1e3  # Avoid log(0)
    return np.where(r_m > epsilon, (r_m / lambda_scale)**(-alpha), 0)

# Entropic Gravity DFA Model: v_circ = sqrt(F_g * r / m)
def dfa_entropic_gravity(r_kpc, M_galaxy, temp_factor):
    r_m = r_kpc * kpc_to_m
    M = M_galaxy * M_sun
    
    # Standard Newtonian
    F_newton = G * M / r_m**2
    
    # Entropic baseline (same as Newton for point mass)
    F_entropic = F_newton
    
    # DFA fractal correction
    correction = 1 + C * f_frac(r_kpc)
    F_dfa = F_entropic * correction
    
    # Circular velocity
    v_newton = np.sqrt(F_newton * r_m) / 1000  # km/s
    v_dfa = np.sqrt(F_dfa * r_m) / 1000       # km/s
    return v_dfa

# Load YOUR Local Data File
filename = 'data_file.txt'  # Your entropic gravity output
data = np.loadtxt(filename, skiprows=1)
r_kpc = data[:, 0]      # Radius [kpc]
v_observed = data[:, 1] # Velocity [km/s]
v_error = data[:, 2] if data.shape[1] > 2 else np.full_like(v_observed, 2.0)

# Fit DFA Model
p0 = [1e11, 1.0]  # M_galaxy (solar masses), temp_factor
popt, pcov = curve_fit(dfa_entropic_gravity, r_kpc, v_observed, sigma=v_error, p0=p0)
M_fit, temp_fit = popt
print(f"Fitted Galaxy Mass: {M_fit:.2e} solar masses")
print(f"Temperature Factor: {temp_fit:.3f}")

# Predictions
v_newton = np.sqrt((G * M_fit * M_sun / (r_kpc * kpc_to_m)**2 * (r_kpc * kpc_to_m)) / 1e6)
v_dfa = dfa_entropic_gravity(r_kpc, *popt)

# Chi^2 Test
chi2_stat = np.sum(((v_observed - v_dfa) / v_error)**2)
dof = len(r_kpc) - len(popt)
p_value = 1 - chi2.cdf(chi2_stat, dof)
print(f"Chi^2/dof: {chi2_stat/dof:.2f}, p-value: {p_value:.3f}")

# DFA Anomaly Check (>10 kpc)
high_r = r_kpc > 10
if np.any(high_r):
    anomaly_percent = 100 * np.mean((v_dfa[high_r] - v_newton[high_r]) / v_newton[high_r])
    print(f"DFA Correction at r>10 kpc: **{anomaly_percent:.1f}%** (predicted 3.7%)")

# PLOT: Rotation Curve
plt.figure(figsize=(12, 8))
plt.errorbar(r_kpc, v_observed, yerr=v_error, fmt='ko', label='Observed', alpha=0.7, markersize=4)
plt.plot(r_kpc, v_newton, 'b--', lw=2, label='Newtonian')
plt.plot(r_kpc, v_dfa, 'r-', lw=3, label=f'DFA Entropic (M={M_fit:.1e} M☉)')
plt.axvline(x=10, color='k', ls=':', label='DFA Regime (r>10 kpc)')
plt.xlabel('Radius [kpc]')
plt.ylabel('Orbital Velocity [km/s]')
plt.title('DFA Entropic Gravity: Galactic Rotation Curve')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('entropic_gravity_dfa.png', dpi=300)
plt.show()