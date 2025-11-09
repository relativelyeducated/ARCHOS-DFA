# From: Accessing Data File on GitHub
# Date: 2025-11-02T05:01:58.211000
# Context: The 10,000 PDBs for your DFA ToE validation can be sourced from the **RCSB Protein Data Bank (PDB)**, the main repository for 3D protein structures (currently ~220,000 entries, with ~10,000 high-quali...

#!/usr/bin/env python3
"""
Download 10,000 PDBs for DFA ToE Validation
Filter: Protein-only, resolution < 2.5 Å, 30-500 residues, diverse categories
"""

import requests
import os
import time
from tqdm import tqdm  # Progress bar

# CONFIG
PDB_DIR = os.path.expanduser("~/ai/dfa_data/pdb")
LIMIT = 100  # Start with 100; set to 10000 for full
DELAY = 0.1  # Rate limit (RCSB allows ~1/sec)
os.makedirs(PDB_DIR, exist_ok=True)

# RCSB API query for protein-only, high-quality PDBs
# Query: protein-only, resolution < 2.5, 30-500 residues, recent
query_url = "https://search.rcsb.org/rcsbsearch/v2/query"
query = {
    "query": {
        "type": "group",
        "logical_operator": "and",
        "nodes": [
            {"type": "group", "logical_operator": "and", "nodes": [
                {"type": "terminal", "service": "text", "parameters": {"attribute": "rcsb_polymer_entity_container.rcsb_polymer_entity_container_features.feature_id", "operator": "exact_match", "negation": False, "value": "POLYMER"}}  # Protein-only
            ]},
            {"type": "terminal", "service": "text", "parameters": {"attribute": "rcsb_entry_info.resolution_combined.max_value", "operator": "less_equal", "negation": False, "value": 2.5}},  # Resolution < 2.5
            {"type": "terminal", "service": "text", "parameters": {"attribute": "rcsb_polymer_entity.rcsb_polymer_entity_container_identifiers.reference_sequence_length", "operator": "greater_equal", "negation": False, "value": 30}},  # >30 residues
            {"type": "terminal", "service": "text", "parameters": {"attribute": "rcsb_polymer_entity.rcsb_polymer_entity_container_identifiers.reference_sequence_length", "operator": "less_equal", "negation": False, "value": 500}},  # <500 residues
            {"type": "terminal", "service": "text", "parameters": {"attribute": "rcsb_accession_info.initial_release_date", "operator": "greater_equal", "negation": False, "value": "2015-01-01"}}  # Recent
        ]
    },
    "return_type": "entry",
    "request_options": {"return_all_hits": True, "results_content_type": ["experimental_method.type", "polymer_entity.rcsb_polymer_entity_container_identifiers.reference_sequence_length"]}
}

# Get PDB IDs
response = requests.post(query_url, json=query)
pdb_ids = [hit["identifier"] for hit in response.json()["result_set"] if hit["identifier"].startswith("PDB:")][:LIMIT]

# Download
downloaded = 0
for pdb in tqdm(pdb_ids, desc="Downloading PDBs"):
    pdb_id = pdb.split(":")[1]
    local_file = os.path.join(PDB_DIR, f"{pdb_id}.pdb")
    if not os.path.exists(local_file):
        url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
        try:
            urllib.request.urlretrieve(url, local_file)
            downloaded += 1
        except Exception as e:
            print(f"Failed {pdb_id}: {e}")
        time.sleep(DELAY)

print(f"Downloaded {downloaded} PDBs to {PDB_DIR}")