import re

with open("chapter3.html", "r", encoding="utf-8") as f:
    text = f.read()

matches = list(re.finditer(r"<!-- ===== EXAMPLE ([\d-]+) ===== -->", text))
for i, m in enumerate(matches):
    start = m.start()
    end = matches[i+1].start() if i+1 < len(matches) else text.find("</main>", start)
    chunk = text[start:end]
    ex_num = m.group(1)
    
    div_open = len(re.findall(r"<div\b", chunk))
    div_close = len(re.findall(r"</div\b", chunk))
    layout_open = len(re.findall(r"example-problem-layout", chunk))
    fig_count = len(re.findall(r"fig-container", chunk))
    
    print(f"Ex {ex_num:5s}: opens={div_open:2d}, closes={div_close:2d}, layout={layout_open}, figs={fig_count}, diff={div_open - div_close:2d}")
