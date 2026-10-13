import re

with open('chapter3.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern matching deriv block:
pattern = r'(<!--[^\n]*Derivation[^\n]*-->\s*)?<div class="deriv-toggle-row">[\s\S]*?<button[^>]+aria-controls="([^"]+)"[\s\S]*?</button>\s*</div>\s*<div class="deriv-wrap" id="\2">\s*<div class="deriv-inner">([\s\S]*?)</div>\s*</div>'

matches = list(re.finditer(pattern, content))
print(f"Matched {len(matches)} derivation blocks using full pattern")

for i, m in enumerate(matches):
    deriv_id = m.group(2)
    comment = m.group(1) or ""
    inner = m.group(3)
    print(f"[{i+1}] ID: {deriv_id} | comment: {comment.strip()} | inner len: {len(inner)}")
