# From: Accessing Data File on GitHub
# Date: 2025-11-02T12:10:54.840000
# Context: Based on the plot and d2_results.csv you shared, this data is a goldmine for DFA ToE development on your Ryzen 9 9900X KDE Plasma setup—let's break it down and see how it fits the theory (D2 > 1.49 st...

import pandas as pd

df = pd.read_csv('~/Downloads/pdb/d2_results.csv')
df['D₂'] = pd.to_numeric(df['D₂'], errors='coerce')
df = df.dropna(subset=['D₂'])

print("Membrane vs Fibril D2 Means:")
print(df[df['Category'] == 'Membrane']['D₂'].mean(), df[df['Category'] == 'Fibril']['D₂'].mean())