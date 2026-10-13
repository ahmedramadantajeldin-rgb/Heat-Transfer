import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('chapter3.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's find all example cards:
cards = re.split(r'(<div class="example-card">)', content)

# cards[0] is preamble before first card
out = []
for i in range(1, len(cards), 2):
    card_header = cards[i]
    card_body = cards[i+1]
    # find the end of this example card (first </div>\s*</div> that closes example-body and example-card, or before next example-card/section)
    # let's extract the h3
    h3_m = re.search(r'<h3>(.*?)</h3>', card_body)
    title = h3_m.group(1) if h3_m else "Unknown"
    
    # Let's see if there is a fig-container
    has_fig = '<div class="fig-container' in card_body[:1000]
    
    # Let's find sol-wrap
    has_sol = 'class="sol-wrap"' in card_body
    
    out.append(f"Title: {title}\nHas Fig early: {has_fig}\nHas Sol: {has_sol}\nFirst 500 chars:\n{card_body[:500]}\n" + "-"*50)

with open('scratch/examples_summary.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

print(f"Summarized {len(out)} examples to scratch/examples_summary.txt")
