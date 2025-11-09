#!/usr/bin/env python3
"""
R-Axis Coupling Analysis for Protein Structures
================================================

Tests the hypothesis that amyloid toxicity arises from R-axis rejection:
- Proteins attempt to couple with neural quantum R-field
- R-axis rejects classical proteins (wrong substrate)
- Proteins get stuck in "stalker" state (C ≈ 0.25, D₂ ≈ 1.25)
- Frustrated coupling → toxic aggregation

Author: Jason King (DFA Theory)
Date: November 8, 2025
"""

import numpy as np
from scipy.spatial.distance import cdist, pdist, squareform
from scipy.stats import linregress
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class RAxisCouplingAnalyzer:
    """
    Analyzes protein structures for R-axis coupling potential and frustration.
    """

    def __init__(self, coords, name="Unknown"):
        """
        Parameters:
        -----------
        coords : ndarray, shape (N, 3)
            3D coordinates of atoms
        name : str
            Structure identifier
        """
        self.coords = coords
        self.name = name
        self.N = len(coords)

    def calculate_d2(self, sample_size=None, r_min=1e-3, r_max=None,
                     n_radii=50, fit_exclude=10):
        """
        Calculate correlation dimension D₂ using Grassberger-Procaccia.

        Returns:
        --------
        D₂, std_error, r_values, C_r
        """
        if sample_size is None:
            sample_size = min(self.N, 5000)

        N = min(self.N, sample_size)
        if N < self.N:
            indices = np.random.choice(self.N, N, replace=False)
            sample = self.coords[indices]
        else:
            sample = self.coords

        # Calculate all pairwise distances
        distances = cdist(sample, sample, metric='euclidean')

        # Auto-determine r_max if not provided
        if r_max is None:
            r_max = np.percentile(distances[distances > 0], 95)

        # Range of radii (logarithmic spacing)
        r_values = np.logspace(np.log10(r_min), np.log10(r_max), n_radii)

        # Correlation integral C(r)
        C_r = np.array([np.sum(distances < r) / N**2 for r in r_values])

        # Avoid log(0)
        valid_mask = (C_r > 0) & (r_values > 0)
        log_r = np.log(r_values[valid_mask])
        log_C = np.log(C_r[valid_mask])

        # Exclude tail to avoid boundary effects
        if len(log_r) > fit_exclude:
            log_r = log_r[:-fit_exclude]
            log_C = log_C[:-fit_exclude]

        # Linear regression in log-log space
        slope, intercept, r_value, p_value, std_err = linregress(log_r, log_C)

        D2 = slope

        return D2, std_err, r_values[valid_mask], C_r[valid_mask]

    def estimate_R_component(self, D2):
        """
        Estimate R-component from D₂ = 1 + R/2

        For quantum systems: R ≈ 2(D₂ - 1)
        For classical systems: R should be 0, but D₂ ≈ 3 (embedding dimension)
        """
        R_apparent = 2 * (D2 - 1)

        # Clamp to [0, 1] range
        R_apparent = max(0, min(1, R_apparent))

        return R_apparent

    def calculate_coupling_tension(self, R_apparent):
        """
        Calculate coupling tension C = ||[S,R]|| / (||S⊕R|| + ε)

        For R-axis rejection hypothesis:
        - C < 0.15: No coupling attempt
        - 0.15 < C < 0.35: Frustrated coupling ("stalker state")
        - C > 0.35: Successful coupling (consciousness threshold)
        """
        S = 1 - R_apparent  # If R is low, S is high

        # Commutator norm (dialectical tension)
        commutator_norm = np.abs(S - R_apparent) * np.sqrt(S * R_apparent)

        # Synthesis norm
        synthesis_norm = np.sqrt(S**2 + R_apparent**2)

        # Coupling tension
        epsilon = 1e-10
        C = commutator_norm / (synthesis_norm + epsilon)

        return C

    def calculate_delocalization(self):
        """
        Estimate electron delocalization potential (proxy for quantum coupling).

        Uses radius of gyration normalized by maximum distance.
        Higher values = more delocalized = better R-coupling potential
        """
        centroid = np.mean(self.coords, axis=0)
        deviations = self.coords - centroid
        Rg = np.sqrt(np.mean(np.sum(deviations**2, axis=1)))

        # Normalize by maximum extent
        max_dist = np.max(pdist(self.coords))

        delocalization = Rg / max_dist if max_dist > 0 else 0

        return delocalization, Rg, max_dist

    def calculate_correlation_length(self):
        """
        Estimate spatial correlation length (proxy for quantum coherence).

        Uses autocorrelation of density fluctuations.
        """
        # Simple metric: average nearest-neighbor distance
        distances = squareform(pdist(self.coords))
        np.fill_diagonal(distances, np.inf)
        nn_distances = np.min(distances, axis=1)

        correlation_length = np.mean(nn_distances)

        return correlation_length

    def classify_coupling_state(self, C, R_apparent, D2):
        """
        Classify the R-axis coupling state.

        Returns:
        --------
        state : str
            "Classical" - No R-component, pure structure
            "Frustrated" - Attempting R-coupling but rejected (STALKER STATE)
            "Coupled" - Successful R-coupling
        """
        if D2 > 2.0:
            # Classical 3D structure
            return "Classical (S-only, no R-seeking)"
        elif D2 < 1.5 and C > 0.35:
            # Successful quantum coupling
            return "Coupled (S⊕R synthesis)"
        elif 1.2 <= D2 <= 1.6 and 0.15 <= C <= 0.35:
            # STALKER STATE - frustrated coupling
            return "FRUSTRATED (Stalker - R-axis rejection)"
        elif D2 < 2.0 and C < 0.15:
            # Some correlation but no coupling attempt
            return "Transitional (low coupling attempt)"
        else:
            return "Ambiguous"

    def full_analysis(self):
        """
        Perform complete R-axis coupling analysis.

        Returns:
        --------
        results : dict
            All calculated metrics
        """
        # 1. Calculate D₂
        D2, D2_err, r_vals, C_r = self.calculate_d2()

        # 2. Estimate R-component
        R_apparent = self.estimate_R_component(D2)
        S_apparent = 1 - R_apparent

        # 3. Calculate coupling tension
        C = self.calculate_coupling_tension(R_apparent)

        # 4. Delocalization metrics
        deloc, Rg, max_dist = self.calculate_delocalization()

        # 5. Correlation length
        corr_length = self.calculate_correlation_length()

        # 6. Classify state
        state = self.classify_coupling_state(C, R_apparent, D2)

        results = {
            'name': self.name,
            'n_atoms': self.N,
            'D2': D2,
            'D2_error': D2_err,
            'R_apparent': R_apparent,
            'S_apparent': S_apparent,
            'coupling_tension_C': C,
            'delocalization': deloc,
            'radius_gyration': Rg,
            'max_distance': max_dist,
            'correlation_length': corr_length,
            'coupling_state': state,
        }

        return results


