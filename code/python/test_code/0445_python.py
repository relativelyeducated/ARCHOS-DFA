# From: GEEKOM A9 Max AI Performance Overview
# Date: 2025-10-07T22:26:26.136000
# Context: ### Creating Fine-Tuning Examples from ~200 Chat AI Threads

Turning your 200 chat AI threads (on the same topic) into fine-tuning examples is a smart way to customize an LLM or SLM—like the Phi-3.5-m...

import pandas as pd
import json

# Step 1: Load your chat threads CSV
df = pd.read_csv('your_chat_threads.csv')  # Columns: 'thread_id', 'message_id', 'role' (user/assistant), 'text'

# Step 2: Group by thread and create examples
examples = []
system_prompt = "You are a helpful AI expert on [your topic]. Provide accurate, concise responses based on the conversation."

for thread_id, group in df.groupby('thread_id'):
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add messages in order
    for _, row in group.sort_values('message_id').iterrows():
        messages.append({"role": row['role'], "content": row['text']})
    
    # Only include complete threads (e.g., ends with assistant)
    if messages[-1]['role'] == 'assistant':
        examples.append({"messages": messages})

# Step 3: Save as JSONL for fine-tuning
with open('fine_tuning_examples.jsonl', 'w') as f:
    for ex in examples:
        f.write(json.dumps(ex) + '\n')

print(f"Generated {len(examples)} fine-tuning examples.")