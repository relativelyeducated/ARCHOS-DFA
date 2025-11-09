#!/usr/bin/env python3
"""
Spatial Fractal Dimension Analysis for Protein Structures
==========================================================

Calculates box-counting fractal dimension for 3D spatial distribution
of protein atoms, matching the methodology used for synthetic protein data.

This is different from correlation dimension D₂ which measures
how a 1D path (backbone) fills space.

Author: Jason King (DFA Theory)
Date: November 8, 2025
"""

import numpy as np
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def parse_pdb_all_atoms(pdb_file):
    """Parse PDB and get ALL heavy atom coordinates."""
    coords = []
    with open(pdb_file, 'r') as f:
        for line in f:
            if line.startswith('ATOM'):
                atom_name = line[12:16].strip()
                if not atom_name.startswith('H'):  # Skip hydrogens
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    coords.append([x, y, z])
    return np.array(coords)

def box_counting_dimension(coords, min_box_size=None, max_box_size=None, n_sizes=15):
    """
    Calculate spatial fractal dimension using box-counting method.

    D_box = -d(log N)/d(log ε)

    where N(ε) = number of boxes of size ε needed to cover the structure
    """
    if len(coords) < 10:
        return np.nan, np.nan

    # Center coordinates
    coords = coords - coords.mean(axis=0)

    # Determine box size range
    if max_box_size is None:
        max_extent = np.max(np.abs(coords))
        max_box_size = max_extent * 2

    if min_box_size is None:
        min_box_size = max_box_size / 100

    # Logarithmic spacing of box sizes
    box_sizes = np.logspace(np.log10(min_box_size), np.log10(max_box_size), n_sizes)
    box_counts = []

    for box_size in box_sizes:
        # Grid the space
        grid_coords = np.floor(coords / box_size).astype(int)

        # Count unique boxes
        unique_boxes = len(set(map(tuple, grid_coords)))
        box_counts.append(unique_boxes)

    box_counts = np.array(box_counts)

    # Fit D = -slope in log-log plot
    valid_mask = (box_counts > 0) & (box_sizes > 0)
    if np.sum(valid_mask) < 5:
        return np.nan, np.nan

    log_epsilon = np.log(box_sizes[valid_mask])
    log_N = np.log(box_counts[valid_mask])

    # Use middle 60% for fitting
    n_points = len(log_epsilon)
    start_idx = int(0.2 * n_points)
    end_idx = int(0.8 * n_points)

    if end_idx - start_idx < 3:
        start_idx = 0
        end_idx = n_points

    fit_log_eps = log_epsilon[start_idx:end_idx]
    fit_log_N = log_N[start_idx:end_idx]

    slope, intercept, r_value, p_value, std_err = linregress(fit_log_eps, fit_log_N)

    D_box = -slope  # Negative because N decreases as ε increases
    r_squared = r_value ** 2

    return D_box, r_squared

def analyze_protein_spatial_fractal(pdb_file):
    """Complete spatial fractal analysis for one protein."""
    name = Path(pdb_file).stem

    try:
        coords = parse_pdb_all_atoms(pdb_file)

        if len(coords) < 10:
            return None

        D_box, r_squared = box_counting_dimension(coords)

        # Calculate related metrics
        centroid = coords.mean(axis=0)
        Rg = np.sqrt(np.mean(np.sum((coords - centroid)**2, axis=1)))
        max_dist = np.max(np.linalg.norm(coords - centroid, axis=1))

        # Estimate R-component from D_box
        # For classical 3D structure: D_box ≈ 3
        # For fractal: D_box < 3
        # DFA predicts: D₂ = 1 + R/2, so R ≈ 2(D_box - 1)
        # But D_box ≠ D₂, so we use empirical calibration

        R_apparent = max(0, min(1, 2 * (D_box - 1) / 2))  # Rough estimate
        S_apparent = 1 - R_apparent

        # Coupling tension
        commutator_norm = np.abs(S_apparent - R_apparent) * np.sqrt(S_apparent * R_apparent)
        synthesis_norm = np.sqrt(S_apparent**2 + R_apparent**2)
        C = commutator_norm / (synthesis_norm + 1e-10)

        # Classify state
        if D_box > 2.5:
            state = "Classical (S-only, D>2.5)"
        elif 1.2 <= D_box <= 1.6 and 0.15 <= C <= 0.35:
            state = "FRUSTRATED (Stalker - R-axis rejection)"
        elif D_box < 2.0 and C < 0.15:
            state = "Transitional (low coupling)"
        elif D_box < 2.0 and C > 0.35:
            state = "Coupled (S⊕R synthesis)"
        else:
            state = "Ambiguous"

        result = {
            'name': name,
            'n_atoms': len(coords),
            'D_box': D_box,
            'r_squared': r_squared,
            'R_apparent': R_apparent,
            'S_apparent': S_apparent,
            'coupling_tension_C': C,
            'radius_gyration': Rg,
            'max_distance': max_dist,
            'coupling_state': state,
        }

        return result

    except Exception as e:
        print(f"  ✗ Error processing {name}: {e}")
        return None