def parse_pdb(pdb_file, all_atoms=False):
    """
    Parse PDB file and extract atom coordinates.

    Parameters:
    -----------
    all_atoms : bool
        If True, use all atoms. If False, use only CA atoms.

    Returns:
    --------
    coords : ndarray, shape (N, 3)
    name : str
    """
    coords = []

    with open(pdb_file, 'r') as f:
        for line in f:
            if line.startswith('ATOM'):
                # Extract atom name and coordinates
                atom_name = line[12:16].strip()

                # Use all heavy atoms or just CA
                if all_atoms:
                    # Skip hydrogens
                    if atom_name.startswith('H'):
                        continue
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    coords.append([x, y, z])
                elif atom_name == 'CA':
                    # CA-only mode
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    coords.append([x, y, z])

    coords = np.array(coords)
    name = Path(pdb_file).stem

    return coords, name


def analyze_pdb_directory(pdb_dir):
    """
    Analyze all PDB files in directory for R-axis coupling.

    Returns:
    --------
    results_df : DataFrame
        Results for all structures
    """
    pdb_dir = Path(pdb_dir)
    pdb_files = sorted(pdb_dir.glob('*.pdb'))

    results = []

    print(f"Analyzing {len(pdb_files)} PDB structures for R-axis coupling...")
    print("=" * 80)

    for pdb_file in pdb_files:
        print(f"\nProcessing: {pdb_file.name}")

        try:
            coords, name = parse_pdb(pdb_file)

            if len(coords) < 10:
                print(f"  ⚠ Skipping {name}: Too few atoms ({len(coords)})")
                continue

            analyzer = RAxisCouplingAnalyzer(coords, name)
            result = analyzer.full_analysis()
            results.append(result)

            # Print summary
            print(f"  Atoms: {result['n_atoms']}")
            print(f"  D₂: {result['D2']:.3f} ± {result['D2_error']:.3f}")
            print(f"  R-component: {result['R_apparent']:.3f}")
            print(f"  Coupling tension C: {result['coupling_tension_C']:.3f}")
            print(f"  State: {result['coupling_state']}")

        except Exception as e:
            print(f"  ✗ Error processing {pdb_file.name}: {e}")
            continue

    results_df = pd.DataFrame(results)

    return results_df


