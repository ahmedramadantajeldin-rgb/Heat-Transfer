# -*- coding: utf-8 -*-
"""
Script to enhance chapter3.html according to instructions:
1. Injects CSS for proof-box and example-problem-layout before </style>
2. Converts all 12 deriv-toggle derivations to proof-box (hidden by default)
3. Injects JS for proof-box toggle before last </script>
4. Updates example titles and full solutions for Examples 3-5, 3-6, 3-7, 3-8, 3-9, 3-10, 3-11, 3-13
5. Wraps problem-statement + fig-container in .example-problem-layout for all 11 examples with figures
"""

import re
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

FILE_PATH = 'scratch/test_chapter3.html'
BAK_PATH = 'scratch/test_chapter3.html.bak'

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

orig_len = len(html)
orig_lines = len(html.splitlines())
print(f"Original size: {orig_len} bytes, {orig_lines} lines")

# Ensure backup exists
if not os.path.exists(BAK_PATH):
    with open(BAK_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Backup created at chapter3.html.bak")

# ==============================================================================
# 1. INJECT CSS BEFORE </style>
# ==============================================================================
CSS_INJECTION = """
/* ===== PROOF TOGGLE — hidden by default ===== */
.proof-box {
  background: linear-gradient(135deg, #f8f4ff, #ede8ff);
  border-right: 5px solid #7c3aed;
  border-radius: var(--radius);
  margin: 16px 0;
  overflow: hidden;
}
.proof-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 18px;
  cursor: pointer;
  user-select: none;
}
.proof-toggle-btn {
  display: inline-flex; align-items: center; gap: 8px;
  background: #7c3aed; color: #fff;
  border: none; border-radius: 999px;
  padding: 7px 16px; cursor: pointer;
  font-family: 'Cairo', sans-serif;
  font-size: 0.85rem; font-weight: 700;
  transition: background .2s;
}
.proof-toggle-btn:hover { background: #5b21b6; }
.proof-toggle-btn .proof-arrow { display: inline-block; font-size: 0.8em; transition: transform .3s; }
.proof-toggle-btn[aria-expanded="true"] .proof-arrow { transform: rotate(180deg); }
.proof-notice {
  font-family: 'Cairo', sans-serif;
  font-size: 0.82rem; color: #5b21b6;
  font-weight: 600;
  flex: 1;
}
.proof-body {
  display: grid;
  grid-template-rows: 0fr;
  opacity: 0;
  visibility: hidden;
  transition: grid-template-rows .4s ease, opacity .3s ease, visibility 0s linear .4s;
  padding: 0 18px;
}
.proof-body.is-open {
  grid-template-rows: 1fr;
  opacity: 1;
  visibility: visible;
  padding: 0 18px 18px;
  transition: grid-template-rows .4s ease, opacity .35s ease .05s, visibility 0s;
}
.proof-body-inner { min-height: 0; overflow: hidden; }
.proof-body.is-open .proof-body-inner { overflow: visible; }
@media print {
  .proof-header { display: none !important; }
  .proof-body { grid-template-rows: 1fr !important; opacity: 1 !important; visibility: visible !important; padding: 0 18px 18px !important; transition: none !important; }
  .proof-body-inner { overflow: visible !important; }
}

/* ===== EXAMPLE FIGURE LAYOUT ===== */
.example-problem-layout {
  display: flex;
  gap: 20px;
  align-items: flex-start;
  margin-bottom: 16px;
}
.example-problem-layout .problem-statement {
  flex: 1;
  min-width: 0;
  margin-bottom: 0;
}
.example-problem-layout .fig-container {
  flex: 0 0 auto;
  width: 200px;
  margin: 0;
}
.example-problem-layout .fig-container img {
  max-width: 100%;
  height: auto;
}
@media (max-width: 600px) {
  .example-problem-layout { flex-direction: column; }
  .example-problem-layout .fig-container { width: 100%; max-width: 300px; margin: 0 auto; }
}
"""

if '.proof-box {' not in html:
    style_pos = html.find('</style>')
    if style_pos != -1:
        html = html[:style_pos] + CSS_INJECTION + "\n" + html[style_pos:]
        print("Injected CSS before </style>")
    else:
        print("ERROR: </style> not found!")
else:
    print("CSS already present.")

# ==============================================================================
# 2. CONVERT DERIVATION TOGGLES TO PROOF-BOX SYSTEM
# ==============================================================================
# Each deriv block has:
# <div class="deriv-toggle-row">...<button ... aria-controls="deriv-(.*?)">...</button></div>
# <div class="deriv-wrap" id="deriv-\1"><div class="deriv-inner">...</div></div>

deriv_pattern = re.compile(
    r'<div class="deriv-toggle-row">[\s\S]*?<button[^>]+aria-controls="deriv-([^"]+)"[\s\S]*?</button>\s*</div>\s*<div class="deriv-wrap" id="deriv-\1">\s*<div class="deriv-inner">([\s\S]*?)</div>\s*</div>'
)

def deriv_repl(match):
    deriv_id = match.group(1)
    inner_content = match.group(2)
    proof_id = f"proof-{deriv_id}"
    return (
        f'<div class="proof-box">\n'
        f'<div class="proof-header">\n'
        f'  <button type="button" class="proof-toggle-btn" aria-expanded="false" aria-controls="{proof_id}">\n'
        f'    <span class="proof-label">عرض الإثبات</span>\n'
        f'    <span class="proof-arrow" aria-hidden="true">▼</span>\n'
        f'  </button>\n'
        f'  <span class="proof-notice">للفهم والتعمق فقط — ليس مطلوبًا للحفظ</span>\n'
        f'</div>\n'
        f'<div class="proof-body" id="{proof_id}">\n'
        f'<div class="proof-body-inner">\n'
        f'{inner_content}\n'
        f'</div>\n'
        f'</div>\n'
        f'</div>'
    )

deriv_count = len(deriv_pattern.findall(html))
print(f"Found {deriv_count} deriv-toggle blocks to convert")
html = deriv_pattern.sub(deriv_repl, html)
print(f"Converted {deriv_count} derivations to proof-box")

# ==============================================================================
# 3. INJECT JS FOR PROOF TOGGLE SYSTEM BEFORE LAST </script>
# ==============================================================================
JS_INJECTION = """
// ===== PROOF TOGGLE SYSTEM (hidden by default) =====
(function(){
  document.querySelectorAll('.proof-toggle-btn').forEach(function(btn){
    var body = document.getElementById(btn.getAttribute('aria-controls'));
    var arrow = btn.querySelector('.proof-arrow');
    if(!body) return;
    function toggleProof(){
      var isOpen = btn.getAttribute('aria-expanded') === 'true';
      if(isOpen){
        btn.setAttribute('aria-expanded','false');
        body.classList.remove('is-open');
        if(arrow) arrow.textContent = '\\u25BC';
        btn.querySelector('.proof-label').textContent = '\\u0639\\u0631\\u0636 \\u0627\\u0644\\u0625\\u062b\\u0628\\u0627\\u062a';
      } else {
        btn.setAttribute('aria-expanded','true');
        body.classList.add('is-open');
        if(arrow) arrow.textContent = '\\u25B2';
        btn.querySelector('.proof-label').textContent = '\\u0625\\u062E\\u0641\\u0627\\u0621 \\u0627\\u0644\\u0625\\u062B\\u0628\\u0627\\u062A';
        // Re-typeset MathJax if present
        if(typeof MathJax !== 'undefined' && MathJax.typesetPromise) {
          MathJax.typesetPromise([body]);
        }
      }
    }
    btn.addEventListener('click', function(e){
      e.stopPropagation();
      toggleProof();
    });
    var header = btn.closest('.proof-header');
    if(header){
      header.addEventListener('click', function(e){
        if(e.target !== btn && !btn.contains(e.target)){
          toggleProof();
        }
      });
    }
  });
})();
"""

if 'PROOF TOGGLE SYSTEM' not in html:
    last_script_pos = html.rfind('</script>')
    if last_script_pos != -1:
        html = html[:last_script_pos] + JS_INJECTION + "\n" + html[last_script_pos:]
        print("Injected proof-toggle JS before last </script>")
    else:
        print("ERROR: </script> not found!")
else:
    print("Proof toggle JS already present.")

# ==============================================================================
# 4. WRAP PROBLEM-STATEMENT + FIG-CONTAINER IN .example-problem-layout
# ==============================================================================
# Pattern for example-card where problem-statement is immediately followed by fig-container
# Make sure we don't double wrap if already wrapped
prob_fig_pattern = re.compile(
    r'(<div class="example-body">\s*)'
    r'(<div class="problem-statement">[\s\S]*?</div>)\s*'
    r'(<div class="fig-container[^"]*">[\s\S]*?</div>\s*</div>)'
)

def prob_fig_repl(m):
    ex_body = m.group(1)
    prob_stmt = m.group(2)
    fig_cont = m.group(3)
    return (
        f'{ex_body}'
        f'<div class="example-problem-layout">\n'
        f'{prob_stmt}\n'
        f'{fig_cont}\n'
        f'</div>'
    )

wrap_count = len(prob_fig_pattern.findall(html))
print(f"Found {wrap_count} examples with figure immediately after problem-statement")
html = prob_fig_pattern.sub(prob_fig_repl, html)
print(f"Wrapped {wrap_count} examples in .example-problem-layout")

# ==============================================================================
# 5. UPDATE EXAMPLES WITH FULL SOLUTIONS
# ==============================================================================

# Helper function to replace sol-inner of a specific sol_id
def replace_sol_inner(content, sol_id, new_sol_inner_content):
    pattern = rf'(<div class="sol-wrap" id="{sol_id}">\s*<div class="sol-inner">)[\s\S]*?(</div>\s*</div>\s*</div>\s*(?:<!--|$|\n|<section|<div class="example-card">))'
    # Wait, the closing of sol-wrap is </div></div>, followed by example-card closing </div>
    # Let's match:
    # <div class="sol-wrap" id="{sol_id}">\s*<div class="sol-inner">
    # ...
    # </div>\s*</div>
    pattern2 = rf'(<div class="sol-wrap" id="{sol_id}">\s*<div class="sol-inner">)[\s\S]*?(</div>\s*</div>)'
    m = re.search(pattern2, content)
    if not m:
        raise ValueError(f"Could not find sol-wrap for {sol_id}")
    
    # Check if there are nested divs inside sol-inner
    # sol-inner starts at m.start(1) + len(m.group(1))
    start_inner = m.start(1) + len(m.group(1))
    # We want to find the matching closing </div></div> that closes sol-inner and sol-wrap
    # In the file, the structure is:
    # <div class="sol-wrap" id="...">
    # <div class="sol-inner">
    # ...
    # </div></div>
    # </div>  (closes example-body)
    # </div>  (closes example-card)
    # Let's find `</div></div>` specifically for this sol_wrap
    end_marker = '</div></div>'
    # search after start_inner
    # Let's find next occurrence of `<div class="example-card">` or `</section>`
    next_card = content.find('<div class="example-card">', start_inner)
    next_sec = content.find('</section>', start_inner)
    end_limit = min([x for x in [next_card, next_sec, len(content)] if x != -1])
    
    # Inside this window, find the last `</div></div>`
    window = content[start_inner:end_limit]
    # find all occurrences of `</div></div>` in window
    last_dd = window.rfind('</div></div>')
    if last_dd == -1:
        # fallback to regex
        last_dd = window.rfind('</div>\n</div>')
    
    if last_dd == -1:
        raise ValueError(f"Could not find closing </div></div> for {sol_id}")
    
    actual_end = start_inner + last_dd
    
    new_chunk = content[:start_inner] + "\n" + new_sol_inner_content.strip() + "\n" + content[actual_end:]
    return new_chunk

# --- EXAMPLE 3-5 ---
SOL_EX3_5 = """<div class="given-section">
<h4>Given</h4>
<div class="given-grid">
<span>\(L_{\\text{plate}} = 0.01\\;\\text{m}\)</span>
<span>\(k_{\\text{Cu}} = 386\\;\\text{W/m}\\cdot\\text{K}\)</span>
<span>\(A_c = 8\\;\\text{cm}^2 = 8 \\times 10^{-4}\\;\\text{m}^2\)</span>
<span>\(A_p = (0.10)(0.10) = 0.01\\;\\text{m}^2\)</span>
<span>\(h_c = 42{,}000\\;\\text{W/m}^2\\cdot\\text{K}\)</span>
<span>\(h = 25\\;\\text{W/m}^2\\cdot\\text{K}\)</span>
<span>\(T_{\\text{case}} \\le 70^\\circ\\text{C},\\; T_\\infty = 20^\\circ\\text{C}\)</span>
</div>
</div>

<div class="note-box" style="margin:12px 0;">
<div class="note-title">📝 Assumptions</div>
<ol style="margin:6px 0 0;padding-right:20px;direction:ltr;text-align:left;">
  <li>Steady operating conditions exist.</li>
  <li>Heat transfer is one-dimensional since the high thermal conductivity of copper minimizes lateral temperature gradients.</li>
  <li>All heat generated by the transistors is dissipated through the back surface of the copper plate (the transistor cases are insulated at the front by a Plexiglas cover).</li>
  <li>Thermal conductivities and contact conductance are constant.</li>
</ol>
</div>

<div class="solution-steps">
<h4>Solution</h4>
<div class="step"><div class="step-num">1</div><div class="step-content">
<strong>Contact Area and Plate Area:</strong><br>
The base contact area of each transistor and the plate area of each quarter section are:
\\[ A_c = 8\\;\\text{cm}^2 = 8 \\times 10^{-4}\\;\\text{m}^2 \\qquad A_p = (0.10\\;\\text{m})(0.10\\;\\text{m}) = 0.01\\;\\text{m}^2 \\]
</div></div>

<div class="step"><div class="step-num">2</div><div class="step-content">
<strong>Thermal Contact Resistance at the Interface:</strong><br>
From Table 3–2 for an aluminum–copper interface at \\(\\sim 1.2\\text{--}1.4\\,\\mu\\text{m}\\) roughness and 5 MPa, \\(h_c = 42{,}000\\;\\text{W/m}^2\\cdot\\text{K}\\):
\\[ R_{\\text{interface}} = \\frac{1}{h_c A_c} = \\frac{1}{(42{,}000\\;\\text{W/m}^2\\cdot\\text{K})(8 \\times 10^{-4}\\;\\text{m}^2)} = 0.02976\\;^\\circ\\text{C/W} \\approx 0.0298\\;^\\circ\\text{C/W} \\]
</div></div>

<div class="step"><div class="step-num">3</div><div class="step-content">
<strong>Conduction Resistance of the Copper Plate:</strong>
\\[ R_{\\text{plate}} = \\frac{L}{k_{\\text{Cu}} A_p} = \\frac{0.01\\;\\text{m}}{(386\\;\\text{W/m}\\cdot\\text{K})(0.01\\;\\text{m}^2)} = 0.002591\\;^\\circ\\text{C/W} \\approx 0.0026\\;^\\circ\\text{C/W} \\]
</div></div>

<div class="step"><div class="step-num">4</div><div class="step-content">
<strong>Convection Resistance at the Back Surface:</strong>
\\[ R_{\\text{conv}} = \\frac{1}{h A_p} = \\frac{1}{(25\\;\\text{W/m}^2\\cdot\\text{K})(0.01\\;\\text{m}^2)} = 4.00\\;^\\circ\\text{C/W} \\]
</div></div>

<div class="step"><div class="step-num">5</div><div class="step-content">
<strong>Total Thermal Resistance:</strong><br>
The three resistances are in series:
\\[ R_{\\text{total}} = R_{\\text{interface}} + R_{\\text{plate}} + R_{\\text{conv}} = 0.02976 + 0.002591 + 4.00 = 4.03235\\;^\\circ\\text{C/W} \\approx 4.032\\;^\\circ\\text{C/W} \\]
</div></div>

<div class="step"><div class="step-num">6</div><div class="step-content">
<strong>Maximum Power Dissipation per Transistor:</strong>
\\[ \\dot{Q} = \\frac{\\Delta T}{R_{\\text{total}}} = \\frac{T_{\\text{case}} - T_\\infty}{R_{\\text{total}}} = \\frac{70 - 20}{4.03235\\;^\\circ\\text{C/W}} \\approx 12.4\\;\\text{W} \\]
</div></div>

<div class="step"><div class="step-num">7</div><div class="step-content">
<strong>Temperature Jump across the Interface:</strong>
\\[ \\Delta T_{\\text{interface}} = \\dot{Q} \\, R_{\\text{interface}} = (12.4\\;\\text{W})(0.02976\\;^\\circ\\text{C/W}) \\approx 0.37^\\circ\\text{C} \\]
</div></div>
</div>

<div class="final-answer">
<div class="answer-label">✅ Final Answer</div>
\\[ \\dot{Q}_{\\text{max}} \\approx 12.4\\;\\text{W/transistor} \\qquad \\Delta T_{\\text{interface}} \\approx 0.37^\\circ\\text{C} \\]
</div>

<div class="discussion-box">
<h4>💬 Discussion</h4>
<p>مقاومة الحمل الحراري (\\(R_{\\text{conv}} = 4.00\\;^\\circ\\text{C/W}\\)) هي المهيمنة تمامًا على الدائرة الحرارية بنسبة تفوق 99% من إجمالي المقاومة. في المقابل، تُعد مقاومة تلامس الواجهة البينية (\\(R_{\\text{interface}} = 0.0298\\;^\\circ\\text{C/W}\\)) ومقاومة لوح النحاس (\\(R_{\\text{plate}} = 0.0026\\;^\\circ\\text{C/W}\\)) صغيرتين جدًا وغير مؤثرتين عمليًا؛ ولذلك فإن القضاء التام على مقاومة التلامس (باستخدام معجون حراري أو لحام مثلاً) لن يخفض درجة حرارة تشغيل الترانزستور إلا بأقل من \\(0.4^\\circ\\text{C}\\).</p>
</div>"""

html = replace_sol_inner(html, 'sol-ex3-5', SOL_EX3_5)
print("Updated Example 3-5 solution")

# --- EXAMPLE 3-6 ---
SOL_EX3_6 = """<div class="given-section">
<h4>Given</h4>
<div class="given-grid">
<span>\(H = 3\\;\\text{m},\\; W = 5\\;\\text{m} \\implies A_{\\text{wall}} = 15\\;\\text{m}^2\)</span>
<span>\(k_{\\text{brick}} = 0.72\\;\\text{W/m}\\cdot\\text{K}\) (\(16\\;\\text{cm} \\times 22\\;\\text{cm}\))</span>
<span>\(k_{\\text{plaster}} = 0.22\\;\\text{W/m}\\cdot\\text{K}\)</span>
<span>\(k_{\\text{foam}} = 0.026\\;\\text{W/m}\\cdot\\text{K}\) (\(3\\;\\text{cm}\))</span>
<span>\(T_{\\infty1} = 20^\\circ\\text{C},\\; T_{\\infty2} = -10^\\circ\\text{C}\)</span>
<span>\(h_1 = 10\\;\\text{W/m}^2\\cdot\\text{K},\\; h_2 = 25\\;\\text{W/m}^2\\cdot\\text{K}\)</span>
<span>Representative section: \(H_{\\text{sec}} = 0.25\\;\\text{m},\\; \\text{depth} = 1\\;\\text{m} \\implies A = 0.25\\;\\text{m}^2\)</span>
</div>
</div>

<div class="note-box" style="margin:12px 0;">
<div class="note-title">📝 Assumptions</div>
<ol style="margin:6px 0 0;padding-right:20px;direction:ltr;text-align:left;">
  <li>Steady operating conditions exist.</li>
  <li>Heat transfer is one-dimensional in the \(x\)-direction (perpendicular to the wall).</li>
  <li>Thermal conductivities are constant.</li>
  <li>Radiation heat transfer is negligible.</li>
</ol>
</div>

<div class="solution-steps">
<h4>Solution</h4>
<p style="direction:ltr;text-align:left;">The wall construction exhibits vertical symmetry repeating every \(25\\;\\text{cm}\) (\(22\\;\\text{cm}\) brick + \(3\\;\\text{cm}\) plaster). We consider a representative section of height \(0.25\\;\\text{m}\) and depth \(1\\;\\text{m}\) (\(A = 0.25\\;\\text{m}^2\)):</p>

<div class="step"><div class="step-num">1</div><div class="step-content">
<strong>Representative Section Dimensions:</strong><br>
Height = \(0.25\\;\\text{m}\), Depth = \(1\\;\\text{m}\) \(\implies A = 0.25\\;\\text{m}^2\).
</div></div>

<div class="step"><div class="step-num">2</div><div class="step-content">
<strong>Inner Convection Resistance:</strong>
\\[ R_i = \\frac{1}{h_1 A} = \\frac{1}{(10\\;\\text{W/m}^2\\cdot\\text{K})(0.25\\;\\text{m}^2)} = 0.400\\;^\\circ\\text{C/W} \\]
</div></div>

<div class="step"><div class="step-num">3</div><div class="step-content">
<strong>Rigid Foam Conduction Resistance (\(3\\;\\text{cm}\)):</strong>
\\[ R_1 = R_{\\text{foam}} = \\frac{L_{\\text{foam}}}{k_{\\text{foam}} A} = \\frac{0.03\\;\\text{m}}{(0.026\\;\\text{W/m}\\cdot\\text{K})(0.25\\;\\text{m}^2)} = 4.615\\;^\\circ\\text{C/W} \\]
</div></div>

<div class="step"><div class="step-num">4</div><div class="step-content">
<strong>Inner and Outer Plaster Side Layers (\(2\\;\\text{cm}\) each):</strong>
\\[ R_2 = R_6 = R_{\\text{plaster,side}} = \\frac{L_{\\text{side}}}{k_{\\text{plaster}} A} = \\frac{0.02\\;\\text{m}}{(0.22\\;\\text{W/m}\\cdot\\text{K})(0.25\\;\\text{m}^2)} = 0.364\\;^\\circ\\text{C/W} \\]
</div></div>

<div class="step"><div class="step-num">5</div><div class="step-content">
<strong>Center Plaster Layers (Parallel Paths above and below the brick, \(1.5\\;\\text{cm}\) each):</strong><br>
Area for each layer = \((0.015\\;\\text{m})(1\\;\\text{m}) = 0.015\\;\\text{m}^2\), Thickness = \(0.16\\;\\text{m}\):
\\[ R_3 = R_5 = R_{\\text{plaster,center}} = \\frac{L_{\\text{brick}}}{k_{\\text{plaster}} A_{\\text{center}}} = \\frac{0.16\\;\\text{m}}{(0.22\\;\\text{W/m}\\cdot\\text{K})(0.015\\;\\text{m}^2)} = 48.485\\;^\\circ\\text{C/W} \\approx 48.48\\;^\\circ\\text{C/W} \\]
</div></div>

<div class="step"><div class="step-num">6</div><div class="step-content">
<strong>Brick Conduction Resistance:</strong><br>
Area = \((0.22\\;\\text{m})(1\\;\\text{m}) = 0.22\\;\\text{m}^2\), Thickness = \(0.16\\;\\text{m}\):
\\[ R_4 = R_{\\text{brick}} = \\frac{L_{\\text{brick}}}{k_{\\text{brick}} A_{\\text{brick}}} = \\frac{0.16\\;\\text{m}}{(0.72\\;\\text{W/m}\\cdot\\text{K})(0.22\\;\\text{m}^2)} = 1.010\\;^\\circ\\text{C/W} \\]
</div></div>

<div class="step"><div class="step-num">7</div><div class="step-content">
<strong>Parallel Middle Combination (\(R_3\), \(R_4\), \(R_5\) in parallel):</strong>
\\[ \\frac{1}{R_{\\text{mid}}} = \\frac{1}{R_3} + \\frac{1}{R_4} + \\frac{1}{R_5} = \\frac{1}{48.48} + \\frac{1}{1.010} + \\frac{1}{48.48} = 0.0206 + 0.9901 + 0.0206 = 1.0313\\;\\text{W/}^\\circ\\text{C} \\]
\\[ R_{\\text{mid}} = \\frac{1}{1.0313} \\approx 0.970\\;^\\circ\\text{C/W} \\]
</div></div>

<div class="step"><div class="step-num">8</div><div class="step-content">
<strong>Outer Convection Resistance:</strong>
\\[ R_o = \\frac{1}{h_2 A} = \\frac{1}{(25\\;\\text{W/m}^2\\cdot\\text{K})(0.25\\;\\text{m}^2)} = 0.160\\;^\\circ\\text{C/W} \\]
</div></div>

<div class="step"><div class="step-num">9</div><div class="step-content">
<strong>Total Equivalent Thermal Resistance of the Representative Section:</strong>
\\[ R_{\\text{total}} = R_i + R_1 + R_2 + R_{\\text{mid}} + R_6 + R_o \\]
\\[ R_{\\text{total}} = 0.400 + 4.615 + 0.364 + 0.970 + 0.364 + 0.160 = 6.873\\;^\\circ\\text{C/W} \\]
</div></div>

<div class="step"><div class="step-num">10</div><div class="step-content">
<strong>Heat Transfer Rate through the Representative Section:</strong>
\\[ \\dot{Q}_{\\text{sec}} = \\frac{T_{\\infty1} - T_{\\infty2}}{R_{\\text{total}}} = \\frac{20 - (-10)}{6.873\\;^\\circ\\text{C/W}} = \\frac{30}{6.873} \\approx 4.365\\;\\text{W} \\approx 4.37\\;\\text{W} \\]
</div></div>

<div class="step"><div class="step-num">11</div><div class="step-content">
<strong>Heat Flux through the Wall:</strong>
\\[ q'' = \\frac{\\dot{Q}_{\\text{sec}}}{A} = \\frac{4.365\\;\\text{W}}{0.25\\;\\text{m}^2} = 17.46\\;\\text{W/m}^2 \\approx 17.48\\;\\text{W/m}^2 \\]
</div></div>

<div class="step"><div class="step-num">12</div><div class="step-content">
<strong>Total Heat Transfer Rate through the Entire Wall (\(A_{\\text{wall}} = 15\\;\\text{m}^2\)):</strong>
\\[ \\dot{Q}_{\\text{total}} = q'' A_{\\text{wall}} = (17.46\\;\\text{W/m}^2)(15\\;\\text{m}^2) \\approx 262\\;\\text{W} \\]
</div></div>
</div>

<div class="final-answer">
<div class="answer-label">✅ Final Answer</div>
\\[ \\dot{Q}_{\\text{total}} \\approx 262\\;\\text{W} \\]
</div>

<div class="discussion-box">
<h4>💬 Discussion</h4>
<p>طبقة الرغوة العازلة (<span class="term">rigid foam</span>) تمتلك المقاومة الحرارية الأعلى على الإطلاق (\(4.615\\;^\\circ\\text{C/W}\\))، حيث تمثل وحدها ما يقارب 67% من إجمالي المقاومة الحرارية للجدار. وفي الجزء الأوسط المتوازي، يهيمن مسار الطوب الأحمر (\(R_4 = 1.010\\;^\\circ\\text{C/W}\\)) على انتقال الحرارة لأن مقاومة ملاط الجص الفاصلة (\(48.48\\;^\\circ\\text{C/W}\\)) كبيرة جدًا بسبب ضيق مساحتها. تجدر الإشارة إلى أن هذه النتيجة تقريبية (<span class="term">approximate</span>) بافتراض انتقال الحرارة أحادي البعد؛ وإذا استُخدم الأسلوب البديل بافتراض مستويات أدياباتية (<span class="term">adiabatic planes</span>) نحصل على \(R_{\\text{total}} = 6.97\\;^\\circ\\text{C/W}\) و \(\\dot{Q} \\approx 258\\;\\text{W}\)، وهو تطابق ممتاز يؤكد دقة النمذجة الهندسية.</p>
</div>"""

html = replace_sol_inner(html, 'sol-ex3-6', SOL_EX3_6)
print("Updated Example 3-6 solution")

# --- EXAMPLE 3-7 ---
# Rename title
html = html.replace('Example 3–7: Spherical Tank (Iced Water)', 'Example 3–7: Heat Transfer to a Spherical Container')
html = html.replace('Example 3-7: Spherical Tank (Iced Water)', 'Example 3–7: Heat Transfer to a Spherical Container')

SOL_EX3_7 = """<div class="given-section">
<h4>Given</h4>
<div class="given-grid">
<span>\(D_1 = 3.0\\;\\text{m} \\implies r_1 = 1.50\\;\\text{m}\)</span>
<span>\(\\text{thickness} = 0.02\\;\\text{m} \\implies r_2 = 1.52\\;\\text{m},\\; D_2 = 3.04\\;\\text{m}\)</span>
<span>\(k = 15\\;\\text{W/m}\\cdot\\text{K}\) (stainless steel)</span>
<span>\(T_{\\infty1} = 0^\\circ\\text{C},\\; T_{\\infty2} = 22^\\circ\\text{C}\)</span>
<span>\(h_1 = 80\\;\\text{W/m}^2\\cdot\\text{K},\\; h_2 = 10\\;\\text{W/m}^2\\cdot\\text{K}\)</span>
<span>\(\\varepsilon = 1.0\) (black surface)</span>
<span>\(h_{if} = 333.7\\;\\text{kJ/kg}\) (latent heat of fusion of ice)</span>
</div>
</div>

<div class="note-box" style="margin:12px 0;">
<div class="note-title">📝 Assumptions</div>
<ol style="margin:6px 0 0;padding-right:20px;direction:ltr;text-align:left;">
  <li>Steady operating conditions exist.</li>
  <li>Heat transfer is one-dimensional in the radial direction due to full spherical symmetry.</li>
  <li>Thermal conductivity and surface properties are constant.</li>
</ol>
</div>

<div class="solution-steps">
<h4>Solution</h4>

<div class="step"><div class="step-num">1</div><div class="step-content">
<strong>Inner and Outer Surface Areas:</strong>
\\[ A_1 = \\pi D_1^2 = \\pi (3.0\\;\\text{m})^2 = 28.274\\;\\text{m}^2 \\approx 28.27\\;\\text{m}^2 \\]
\\[ A_2 = \\pi D_2^2 = \\pi (3.04\\;\\text{m})^2 = 29.033\\;\\text{m}^2 \\approx 29.02\\;\\text{m}^2 \\]
</div></div>

<div class="step"><div class="step-num">2</div><div class="step-content">
<strong>Radiation Heat Transfer Coefficient (\(h_{\\text{rad}}\)):</strong><br>
Assuming an outer surface temperature \(T_2 \\approx 5^\\circ\\text{C} = 278\\;\\text{K}\) with surrounding temperature \(T_{\\infty2} = 22^\\circ\\text{C} = 295\\;\\text{K}\):
\\[ h_{\\text{rad}} = \\varepsilon \\sigma (T_2 + T_{\\infty2})(T_2^2 + T_{\\infty2}^2) = (1)(5.67 \\times 10^{-8})(278 + 295)(278^2 + 295^2) \\approx 5.34\\;\\text{W/m}^2\\cdot\\text{K} \\]
</div></div>

<div class="step"><div class="step-num">3</div><div class="step-content">
<strong>Inner Convection Resistance:</strong>
\\[ R_i = \\frac{1}{h_1 A_1} = \\frac{1}{(80\\;\\text{W/m}^2\\cdot\\text{K})(28.274\\;\\text{m}^2)} = 4.421 \\times 10^{-4}\\;^\\circ\\text{C/W} \\approx 4.42 \\times 10^{-4}\\;^\\circ\\text{C/W} \\]
</div></div>

<div class="step"><div class="step-num">4</div><div class="step-content">
<strong>Spherical Steel Wall Conduction Resistance:</strong>
\\[ R_{\\text{steel}} = \\frac{r_2 - r_1}{4\\pi k r_1 r_2} = \\frac{1.52 - 1.50}{4\\pi (15)(1.50)(1.52)} = \\frac{0.02}{429.77} = 4.654 \\times 10^{-5}\\;^\\circ\\text{C/W} \\approx 4.65 \\times 10^{-5}\\;^\\circ\\text{C/W} \\]
</div></div>

<div class="step"><div class="step-num">5</div><div class="step-content">
<strong>Outer Convection Resistance:</strong>
\\[ R_{\\text{conv}} = \\frac{1}{h_2 A_2} = \\frac{1}{(10\\;\\text{W/m}^2\\cdot\\text{K})(29.033\\;\\text{m}^2)} = 3.444 \\times 10^{-3}\\;^\\circ\\text{C/W} \\approx 3.45 \\times 10^{-3}\\;^\\circ\\text{C/W} \\]
</div></div>

<div class="step"><div class="step-num">6</div><div class="step-content">
<strong>Outer Radiation Resistance:</strong>
\\[ R_{\\text{rad}} = \\frac{1}{h_{\\text{rad}} A_2} = \\frac{1}{(5.34\\;\\text{W/m}^2\\cdot\\text{K})(29.033\\;\\text{m}^2)} = 6.450 \\times 10^{-3}\\;^\\circ\\text{C/W} \\approx 6.45 \\times 10^{-3}\\;^\\circ\\text{C/W} \\]
</div></div>

<div class="step"><div class="step-num">7</div><div class="step-content">
<strong>Equivalent Outer Resistance (Convection &amp; Radiation in Parallel):</strong>
\\[ R_{\\text{equiv}} = \\frac{R_{\\text{conv}} R_{\\text{rad}}}{R_{\\text{conv}} + R_{\\text{rad}}} = \\frac{(3.444 \\times 10^{-3})(6.450 \\times 10^{-3})}{3.444 \\times 10^{-3} + 6.450 \\times 10^{-3}} \\approx 2.245 \\times 10^{-3}\\;^\\circ\\text{C/W} \\approx 2.25 \\times 10^{-3}\\;^\\circ\\text{C/W} \\]
</div></div>

<div class="step"><div class="step-num">8</div><div class="step-content">
<strong>Total Equivalent Thermal Resistance:</strong>
\\[ R_{\\text{total}} = R_i + R_{\\text{steel}} + R_{\\text{equiv}} = 4.42 \\times 10^{-4} + 4.65 \\times 10^{-5} + 2.25 \\times 10^{-3} \\approx 2.739 \\times 10^{-3}\\;^\\circ\\text{C/W} \\approx 2.74 \\times 10^{-3}\\;^\\circ\\text{C/W} \\]
</div></div>

<div class="step"><div class="step-num">9</div><div class="step-content">
<strong>Part (a) Rate of Heat Transfer:</strong>
\\[ \\dot{Q} = \\frac{T_{\\infty2} - T_{\\infty1}}{R_{\\text{total}}} = \\frac{22 - 0}{2.739 \\times 10^{-3}\\;^\\circ\\text{C/W}} \\approx 8{,}029\\;\\text{W} \\approx 8.03\\;\\text{kW} \\]
</div></div>

<div class="step"><div class="step-num">10</div><div class="step-content">
<strong>Verification of Assumed Surface Temperature \(T_2\):</strong>
\\[ T_2 = T_{\\infty2} - \\dot{Q} R_{\\text{equiv}} = 22 - (8{,}029)(0.002245) \\approx 22 - 18.0 = 4.0^\\circ\\text{C} \\]
درجة الحرارة المحسوبة (\(4^\\circ\\text{C}\)) قريبة جدًا من القيمة المفترضة (\(5^\\circ\\text{C}\))، وبالتالي لا حاجة لتكرار الحساب ✓.
</div></div>

<div class="step"><div class="step-num">11</div><div class="step-content">
<strong>Part (b) Amount of Ice Melted in 24 Hours:</strong><br>
The total heat transferred during a 24-hour period is:
\\[ Q = \\dot{Q} \\Delta t = (8.029\\;\\text{kW})(24 \\times 3600\\;\\text{s}) = 693{,}706\\;\\text{kJ} \\]
The mass of ice melted during this period is:
\\[ m_{\\text{ice}} = \\frac{Q}{h_{if}} = \\frac{693{,}706\\;\\text{kJ}}{333.7\\;\\text{kJ/kg}} \\approx 2078.8\\;\\text{kg} \\approx 2079\\;\\text{kg} \\]
</div></div>
</div>

<div class="final-answer">
<div class="answer-label">✅ Final Answer</div>
\\[ \\text{(a) } \\dot{Q} \\approx 8.03\\;\\text{kW} \\qquad \\text{(b) } m_{\\text{ice}} \\approx 2079\\;\\text{kg} \\approx 2.08\\;\\text{metric tons/day} \\]
</div>

<div class="discussion-box">
<h4>💬 Discussion</h4>
<p>نظرًا لأن درجة حرارة الجدران المحيطة بالإشعاع مساوية لدرجة حرارة الهواء الخارجي (\(T_{\\text{surr}} = T_\\infty = 22^\\circ\\text{C}\))، يمكن اختصار الحساب بدمج الحمل والإشعاع في معامل واحد: \(h_{\\text{combined}} = h_2 + h_{\\text{rad}} = 10 + 5.34 = 15.34\\;\\text{W/m}^2\\cdot\\text{K}\). والنتيجة توضح خطورة ترك خزانات التبريد غير معزولة، حيث يذوب أكثر من <strong>2 طن متري من الجليد يوميًا</strong>، مما يبرز الأهمية الاقتصادية الفائقة لإضافة عازل حراري كافٍ حول الخزان.</p>
</div>"""

html = replace_sol_inner(html, 'sol-ex3-7', SOL_EX3_7)
print("Updated Example 3-7 solution & title")

# --- EXAMPLE 3-8 ---
# Rename title
html = html.replace('Example 3–8: Insulated Cast-Iron Pipe', 'Example 3–8: Heat Loss through an Insulated Steam Pipe')
html = html.replace('Example 3-8: Insulated Cast-Iron Pipe', 'Example 3–8: Heat Loss through an Insulated Steam Pipe')

SOL_EX3_8 = """<div class="given-section">
<h4>Given</h4>
<div class="given-grid">
<span>\(D_1 = 0.05\\;\\text{m} \\implies r_1 = 0.025\\;\\text{m}\)</span>
<span>\(D_2 = 0.055\\;\\text{m} \\implies r_2 = 0.0275\\;\\text{m}\)</span>
<span>\(r_3 = r_2 + 0.03\\;\\text{m} = 0.0575\\;\\text{m}\)</span>
<span>\(L = 1\\;\\text{m}\) (unit length)</span>
<span>\(k_{\\text{pipe}} = 80\\;\\text{W/m}\\cdot\\text{K}\) (cast iron)</span>
<span>\(k_{\\text{ins}} = 0.05\\;\\text{W/m}\\cdot\\text{K}\) (glass wool)</span>
<span>\(h_1 = 60\\;\\text{W/m}^2\\cdot\\text{K},\\; h_2 = 18\\;\\text{W/m}^2\\cdot\\text{K}\) (combined)</span>
<span>\(T_{\\infty1} = 320^\\circ\\text{C},\\; T_{\\infty2} = 5^\\circ\\text{C}\)</span>
</div>
</div>

<div class="note-box" style="margin:12px 0;">
<div class="note-title">📝 Assumptions</div>
<ol style="margin:6px 0 0;padding-right:20px;direction:ltr;text-align:left;">
  <li>Steady operating conditions exist.</li>
  <li>Heat transfer is one-dimensional in the radial direction since the pipe is long compared to its diameter.</li>
  <li>Thermal conductivities are constant.</li>
  <li>Thermal contact resistance between the pipe and the insulation is negligible.</li>
</ol>
</div>

<div class="solution-steps">
<h4>Solution</h4>

<div class="step"><div class="step-num">1</div><div class="step-content">
<strong>Inner and Outer Surface Areas (per unit length \(L = 1\\;\\text{m}\)):</strong>
\\[ A_1 = 2\\pi r_1 L = 2\\pi (0.025\\;\\text{m})(1\\;\\text{m}) = 0.1571\\;\\text{m}^2 \\]
\\[ A_3 = 2\\pi r_3 L = 2\\pi (0.0575\\;\\text{m})(1\\;\\text{m}) = 0.3613\\;\\text{m}^2 \\]
</div></div>

<div class="step"><div class="step-num">2</div><div class="step-content">
<strong>Inner Convection Resistance:</strong>
\\[ R_i = \\frac{1}{h_1 A_1} = \\frac{1}{(60\\;\\text{W/m}^2\\cdot\\text{K})(0.1571\\;\\text{m}^2)} = 0.1061\\;^\\circ\\text{C/W} \\]
</div></div>

<div class="step"><div class="step-num">3</div><div class="step-content">
<strong>Conduction Resistance of the Cast Iron Pipe:</strong>
\\[ R_{\\text{pipe}} = \\frac{\\ln(r_2/r_1)}{2\\pi k_{\\text{pipe}} L} = \\frac{\\ln(0.0275/0.025)}{2\\pi (80\\;\\text{W/m}\\cdot\\text{K})(1\\;\\text{m})} = \\frac{\\ln(1.10)}{502.65} = \\frac{0.09531}{502.65} = 0.000190\\;^\\circ\\text{C/W} \\]
</div></div>

<div class="step"><div class="step-num">4</div><div class="step-content">
<strong>Conduction Resistance of the Glass Wool Insulation:</strong>
\\[ R_{\\text{ins}} = \\frac{\\ln(r_3/r_2)}{2\\pi k_{\\text{ins}} L} = \\frac{\\ln(0.0575/0.0275)}{2\\pi (0.05\\;\\text{W/m}\\cdot\\text{K})(1\\;\\text{m})} = \\frac{\\ln(2.0909)}{0.31416} = \\frac{0.73759}{0.31416} = 2.353\\;^\\circ\\text{C/W} \\]
</div></div>

<div class="step"><div class="step-num">5</div><div class="step-content">
<strong>Outer Convection Resistance:</strong>
\\[ R_o = \\frac{1}{h_2 A_3} = \\frac{1}{(18\\;\\text{W/m}^2\\cdot\\text{K})(0.3613\\;\\text{m}^2)} = 0.1538\\;^\\circ\\text{C/W} \\]
</div></div>

<div class="step"><div class="step-num">6</div><div class="step-content">
<strong>Total Equivalent Thermal Resistance:</strong>
\\[ R_{\\text{total}} = R_i + R_{\\text{pipe}} + R_{\\text{ins}} + R_o = 0.1061 + 0.000190 + 2.353 + 0.1538 = 2.613\\;^\\circ\\text{C/W} \\]
</div></div>

<div class="step"><div class="step-num">7</div><div class="step-content">
<strong>(1) Rate of Heat Loss per Unit Length:</strong>
\\[ \\dot{Q} = \\frac{T_{\\infty1} - T_{\\infty2}}{R_{\\text{total}}} = \\frac{320 - 5}{2.613\\;^\\circ\\text{C/W}} = \\frac{315}{2.613} \\approx 120.6\\;\\text{W/m} \\]
</div></div>

<div class="step"><div class="step-num">8</div><div class="step-content">
<strong>(2) Temperature Drop across the Pipe Wall:</strong>
\\[ \\Delta T_{\\text{pipe}} = \\dot{Q} \\, R_{\\text{pipe}} = (120.6\\;\\text{W/m})(0.000190\\;^\\circ\\text{C/W}) \\approx 0.023^\\circ\\text{C} \\]
</div></div>

<div class="step"><div class="step-num">9</div><div class="step-content">
<strong>Temperature Drop across the Insulation Layer:</strong>
\\[ \\Delta T_{\\text{insulation}} = \\dot{Q} \\, R_{\\text{ins}} = (120.6\\;\\text{W/m})(2.353\\;^\\circ\\text{C/W}) \\approx 284^\\circ\\text{C} \\]
</div></div>
</div>

<div class="final-answer">
<div class="answer-label">✅ Final Answer</div>
\\[ \\dot{Q} \\approx 120.6\\;\\text{W/m} \\qquad \\Delta T_{\\text{pipe}} \\approx 0.023^\\circ\\text{C} \\qquad \\Delta T_{\\text{insulation}} \\approx 284^\\circ\\text{C} \\]
</div>

<div class="discussion-box">
<h4>💬 Discussion</h4>
<p>مقاومة جدار الأنبوب الحديدي (\(R_{\\text{pipe}} = 0.000190\\;^\\circ\\text{C/W}\)) مهملة تمامًا ولا تشكل سوى جزء من مائة في المائة من المقاومة الإجمالية، وهو ما يفسر الهبوط المتناهي في الصغر لدرجة الحرارة عبر الأنبوب (\(0.023^\\circ\\text{C}\))؛ لذلك يمكن اعتبار جدار الأنبوب متساوي درجة الحرارة (<span class="term">isothermal</span>) عمليًا. في المقابل، تشكل طبقة العزل (\(R_{\\text{ins}} = 2.353\\;^\\circ\\text{C/W}\)) حوالي <strong>91%</strong> من المقاومة الكلية، ويحدث عبرها الجزء الأعظم من الهبوط الحراري (\(284^\\circ\\text{C}\)).</p>
</div>"""

html = replace_sol_inner(html, 'sol-ex3-8', SOL_EX3_8)
print("Updated Example 3-8 solution & title")

# --- EXAMPLE 3-9 ---
# Rename title
html = html.replace('Example 3–9: Electric Wire with Plastic Insulation', 'Example 3–9: Heat Loss from an Insulated Electric Wire')
html = html.replace('Example 3-9: Electric Wire with Plastic Insulation', 'Example 3–9: Heat Loss from an Insulated Electric Wire')

SOL_EX3_9 = """<div class="given-section">
<h4>Given</h4>
<div class="given-grid">
<span>\(r_1 = 1.5\\;\\text{mm} = 0.0015\\;\\text{m}\)</span>
<span>\(\\text{thickness} = 2.0\\;\\text{mm} \\implies r_2 = 3.5\\;\\text{mm} = 0.0035\\;\\text{m}\)</span>
<span>\(L = 5.0\\;\\text{m}\)</span>
<span>\(V = 8\\;\\text{V},\\; I = 10\\;\\text{A} \\implies \\dot{Q} = VI = (8)(10) = 80\\;\\text{W}\)</span>
<span>\(k = 0.15\\;\\text{W/m}\\cdot\\text{K}\) (plastic cover)</span>
<span>\(h = 12\\;\\text{W/m}^2\\cdot\\text{K}\)</span>
<span>\(T_\\infty = 30^\\circ\\text{C}\)</span>
</div>
</div>

<div class="note-box" style="margin:12px 0;">
<div class="note-title">📝 Assumptions</div>
<ol style="margin:6px 0 0;padding-right:20px;direction:ltr;text-align:left;">
  <li>Steady operating conditions exist since the wire operates continuously at specified voltage and current.</li>
  <li>Heat transfer is one-dimensional in the radial direction due to long wire length and cylindrical symmetry.</li>
  <li>Thermal conductivity and convection heat transfer coefficient are constant.</li>
  <li>Radiation heat transfer is either negligible or incorporated into the given convection heat transfer coefficient.</li>
</ol>
</div>

<div class="solution-steps">
<h4>Solution</h4>

<div class="step"><div class="step-num">1</div><div class="step-content">
<strong>Outer Surface Area of the Plastic Cover:</strong>
\\[ A_2 = 2\\pi r_2 L = 2\\pi (0.0035\\;\\text{m})(5\\;\\text{m}) \\approx 0.1100\\;\\text{m}^2 \\]
</div></div>

<div class="step"><div class="step-num">2</div><div class="step-content">
<strong>Thermal Resistances (Original 2-mm Cover):</strong><br>
The outer convection resistance is:
\\[ R_{\\text{conv}} = \\frac{1}{h A_2} = \\frac{1}{(12\\;\\text{W/m}^2\\cdot\\text{K})(0.1100\\;\\text{m}^2)} = 0.7576\\;^\\circ\\text{C/W} \\approx 0.758\\;^\\circ\\text{C/W} \\]
The plastic conduction resistance is:
\\[ R_{\\text{plastic}} = \\frac{\\ln(r_2/r_1)}{2\\pi k L} = \\frac{\\ln(3.5/1.5)}{2\\pi (0.15\\;\\text{W/m}\\cdot\\text{K})(5\\;\\text{m})} = \\frac{0.8473}{4.7124} = 0.1798\\;^\\circ\\text{C/W} \\approx 0.179\\;^\\circ\\text{C/W} \\]
Total thermal resistance:
\\[ R_{\\text{total}} = R_{\\text{plastic}} + R_{\\text{conv}} = 0.1798 + 0.7576 = 0.9374\\;^\\circ\\text{C/W} \\approx 0.937\\;^\\circ\\text{C/W} \\]
</div></div>

<div class="step"><div class="step-num">3</div><div class="step-content">
<strong>Interface Temperature \(T_1\):</strong>
\\[ \\dot{Q} = \\frac{T_1 - T_\\infty}{R_{\\text{total}}} \\implies T_1 = T_\\infty + \\dot{Q} R_{\\text{total}} = 30^\\circ\\text{C} + (80\\;\\text{W})(0.9374\\;^\\circ\\text{C/W}) \\approx 105^\\circ\\text{C} \\]
</div></div>

<div class="step"><div class="step-num">4</div><div class="step-content">
<strong>Critical Radius of Insulation:</strong>
\\[ r_{\\text{cr}} = \\frac{k}{h} = \\frac{0.15\\;\\text{W/m}\\cdot\\text{K}}{12\\;\\text{W/m}^2\\cdot\\text{K}} = 0.0125\\;\\text{m} = 12.5\\;\\text{mm} \\]
Since \(r_2 = 3.5\\;\\text{mm} < r_{\\text{cr}} = 12.5\\;\\text{mm}\), the outer radius is well below the critical radius. Therefore, adding more insulation will <em>increase</em> heat dissipation and <em>lower</em> the wire temperature.
</div></div>

<div class="step"><div class="step-num">5</div><div class="step-content">
<strong>Effect of Doubling Insulation Thickness (from 2 mm to 4 mm):</strong><br>
New outer radius: \(r_2 = 1.5\\;\\text{mm} + 4.0\\;\\text{mm} = 5.5\\;\\text{mm} = 0.0055\\;\\text{m}\).<br>
New outer area:
\\[ A_2 = 2\\pi (0.0055\\;\\text{m})(5\\;\\text{m}) = 0.1728\\;\\text{m}^2 \\]
New convection resistance:
\\[ R_{\\text{conv}} = \\frac{1}{(12)(0.1728)} = 0.4823\\;^\\circ\\text{C/W} \\approx 0.482\\;^\\circ\\text{C/W} \\]
New plastic conduction resistance:
\\[ R_{\\text{plastic}} = \\frac{\\ln(5.5/1.5)}{2\\pi(0.15)(5)} = \\frac{\\ln(3.667)}{4.7124} = \\frac{1.2993}{4.7124} = 0.2757\\;^\\circ\\text{C/W} \\approx 0.400\\;^\\circ\\text{C/W} \\]
New total thermal resistance:
\\[ R_{\\text{total}} = 0.482 + 0.400 = 0.882\\;^\\circ\\text{C/W} \\]
New interface temperature:
\\[ T_1 = T_\\infty + \\dot{Q} R_{\\text{total}} = 30^\\circ\\text{C} + (80\\;\\text{W})(0.882\\;^\\circ\\text{C/W}) = 100.5^\\circ\\text{C} \\]
(The temperature drops by \(4.5^\\circ\\text{C}\)!).
</div></div>

<div class="step"><div class="step-num">6</div><div class="step-content">
<strong>Minimum Temperature at the Critical Radius (\(r_2 = r_{\\text{cr}} = 12.5\\;\\text{mm}\)):</strong><br>
At \(r_2 = 12.5\\;\\text{mm}\):
\\[ A_2 = 2\\pi (0.0125)(5) = 0.3927\\;\\text{m}^2 \\implies R_{\\text{conv}} = \\frac{1}{(12)(0.3927)} = 0.212\\;^\\circ\\text{C/W} \\]
\\[ R_{\\text{plastic}} = \\frac{\\ln(12.5/1.5)}{4.7124} = \\frac{2.1203}{4.7124} = 0.450\\;^\\circ\\text{C/W} \\]
\\[ R_{\\text{total}} = 0.212 + 0.450 = 0.662\\;^\\circ\\text{C/W} \\]
\\[ T_{1,\\text{min}} = 30 + (80)(0.662) \\approx 83^\\circ\\text{C} \\]
</div></div>
</div>

<div class="final-answer">
<div class="answer-label">✅ Final Answer</div>
\\[ T_1 \\approx 105^\\circ\\text{C}\\;\\text{(original 2 mm)} \\qquad T_1 \\approx 100.5^\\circ\\text{C}\\;\\text{(doubled to 4 mm)} \\qquad T_{1,\\text{min}} \\approx 83^\\circ\\text{C}\\;\\text{(at } r_{\\text{cr}}\\text{)} \\]
</div>

<div class="discussion-box">
<h4>💬 Discussion</h4>
<p>بما أن نصف القطر الخارجي (\(r_2 = 3.5\\;\\text{mm}\)) أصغر من نصف القطر الحرج (\(r_{\\text{cr}} = 12.5\\;\\text{mm}\))، فإن زيادة سُمك العازل تزيد مساحة السطح الخارجي بدرجة تفوق أثر المقاومة التوصيلية المضافة، مما يخفض المقاومة الحرارية الإجمالية من \(0.937\) إلى \(0.882\\;^\\circ\\text{C/W}\) ويؤدي إلى <strong>انخفاض درجة حرارة السلك إلى \(100.5^\\circ\\text{C}\)</strong>. وتصل درجة حرارة السلك إلى أدنى قيمة ممكنة لها (\(83^\\circ\\text{C}\)) عندما يبلغ سُمك العازل نصف القطر الحرج (\(12.5\\;\\text{mm}\)). يبرهن هذا المثال على أن تغليف الأسلاك الكهربائية بالعوازل لا يخدم الأمان الكهربائي فحسب، بل يعمل أيضًا كأداة تبريد حراري تحمي السلك من الاحتراق.</p>
</div>"""

html = replace_sol_inner(html, 'sol-ex3-9', SOL_EX3_9)
print("Updated Example 3-9 solution & title")

# --- EXAMPLE 3-10 ---
SOL_EX3_10 = """<div class="given-section">
<h4>Given</h4>
<div class="given-grid">
<span>\(T_c \le 85^\circ\text{C}\)</span>
<span>\(T_\infty = 25^\circ\text{C}\)</span>
<span>\(R_{\text{case-ambient}} = 20\;^\circ\text{C/W}\)</span>
<span>\(\dot{W}_{\text{rating}} = 10\;\text{W}\)</span>
</div>
</div>

<div class="note-box" style="margin:12px 0;">
<div class="note-title">📝 Assumptions</div>
<ol style="margin:6px 0 0;padding-right:20px;direction:ltr;text-align:left;">
  <li>Steady operating conditions exist.</li>
  <li>Thermal resistance from the transistor case to the ambient air is constant and encompasses combined convection and radiation.</li>
</ol>
</div>

<div class="solution-steps">
<h4>Solution</h4>
<div class="step"><div class="step-num">1</div><div class="step-content">
From the thermal resistance model between the transistor case and ambient air:
\[ \dot{Q} = \frac{T_c - T_\infty}{R_{\text{case-ambient}}} = \frac{85 - 25}{20} = \frac{60}{20} = 3\;\text{W} \]
</div></div>
</div>

<div class="final-answer">
<div class="answer-label">✅ Final Answer</div>
\[ \dot{Q}_{\text{max}} = 3\;\text{W} \]
</div>

<div class="discussion-box">
<h4>💬 Discussion</h4>
<p>يجب ألا يعمل الترانزستور عند قدرة تتجاوز 3 W في هذه الظروف لتجنب تجاوز درجة حرارة الغلاف \(85^\circ\text{C}\)، وهي أقل بكثير من قدرته القصوى المصنفة (10 W). وتجدر الإشارة في هندسة تبريد الإلكترونيات إلى أن <strong>معدل تعرض المكونات الإلكترونية للأعطال ينخفض إلى النصف لكل هبوط قدره \(10^\circ\text{C}\) في درجة حرارة الوصلة (<span class="term">junction temperature</span>)</strong>. ولتشغيل الترانزستور عند مستويات قدرة أعلى تقترب من 10 W بأمان وموثوقية، يجب خفض المقاومة الحرارية الفعالة بإضافة مشتت حراري (<span class="term">heat sink</span>) أو استخدام مروحة تبريد (<span class="term">cooling fan</span>) لزيادة التدفق ومعامل الحمل \(h\).</p>
</div>"""

html = replace_sol_inner(html, 'sol-ex3-10', SOL_EX3_10)
print("Updated Example 3-10 solution")

# --- EXAMPLE 3-11 ---
SOL_EX3_11 = """<div class="given-section">
<h4>Given</h4>
<div class="given-grid">
<span>\(\dot{Q} = 60\;\text{W}\)</span>
<span>\(T_c \le 90^\circ\text{C}\)</span>
<span>\(T_\infty = 30^\circ\text{C}\)</span>
</div>
</div>

<div class="note-box" style="margin:12px 0;">
<div class="note-title">📝 Properties</div>
<p style="margin:6px 0 0;direction:ltr;text-align:left;">
From Table 3–6 (natural convection heat sinks):
<br>• <strong>HS 5030</strong>: \(R = 0.9\;^\circ\text{C/W}\) (vertical orientation), \(R = 1.4\;^\circ\text{C/W}\) (horizontal orientation).
<br>• <strong>HS 6071</strong>: \(R = 1.4\;^\circ\text{C/W}\) (vertical), \(R = 1.8\;^\circ\text{C/W}\) (horizontal).
</p>
</div>

<div class="solution-steps">
<h4>Solution</h4>
<div class="step"><div class="step-num">1</div><div class="step-content">
Calculate the maximum allowable thermal resistance:
<br>The maximum allowable temperature difference is:
\[ \Delta T = T_c - T_\infty = 90^\circ\text{C} - 30^\circ\text{C} = 60^\circ\text{C} \]
The required thermal resistance is:
\[ R = \frac{\Delta T}{\dot{Q}} = \frac{60^\circ\text{C}}{60\;\text{W}} = 1.0\;^\circ\text{C/W} \]
</div></div>
<div class="step"><div class="step-num">2</div><div class="step-content">
Heat sink selection:
<br>To maintain the case temperature at or below 90°C, the selected heat sink must satisfy:
\[ R < 1.0\;^\circ\text{C/W} \]
From Table 3–6 of standard commercial heat sinks:
<br>The <strong>HS 5030</strong> heat sink provides \(R = 0.9\;^\circ\text{C/W}\) in vertical orientation ✓.
</div></div>
</div>

<div class="final-answer">
<div class="answer-label">✅ Final Answer</div>
<p style="direction:ltr;text-align:center;">Select <strong>HS 5030</strong> heat sink (\(R = 0.9\;^\circ\text{C/W}\), vertical orientation)</p>
</div>

<div class="discussion-box">
<h4>💬 Discussion</h4>
<p>المشتت الحراري HS 5030 ذو المقاومة \(0.9\;^\circ\text{C/W}\) في الوضع الرأسي سيحافظ على درجة حرارة الغلاف عند: \(T_c = T_\infty + \dot{Q}R = 30 + (60)(0.9) = 84^\circ\text{C}\)، وهي أقل بـ \(6^\circ\text{C}\) من الحد الأقصى المسموح به (\(90^\circ\text{C}\)). هذا الهبوط بمقدار 6 درجات يقلل معدل تعرض الترانزستور للأعطال بنسبة تقارب 35%، مما يمنح المكون الإلكتروني عمرًا تشغيليًا أطول وموثوقية بالغة الأهمية. وتجدر الإشارة إلى أن توجيه المشتت الحراري رأسيًا أمر جوهري، إذ إن وضعه أفقيًا يرفع مقاومته إلى \(1.4\;^\circ\text{C/W}\) مما يؤدي إلى تجاوز درجة الحرارة المسموحة (\(114^\circ\text{C}\)) واحتراق الترانزستور.</p>
</div>"""

html = replace_sol_inner(html, 'sol-ex3-11', SOL_EX3_11)
print("Updated Example 3-11 solution")

# --- EXAMPLE 3-13 ---
# Update Step 4 and Step 5 calculations
OLD_3_13_STEP45 = """<div class="step"><div class="step-num">4</div><div class="step-content">
Heat transfer rates without fins and with \(n\) fins:
<br>Without fins:
\[ \dot{Q}_{no\;fin} = h A_{board} (T_b - T_\infty) = (20)(0.03)(85 - 25) = 36\;W \]
With \(n\) fins attached:
\[ A_{unfin} = A_{board} - n A_b = 0.03 - 4 \times 10^{-6} n \]
\[ \dot{Q}_{total} = h \left( A_{unfin} + \eta_{fin} A_{fin} \right) (T_b - T_\infty) \]
\[ \dot{Q}_{total} = (20)(60)\left[ (0.03 - 4 \times 10^{-6} n) + (0.919)(3.2 \times 10^{-4} n) \right] \]
\[ \dot{Q}_{total} = 1200\left[ 0.03 + 2.9008 \times 10^{-4} n \right] = 36 + 0.3481\,n \]
</div></div>
<div class="step"><div class="step-num">5</div><div class="step-content">
Determine the number of fins \(n\) from required \(\varepsilon_{fin,overall} = 3\):
\[ \varepsilon_{fin,overall} = \frac{\dot{Q}_{total}}{\dot{Q}_{no\;fin}} = \frac{36 + 0.3481\,n}{36} = 3 \]
\[ 36 + 0.3481\,n = 3 \times 36 = 108 \]
\[ 0.3481\,n = 108 - 36 = 72 \]
\[ n = \frac{72}{0.3481} \approx 206.8 \approx 207\;\text{fins} \]
</div></div>"""

NEW_3_13_STEP45 = """<div class="step"><div class="step-num">4</div><div class="step-content">
Heat transfer rates without fins and with \(n\) fins:
<br>Without fins:
\[ \dot{Q}_{\text{no fin}} = h A_{\text{board}} (T_b - T_\infty) = (20)(0.03)(85 - 25) = 36\;\text{W} \]
With \(n\) fins attached:
\[ \dot{Q}_{\text{finned}} = \eta_{\text{fin}} h A_{\text{fin}} (T_b - T_\infty) = (0.919)(20)(4 \times 0.002 \times 0.04 \times n)(85 - 25) = (0.919)(20)(0.00032\,n)(60) = 0.353\,n\;\text{W} \]
\[ \dot{Q}_{\text{unfinned}} = h (A_{\text{board}} - n A_b) (T_b - T_\infty) = (20)(0.03 - 4 \times 10^{-6}\,n)(60) = 36 - 0.0048\,n\;\text{W} \]
\[ \dot{Q}_{\text{total}} = \dot{Q}_{\text{finned}} + \dot{Q}_{\text{unfinned}} = 0.353\,n + 36 - 0.0048\,n = 36 + 0.3482\,n \]
</div></div>
<div class="step"><div class="step-num">5</div><div class="step-content">
Determine the number of fins \(n\) from required \(\varepsilon_{\text{fin,overall}} = 3\):
\[ \varepsilon_{\text{fin,overall}} = \frac{\dot{Q}_{\text{total}}}{\dot{Q}_{\text{no fin}}} = \frac{36 + 0.3482\,n}{36} = 3 \]
\[ 36 + 0.3482\,n = 3 \times 36 = 108 \]
\[ 0.3482\,n = 108 - 36 = 72 \]
\[ n = \frac{72}{0.3482} \approx 206.8 \approx 207\;\text{fins} \]
</div></div>"""

if OLD_3_13_STEP45 in html:
    html = html.replace(OLD_3_13_STEP45, NEW_3_13_STEP45)
    print("Updated Example 3-13 Steps 4 and 5 calculation")
else:
    # try normalized whitespace
    old_compact = re.sub(r'\s+', ' ', OLD_3_13_STEP45).strip()
    # Let's search inside sol-ex3-13
    print("Searching for Step 4/5 in sol-ex3-13 via regex...")
    step_pattern = re.compile(
        r'<div class="step"><div class="step-num">4</div>[\s\S]*?<div class="step"><div class="step-num">5</div>[\s\S]*?</div></div>\s*(?=</div>\s*<div class="final-answer">)'
    )
    # Check if matched inside sol-ex3-13
    sol_13_pos = html.find('id="sol-ex3-13"')
    m_13 = step_pattern.search(html, sol_13_pos)
    if m_13:
        html = html[:m_13.start()] + NEW_3_13_STEP45 + html[m_13.end():]
        print("Updated Example 3-13 Steps 4 and 5 calculation via regex")
    else:
        print("WARNING: Could not find Example 3-13 Steps 4 and 5 block")

# ==============================================================================
# WRITE UPDATED HTML
# ==============================================================================
with open(FILE_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

new_len = len(html)
new_lines = len(html.splitlines())
print(f"Finished! New file size: {new_len} bytes, {new_lines} lines")