# Protein database (same as before)
PROTEIN_DATABASE = {
    'native_folded': [
        '1UBQ', '1ENH', '1PGB', '1SHG', '1LMB', '1ROP', '2CI2', '1TIT', '1WIT'
    ],
    'amyloid_fibrils': [
        '2MXU',  # Amyloid-β 42 fibril
        '3OW9',  # KLVFFA from Amyloid-β
    ],
    'prion_related': [
        '1QLX', '1HJM'
    ],
    'large_assemblies': [
        '2BEG', '2K4K', '1V54'
    ]
}

def main():
    pdb_dir = Path('/home/king/Downloads/pdb')
    output_dir = Path('/home/king/githubs/dialectical-fractal-theory/results/spatial_fractal')
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("SPATIAL FRACTAL DIMENSION ANALYSIS (Box-Counting Method)")
    print("Testing stalker hypothesis with proper spatial D_box calculation")
    print("=" * 80)

    all_results = []

    for category, pdb_ids in PROTEIN_DATABASE.items():
        print(f"\n{'='*70}")
        print(f"{category.upper().replace('_', ' ')}")
        print(f"{'='*70}\n")

        for pdb_id in pdb_ids:
            pdb_file = None
            for f in pdb_dir.glob(f"{pdb_id}.*"):
                if f.suffix.lower() == '.pdb':
                    pdb_file = f
                    break

            if pdb_file is None:
                print(f"  ⚠ {pdb_id}: Not found")
                continue

            result = analyze_protein_spatial_fractal(pdb_file)

            if result is not None:
                result['category'] = category
                all_results.append(result)

                print(f"  ✓ {pdb_id}:")
                print(f"      Atoms: {result['n_atoms']}")
                print(f"      D_box: {result['D_box']:.3f} (R²={result['r_squared']:.3f})")
                print(f"      R: {result['R_apparent']:.3f}, S: {result['S_apparent']:.3f}")
                print(f"      C: {result['coupling_tension_C']:.3f}")
                print(f"      State: {result['coupling_state']}")

                if 'FRUSTRATED' in result['coupling_state']:
                    print(f"      🚨 STALKER STATE!")

    # Save results
    results_df = pd.DataFrame(all_results)
    results_csv = output_dir / 'spatial_fractal_results.csv'
    results_df.to_csv(results_csv, index=False)

    print(f"\n{'='*80}")
    print("SUMMARY BY CATEGORY")
    print("=" * 80)

    for cat in results_df['category'].unique():
        cat_data = results_df[results_df['category'] == cat]
        print(f"\n{cat.upper().replace('_', ' ')}:")
        print(f"  N = {len(cat_data)}")
        print(f"  D_box = {cat_data['D_box'].mean():.3f} ± {cat_data['D_box'].std():.3f}")
        print(f"  Range: [{cat_data['D_box'].min():.3f}, {cat_data['D_box'].max():.3f}]")

        stalkers = cat_data[cat_data['coupling_state'].str.contains('FRUSTRATED', na=False)]
        if len(stalkers) > 0:
            print(f"  🚨 STALKER STATES: {len(stalkers)}/{len(cat_data)}")

    # Test hypothesis
    print(f"\n{'='*80}")
    print("STALKER HYPOTHESIS TEST")
    print("=" * 80)

    native = results_df[results_df['category'] == 'native_folded']
    amyloid = results_df[results_df['category'] == 'amyloid_fibrils']

    if len(native) > 0 and len(amyloid) > 0:
        print(f"\nNative proteins: D_box = {native['D_box'].mean():.3f} ± {native['D_box'].std():.3f}")
        print(f"Amyloid fibrils: D_box = {amyloid['D_box'].mean():.3f} ± {amyloid['D_box'].std():.3f}")
        print(f"\nΔ D_box = {abs(native['D_box'].mean() - amyloid['D_box'].mean()):.3f}")

        print(f"\nPREDICTION:")
        print(f"  Native: D_box ≈ 2.3-3.0 (classical 3D)")
        print(f"  Amyloid: D_box ≈ 1.2-1.4 (stalker state)")

        if amyloid['D_box'].mean() < native['D_box'].mean():
            print(f"\n✓ HYPOTHESIS SUPPORTED: Amyloids have lower D_box")
        else:
            print(f"\n✗ HYPOTHESIS NOT SUPPORTED")

    print(f"\n✓ Results saved to: {results_csv}")

    return results_df

if __name__ == '__main__':
    results = main()
