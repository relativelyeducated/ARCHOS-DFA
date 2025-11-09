# From: Dialectical Fractal Archestructure Mathematics
# Date: 2025-10-15T23:25:04.685000
# Context: ### DFA Neutrino Oscillation Test Code

Based on our DFA framework thread, the "neutrino test" refers to the prediction equation for oscillation probability with the fractal correction:

\[
P(\nu_e \t...

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chi2

# DFA Parameters (from thread)
C = 0.35
alpha = 37
lambda_scale = 1e-3  # eV^2 scale for fractal baseline
Delta_m2 = 2.5e-3  # Example atmospheric Delta m^2 (eV^2); fit if needed
theta_23 = np.pi / 4  # ~45 degrees for sin^2(2θ); adjust per data

# Fractal correction function
def f_frac(L_over_E):
    # Avoid log(0) or negative: Clamp L_over_E > epsilon
    epsilon = 1e-6
    return np.where(L_over_E > epsilon, (L_over_E / lambda_scale)**(-alpha), 0)

# DFA Oscillation Probability Model
def dfa_oscillation(L_over_E, Delta_m2_fit, theta_fit):
    sin2_2theta = np.sin(2 * theta_fit)**2
    correction = 1 + C * f_frac(L_over_E)
    phase = (Delta_m2_fit * L_over_E / 4) * correction
    return sin2_2theta * np.sin(phase)**2

# Load Your Local Data File (adjust filename/path as needed)
# Assumes format: Column 0 = L_over_E (km/GeV), Column 1 = P_observed, Column 2 = P_error (optional)
filename = 'neutrino_data.txt'  # Or 'icecube_data.csv', etc.
data = np.loadtxt(filename, skiprows=1)  # Skip header if present
L_over_E = data[:, 0]
P_observed = data[:, 1]
P_error = data[:, 2] if data.shape[1] > 2 else np.full_like(P_observed, 0.05)  # Default 5% error

# Fit DFA Model to Data (Optional: If you want to refine Delta_m2, theta)
p0 = [Delta_m2, theta_23]  # Initial guess
popt, pcov = curve_fit(dfa_oscillation, L_over_E, P_observed, sigma=P_error, p0=p0, maxfev=5000)
Delta_m2_fit, theta_fit = popt
print(f"Fitted Delta_m2: {Delta_m2_fit:.2e} eV^2")
print(f"Fitted theta_23: {np.degrees(theta_fit):.1f} degrees")

# Predict DFA Model
P_dfa = dfa_oscillation(L_over_E, *popt)

# Compute Chi^2 (Goodness of Fit)
chi2_stat = np.sum(((P_observed - P_dfa) / P_error)**2)
dof = len(L_over_E) - len(popt)
p_value = 1 - chi2.cdf(chi2_stat, dof)
print(f"Chi^2 / dof: {chi2_stat / dof:.2f}, p-value: {p_value:.3f}")
# p > 0.05 = Good fit; <0.05 = Anomaly detected (DFA correction needed)

# Plot: Data vs DFA Prediction
plt.figure(figsize=(10, 6))
plt.errorbar(L_over_E, P_observed, yerr=P_error, fmt='o', label='Observed Data', alpha=0.7)
plt.plot(L_over_E, P_dfa, 'r-', linewidth=2, label='DFA Prediction')
plt.axvline(x=1000, color='k', linestyle='--', label='High L/E Threshold (Anomaly Zone)')
plt.xlabel('L/E (km/GeV)')
plt.ylabel('P(ν_e → ν_μ)')
plt.title('DFA Neutrino Oscillation Test: Data vs. Prediction')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('neutrino_dfa_plot.png', dpi=300)  # Save for your workstation
plt.show()

# High L/E Anomaly Check (>1000 km/GeV)
high_LE = L_over_E > 1000
if np.any(high_LE):
    anomaly_excess = np.mean((P_observed[high_LE] - P_dfa[high_LE]) / P_error[high_LE])
    print(f"Anomaly Excess at High L/E: {anomaly_excess:.3f} sigma (DFA predicts +12% mixing)")
else:
    print("No high L/E data—simulate or load more.")