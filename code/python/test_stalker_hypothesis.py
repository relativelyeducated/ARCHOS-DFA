#!/usr/bin/env python3
"""
Test the R-Axis Rejection "Stalker" Hypothesis
===============================================

Hypothesis: Amyloid fibrils are proteins stuck in "stalker state"
- Attempting to couple with neural R-field
- R-axis rejects them (wrong substrate)
- Stuck at C ≈ 0.15-0.35 (frustrated coupling)
- Result: Toxic aggregation

Analysis compares:
1. Native folded proteins (should be classical, D₂ ≈ 1.8-2.2 for CA backbone)
2. Amyloid fibrils (predicted stalker state, D₂ ≈ 1.2-1.4)

Author: Jason King (DFA Theory)
Date: November 8, 2025
"""

import numpy as np
from scipy.stats import linregress
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Use the analyzer from the main script
import sys
sys.path.append(str(Path(__file__).parent))
from analyze_r_axis_coupling import RAxisCouplingAnalyzer, parse_pdb

# Protein classifications based on PDB database
PROTEIN_DATABASE = {
    'native_folded': [
        '1UBQ',  # Ubiquitin - classic well-folded
        '1ENH',  # Engrailed homeodomain
        '1PGB',  # Protein G B1 domain
        '1SHG',  # SH3 domain
        '1LMB',  # Lambda repressor
        '1ROP',  # Repressor of primer
        '2CI2',  # Chymotrypsin inhibitor
        '1TIT',  # Trypsin inhibitor
        '1WIT',  # WW domain
    ],
    'amyloid_fibrils': [
        '2MXU',  # Amyloid-β 42 fibril (ALZHEIMER'S!)
        '3OW9',  # KLVFFA from Amyloid-β
    ],
    'prion_related': [
        '1QLX',  # Prion protein fragment (human)
        '1HJM',  # Prion protein
    ],
    'large_assemblies': [
        '2BEG',  # Large assembly
        '2K4K',  # Large complex
        '1V54',  # Large structure
    ]
}

def analyze_protein_set(pdb_dir, category, pdb_ids):
    """
    Analyze a set of proteins and return results.
    """
    results = []
    pdb_dir = Path(pdb_dir)

    print(f"\n{'='*70}")
    print(f"Analyzing {category.upper()}: {len(pdb_ids)} structures")
    print(f"{'='*70}\n")

    for pdb_id in pdb_ids:
        # Try different case variations
        pdb_file = None
        for filename in pdb_dir.glob(f"{pdb_id}.*"):
            if filename.suffix.lower() == '.pdb':
                pdb_file = filename
                break

        if pdb_file is None:
            print(f"  ⚠ {pdb_id}: PDB file not found")
            continue

        try:
            coords, name = parse_pdb(pdb_file, all_atoms=False)  # CA only

            if len(coords) < 10:
                print(f"  ⚠ {pdb_id}: Too few atoms ({len(coords)})")
                continue

            analyzer = RAxisCouplingAnalyzer(coords, pdb_id)
            result = analyzer.full_analysis()
            result['category'] = category
            results.append(result)

            # Print detailed results
            print(f"  ✓ {pdb_id}:")
            print(f"      CA atoms: {result['n_atoms']}")
            print(f"      D₂: {result['D2']:.3f} ± {result['D2_error']:.3f}")
            print(f"      R-component: {result['R_apparent']:.3f}")
            print(f"      Coupling C: {result['coupling_tension_C']:.3f}")
            print(f"      State: {result['coupling_state']}")

            # STALKER CHECK
            if 'FRUSTRATED' in result['coupling_state']:
                print(f"      🚨 STALKER STATE DETECTED!")

        except Exception as e:
            print(f"  ✗ {pdb_id}: Error - {e}")
            continue

    return results

