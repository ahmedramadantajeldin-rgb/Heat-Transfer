import sys
import re

with open('chapter3.html', 'r', encoding='utf-8') as f:
    content = f.read()

examples_to_check = ['3–5', '3–6', '3–7', '3–8', '3–9', '3–10', '3–11', '3–12', '3–13', '3–18', '3–19']

out = []
for ex_num in examples_to_check:
    out.append(f"\n{'='*30} EXAMPLE {ex_num} {'='*30}\n")
    pattern = rf'(<div class="example-card">[\s\S]*?<h3>Example {ex_num}:[\s\S]*?)(?=<div class="example-card">|</section>)'
    m = re.search(pattern, content)
    if m:
        text = m.group(0).strip()
        out.append(text)
    else:
        out.append(f"NOT FOUND: Example {ex_num}")

with open('scratch/target_examples_utf8.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

print("Wrote scratch/target_examples_utf8.txt successfully.")
