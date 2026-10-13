import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/target_examples_utf8.txt', 'r', encoding='utf-8') as f:
    text = f.read()

parts = text.split('='*30)
# parts alternate between blank/header and content
for i in range(1, len(parts), 2):
    header = parts[i].strip()
    content = parts[i+1].strip()
    print(f"\n>>> {header} <<<")
    # print first 5 lines and last 5 lines, plus total line count
    lines = content.splitlines()
    print(f"Lines count: {len(lines)}")
    print("--- First 15 lines ---")
    for l in lines[:15]:
        print(l)
    print("--- Last 10 lines ---")
    for l in lines[-10:]:
        print(l)
