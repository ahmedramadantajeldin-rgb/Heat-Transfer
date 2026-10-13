import sys
import re
import os

with open('chapter3.html', 'r', encoding='utf-8') as f:
    content = f.read()

card_indices = [m.start() for m in re.finditer(r'<div class="example-card">', content)]
card_indices.append(len(content))

os.makedirs('scratch/ex', exist_ok=True)

for i in range(len(card_indices) - 1):
    start = card_indices[i]
    end = card_indices[i+1]
    chunk = content[start:end]
    
    # isolate the card from anything after it: find the matching closing div
    # An example card structure:
    # <div class="example-card">
    #   <div class="example-header">...</div>
    #   <div class="example-body">
    #     ...
    #     <div class="sol-wrap"...><div class="sol-inner">...</div></div>
    #   </div>
    # </div>
    # Let's find </section> or next card if present
    sol_wrap_idx = chunk.find('class="sol-wrap"')
    if sol_wrap_idx != -1:
        # find the closing of sol-wrap, example-body, and example-card
        # after sol-wrap, there is </div></div></div>
        end_sol = chunk.find('</div></div>', sol_wrap_idx)
        if end_sol != -1:
            end_card = chunk.find('</div>', end_sol + 12)
            if end_card != -1:
                card_html = chunk[:end_card + 6]
            else:
                card_html = chunk
        else:
            card_html = chunk
    else:
        card_html = chunk
        
    h3_m = re.search(r'<h3>(Example\s+[^:]+:[^<]+)</h3>', card_html)
    title = h3_m.group(1).strip() if h3_m else f"Ex_{i}"
    
    sol_m = re.search(r'id="(sol-[^"]+)"', card_html)
    sol_id = sol_m.group(1) if sol_m else f"no_sol_{i}"
    
    with open(f'scratch/ex/{sol_id}.html', 'w', encoding='utf-8') as f_out:
        f_out.write(card_html)

print("Saved all 15 example cards to scratch/ex/")