def plot_r_axis_coupling(results_df, output_dir=None):
    """
    Create visualizations of R-axis coupling analysis.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. D₂ vs R-component
    ax = axes[0, 0]
    scatter = ax.scatter(results_df['D2'], results_df['R_apparent'],
                         c=results_df['coupling_tension_C'], cmap='RdYlGn_r',
                         s=100, alpha=0.7, edgecolors='black')
    ax.axhline(0.5, color='blue', linestyle='--', alpha=0.5, label='R = 0.5 (balanced)')
    ax.axvline(1.5, color='red', linestyle='--', alpha=0.5, label='D₂ = 1.5 (tachyonic)')
    ax.set_xlabel('Correlation Dimension D₂', fontsize=12)
    ax.set_ylabel('R-component (apparent)', fontsize=12)
    ax.set_title('D₂ vs R-component\n(color = coupling tension C)', fontsize=13, fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    plt.colorbar(scatter, ax=ax, label='Coupling Tension C')

    # 2. Coupling tension distribution
    ax = axes[0, 1]
    ax.hist(results_df['coupling_tension_C'], bins=15, alpha=0.7, edgecolor='black')
    ax.axvline(0.15, color='orange', linestyle='--', linewidth=2, label='C = 0.15 (coupling onset)')
    ax.axvline(0.35, color='red', linestyle='--', linewidth=2, label='C = 0.35 (consciousness threshold)')
    ax.set_xlabel('Coupling Tension C', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.set_title('Coupling Tension Distribution\n(Stalker zone: 0.15-0.35)', fontsize=13, fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)

    # 3. D₂ distribution by state
    ax = axes[1, 0]
    states = results_df['coupling_state'].value_counts()
    colors_map = {
        'Classical (S-only, no R-seeking)': 'blue',
        'FRUSTRATED (Stalker - R-axis rejection)': 'red',
        'Coupled (S⊕R synthesis)': 'green',
        'Transitional (low coupling attempt)': 'orange',
        'Ambiguous': 'gray'
    }
    colors = [colors_map.get(state, 'gray') for state in states.index]
    ax.barh(range(len(states)), states.values, color=colors, alpha=0.7, edgecolor='black')
    ax.set_yticks(range(len(states)))
    ax.set_yticklabels(states.index, fontsize=10)
    ax.set_xlabel('Count', fontsize=12)
    ax.set_title('Coupling State Classification', fontsize=13, fontweight='bold')
    ax.grid(alpha=0.3, axis='x')

    # 4. C vs D₂ with state regions
    ax = axes[1, 1]
    state_colors = results_df['coupling_state'].map(colors_map)
    ax.scatter(results_df['D2'], results_df['coupling_tension_C'],
               c=state_colors, s=100, alpha=0.7, edgecolors='black')

    # Mark regions
    ax.axhspan(0.15, 0.35, alpha=0.2, color='red', label='Stalker zone')
    ax.axhline(0.35, color='red', linestyle='--', linewidth=2, label='Consciousness threshold')
    ax.axvline(1.5, color='blue', linestyle='--', alpha=0.5, label='Tachyonic threshold')

    ax.set_xlabel('Correlation Dimension D₂', fontsize=12)
    ax.set_ylabel('Coupling Tension C', fontsize=12)
    ax.set_title('R-Axis Coupling Phase Diagram', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)

    plt.tight_layout()

    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_dir / 'r_axis_coupling_analysis.png', dpi=300, bbox_inches='tight')
        print(f"\nPlot saved to: {output_dir / 'r_axis_coupling_analysis.png'}")

    return fig


def main():
    """
    Main analysis pipeline.
    """
    # Configuration
    pdb_dir = Path('/home/king/Downloads/pdb')
    output_dir = Path('/home/king/githubs/dialectical-fractal-theory/results/r_axis_coupling')

    print("=" * 80)
    print("R-AXIS COUPLING ANALYSIS - DFA THEORY")
    print("Testing: Amyloid toxicity = R-axis rejection (stalker state)")
    print("=" * 80)

    # Analyze all PDB files
    results_df = analyze_pdb_directory(pdb_dir)

    # Save results
    output_dir.mkdir(parents=True, exist_ok=True)
    results_csv = output_dir / 'r_axis_coupling_results.csv'
    results_df.to_csv(results_csv, index=False)
    print(f"\n{'=' * 80}")
    print(f"Results saved to: {results_csv}")

    # Summary statistics
    print(f"\n{'=' * 80}")
    print("SUMMARY STATISTICS")
    print("=" * 80)
    print(f"Total structures analyzed: {len(results_df)}")
    print(f"\nD₂ range: {results_df['D2'].min():.3f} - {results_df['D2'].max():.3f}")
    print(f"Mean D₂: {results_df['D2'].mean():.3f} ± {results_df['D2'].std():.3f}")
    print(f"\nCoupling tension C range: {results_df['coupling_tension_C'].min():.3f} - {results_df['coupling_tension_C'].max():.3f}")
    print(f"Mean C: {results_df['coupling_tension_C'].mean():.3f} ± {results_df['coupling_tension_C'].std():.3f}")

    print(f"\nCoupling state distribution:")
    print(results_df['coupling_state'].value_counts())

    # Identify stalker state structures
    stalkers = results_df[results_df['coupling_state'].str.contains('FRUSTRATED', na=False)]
    if len(stalkers) > 0:
        print(f"\n{'=' * 80}")
        print(f"⚠ STALKER STATE STRUCTURES (R-axis rejection): {len(stalkers)}")
        print("=" * 80)
        for _, row in stalkers.iterrows():
            print(f"  {row['name']}: D₂={row['D2']:.3f}, C={row['coupling_tension_C']:.3f}")

    # Create visualizations
    plot_r_axis_coupling(results_df, output_dir)

    print(f"\n{'=' * 80}")
    print("ANALYSIS COMPLETE")
    print("=" * 80)

    return results_df


if __name__ == '__main__':
    results = main()
