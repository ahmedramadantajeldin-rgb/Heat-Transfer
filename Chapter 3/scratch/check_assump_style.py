import re

with open('chapter3.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search inside example 3-1, 3-2, 3-3, 3-4, 3-18 for Assumptions or Properties
for ex in ['sol-ex3-1', 'sol-ex3-2', 'sol-ex3-3', 'sol-ex3-4', 'sol-ex3-18']:
    m = re.search(rf'id="{ex}"[\s\S]*?</div>\s*</div>\s*</div>', content)
    if m:
        text = m.group(0)
        has_assump = 'Assumptions' in text
        has_prop = 'Properties' in text
        print(f"{ex}: Assumptions={has_assump}, Properties={has_prop}")
        if has_assump:
            # print assumption snippet
            idx = text.find('Assumptions')
            print("  Assump snippet:\n" + text[max(0, idx-50):idx+300])
        if has_prop:
            idx = text.find('Properties')
            print("  Prop snippet:\n" + text[max(0, idx-50):idx+300])
