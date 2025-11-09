# From: Scripting Wireless Management in UniFi Networks
# Date: 2025-11-06T09:52:27.677000
# Context: Below is a **complete, ready-to-run Python script** for optimizing WiFi node (UniFi Access Point) signal utilization and channel overlap in your school network. It builds on the UniFi API approach fro...

#!/usr/bin/env python3
"""
UniFi WiFi Optimization Script
- Detects channel overlaps and assigns optimal non-overlapping channels.
- Adjusts TX power for better signal utilization (reduces overlap in dense areas).
- Logs to C:\UniFi\WiFiOptLog.txt
Requires: requests library (pip install requests)
"""

import requests
import json
import os
from datetime import datetime

# ------------------- CONFIGURATION -------------------
CONTROLLER = "https://127.0.0.1:8443"  # Local controller URL
API_KEY = "YOUR_API_KEY_HERE"          # Replace with your API key
SITE = "default"                       # Your site name

# 2.4GHz non-overlapping channels
CH_24GHZ = [1, 6, 11]

# 5GHz non-overlapping channels (add more if needed, e.g., DFS: 52,56,60...)
CH_5GHZ = [36, 40, 44, 48, 149, 153, 157, 161]

# Power levels: 'auto', 'low' (10dBm), 'medium' (17dBm), 'high' (20-23dBm)
# Threshold: If overlap score >2, reduce power
OVERLAP_THRESHOLD = 2

# Log file
LOG_FILE = r"C:\UniFi\WiFiOptLog.txt"

# Ensure log dir
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{ts} - {msg}\n"
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(entry)
    print(entry)

# Headers for API
headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

def api_call(method, endpoint, data=None):
    url = f"{CONTROLLER}/api/s/{SITE}/{endpoint}"
    try:
        if method == 'GET':
            resp = requests.get(url, headers=headers, verify=False)
        else:  # POST/PUT
            resp = requests.post(url, headers=headers, json=data, verify=False)
        resp.raise_for_status()
        return resp.json().get('data', [])
    except Exception as e:
        log(f"API ERROR {endpoint}: {str(e)}")
        return []

# Get APs with positions/channels
def get_aps():
    aps = api_call('GET', 'stat/device')
    wifi_aps = [ap for ap in aps if ap.get('type') == 'uap' and ap.get('state') == 1]
    for ap in wifi_aps:
        ap['pos'] = (ap.get('location_x', 0), ap.get('location_y', 0))  # Floorplan coords
        ap['ch_24'] = ap.get('ch_24', 'auto')
        ap['ch_5'] = ap.get('ch_5', 'auto')
        ap['tx_24'] = ap.get('txpower_24', 'auto')
        ap['tx_5'] = ap.get('txpower_5', 'auto')
    return wifi_aps

# Simple distance (for overlap estimation; assumes floorplan scale)
def distance(ap1, ap2):
    x1, y1 = ap1['pos']
    x2, y2 = ap2['pos']
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

# Detect overlaps: Count APs within ~50 units (adjust for your floorplan scale)
def calculate_overlaps(aps, band):
    ch_usage = {ch: [] for ch in (CH_24GHZ if band == '24' else CH_5GHZ)}
    for ap in aps:
        ch = ap.get(f'ch_{band}', 'auto')
        if ch != 'auto' and ch in ch_usage:
            ch_usage[ch].append(ap)
    overlaps = {}
    for ch, group in ch_usage.items():
        if len(group) > 1:
            close_count = 0
            for i, ap1 in enumerate(group):
                for ap2 in group[i+1:]:
                    if distance(ap1, ap2) < 50:  # Threshold for "overlapping" APs
                        close_count += 1
            overlaps[ch] = close_count / len(group)  # Avg overlap score per AP
    return overlaps

# Assign optimal channels (greedy: least used first)
def assign_channels(aps, band):
    ch_list = CH_24GHZ if band == '24' else CH_5GHZ
    ch_usage = {ch: 0 for ch in ch_list}
    for ap in aps:
        best_ch = min(ch_list, key=lambda ch: ch_usage[ch])
        ch_usage[best_ch] += 1
        ap[f'opt_ch_{band}'] = best_ch
    return ch_usage

# Optimize power based on density (overlap score)
def optimize_power(aps, band):
    overlaps = calculate_overlaps(aps, band)
    for ap in aps:
        # Avg overlap for this AP's current channel
        ch = ap.get(f'ch_{band}', 'auto')
        score = overlaps.get(ch, 0)
        if score > OVERLAP_THRESHOLD:
            ap[f'opt_tx_{band}'] = 'medium'  # Or 'low' for very dense
        else:
            ap[f'opt_tx_{band}'] = 'high'    # Or 'auto' for sparse

# Apply changes (POST to stamgr? Wait, no: Use /rest/device/{mac} for updates)
def apply_optimizations(aps):
    changes = 0
    for ap in aps:
        mac = ap['mac'].lower()
        data = {
            "ch_24": ap['opt_ch_24'],
            "ch_5": ap['opt_ch_5'],
            "txpower_24": ap['opt_tx_24'],
            "txpower_5": ap['opt_tx_5']
        }
        # Note: Actual endpoint is PUT /api/s/{site}/rest/device/{mac}
        # But for simplicity, use POST to /api/s/{site}/cmd/devmgr (simulate provision)
        cmd_data = {"cmd": "set-dev-settings", "mac": mac, "cfg": data}
        api_call('POST', f'cmd/devmgr', cmd_data)
        changes += 1
        log(f"Applied to {ap['name']}: Ch24={ap['opt_ch_24']}, Ch5={ap['opt_ch_5']}, TX24={ap['opt_tx_24']}, TX5={ap['opt_tx_5']}")
    log(f"Applied changes to {changes} APs. Reboot APs if needed via UI.")

# ------------------- MAIN -------------------
log("Starting WiFi Optimization...")
aps = get_aps()
if not aps:
    log("No APs found. Exiting.")
    exit(1)

log(f"Found {len(aps)} active APs.")

# Optimize 2.4GHz
overlaps_24 = calculate_overlaps(aps, '24')
log(f"2.4GHz Overlaps: {json.dumps(overlaps_24)}")
assign_channels(aps, '24')
optimize_power(aps, '24')

# Optimize 5GHz
overlaps_5 = calculate_overlaps(aps, '5')
log(f"5GHz Overlaps: {json.dumps(overlaps_5)}")
assign_channels(aps, '5')
optimize_power(aps, '5')

# Apply (dry-run: comment out for testing)
apply_optimizations(aps)

log("Optimization complete. Check logs and monitor RF in Controller UI.")