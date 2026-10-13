import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('chapter3.html', 'r', encoding='utf-8') as f:
    content = f.read()

for word in ['Assumptions', 'Properties', 'Analysis']:
    matches = [m.start() for m in re.finditer(word, content)]
    print(f"'{word}' found {len(matches)} times")
    for pos in matches[:5]:
        snippet = content[max(0, pos-40):pos+80].replace('\n', ' ')
        print(f"  {snippet}")
