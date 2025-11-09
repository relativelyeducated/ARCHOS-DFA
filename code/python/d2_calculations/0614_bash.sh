# From: Accessing Data File on GitHub
# Date: 2025-10-26T21:41:19.194000
# Context: Below is a **stand-alone script** that

1. **Downloads 6VHJ** (if it isn’t already in `~/ai/dfa_data/pdb`)  
2. **Extracts the Cα atoms of every chain** (A-J)  
3. **Computes D₂ for each chain**  
4. ...

# 1. Save the script
kate ~/ai/compute_delta_d2_6VHJ.py   # paste the code above, Ctrl+S

# 2. Make executable (optional)
chmod +x ~/ai/compute_delta_d2_6VHJ.py

# 3. Execute
conda activate dfa-toe
python ~/ai/compute_delta_d2_6VHJ.py