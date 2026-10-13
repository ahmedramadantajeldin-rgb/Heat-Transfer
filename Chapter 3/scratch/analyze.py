import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('chapter3.html', 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.splitlines()

print('Total lines:', len(lines))
print('Total length:', len(content))

print("\n--- EXAMPLES ---")
for i, line in enumerate(lines):
    if '<div class="example-card">' in line:
        snippet = '\n'.join(lines[i:i+6])
        print(f"Line {i+1}:")
        for subline in lines[i:i+4]:
            print(f"  {subline}")

print("\n--- DERIV TOGGLES ---")
for i, line in enumerate(lines):
    if 'deriv-toggle' in line:
        print(f"Line {i+1}: {line.strip()}")

for i, line in enumerate(lines):
    if '</style>' in line:
        print(f"\n</style> at line {i+1}")

last_script = None
for i, line in enumerate(lines):
    if '</script>' in line:
        last_script = i+1
print(f"Last </script> at line {last_script}")
