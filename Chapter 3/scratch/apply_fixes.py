import sys

with open("chapter3.html", "r", encoding="utf-8") as f:
    text = f.read()

# Marker 1: Cylindrical Derivation in Sec 9
m1_start = '<h3 style="color:var(--navy);font-family:\'Playfair Display\',serif;margin:24px 0 12px;">Derivation of the Cylindrical Conduction Equation</h3>'
m1_end = '<div class="formula-box">\n<div class="box-label">Heat Transfer Through a Cylindrical Layer — Eq. 3-35</div>\n<div class="equation-scroll" style="direction:ltr;">\n\\[ \\dot{Q}_{cyl} = \\frac{2\\pi L k\\,(T_1 - T_2)}{\\ln(r_2/r_1)} \\qquad (W) \\tag{3-35} \\]\n</div>\n</div>'

idx1_start = text.find(m1_start)
idx1_end = text.find(m1_end, idx1_start) + len(m1_end)
print(f"Sec 9 deriv 1 found at [{idx1_start}:{idx1_end}]")
assert idx1_start != -1 and idx1_end != -1

cyl_inner = text[idx1_start + len(m1_start):text.find(m1_end, idx1_start)].strip()

part1 = '''<div class="proof-box">
<div class="proof-header">
  <button type="button" class="proof-toggle-btn" aria-expanded="false" aria-controls="proof-cyl-conduction">
    <span class="proof-label">عرض الإثبات</span>
    <span class="proof-arrow" aria-hidden="true">▼</span>
  </button>
  <span class="proof-notice">للفهم والتعمق فقط — ليس مطلوبًا للحفظ</span>
</div>
<div class="proof-body" id="proof-cyl-conduction">
<div class="proof-body-inner">

'''
part2 = '''

<div class="equation-scroll" style="direction:ltr;">
\\[ \\dot{Q}_{cyl} = \\frac{2\\pi L k\\,(T_1 - T_2)}{\\ln(r_2/r_1)} \\qquad (W) \\tag{3-35} \\]
</div>

</div>
</div>
</div>
'''

new_sec9_deriv1 = m1_start + '\n\n' + part1 + cyl_inner + part2 + '\n' + m1_end

# Marker 2: Spherical Derivation in Sec 9
m2_start = '<h3 style="color:var(--navy);font-family:\'Playfair Display\',serif;margin:24px 0 12px;">Single Spherical Layer</h3>'
m2_end = '<div class="formula-box">\n<div class="box-label">Heat Transfer Through a Spherical Layer — Eq. 3-38</div>\n<div class="equation-scroll" style="direction:ltr;">\n\\[ \\dot{Q}_{sph} = \\frac{4\\pi k\\, r_1 r_2\\,(T_1 - T_2)}{r_2 - r_1} \\qquad (W) \\tag{3-38} \\]\n</div>\n</div>'

idx2_start = text.find(m2_start)
idx2_end = text.find(m2_end, idx2_start) + len(m2_end)
print(f"Sec 9 deriv 2 found at [{idx2_start}:{idx2_end}]")
assert idx2_start != -1 and idx2_end != -1

sph_inner = text[idx2_start + len(m2_start):text.find(m2_end, idx2_start)].strip()

part3 = '''<div class="proof-box">
<div class="proof-header">
  <button type="button" class="proof-toggle-btn" aria-expanded="false" aria-controls="proof-sph-conduction">
    <span class="proof-label">عرض الإثبات</span>
    <span class="proof-arrow" aria-hidden="true">▼</span>
  </button>
  <span class="proof-notice">للفهم والتعمق فقط — ليس مطلوبًا للحفظ</span>
</div>
<div class="proof-body" id="proof-sph-conduction">
<div class="proof-body-inner">

'''
part4 = '''

<div class="equation-scroll" style="direction:ltr;">
\\[ \\dot{Q}_{sph} = \\frac{4\\pi k\\, r_1 r_2\\,(T_1 - T_2)}{r_2 - r_1} \\qquad (W) \\tag{3-38} \\]
</div>

</div>
</div>
</div>
'''

