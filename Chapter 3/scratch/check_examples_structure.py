import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('chapter3.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find each example card:
# Match <div class="example-card"> up to closing </div>\s*</div> for the card.
# Let's find all example headers and line numbers:
matches = list(re.finditer(r'<div class="example-card">([\s\S]*?)(?=<div class="example-card">|</section>)', content))

print(f"Total example matches: {len(matches)}")
for idx, m in enumerate(matches):
    block = m.group(0)
    h3 = re.search(r'<h3>(.*?)</h3>', block)
    h3_text = h3.group(1) if h3 else "No H3"
    fig = re.search(r'<div class="fig-container[^"]*">([\s\S]*?)</div>\s*</div>', block)
    fig_text = "YES" if '<div class="fig-container' in block else "NO"
    
    # Check problem statement and fig position
    prob = re.search(r'<div class="problem-statement">([\s\S]*?)</div>', block)
    prob_len = len(prob.group(1)) if prob else 0
    
    # Check if figure is immediately after problem-statement
    fig_after_prob = False
    if prob:
        prob_end = block.find('</div>', block.find('<div class="problem-statement">')) + 6
        after_prob = block[prob_end:].strip()
        if after_prob.startswith('<div class="fig-container'):
            fig_after_prob = True
            
    print(f"[{idx+1}] {h3_text} | Fig present: {fig_text} | Fig immediately after prob: {fig_after_prob}")
