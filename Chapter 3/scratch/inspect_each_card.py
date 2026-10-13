import sys
import re

with open('chapter3.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Split content by <div class="example-card">
cards = content.split('<div class="example-card">')

print(f"Number of cards: {len(cards)-1}")

for i in range(1, len(cards)):
    card = cards[i]
    # find title
    h3_m = re.search(r'<h3>(.*?)</h3>', card)
    title = h3_m.group(1).encode('ascii', 'replace').decode('ascii') if h3_m else "Unknown"
    
    # check problem-statement
    prob_m = re.search(r'<div class="problem-statement">([\s\S]*?)</div>', card)
    
    # check if fig-container is directly after problem-statement
    has_fig_after = False
    fig_match = None
    if prob_m:
        prob_end = prob_m.end()
        after = card[prob_end:].strip()
        if after.startswith('<div class="fig-container'):
            has_fig_after = True
            # find end of fig container: </div>\s*</div>
            fig_end_m = re.search(r'<div class="fig-container[^"]*">[\s\S]*?</div>\s*</div>', after)
            if fig_end_m:
                fig_match = fig_end_m.group(0)[:60]
                
    print(f"Card {i}: {title}")
    print(f"   prob_m: {'YES' if prob_m else 'NO'} | fig directly after: {has_fig_after} | {fig_match}")
