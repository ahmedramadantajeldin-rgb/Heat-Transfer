import re

with open('chapter3.html', 'r', encoding='utf-8') as f:
    content = f.read()

matches = re.findall(r'deriv-[a-zA-Z0-9_-]+', content)
print("Unique deriv- matches:", set(matches))
for m in set(matches):
    count = content.count(m)
    print(f"  {m}: {count} occurrences")
