import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/test_chapter3.html', 'r', encoding='utf-8') as f:
    content = f.read()

proof_bodies = list(re.finditer(r'<div class="proof-body" id="([^"]+)">', content))
print(f"Proof bodies count: {len(proof_bodies)}")
for i, pb in enumerate(proof_bodies):
    print(f"  [{i+1}] {pb.group(1)}")
