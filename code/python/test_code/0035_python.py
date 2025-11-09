# From: ASUS ROG Strix G16CHR-XS776S Specs
# Date: 2025-10-04T18:46:26.151000
# Context: Got it—your clarification sharpens the dialectic beautifully! Dropping the overseer role keeps the game lean and focused, preserving the core **asymmetric co-op dialectic** between the **Field Operati...

import random
import time

# Sim state
field = {"role": "Assault", "pos": "alley", "health": 100, "gear": ["pistol"]}
handler = {"bandwidth": 80, "feeds": ["cam1", "cam2"], "uploads": ["Grenade Launcher", "Holo-Disguise", "Helo Pilot"]}
mission = {"obj": "Steal Data", "zone": "corp_tower", "threats": ["guards", "drones"]}
link_stability = 90  # Affects comms

def simulate_static(message):
    """Add distortion to comms if link is weak."""
    if link_stability < 60:
        words = message.split()
        return " ".join(w + ("..." if random.random() < 0.3 else "") for w in words[:random.randint(1, len(words))])
    return message

def field_turn():
    """Field operative's action."""
    action = input(f"[Field/{field['role']} @ {field['pos']}]: Request (e.g., 'Cam feed', 'Exit', 'Skill')? ")
    action = simulate_static(action)
    print(f"[Field Comms]: {action}")
    if "cam" in action.lower():
        print(f"[Handler]: Feed active—{random.choice(mission['threats'])} in sector 3.")
    elif "exit" in action.lower():
        print(f"[Handler]: Hacking exit—{random.choice(['rooftop', 'sewer'])} open in 10s.")
    elif "skill" in action.lower():
        print(f"[Handler]: Uploading... {random.choice(handler['uploads'])}.")
        field['gear'].append(random.choice(handler['uploads']))
    else:
        print(f"[Handler]: Comms garbled—repeat request!")
    # Check HUD for uploads
    if random.random() < 0.4:  # Handler proactive push
        new_gear = random.choice(handler['uploads'])
        field['gear'].append(new_gear)
        print(f"[Field HUD]: New Upload - {new_gear}. Adapt!")
    print(f"[Field Status]: Gear: {field['gear']}, Health: {field['health']}")

def handler_turn():
    """Handler's prep and positioning."""
    print(f"[Handler]: Feeds: {handler['feeds']}, Bandwidth: {handler['bandwidth']}%")
    action = input("[Handler]: Action (e.g., 'Hack cam', 'Upload skill', 'Reroute env')? ")
    if "hack" in action.lower():
        handler['feeds'].append(f"cam{len(handler['feeds'])+1}")
        print(f"[Handler]: New feed acquired—{mission['threats'][0]} moving.")
    elif "upload" in action.lower():
        upload = random.choice(handler['uploads'])
        field['gear'].append(upload)
        print(f"[Field HUD]: {upload} uploaded—use it!")
    elif "reroute" in action.lower():
        print(f"[Handler]: Env rerouted—new exit: {random.choice(['vent', 'service door'])}.")
    else:
        print(f"[Handler]: Action failed—low bandwidth.")
    # Proactive push
    if random.random() < 0.5:
        upload = random.choice(handler['uploads'])
        field['gear'].append(upload)
        print(f"[Handler]: Proactive upload—{upload} sent to Field HUD.")
    handler['bandwidth'] -= random.randint(5, 15)
    global link_stability
    link_stability -= random.randint(0, 10)  # Static risk

# Sim one turn
print(f"Mission: {mission['obj']} in {mission['zone']}")
field_turn()
handler_turn()
print(f"[Mission]: Link Stability: {link_stability}%")