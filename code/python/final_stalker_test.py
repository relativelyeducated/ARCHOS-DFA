#!/usr/bin/env python3
"""
DEFINITIVE STALKER HYPOTHESIS TEST
===================================

Properly categorized analysis of:
- Monomers (expected D_box ≈ 1.2-1.4)
- Oligomers (expected D_box ≈ 1.5-1.8 - MOST TOXIC)
- Fibrils (expected D_box ≈ 2.0-2.5)

Tests if toxicity correlates with frustrated coupling state.

Author: Jason King (DFA Theory)
Date: November 8, 2025
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from spatial_fractal_analysis import analyze_protein_spatial_fractal
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# PROPERLY CURATED DATABASE
PROTEIN_CATEGORIES = {
    'monomers_native': {
        'desc': 'Native folded monomers (control)',
        'pdbs': ['1UBQ', '1ENH', '1PGB', '1SHG', '1ROP', '2CI2', '1TIT', '1WIT'],
    },
    'monomers_amyloid': {
        'desc': 'Amyloid-β monomers (misfolded)',
        'pdbs': ['1IYT', '6SZF'],  # Aβ monomers
    },
    'oligomers_toxic': {
        'desc': 'Amyloid oligomers (PREDICTED STALKER - MOST TOXIC)',
        'pdbs': ['2NAO', '2MPZ', '6SHS', '6H6B'],  # Aβ and α-synuclein oligomers
    },
    'fibrils_large': {
        'desc': 'Large amyloid fibrils (classical)',
        'pdbs': ['2MXU', '3OW9', '2BEG', '2N0A', '5O3L'],  # Large fibril assemblies
    },
    'prions': {
        'desc': 'Prion proteins',
        'pdbs': ['1QLX', '1HJM'],
    },
}

def analyze_all_categories():
    """
    Run spatial fractal analysis on all properly categorized proteins.
    """
    pdb_dir = Path('/home/king/Downloads/pdb')
    all_results = []

    print("=" * 80)
    print("DEFINITIVE STALKER HYPOTHESIS TEST")
    print("=" * 80)
    print("\nPREDICTIONS:")
    print("  Monomers:  D_box ≈ 1.2-1.4, C ≈ 0.2-0.3 (low frustration)")
    print("  Oligomers: D_box ≈ 1.5-1.8, C ≈ 0.25-0.35 (STALKER - max toxicity)")
    print("  Fibrils:   D_box ≈ 2.0-2.5, C → 0 (classical, inert)")
    print("=" * 80)

    for category, info in PROTEIN_CATEGORIES.items():
        print(f"\n{'='*70}")
        print(f"{info['desc'].upper()}")
        print(f"{'='*70}\n")

        for pdb_id in info['pdbs']:
            pdb_file = None
            for f in pdb_dir.glob(f"{pdb_id}.*"):
                if f.suffix.lower() == '.pdb':
                    pdb_file = f
                    break

            if pdb_file is None:
                print(f"  ⚠ {pdb_id}: Not found")
                continue

            result = analyze_protein_spatial_fractal(pdb_file)

            if result:
                result['category'] = category
                result['category_desc'] = info['desc']
                all_results.append(result)

                print(f"  ✓ {pdb_id}:")
                print(f"      Atoms: {result['n_atoms']}")
                print(f"      D_box: {result['D_box']:.3f} (R²={result['r_squared']:.3f})")
                print(f"      C: {result['coupling_tension_C']:.3f}")
                print(f"      State: {result['coupling_state']}")

                # Highlight stalker state
                if 'FRUSTRATED' in result['coupling_state']:
                    print(f"      🚨 STALKER STATE DETECTED!")

    return pd.DataFrame(all_results)

def plot_results(df, output_dir):
    """
    Create publication-quality plots.
    """
    fig = plt.figure(figsize=(18, 12))

    # Color scheme
    colors = {
        'monomers_native': '#2E86AB',
        'monomers_amyloid': '#A23B72',
        'oligomers_toxic': '#FF0000',  # RED for predicted stalkers
        'fibrils_large': '#4A7C59',
        'prions': '#F18F01',
    }

    # 1. D_box by category (TOP LEFT)
    ax1 = plt.subplot(2, 3, 1)
    categories = list(PROTEIN_CATEGORIES.keys())
    cat_labels = [PROTEIN_CATEGORIES[c]['desc'] for c in categories]

    for cat in categories:
        data = df[df['category'] == cat]['D_box']
        positions = [categories.index(cat)] * len(data)
        ax1.scatter(positions, data, color=colors[cat], s=150, alpha=0.7,
                   edgecolors='black', linewidth=2, zorder=3)

    # Mark zones
    ax1.axhspan(1.2, 1.4, alpha=0.15, color='blue', label='Monomer zone')
    ax1.axhspan(1.5, 1.8, alpha=0.25, color='red', label='STALKER zone (max toxicity)')
    ax1.axhspan(2.0, 2.5, alpha=0.15, color='green', label='Fibril zone (inert)')

    ax1.set_xticks(range(len(categories)))
    ax1.set_xticklabels([c.replace('_', '\n') for c in categories], fontsize=9)
    ax1.set_ylabel('D_box (Spatial Fractal Dimension)', fontsize=12, fontweight='bold')
    ax1.set_title('D_box by Protein Category', fontsize=13, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.grid(alpha=0.3, axis='y')
    ax1.set_ylim(0.5, 2.8)

    # 2. Coupling tension by category (TOP MIDDLE)
    ax2 = plt.subplot(2, 3, 2)
    for cat in categories:
        data = df[df['category'] == cat]['coupling_tension_C']
        positions = [categories.index(cat)] * len(data)
        ax2.scatter(positions, data, color=colors[cat], s=150, alpha=0.7,
                   edgecolors='black', linewidth=2)

    ax2.axhspan(0.15, 0.35, alpha=0.3, color='red')
    ax2.text(2.5, 0.25, 'STALKER\nZONE', fontsize=16, fontweight='bold',
             ha='center', va='center', color='darkred', alpha=0.5)

    ax2.set_xticks(range(len(categories)))
    ax2.set_xticklabels([c.replace('_', '\n') for c in categories], fontsize=9)
    ax2.set_ylabel('Coupling Tension C', fontsize=12, fontweight='bold')
    ax2.set_title('Frustration by Category', fontsize=13, fontweight='bold')
    ax2.grid(alpha=0.3, axis='y')

    # 3. D_box vs C scatter (TOP RIGHT)
    ax3 = plt.subplot(2, 3, 3)
    for cat in categories:
        data = df[df['category'] == cat]
        ax3.scatter(data['D_box'], data['coupling_tension_C'],
                   label=cat.replace('_', ' ').title(),
                   color=colors[cat], s=150, alpha=0.7,
                   edgecolors='black', linewidth=2)

    # Mark stalker zone
    from matplotlib.patches import Rectangle
    stalker_zone = Rectangle((1.5, 0.15), 0.3, 0.2, linewidth=3,
                             edgecolor='red', facecolor='red', alpha=0.2)
    ax3.add_patch(stalker_zone)
    ax3.text(1.65, 0.38, 'PREDICTED\nSTALKER ZONE', fontsize=11,
             fontweight='bold', ha='center', color='darkred')

    ax3.set_xlabel('D_box', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Coupling Tension C', fontsize=12, fontweight='bold')
    ax3.set_title('Stalker Phase Diagram', fontsize=13, fontweight='bold')
    ax3.legend(fontsize=8, loc='upper left')
    ax3.grid(alpha=0.3)
    ax3.set_xlim(0.5, 2.8)
    ax3.set_ylim(0, 0.5)

    # 4. Summary statistics table (BOTTOM LEFT)
    ax4 = plt.subplot(2, 3, 4)
    ax4.axis('off')

    summary_data = []
    for cat in categories:
        data = df[df['category'] == cat]
        if len(data) > 0:
            stalkers = len(data[data['coupling_state'].str.contains('FRUSTRATED', na=False)])
            summary_data.append([
                cat.replace('_', ' ').title(),
                len(data),
                f"{data['D_box'].mean():.2f}±{data['D_box'].std():.2f}",
                f"{data['coupling_tension_C'].mean():.2f}",
                f"{stalkers}/{len(data)}"
            ])

    table = ax4.table(cellText=summary_data,
                      colLabels=['Category', 'N', 'D_box', 'C', 'Stalkers'],
                      cellLoc='center',
                      loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2.5)

    for i, cat in enumerate(categories):
        if len(df[df['category'] == cat]) > 0:
            table[(i+1, 0)].set_facecolor(colors[cat])
            table[(i+1, 0)].set_alpha(0.3)

    ax4.set_title('Summary Statistics', fontsize=13, fontweight='bold', pad=20)

    # 5. Hypothesis test results (BOTTOM MIDDLE)
    ax5 = plt.subplot(2, 3, 5)
    ax5.axis('off')

    # Calculate stats
    monomers = df[df['category'].str.contains('monomer')]
    oligomers = df[df['category'] == 'oligomers_toxic']
    fibrils = df[df['category'] == 'fibrils_large']

    test_text = "STALKER HYPOTHESIS TEST\n"
    test_text += "="*40 + "\n\n"

    if len(monomers) > 0:
        test_text += f"MONOMERS (n={len(monomers)}):\n"
        test_text += f"  D_box = {monomers['D_box'].mean():.2f} ± {monomers['D_box'].std():.2f}\n"
        test_text += f"  C = {monomers['coupling_tension_C'].mean():.2f}\n\n"

    if len(oligomers) > 0:
        test_text += f"OLIGOMERS (n={len(oligomers)}):\n"
        test_text += f"  D_box = {oligomers['D_box'].mean():.2f} ± {oligomers['D_box'].std():.2f}\n"
        test_text += f"  C = {oligomers['coupling_tension_C'].mean():.2f}\n"
        stalker_count = len(oligomers[oligomers['coupling_state'].str.contains('FRUSTRATED', na=False)])
        test_text += f"  Stalkers: {stalker_count}/{len(oligomers)}\n\n"

    if len(fibrils) > 0:
        test_text += f"FIBRILS (n={len(fibrils)}):\n"
        test_text += f"  D_box = {fibrils['D_box'].mean():.2f} ± {fibrils['D_box'].std():.2f}\n"
        test_text += f"  C = {fibrils['coupling_tension_C'].mean():.2f}\n\n"

    # Verdict
    if len(oligomers) > 0 and len(monomers) > 0:
        if oligomers['D_box'].mean() > monomers['D_box'].mean() and oligomers['D_box'].mean() < 2.0:
            test_text += "\n✓ HYPOTHESIS SUPPORTED:\n"
            test_text += "  Oligomers intermediate\n"
            test_text += "  between monomers & fibrils"
        else:
            test_text += "\n⚠ HYPOTHESIS NEEDS REFINEMENT"

    ax5.text(0.1, 0.5, test_text, fontsize=10, family='monospace',
             verticalalignment='center')
    ax5.set_title('Quantitative Analysis', fontsize=13, fontweight='bold', pad=20)

    # 6. Size vs D_box (BOTTOM RIGHT)
    ax6 = plt.subplot(2, 3, 6)
    for cat in categories:
        data = df[df['category'] == cat]
        ax6.scatter(data['n_atoms'], data['D_box'],
                   label=cat.replace('_', ' ').title(),
                   color=colors[cat], s=150, alpha=0.7,
                   edgecolors='black', linewidth=2)

    ax6.set_xscale('log')
    ax6.set_xlabel('Number of Atoms (log scale)', fontsize=12, fontweight='bold')
    ax6.set_ylabel('D_box', fontsize=12, fontweight='bold')
    ax6.set_title('Size vs Fractal Dimension', fontsize=13, fontweight='bold')
    ax6.legend(fontsize=8)
    ax6.grid(alpha=0.3)
    ax6.axhspan(1.5, 1.8, alpha=0.2, color='red')

    plt.tight_layout()

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_dir / 'final_stalker_test.png', dpi=300, bbox_inches='tight')
    print(f"\n📊 Plot saved: {output_dir / 'final_stalker_test.png'}")

    return fig

def main():
    # Run analysis
    df = analyze_all_categories()

    # Save results
    output_dir = Path('/home/king/githubs/dialectical-fractal-theory/results/final_stalker_test')
    output_dir.mkdir(parents=True, exist_ok=True)

    results_csv = output_dir / 'final_stalker_results.csv'
    df.to_csv(results_csv, index=False)

    # Print summary
    print("\n" + "=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)

    for cat in PROTEIN_CATEGORIES.keys():
        cat_data = df[df['category'] == cat]
        if len(cat_data) > 0:
            print(f"\n{cat.upper().replace('_', ' ')}:")
            print(f"  N = {len(cat_data)}")
            print(f"  D_box = {cat_data['D_box'].mean():.3f} ± {cat_data['D_box'].std():.3f}")
            print(f"  Range: [{cat_data['D_box'].min():.3f}, {cat_data['D_box'].max():.3f}]")
            print(f"  C = {cat_data['coupling_tension_C'].mean():.3f}")

            stalkers = cat_data[cat_data['coupling_state'].str.contains('FRUSTRATED', na=False)]
            if len(stalkers) > 0:
                print(f"  🚨 STALKERS: {len(stalkers)}/{len(cat_data)}")

    # Create plots
    plot_results(df, output_dir)

    print(f"\n✓ Results saved to: {results_csv}")
    print("=" * 80)

    return df

if __name__ == '__main__':
    results = main()
