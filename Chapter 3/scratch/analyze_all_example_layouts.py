import sys
import re

with open('chapter3.html', 'r', encoding='utf-8') as f:
    content = f.read()

card_matches = list(re.finditer(r'<div class="example-card">', content))
print(f"Total cards: {len(card_matches)}")

for i, cm in enumerate(card_matches):
    start = cm.start()
    end = card_matches[i+1].start() if i+1 < len(card_matches) else len(content)
    chunk = content[start:end]
    
    # title
    h3 = re.search(r'<h3>(.*?)</h3>', chunk)
    title = h3.group(1) if h3 else "Unknown"
    
    # check problem-statement
    prob_m = re.search(r'<div class="problem-statement">([\s\S]*?)</div>', chunk)
    
    # check fig-container
    fig_m = re.search(r'<div class="fig-container[^"]*">[\s\S]*?</div>\s*</div>', chunk)
    
    # check if already in example-problem-layout
    has_layout = 'example-problem-layout' in chunk
    
    # check if fig is right after problem statement
    is_right_after = False
    if prob_m:
        prob_end = prob_m.end()
        after_prob = chunk[prob_end:].strip()
        if after_prob.startswith('<div class="fig-container'):
            is_right_after = True
            
    print(f"Ex {i+1}: {title}")
    print(f"   prob: {'YES' if prob_m else 'NO'} | fig: {'YES' if fig_m else 'NO'} | right after: {is_right_after} | has_layout: {has_layout}")
