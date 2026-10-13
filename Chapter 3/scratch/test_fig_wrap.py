import re

with open('chapter3.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern strictly within a single example-card:
pattern = r'(<div class="example-card">(?:(?!<div class="example-card">)[\s\S])*?<div class="example-body">\s*)(<div class="problem-statement">[\s\S]*?</div>)\s*(<div class="fig-container[^"]*">[\s\S]*?</div>\s*</div>)'

matches = list(re.finditer(pattern, content))
print(f"Strict matched {len(matches)} example problem+fig pairs!")

for i, m in enumerate(matches):
    chunk = m.group(0)
    h3 = re.search(r'<h3>(.*?)</h3>', chunk)
    title = h3.group(1) if h3 else "Unknown"
    fig_class = re.search(r'class="(fig-container[^"]*)"', m.group(3)).group(1)
    print(f"[{i+1}] {title} | {fig_class}")
