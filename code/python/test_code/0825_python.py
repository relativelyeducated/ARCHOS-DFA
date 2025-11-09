# From: Scripting Wireless Management in UniFi Networks
# Date: 2025-11-06T09:54:32.594000
# Context: Below is a **complete, ready-to-email document** (copy-paste into Word, Google Docs, or a plain-text email).  
It contains **all scripts**, **setup steps**, **software requirements**, **links**, and *...

#!/usr/bin/env python3
"""
UniFi WiFi Optimization – Reduces channel overlap & adjusts TX power
"""

import requests, json, os
from datetime import datetime

# ------------------- CONFIG -------------------
CONTROLLER = "https://127.0.0.1:8443"
API_KEY = "YOUR_API_KEY_HERE"          # ← CHANGE THIS
SITE = "default"

CH_24GHZ = [1, 6, 11]
CH_5GHZ = [36, 40, 44, 48, 149, 153, 157, 161]
OVERLAP_THRESHOLD = 2
LOG_FILE = r"C:\UniFi\WiFiOptLog.txt"
# ---------------------------------------------

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
def log(msg): 
    entry = f"{datetime.now():%Y-%m-%d %H:%M:%S} - {msg}\n"
    with open(LOG_FILE, 'a', encoding='utf-8') as f: f.write(entry)
    print(entry.strip())

headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

def api_call(method, endpoint, data=None):
    url = f"{CONTROLLER}/api/s/{SITE}/{endpoint}"
    try:
        resp = requests.request(method, url, headers=headers, json=data, verify=False)
        resp.raise_for_status()
        return resp.json().get('data', [])
    except Exception as e: log(f"API ERROR: {e}"); return []

def get_aps():
    aps = [a for a in api_call('GET', 'stat/device') if a.get('type') == 'uap' and a.get('state') == 1]
    for a in aps:
        a['pos'] = (a.get('location_x', 0), a.get('location_y', 0))
        a['ch_24'] = a.get('radio_table', [{}])[0].get('channel', 'auto')
        a['ch_5'] = a.get('radio_table', [{}])[1].get('channel', 'auto') if len(a.get('radio_table', [])) > 1 else 'auto'
    return aps

def distance(a1, a2): 
    x1,y1 = a1['pos']; x2,y2 = a2['pos']
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def calculate_overlaps(aps, band):
    ch_list = CH_24GHZ if band == '24' else CH_5GHZ
    usage = {ch: [] for ch in ch_list}
    for ap in aps:
        ch = ap.get(f'ch_{band}', 'auto')
        if ch in usage: usage[ch].append(ap)
    overlaps = {}
    for ch, group in usage.items():
        if len(group) > 1:
            close = sum(1 for i in range(len(group)) for j in range(i+1, len(group)) if distance(group[i], group[j]) < 50)
            overlaps[ch] = close / len(group)
    return overlaps

def assign_channels(aps, band):
    ch_list = CH_24GHZ if band == '24' else CH_5GHZ
    usage = {ch: 0 for ch in ch_list}
    for ap in aps:
        best = min(ch_list, key=lambda c: usage[c])
        usage[best] += 1
        ap[f'opt_ch_{band}'] = best

def optimize_power(aps, band):
    overlaps = calculate_overlaps(aps, band)
    for ap in aps:
        ch = ap.get(f'ch_{band}', 'auto')
        score = overlaps.get(ch, 0)
        ap[f'opt_tx_{band}'] = 'medium' if score > OVERLAP_THRESHOLD else 'high'

def apply_optimizations(aps):
    for ap in aps:
        mac = ap['mac'].lower()
        data = {
            "radio_table": [
                {"channel": ap['opt_ch_24'], "tx_power_mode": ap['opt_tx_24']},
                {"channel": ap['opt_ch_5'], "tx_power_mode": ap['opt_tx_5']}
            ]
        }
        api_call('PUT', f'rest/device/{mac}', data)
        log(f"AP {ap['name']}: Ch24={ap['opt_ch_24']}({ap['opt_tx_24']}), Ch5={ap['opt_ch_5']}({ap['opt_tx_5']})")

# ------------------- RUN -------------------
log("Starting WiFi Optimization...")
aps = get_aps()
if not aps: log("No APs found."); exit()

assign_channels(aps, '24'); optimize_power(aps, '24')
assign_channels(aps, '5'); optimize_power(aps, '5')

# DRY-RUN: Comment line below to test without applying
apply_optimizations(aps)

log("Optimization complete.")