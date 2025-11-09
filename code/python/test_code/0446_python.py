# From: Dialectic Evolution Research Overview
# Date: 2025-10-08T18:24:17
# Context: Nope, I don’t have direct access to our past chat threads, including the "Dialectic Evolution Research Collaboration Brief" you mentioned. Each Grok session is sandboxed for privacy and clarity, so I ...

from qutip import *
N = 10000
rho = qeye(2)/2  # Unpolarized
up, down = basis(2,0), basis(2,1)
counts = {'up': 0, 'down': 0}
for _ in range(N):
    outcome = measure(rho, [up*up.dag(), down*down.dag()])
    counts['up' if outcome == 0 else 'down'] += 1
    rho = outcome * rho * outcome.dag() / trace(outcome * rho * outcome.dag())  # Update state
print(f"Up: {counts['up']/N:.3f}, Down: {counts['down']/N:.3f}")