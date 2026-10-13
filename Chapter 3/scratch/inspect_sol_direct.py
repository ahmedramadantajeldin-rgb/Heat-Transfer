import sys
import re

with open('chapter3.html', 'r', encoding='utf-8') as f:
    content = f.read()

out = []
def show_example(ex_id):
    m = re.search(rf'<button[^>]+aria-controls="{ex_id}"[\s\S]*?</section>', content)
    if not m:
        m = re.search(rf'<button[^>]+aria-controls="{ex_id}"[\s\S]*?(?=<div class="example-card">)', content)
    if m:
        text = m.group(0)
        wrap_start = text.find(f'id="{ex_id}"')
        out.append(f"=== {ex_id} ===")
        out.append(text[wrap_start:wrap_start+2500])
        out.append("...\n\n")

for ex_id in ['sol-ex3-5', 'sol-ex3-6', 'sol-ex3-7', 'sol-ex3-8', 'sol-ex3-9', 'sol-ex3-10', 'sol-ex3-11', 'sol-ex3-12', 'sol-ex3-13', 'sol-ex3-18', 'sol-ex3-19']:
    show_example(ex_id)

with open('scratch/direct_sols.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

print("Wrote scratch/direct_sols.txt")
