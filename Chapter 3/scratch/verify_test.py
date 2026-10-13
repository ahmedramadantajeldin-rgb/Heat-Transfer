import sys
import re
from html.parser import HTMLParser

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/test_chapter3.html', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
print(f"Total lines: {len(lines)}")
print(f"Total size: {len(content)} bytes")

# 1. Count proof-box
proof_boxes = list(re.finditer(r'<div class="proof-box">', content))
print(f"proof-box count: {len(proof_boxes)}")
for i, pb in enumerate(proof_boxes):
    snippet = content[pb.start():pb.start()+250]
    m_id = re.search(r'id="(proof-[^"]+)"', snippet)
    proof_id = m_id.group(1) if m_id else "No ID"
    print(f"  Proof {i+1}: {proof_id}")

# 2. Count example-problem-layout
ex_layouts = list(re.finditer(r'<div class="example-problem-layout">', content))
print(f"\nexample-problem-layout count: {len(ex_layouts)}")

# 3. Count sol-toggle
sol_toggles = list(re.finditer(r'class="sol-toggle"', content))
print(f"\nsol-toggle count: {len(sol_toggles)}")

# 4. Count task-check buttons
tasks = list(re.finditer(r'class="task-check"', content))
print(f"\ntask-check count: {len(tasks)}")

# 5. Check titles of 3-7, 3-8, 3-9
for ex_title in [
    'Example 3–7: Heat Transfer to a Spherical Container',
    'Example 3–8: Heat Loss through an Insulated Steam Pipe',
    'Example 3–9: Heat Loss from an Insulated Electric Wire'
]:
    if ex_title in content:
        print(f"Title verified: '{ex_title}'")
    else:
        print(f"ERROR: Title missing: '{ex_title}'")

# 6. Check Example 3-13 Step 4/5 content
if '0.353' in content and '0.3482' in content:
    print("Example 3-13 calculation verified: contains 0.353 and 0.3482")
else:
    print("ERROR: Example 3-13 calculation missing 0.353 or 0.3482")

# 7. Check Example 3-5 content
if '42,000' in content or '42{,}000' in content:
    print("Example 3-5 h_c verified")
if '4.032' in content or '4.03235' in content:
    print("Example 3-5 R_total verified")

# 8. Check Example 3-6 content
if '6.873' in content and '262' in content:
    print("Example 3-6 R_total and Q_total verified")

# 9. HTML Tag Balance Check using HTMLParser
print("\nRunning HTMLParser balance check...")
class TagChecker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.void_tags = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
        self.errors = []
        
    def handle_starttag(self, tag, attrs):
        if tag not in self.void_tags:
            self.stack.append(tag)
            
    def handle_endtag(self, tag):
        if tag in self.void_tags:
            return
        if not self.stack:
            self.errors.append(f"Unexpected end tag </{tag}> with empty stack")
            return
        last = self.stack.pop()
        if last != tag:
            self.errors.append(f"Mismatched end tag: expected </{last}>, got </{tag}>")

checker = TagChecker()
try:
    checker.feed(content)
    print(f"HTMLParser completed. Errors: {len(checker.errors)}")
    if checker.errors:
        print("First 5 errors:")
        for e in checker.errors[:5]:
            print(" ", e)
    else:
        print("No mismatched tags found!")
    if checker.stack:
        print(f"Unclosed tags count: {len(checker.stack)}")
        print("Unclosed tags remaining on stack:", checker.stack[-10:])
    else:
        print("All tags cleanly closed!")
except Exception as ex:
    print("Parser error:", ex)
