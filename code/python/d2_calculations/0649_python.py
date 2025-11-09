# From: Accessing Data File on GitHub
# Date: 2025-11-02T04:02:17.013000
# Context: ### 50 Protein PDB Dataset for DFA ToE Validation

To get a robust dataset of 50 proteins for testing D₂ thresholds (stable >1.49 vs. collapse ~1.46), we can pull from the RCSB PDB database. I queried...

import os
   import urllib.request

   pdb_list = [
       # Membrane-bound (20)
       '1GZM', '3ZE3', '1BL8', '1F88', '1J5N', '1K4C', '1L6S', '1M56', '1N0A', '1N4A',
       '1O7H', '1P4T', '1QJ8', '1R3J', '1S0I', '1T3E', '1U19', '1V54', '1W9K', '1XKW',

       # Cytosolic/globular (20)
       '1UBQ', '1LMB', '1ROP', '1QLX', '1AG2', '1HJM', '1XQ8', '2N0A', '1IYT', '2LMN',
       '2MZ7', '1TSR', '2OCJ', '1DTD', '1RFO', '3H5C', '4H5C', '5H5C', '6H5C', '7H5C',

       # Fibrils/aggregates (10)
       '5O3L', '6CFP', '3OW9', '2MXU', '6SZF', '5OQV', '6HRE', '2BEG', '3I07', '3I08'
   ]

   for pdb in pdb_list:
       file = f"{pdb}.pdb"
       if not os.path.exists(file):
           url = f"https://files.rcsb.org/download/{pdb}.pdb"
           print(f"Downloading {pdb}...")
           urllib.request.urlretrieve(url, file)

   print(f"Downloaded {len(pdb_list)} PDB files to current directory.")