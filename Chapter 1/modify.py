import re
import sys

html_path = r"C:\Users\ahmed\Documents\GitHub\Heat-Transfer\Chapter 1\chapter1.html"

with open(html_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_section_header = False
sec_num = None

i = 0
while i < len(lines):
    line = lines[i]
    new_lines.append(line)
    
    sec_match = re.search(r'<section class="section" id="sec(\d+)">', line)
    if sec_match:
        sec_num = int(sec_match.group(1))
        in_section_header = True
        
    if in_section_header and sec_num is not None and sec_num <= 17:
        if '<div class="section-title-group">' in line:
            # Read forward until closing </div>
            while True:
                i += 1
                if i >= len(lines):
                    break
                next_line = lines[i]
                new_lines.append(next_line)
                if '</div>' in next_line:
                    # Found closing div for section-title-group
                    # Insert the button exactly here
                    button_html = f"""<button class="task-check" data-task="sec{sec_num}" aria-label="Mark as completed" title="أكمل المهمة">
  <svg class="check-svg" viewBox="0 0 24 24" width="28" height="28"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/><path class="check-path" d="M7 12.5l3 3 7-7" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
  <span class="task-label">Task <span class="task-num">{sec_num}</span></span>
</button>
"""
                    new_lines.append(button_html)
                    in_section_header = False
                    sec_num = None
                    break
    
    i += 1

with open(html_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Done")
