import re

with open(r"C:\Users\ahmed\Documents\GitHub\Heat-Transfer\Chapter 3\chapter3.html", "r", encoding="utf-8") as f:
    content = f.read()

# Add progress bar and banner after </header>
progress_html = """
<!-- Task Progress -->
<div class="task-progress-wrapper">
  <div class="task-progress-bar">
    <div class="task-progress-fill" id="progressFill"></div>
  </div>
  <div class="task-progress-text" id="progressText">0 / 14 Tasks</div>
</div>

<!-- Chapter Complete Banner (hidden by default) -->
<div class="chapter-complete-banner" id="chapterBanner" style="display:none;">
  <div class="banner-content">
    <span class="banner-emoji">🏆</span>
    <h2>Chapter 3 Completed!</h2>
    <p>خلصت Chapter 3! عاش عليك! 🎉</p>
  </div>
</div>
"""
content = content.replace("</header>", "</header>\n" + progress_html)

# Add task buttons to each section sec1 through sec14
for i in range(1, 15):
    btn_html = f"""
<button class="task-check" data-task="sec{i}" aria-label="Mark as completed" title="أكمل المهمة">
  <svg class="check-svg" viewBox="0 0 24 24" width="28" height="28"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/><path class="check-path" d="M7 12.5l3 3 7-7" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
  <span class="task-label">Task <span class="task-num">{i}</span></span>
</button>"""
    
    # We want to insert btn_html after the closing </div> of <div class="section-titles"> within each <section id="secX">
    # We can match the start of the section up to the closing </div> of section-titles.
    pattern = re.compile(rf'(<section class="section" id="sec{i}">.*?<div class="section-titles">.*?</div>)', re.DOTALL)
    
    # Replace the matched part by appending the button
    content = pattern.sub(rf'\1{btn_html}', content, count=1)

with open(r"C:\Users\ahmed\Documents\GitHub\Heat-Transfer\Chapter 3\chapter3.html", "w", encoding="utf-8") as f:
    f.write(content)
print("HTML updated successfully.")
