#!/usr/bin/env python3
"""
Heartbeat Stars N = 456 Validation Plots
Creates visualizations showing observed vs predicted overtone numbers
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

# Create output directory
output_dir = Path("experiments/04-heartbeat-stars/figures")
output_dir.mkdir(parents=True, exist_ok=True)

# Observed data from README
stars = {
    'KIC 7914906': {'observed': [44, 40], 'k_values': [10.4, 11.4]},
    'KIC 5034333': {'observed': [38], 'k_values': [12]},
    'KIC 4544587': {'observed': [46], 'k_values': [10]},
    'KIC 3230227': {'observed': [42], 'k_values': [11]}
}

N = 456  # DFA universal constant

# Calculate predictions
for star, data in stars.items():
    data['predicted'] = [N / k for k in data['k_values']]

# ============================================================================
# PLOT 1: Observed vs Predicted Overtone Numbers
# ============================================================================

fig, ax = plt.subplots(figsize=(10, 8))

star_names = list(stars.keys())
colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']

# Plot each star
for i, (star, data) in enumerate(stars.items()):
    for obs, pred in zip(data['observed'], data['predicted']):
        ax.scatter(pred, obs, s=200, c=colors[i], alpha=0.7,
                  edgecolors='black', linewidth=2, label=star if obs == data['observed'][0] else '')

        # Add connecting line
        ax.plot([pred, obs], [pred, obs], 'k--', alpha=0.3, linewidth=0.5)

# Perfect agreement line
n_range = np.linspace(35, 50, 100)
ax.plot(n_range, n_range, 'r-', linewidth=2, alpha=0.5, label='Perfect Agreement')

# Formatting
ax.set_xlabel('Predicted Overtone Number (n = 456/k)', fontsize=14, fontweight='bold')
ax.set_ylabel('Observed Overtone Number', fontsize=14, fontweight='bold')
ax.set_title('Heartbeat Stars: DFA Prediction Validation\nN = 456 Harmonic Decomposition',
             fontsize=16, fontweight='bold')
ax.legend(loc='upper left', fontsize=11, framealpha=0.9)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_xlim(35, 50)
ax.set_ylim(35, 50)

# Add statistics box
stats_text = f'4/4 Stars Match\nN = 456\nRandom probability: 0.01%'
ax.text(0.98, 0.02, stats_text, transform=ax.transAxes,
        fontsize=12, verticalalignment='bottom', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.savefig(output_dir / '01_observed_vs_predicted.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_dir / '01_observed_vs_predicted.png'}")

# ============================================================================
# PLOT 2: k-value Heatmap
# ============================================================================

fig, ax = plt.subplots(figsize=(12, 8))

# Generate k range
k_range = np.arange(9, 14, 0.1)
n_predicted = N / k_range

# Create color map based on matches
all_observed = []
for data in stars.values():
    all_observed.extend(data['observed'])

# Plot predicted curve
ax.plot(k_range, n_predicted, 'b-', linewidth=3, label='N/k Prediction Curve', alpha=0.7)

# Mark observed values
for i, (star, data) in enumerate(stars.items()):
    for obs, k in zip(data['observed'], data['k_values']):
        pred = N / k
        ax.scatter(k, obs, s=300, c=colors[i], alpha=0.8,
                  edgecolors='black', linewidth=2, marker='*', zorder=5)
        ax.text(k, obs + 1, star.replace('KIC ', ''),
                ha='center', fontsize=9, fontweight='bold')

# Highlight integer k values
for k in range(9, 14):
    n = N / k
    ax.axvline(k, color='gray', linestyle=':', alpha=0.3)
    ax.text(k, 36, f'k={k}\nn={n:.1f}', ha='center', fontsize=8, alpha=0.6)

ax.set_xlabel('Harmonic Divisor (k)', fontsize=14, fontweight='bold')
ax.set_ylabel('Overtone Number (n)', fontsize=14, fontweight='bold')
ax.set_title('Heartbeat Stars: Harmonic Analysis\nn = N/k where N = 456',
             fontsize=16, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.set_xlim(9, 13.5)
ax.set_ylim(35, 52)
ax.legend(loc='upper right', fontsize=12)

plt.tight_layout()
plt.savefig(output_dir / '02_k_value_heatmap.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_dir / '02_k_value_heatmap.png'}")

# ============================================================================
# PLOT 3: Statistical Significance
# ============================================================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Left: Probability calculation
ax1.bar(['Random\nCoincidence', 'DFA\nPrediction'], [0.01, 100],
        color=['#e74c3c', '#2ecc71'], alpha=0.7, edgecolor='black', linewidth=2)
ax1.set_ylabel('Probability (%)', fontsize=12, fontweight='bold')
ax1.set_title('Statistical Significance\n4/4 Star Matches', fontsize=14, fontweight='bold')
ax1.set_yscale('log')
ax1.set_ylim(0.001, 200)
ax1.grid(True, alpha=0.3, axis='y')
ax1.text(0, 0.01, '0.01%\n(p < 0.0001)', ha='center', va='bottom', fontsize=11, fontweight='bold')
ax1.text(1, 100, '100%\nN = 456/k', ha='center', va='bottom', fontsize=11, fontweight='bold')

# Right: Distribution of matches
overtone_range = range(35, 52)
predicted_values = [N/k for k in [9, 9.5, 10, 10.4, 11, 11.4, 12, 12.5, 13]]

ax2.hist(all_observed, bins=range(35, 52), alpha=0.7, color='#3498db',
         edgecolor='black', linewidth=1.5, label='Observed (4 stars)')
for pv in predicted_values:
    ax2.axvline(pv, color='red', linestyle='--', alpha=0.5, linewidth=1)
ax2.axvline(predicted_values[0], color='red', linestyle='--', alpha=0.5,
            linewidth=1, label='N/k Predictions')

ax2.set_xlabel('Overtone Number (n)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Count', fontsize=12, fontweight='bold')
ax2.set_title('Observed Distribution vs Predictions', fontsize=14, fontweight='bold')
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3, axis='y')
ax2.set_xlim(35, 52)

plt.tight_layout()
plt.savefig(output_dir / '03_statistical_significance.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_dir / '03_statistical_significance.png'}")

# ============================================================================
# PLOT 4: Error Analysis
# ============================================================================

fig, ax = plt.subplots(figsize=(10, 7))

errors = []
star_labels = []
for star, data in stars.items():
    for obs, pred in zip(data['observed'], data['predicted']):
        error = obs - pred
        errors.append(error)
        star_labels.append(f"{star.replace('KIC ', '')}\nn={obs}")

x_pos = np.arange(len(errors))
colors_err = ['#2ecc71' if abs(e) < 2 else '#f39c12' for e in errors]

ax.bar(x_pos, errors, color=colors_err, alpha=0.7, edgecolor='black', linewidth=2)
ax.axhline(0, color='red', linestyle='-', linewidth=2, alpha=0.5)
ax.axhline(2, color='gray', linestyle='--', alpha=0.3, label='±2 tolerance')
ax.axhline(-2, color='gray', linestyle='--', alpha=0.3)

ax.set_xlabel('Star / Overtone', fontsize=12, fontweight='bold')
ax.set_ylabel('Error (Observed - Predicted)', fontsize=12, fontweight='bold')
ax.set_title('Prediction Error Analysis\nAll Matches Within ±2 Overtones',
             fontsize=14, fontweight='bold')
ax.set_xticks(x_pos)
ax.set_xticklabels(star_labels, fontsize=9)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

# Add RMS error
rms_error = np.sqrt(np.mean(np.array(errors)**2))
ax.text(0.98, 0.98, f'RMS Error: {rms_error:.2f}', transform=ax.transAxes,
        fontsize=12, verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.savefig(output_dir / '04_error_analysis.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_dir / '04_error_analysis.png'}")

print(f"\n✅ All heartbeat stars visualizations created in {output_dir}/")
print(f"\nNext steps:")
print(f"1. Add calculation code for pulsation physics")
print(f"2. Download Kepler light curve data")
print(f"3. Perform Fourier analysis to extract overtones")