intro_sph = '<p>نأخذ <span class="term">spherical shell</span> نصف قطريه \\(r_1\\) و\\(r_2\\) ومعامل توصيله \\(k\\) ودرجتي حرارة سطحيه \\(T_1\\) و\\(T_2\\) (المقطع في Figure 3–24 يمثل الحالتين).</p>\n\n'
new_sec9_deriv2 = m2_start + '\n' + intro_sph + part3 + sph_inner + part4 + '\n' + m2_end

# Marker 3: Example 3-11 & Example 3-13
ex11_card_open = '<!-- ===== EXAMPLE 3-11 ===== -->\n<div class="example-card">\n<div class="example-header"><h3>Example 3–11: Selecting a Heat Sink for a Transistor</h3></div>\n<div class="example-body">\n<div class="example-problem-layout">'
assert ex11_card_open in text, "ex11_card_open not matched"

ex11_card_open_fixed = '<!-- ===== EXAMPLE 3-11 ===== -->\n<div class="example-card">\n<div class="example-header"><h3>Example 3–11: Selecting a Heat Sink for a Transistor</h3></div>\n<div class="example-body">'

ex11_end_and_ex13_open = """</div></div>
</div>
</div>

<!-- ===== EXAMPLE 3-13 ===== -->
<div class="example-card">
<div class="example-header"><h3>Example 3–13: Preventing Circuit Board Overheating</h3></div>
<div class="example-body">
<div class="problem-statement">"""

ex11_end_and_ex13_open_fixed = """</div></div>
</div>
</div>

<!-- ===== EXAMPLE 3-13 ===== -->
<div class="example-card">
<div class="example-header"><h3>Example 3–13: Preventing Circuit Board Overheating</h3></div>
<div class="example-body">
<div class="example-problem-layout">
<div class="problem-statement">"""

assert ex11_end_and_ex13_open in text, "ex11_end_and_ex13_open not matched"

# In Example 3-4 and Example 3-5:
ex4_and_ex5_old = """<!-- ===== EXAMPLE 3-4 ===== -->
<div class="example-card">
<div class="example-header"><h3>Example 3–4: Equivalent Thickness for Contact Resistance</h3></div>
<div class="example-body">
<div class="example-problem-layout">
<div class="problem-statement">"""

ex4_and_ex5_fixed = """<!-- ===== EXAMPLE 3-4 ===== -->
<div class="example-card">
<div class="example-header"><h3>Example 3–4: Equivalent Thickness for Contact Resistance</h3></div>
<div class="example-body">
<div class="problem-statement">"""
assert ex4_and_ex5_old in text, "ex4_and_ex5_old not matched"

ex5_open_old = """<!-- ===== EXAMPLE 3-5 ===== -->
<div class="example-card">
<div class="example-header"><h3>Example 3–5: Contact Resistance of Transistors</h3></div>
<div class="example-body">
<div class="problem-statement">"""

ex5_open_fixed = """<!-- ===== EXAMPLE 3-5 ===== -->
<div class="example-card">
<div class="example-header"><h3>Example 3–5: Contact Resistance of Transistors</h3></div>
<div class="example-body">
<div class="example-problem-layout">
<div class="problem-statement">"""
assert ex5_open_old in text, "ex5_open_old not matched"

# Perform replacements
text = text.replace(ex11_card_open, ex11_card_open_fixed, 1)
text = text.replace(ex11_end_and_ex13_open, ex11_end_and_ex13_open_fixed, 1)
text = text.replace(ex4_and_ex5_old, ex4_and_ex5_fixed, 1)
text = text.replace(ex5_open_old, ex5_open_fixed, 1)

# Now replace sec 9 derivations
idx2_start = text.find(m2_start)
idx2_end = text.find(m2_end, idx2_start) + len(m2_end)
text = text[:idx2_start] + new_sec9_deriv2 + text[idx2_end:]

idx1_start = text.find(m1_start)
idx1_end = text.find(m1_end, idx1_start) + len(m1_end)
text = text[:idx1_start] + new_sec9_deriv1 + text[idx1_end:]

with open("chapter3.html", "w", encoding="utf-8") as f:
    f.write(text)

print("All replacements done successfully!")
