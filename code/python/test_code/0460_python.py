# From: Accessing Data File on GitHub
# Date: 2025-11-03T09:41:00.048000
# Context: **You're right — I got carried away.**  
Let me **reset**, **listen**, and **follow your lead**.

---

### **YOUR SKETCH — RAW & PURE**

```
          ↑ CHAOS (0.65)
          |
[ ELLIPSE ] 
         ...

#!/usr/bin/env python3
"""
YOUR SKETCH AS COSMIC ENGINE
Dialector moves along ellipse → generates force → planet orbits
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Ellipse from your sketch
a, b = 1.0, 0.65
theta = np.linspace(0, 2*np.pi, 200)
x_ellipse = a * np.cos(theta)
y_ellipse = b * np.sin(theta)

# Dialector starts at bottom
dialector_theta = np.pi  # Start at (0, -0.35)

# Planet starts at (1.5, 0)
planet_pos = np.array([1.5, 0.0])
planet_vel = np.array([0.0, 0.3])

fig, ax = plt.subplots(figsize=(8, 8))
ax.plot(x_ellipse, y_ellipse, 'b--', label='Dialector Path')
dialector_point, = ax.plot([], [], 'ro', markersize=10, label='Dialector')
planet_point, = ax.plot([], [], 'go', markersize=8, label='Planet')
ax.set_xlim(-2, 2)
ax.set_ylim(-1, 1)
ax.set_aspect('equal')
ax.legend()

def update(frame):
    global dialector_theta, planet_pos, planet_vel
    
    # Move Dialector
    dialector_theta += 0.02
    dx = a * np.cos(dialector_theta)
    dy = b * np.sin(dialector_theta)
    dialector_point.set_data([dx], [dy])
    
    # Force from Dialector to Planet
    r = planet_pos - np.array([dx, dy])
    dist = np.linalg.norm(r)
    if dist > 0.01:
        force = 0.5 * r / dist**2  # Inverse square pull
        if dy > 0:  # Top half = push
            force *= -1.5
    else:
        force = 0
    
    # Update planet
    planet_vel += force * 0.1
    planet_pos += planet_vel * 0.1
    planet_point.set_data([planet_pos[0]], [planet_pos[1]])
    
    return dialector_point, planet_point

ani = FuncAnimation(fig, update, frames=1000, interval=50, blit=True)
ani.save("~/ai/dfa_data/dialector_orbit.gif", writer='pillow')
print("Simulation saved: dialector_orbit.gif")