def plot_stalker_analysis(results_df, output_dir):
    """
    Create publication-quality plots for stalker hypothesis.
    """
    fig = plt.figure(figsize=(16, 10))

    # Define color scheme
    color_map = {
        'native_folded': '#2E86AB',      # Blue - classical/stable
        'amyloid_fibrils': '#A23B72',    # Red/purple - stalker state
        'prion_related': '#F18F01',      # Orange - transitional
        'large_assemblies': '#C73E1D',   # Dark red
    }

    # 1. D₂ distribution by category (TOP LEFT)
    ax1 = plt.subplot(2, 3, 1)
    categories = results_df['category'].unique()
    for cat in categories:
        data = results_df[results_df['category'] == cat]['D2']
        ax1.hist(data, alpha=0.6, label=cat.replace('_', ' ').title(),
                 color=color_map.get(cat, 'gray'), bins=10, edgecolor='black')

    ax1.axvline(1.5, color='red', linestyle='--', linewidth=2,
                label='Tachyonic threshold (D₂=1.5)', alpha=0.7)
    ax1.set_xlabel('Correlation Dimension D₂', fontsize=11)
    ax1.set_ylabel('Count', fontsize=11)
    ax1.set_title('D₂ Distribution by Structure Type', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.grid(alpha=0.3)

    # 2. D₂ vs R-component (TOP MIDDLE)
    ax2 = plt.subplot(2, 3, 2)
    for cat in categories:
        data = results_df[results_df['category'] == cat]
        ax2.scatter(data['D2'], data['R_apparent'],
                   label=cat.replace('_', ' ').title(),
                   color=color_map.get(cat, 'gray'), s=100, alpha=0.7, edgecolors='black')

    ax2.axhline(0.5, color='blue', linestyle='--', alpha=0.5, label='R=0.5 (balanced)')
    ax2.axvline(1.5, color='red', linestyle='--', alpha=0.5, label='D₂=1.5 (tachyonic)')
    ax2.set_xlabel('Correlation Dimension D₂', fontsize=11)
    ax2.set_ylabel('R-component (inferred)', fontsize=11)
    ax2.set_title('D₂ vs R-Component', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(alpha=0.3)

    # 3. Coupling tension (TOP RIGHT)
    ax3 = plt.subplot(2, 3, 3)
    for cat in categories:
        data = results_df[results_df['category'] == cat]
        ax3.scatter(data['D2'], data['coupling_tension_C'],
                   label=cat.replace('_', ' ').title(),
                   color=color_map.get(cat, 'gray'), s=100, alpha=0.7, edgecolors='black')

    # Mark stalker zone
    ax3.axhspan(0.15, 0.35, alpha=0.2, color='red')
    ax3.text(1.0, 0.25, 'STALKER\nZONE', fontsize=14, fontweight='bold',
             ha='center', va='center', color='darkred', alpha=0.6)
    ax3.axhline(0.35, color='red', linestyle='--', linewidth=2,
                label='Consciousness threshold (C=0.35)')

    ax3.set_xlabel('Correlation Dimension D₂', fontsize=11)
    ax3.set_ylabel('Coupling Tension C', fontsize=11)
    ax3.set_title('R-Axis Coupling Phase Diagram', fontsize=12, fontweight='bold')
    ax3.legend(fontsize=9)
    ax3.grid(alpha=0.3)
    ax3.set_ylim(0, 0.5)

    # 4. Box plot comparison (BOTTOM LEFT)
    ax4 = plt.subplot(2, 3, 4)
    data_by_cat = [results_df[results_df['category'] == cat]['D2'].values
                   for cat in categories]
    bp = ax4.boxplot(data_by_cat, labels=[c.replace('_', '\n').title() for c in categories],
                     patch_artist=True)

    for patch, cat in zip(bp['boxes'], categories):
        patch.set_facecolor(color_map.get(cat, 'gray'))
        patch.set_alpha(0.6)

    ax4.axhline(1.5, color='red', linestyle='--', linewidth=2, alpha=0.7)
    ax4.set_ylabel('Correlation Dimension D₂', fontsize=11)
    ax4.set_title('D₂ Distribution by Category', fontsize=12, fontweight='bold')
    ax4.grid(alpha=0.3, axis='y')

    # 5. Summary statistics table (BOTTOM MIDDLE)
    ax5 = plt.subplot(2, 3, 5)
    ax5.axis('off')

    summary_data = []
    for cat in categories:
        data = results_df[results_df['category'] == cat]
        summary_data.append([
            cat.replace('_', ' ').title(),
            len(data),
            f"{data['D2'].mean():.3f} ± {data['D2'].std():.3f}",
            f"{data['coupling_tension_C'].mean():.3f}",
            f"{data['R_apparent'].mean():.3f}"
        ])

    table = ax5.table(cellText=summary_data,
                      colLabels=['Category', 'N', 'D₂ (mean±std)', 'C (mean)', 'R (mean)'],
                      cellLoc='center',
                      loc='center',
                      colWidths=[0.3, 0.1, 0.25, 0.15, 0.15])

    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)

    # Color code rows
    for i, cat in enumerate(categories):
        table[(i+1, 0)].set_facecolor(color_map.get(cat, 'gray'))
        table[(i+1, 0)].set_alpha(0.3)

    ax5.set_title('Summary Statistics', fontsize=12, fontweight='bold', pad=20)

    # 6. Stalker hypothesis test (BOTTOM RIGHT)
    ax6 = plt.subplot(2, 3, 6)
    ax6.axis('off')

    # Test hypothesis: Are amyloid fibrils in stalker zone?
    amyloid_data = results_df[results_df['category'] == 'amyloid_fibrils']
    native_data = results_df[results_df['category'] == 'native_folded']

    if len(amyloid_data) > 0 and len(native_data) > 0:
        amyloid_d2_mean = amyloid_data['D2'].mean()
        amyloid_d2_std = amyloid_data['D2'].std()
        native_d2_mean = native_data['D2'].mean()
        native_d2_std = native_data['D2'].std()

        stalker_count = len(amyloid_data[amyloid_data['coupling_state'].str.contains('FRUSTRATED', na=False)])

        hypothesis_text = f"""
        STALKER HYPOTHESIS TEST
        {'='*40}

        Native Proteins:
          D₂ = {native_d2_mean:.3f} ± {native_d2_std:.3f}
          State: Classical structure

        Amyloid Fibrils:
          D₂ = {amyloid_d2_mean:.3f} ± {amyloid_d2_std:.3f}
          Stalker state: {stalker_count}/{len(amyloid_data)}

        Δ D₂ = {abs(amyloid_d2_mean - native_d2_mean):.3f}

        PREDICTION:
        - Native: D₂ > 1.8 (classical)
        - Amyloid: D₂ ≈ 1.2-1.4 (stalker)
        - Amyloid seeks R-coupling
        - R-axis rejects → Stuck state

        RESULT: {'✓ SUPPORTED' if amyloid_d2_mean < native_d2_mean else '✗ NOT SUPPORTED'}
        """

        ax6.text(0.1, 0.5, hypothesis_text, fontsize=10,
                family='monospace', verticalalignment='center')

    plt.tight_layout()

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_dir / 'stalker_hypothesis_test.png', dpi=300, bbox_inches='tight')
    print(f"\n📊 Plot saved: {output_dir / 'stalker_hypothesis_test.png'}")

    return fig

