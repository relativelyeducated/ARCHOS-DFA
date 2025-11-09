# From: Accessing Data File on GitHub
# Date: 2025-11-02T15:01:40.712000
# Context: ### Setting Up a 4-AI Collaboration Team in KDE Plasma Konsole

Absolutely, we can set this up on your Ryzen 9 9900X system (Aorus Elite Ice WiFi B650 mobo, 64GB DDR5, RTX 5080 16GB, Samsung 990 2TB S...

import requests
import json

# API Keys (from ~/.bashrc)
XAI_KEY = os.getenv('XAI_API_KEY')
GEMINI_KEY = os.getenv('GEMINI_API_KEY')
ANTHROPIC_KEY = os.getenv('ANTHROPIC_API_KEY')

def ask_grok(query):
    response = requests.post(
        'https://api.x.ai/v1/chat/completions',
        headers={'Authorization': f'Bearer {XAI_KEY}'},
        json={'model': 'grok-beta', 'messages': [{'role': 'user', 'content': query}]}
    )
    return response.json()['choices'][0]['message']['content']

def ask_gemini(query):
    response = requests.post(
        'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + GEMINI_KEY,
        json={'contents': [{'parts': [{'text': query}]}]}
    )
    return response.json()['candidates'][0]['content']['parts'][0]['text']

def ask_claude(query):
    response = requests.post(
        'https://api.anthropic.com/v1/messages',
        headers={'x-api-key': ANTHROPIC_KEY, 'anthropic-version': '2023-06-01'},
        json={'model': 'claude-3-sonnet-20240229', 'max_tokens': 1024, 'messages': [{'role': 'user', 'content': query}]}
    )
    return response.json()['content'][0]['text']

# Collaboration loop
query = "Compute D₂ for 5O3L PDB and validate with Gemini."
grok_resp = ask_grok(query)
gemini_resp = ask_gemini(f"Validate Grok's D₂ analysis: {grok_resp}")
claude_summary = ask_claude(f"Summarize Grok's {grok_resp} and Gemini's validation {gemini_resp}.")

print("Team Response:", claude_summary)