import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('chapter3.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's find all indices of '<div class="example-card">'
card_indices = [m.start() for m in re.finditer(r'<div class="example-card">', content)]
card_indices.append(len(content))

examples = []
for i in range(len(card_indices) - 1):
    start = card_indices[i]
    end = card_indices[i+1]
    chunk = content[start:end]
    
    # We want to find the exact closing </div>\s*</div> for the card before any trailing content
    # Look for <h3>Example ...</h3>
    h3_m = re.search(r'<h3>(Example\s+[^:]+:[^<]+)</h3>', chunk)
    title = h3_m.group(1).strip() if h3_m else "Unknown"
    
    # Find sol-wrap id
    sol_m = re.search(r'id="(sol-[^"]+)"', chunk)
    sol_id = sol_m.group(1) if sol_m else "No sol id"
    
    examples.append({
        'index': i,
        'title': title,
        'sol_id': sol_id,
        'start': start,
        'chunk': chunk
    })

print(f"Total examples found: {len(examples)}")
for ex in examples:
    print(f"[{ex['index']}] {ex['title']} | sol_id: {ex['sol_id']}")
