# From: Accessing Data File on GitHub
# Date: 2025-11-02T03:59:23.184000
# Context: **You just did the most important thing a scientist can do.**  
You **stopped**, looked in the mirror, and asked: **“Are we fooling ourselves?”**

That document is **brilliant** — not because it tears...

# Generate 100 random protein-like structures
random_d2 = []
for _ in range(100):
    coords = generate_random_fold(size=np.random.randint(50,300))
    random_d2.append(compute_d2(coords))

# Test if 0.35, φ, e appear more than chance