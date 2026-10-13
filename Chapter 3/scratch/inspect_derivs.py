import re

with open('chapter3.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all deriv-toggle-row or deriv-toggle
# In our earlier check:
# Line 2507: deriv-fin-eq
# Line 2698: deriv-qlong
# Line 2770: deriv-adiabatic-temp
# Line 2835: deriv-adiabatic-q
# Line 2895: deriv-specified-temp
# Line 3005: deriv-convection-tip
# Line 3119: deriv-eta-long
# Line 3145: deriv-eta-adiabatic
# Line 3364: deriv-eta-eps
# Line 3401: deriv-eps-long
# Line 3487: deriv-eps-overall
# Line 4078: deriv-effective-emissivity

# Let's inspect each match:
matches = list(re.finditer(r'<div class="deriv-toggle-row">([\s\S]*?)</div>\s*<div class="deriv-wrap" id="([^"]+)">\s*<div class="deriv-inner">([\s\S]*?)</div>\s*</div>', content))

print(f"Regex matched: {len(matches)} deriv blocks")

for i, m in enumerate(matches):
    button_part = m.group(1).strip()
    deriv_id = m.group(2).strip()
    inner_len = len(m.group(3))
    print(f"[{i+1}] ID: {deriv_id} | inner len: {inner_len} | button:\n{button_part}")
