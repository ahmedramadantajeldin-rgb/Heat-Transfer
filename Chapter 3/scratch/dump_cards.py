import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('chapter3.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's extract each example card accurately
cards = re.split(r'(<div class="example-card">)', content)

for i in range(1, len(cards), 2):
    card_html = cards[i] + cards[i+1]
    # find where the card ends - before the next <div class="example-card"> or </section>
    # Actually let's just find the closing tags:
    # A card has:
    # <div class="example-card">
    #   <div class="example-header">...</div>
    #   <div class="example-body">
    #     ...
    #   </div>
    # </div>
    # Let's find title
    h3_m = re.search(r'<h3>(.*?)</h3>', card_html)
    title = h3_m.group(1) if h3_m else f"Example_{i}"
    clean_title = re.sub(r'[^\w\d–-]', '_', title)[:40]
    
    with open(f'scratch/{clean_title}.html', 'w', encoding='utf-8') as f_out:
        f_out.write(card_html)

print("Dumped all example cards.")