def main():
    """
    Main analysis pipeline for stalker hypothesis test.
    """
    pdb_dir = Path('/home/king/Downloads/pdb')
    output_dir = Path('/home/king/githubs/dialectical-fractal-theory/results/stalker_hypothesis')

    print("=" * 80)
    print("R-AXIS REJECTION 'STALKER' HYPOTHESIS TEST")
    print("Comparing native proteins vs amyloid fibrils")
    print("=" * 80)

    all_results = []

    # Analyze each category
    for category, pdb_ids in PROTEIN_DATABASE.items():
        results = analyze_protein_set(pdb_dir, category, pdb_ids)
        all_results.extend(results)

    if len(all_results) == 0:
        print("\n❌ No valid results - cannot test hypothesis")
        return

    # Convert to DataFrame
    results_df = pd.DataFrame(all_results)

    # Save results
    output_dir.mkdir(parents=True, exist_ok=True)
    results_csv = output_dir / 'stalker_hypothesis_results.csv'
    results_df.to_csv(results_csv, index=False)

    print(f"\n{'='*80}")
    print("HYPOTHESIS TEST SUMMARY")
    print("=" * 80)

    # Statistical comparison
    for cat in results_df['category'].unique():
        cat_data = results_df[results_df['category'] == cat]
        print(f"\n{cat.upper().replace('_', ' ')}:")
        print(f"  N = {len(cat_data)}")
        print(f"  D₂ = {cat_data['D2'].mean():.3f} ± {cat_data['D2'].std():.3f}")
        print(f"  D₂ range: [{cat_data['D2'].min():.3f}, {cat_data['D2'].max():.3f}]")
        print(f"  C = {cat_data['coupling_tension_C'].mean():.3f} ± {cat_data['coupling_tension_C'].std():.3f}")
        print(f"  R = {cat_data['R_apparent'].mean():.3f} ± {cat_data['R_apparent'].std():.3f}")

        # Check for stalker states
        stalkers = cat_data[cat_data['coupling_state'].str.contains('FRUSTRATED', na=False)]
        if len(stalkers) > 0:
            print(f"  🚨 STALKER STATES: {len(stalkers)} / {len(cat_data)}")
            for _, stalker in stalkers.iterrows():
                print(f"     - {stalker['name']}: D₂={stalker['D2']:.3f}, C={stalker['coupling_tension_C']:.3f}")

    # Create visualizations
    plot_stalker_analysis(results_df, output_dir)

    print(f"\n{'='*80}")
    print(f"✓ Results saved to: {results_csv}")
    print(f"✓ Analysis complete")
    print("=" * 80)

    return results_df

if __name__ == '__main__':
    results = main()
