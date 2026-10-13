import sys
import re
import os

with open('scratch/direct_sols.txt', 'r', encoding='utf-8') as f:
    text = f.read()

os.makedirs('scratch/sols', exist_ok=True)
parts = text.split('=== ')
for p in parts:
    if not p.strip():
        continue
    lines = p.strip().splitlines()
    raw_id = lines[0].replace(' ===', '').strip()
    clean_id = re.sub(r'[^a-zA-Z0-9_-]', '', raw_id)
    if not clean_id:
        continue
    body = '\n'.join(lines[1:])
    with open(f'scratch/sols/{clean_id}.txt', 'w', encoding='utf-8') as f_out:
        f_out.write(body)

print("Saved individual sol files.")
