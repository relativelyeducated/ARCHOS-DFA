#!/usr/bin/env python3
"""
PDB Data Validation and Curation
=================================

Validates existing PDB structures and identifies which ones are appropriate
for testing the stalker hypothesis.

Need to find:
1. Amyloid OLIGOMERS (not large fibrils) - predicted D_box ≈ 1.5-1.8
2. Small monomeric proteins - predicted D_box ≈ 1.2-1.4
3. Native vs misfolded comparisons

Author: Jason King (DFA Theory)
Date: November 8, 2025
"""

import requests
from pathlib import Path
import pandas as pd

def query_pdb_info(pdb_id):
    """
    Query RCSB PDB for structure information.
    """
    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id.upper()}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                'pdb_id': pdb_id,
                'title': data.get('struct', {}).get('title', 'N/A'),
                'method': data.get('exptl', [{}])[0].get('method', 'N/A'),
                'resolution': data.get('rcsb_entry_info', {}).get('resolution_combined', [None])[0],
                'keywords': data.get('struct_keywords', {}).get('pdbx_keywords', 'N/A'),
            }
        else:
            return None
    except Exception as e:
        print(f"  Error querying {pdb_id}: {e}")
        return None

def analyze_existing_structures():
    """
    Analyze what we actually have in our PDB directory.
    """
    pdb_dir = Path('/home/king/Downloads/pdb')
    pdb_files = sorted(pdb_dir.glob('*.pdb'))

    print("=" * 80)
    print("ANALYZING EXISTING PDB STRUCTURES")
    print("=" * 80)

    structure_info = []

    for pdb_file in pdb_files:
        pdb_id = pdb_file.stem

        # Count atoms
        with open(pdb_file, 'r') as f:
            atom_count = sum(1 for line in f if line.startswith('ATOM'))
            header = None
            title = None
            for line in f:
                if line.startswith('HEADER'):
                    header = line[10:50].strip()
                if line.startswith('TITLE'):
                    title = line[10:].strip()
                    break

        # Query RCSB for details
        info = query_pdb_info(pdb_id)

        if info:
            info['atom_count'] = atom_count
            info['header'] = header if header else 'N/A'
            structure_info.append(info)

            print(f"\n{pdb_id}: {info['title'][:60]}")
            print(f"  Atoms: {atom_count}, Keywords: {info['keywords']}")

    return pd.DataFrame(structure_info)

def recommend_structures():
    """
    Recommend which PDB structures to download for stalker hypothesis test.
    """
    print("\n" + "=" * 80)
    print("RECOMMENDED STRUCTURES FOR STALKER HYPOTHESIS")
    print("=" * 80)

    recommendations = {
        'Amyloid β oligomers (CRITICAL - test stalker hypothesis)': [
            '2NAO',  # Aβ42 oligomer (toxic species!)
            '2MPZ',  # Aβ oligomer
            '6SHS',  # Aβ42 oligomer
        ],
        'Amyloid β monomers': [
            '1IYT',  # Aβ monomer NMR
            '1Z0Q',  # Aβ peptide
        ],
        'Amyloid β fibrils (large)': [
            '2MXU',  # ✓ Already have
            '5OQV',  # Aβ42 fibril
            '6TI5',  # Aβ fibril
        ],
        'Tau oligomers (Alzheimer\'s related)': [
            '5O3L',  # Tau fragment
            '5O3T',  # Tau PHF
        ],
        'Alpha-synuclein (Parkinson\'s - comparison)': [
            '6H6B',  # α-synuclein oligomer
            '2N0A',  # α-synuclein monomer
        ],
        'Small native proteins (control)': [
            '1UBQ',  # ✓ Already have - Ubiquitin
            '1ENH',  # ✓ Already have - showed stalker!
            '1PGB',  # ✓ Already have - showed stalker!
        ],
        'Prion proteins': [
            '1QLX',  # ✓ Already have
            '3HAK',  # Prion oligomer
        ]
    }

    print("\nKEY STRUCTURES NEEDED:")
    print("-" * 80)

    for category, pdb_ids in recommendations.items():
        print(f"\n{category}:")
        for pdb_id in pdb_ids:
            if '✓' in pdb_id:
                print(f"  {pdb_id}")
            else:
                print(f"  {pdb_id} - DOWNLOAD NEEDED")

    print("\n" + "=" * 80)
    print("STALKER HYPOTHESIS TEST PLAN")
    print("=" * 80)
    print("""
1. MONOMERS (Small native/misfolded proteins):
   Expected: D_box ≈ 1.2-1.4, C ≈ 0.2-0.3 (STALKER STATE)

2. OLIGOMERS (2-50 proteins):
   Expected: D_box ≈ 1.5-1.8, C ≈ 0.3-0.4 (MAXIMALLY FRUSTRATED - MOST TOXIC)

3. FIBRILS (Large assemblies):
   Expected: D_box ≈ 2.0-2.5 (Classical, inert)

PREDICTION: Toxicity peaks at OLIGOMER stage where proteins are stuck
between stalker state and classical state.
""")

    return recommendations

def download_recommended_pdbs():
    """
    Download the recommended PDB structures.
    """
    critical_structures = [
        '2NAO',  # Aβ42 oligomer - CRITICAL
        '2MPZ',  # Aβ oligomer
        '6SHS',  # Aβ42 oligomer
        '5O3L',  # Tau (already have?)
        '6H6B',  # α-synuclein oligomer
        '2N0A',  # α-synuclein monomer (already have?)
        '1IYT',  # Aβ monomer (already have?)
    ]

    pdb_dir = Path('/home/king/Downloads/pdb')
    pdb_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 80)
    print("DOWNLOADING CRITICAL STRUCTURES")
    print("=" * 80)

    for pdb_id in critical_structures:
        pdb_file = pdb_dir / f"{pdb_id}.pdb"

        if pdb_file.exists():
            print(f"\n✓ {pdb_id}: Already exists")
            continue

        url = f"https://files.rcsb.org/download/{pdb_id.upper()}.pdb"

        try:
            print(f"\n⬇ {pdb_id}: Downloading...")
            response = requests.get(url, timeout=30)

            if response.status_code == 200:
                with open(pdb_file, 'w') as f:
                    f.write(response.text)
                print(f"  ✓ Saved to {pdb_file}")
            else:
                print(f"  ✗ Failed: HTTP {response.status_code}")

        except Exception as e:
            print(f"  ✗ Error: {e}")

def main():
    print("PDB DATA VALIDATION FOR STALKER HYPOTHESIS")
    print("=" * 80)

    # Analyze what we have
    df = analyze_existing_structures()

    # Show recommendations
    recommendations = recommend_structures()

    # Ask user if they want to download
    print("\n" + "=" * 80)
    print("READY TO DOWNLOAD CRITICAL STRUCTURES")
    print("=" * 80)
    print("\nDownloading recommended PDB structures...")

    download_recommended_pdbs()

    print("\n" + "=" * 80)
    print("✓ VALIDATION COMPLETE")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Re-run spatial_fractal_analysis.py with new structures")
    print("2. Compare monomer vs oligomer vs fibril D_box values")
    print("3. Test prediction: Oligomers have D_box ≈ 1.5-1.8 (max frustration)")

    return df

if __name__ == '__main__':
    df = main()
