#!/usr/bin/env python3
"""
Assembly script: Splice new Topics 11-13 content into chapter3.html
and add CSS/JS for derivation toggles and table reference modals.
"""
import re, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(BASE, 'chapter3.html')
OUT  = os.path.join(BASE, 'chapter3.html')  # overwrite in place
SCRATCH = os.path.dirname(os.path.abspath(__file__))

# ── Read original ──
with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

lines = html.split('\n')

# ── Find section boundaries ──
sec11_start = None
sec13_end   = None   # line AFTER </section> and <hr> for sec13

for i, line in enumerate(lines):
    if '<!-- ==================== SECTION 11 ====================' in line:
        sec11_start = i
    if sec11_start is not None and i > sec11_start:
        # Find end of section 13 — look for the Key Relations Summary section
        if '<!-- ==================== KEY RELATIONS SUMMARY ====================' in line:
            sec13_end = i
            break

if sec11_start is None or sec13_end is None:
    # Try alternate approach: find the section-divider before Key Relations
    for i, line in enumerate(lines):
        if '<!-- ==================== SECTION 11 ====================' in line:
            sec11_start = i
    # Find the Key Relations section header
    for i in range(len(lines)-1, sec11_start, -1):
        if 'Key Relations Summary' in lines[i]:
            # Go back to find the section tag or divider before it
            for j in range(i, sec11_start, -1):
                if '<section class="section">' in lines[j] or '<!-- =====' in lines[j]:
                    sec13_end = j
                    break
            break

print(f"Section 11 starts at line {sec11_start}")
print(f"Key Relations starts at line {sec13_end}")

# ── Read topic fragments ──
with open(os.path.join(SCRATCH, 'topic11.html'), 'r', encoding='utf-8') as f:
    topic11 = f.read()
with open(os.path.join(SCRATCH, 'topic12.html'), 'r', encoding='utf-8') as f:
    topic12 = f.read()
with open(os.path.join(SCRATCH, 'topic13.html'), 'r', encoding='utf-8') as f:
    topic13 = f.read()

# ── New CSS to inject ──
NEW_CSS = """
/* ===== DERIVATION TOGGLE ===== */
.deriv-toggle-row{margin:14px 0 6px;}
.deriv-toggle{
  display:inline-flex;align-items:center;gap:8px;
  background:linear-gradient(135deg,#e8f4fd,#d6eaf8);
  color:var(--royal);border:2px solid var(--sky);
  border-radius:999px;padding:8px 18px;
  cursor:pointer;font-family:'Cairo',sans-serif;
  font-size:0.88rem;font-weight:700;
  transition:all .25s ease;
}
.deriv-toggle:hover{background:var(--sky);color:var(--white);box-shadow:0 4px 14px rgba(46,134,193,0.25);}
.deriv-toggle:active{transform:scale(0.97);}
.deriv-toggle:focus-visible{outline:3px solid var(--azure);outline-offset:3px;}
.deriv-toggle .deriv-arrow{display:inline-block;font-size:0.8em;line-height:1;transition:transform .35s ease;}
.deriv-toggle[aria-expanded="false"] .deriv-arrow{transform:rotate(180deg);}
.deriv-wrap{
  display:grid;grid-template-rows:1fr;opacity:1;visibility:visible;
  transition:grid-template-rows .4s ease,opacity .3s ease;
}
.deriv-wrap.is-hidden{
  grid-template-rows:0fr;opacity:0;visibility:hidden;
  transition:grid-template-rows .4s ease,opacity .3s ease,visibility 0s linear .4s;
}
.deriv-inner{min-height:0;overflow:hidden;}
.deriv-wrap:not(.is-hidden) .deriv-inner{overflow:visible;}
@media print{
  .deriv-toggle-row{display:none !important;}
  .deriv-wrap{grid-template-rows:1fr !important;opacity:1 !important;visibility:visible !important;transition:none !important;}
  .deriv-inner{overflow:visible !important;}
}

/* ===== TABLE REFERENCE BUTTON ===== */
.table-ref-btn{
  display:inline-flex;align-items:center;gap:6px;
  background:var(--royal);color:var(--white);
  border:none;border-radius:var(--radius-sm);
  padding:6px 14px;cursor:pointer;
  font-family:'Cairo',sans-serif;font-size:0.85rem;font-weight:600;
  transition:background .2s,box-shadow .2s;
}
.table-ref-btn:hover{background:var(--navy);box-shadow:0 4px 12px rgba(11,36,71,0.2);}
.table-ref-btn:focus-visible{outline:2px solid var(--amber);outline-offset:2px;}
.table-ref-icon{font-size:1rem;}

/* ===== TABLE MODAL ===== */
.table-modal-overlay{
  display:none;position:fixed;inset:0;z-index:10001;
  background:rgba(11,36,71,0.75);backdrop-filter:blur(4px);
  justify-content:center;align-items:center;padding:20px;
}
.table-modal-overlay.is-active{display:flex;}
.table-modal-content{
  position:relative;background:var(--white);
  border-radius:var(--radius);box-shadow:var(--shadow-lg);
  max-width:95vw;max-height:90vh;overflow:auto;padding:24px;
}
.table-modal-content img{max-width:100%;height:auto;display:block;margin:0 auto;}
.table-modal-close{
  position:absolute;top:12px;right:12px;
  width:36px;height:36px;border-radius:50%;
  background:var(--coral);color:var(--white);
  border:none;cursor:pointer;font-size:1.2rem;
  display:flex;align-items:center;justify-content:center;
  transition:background .2s,transform .15s;z-index:2;
}
.table-modal-close:hover{background:#c0392b;transform:scale(1.1);}
.table-modal-close:focus-visible{outline:3px solid var(--amber);outline-offset:2px;}
.table-modal-title{
  font-family:'Playfair Display',serif;font-weight:700;
  color:var(--navy);font-size:1.1rem;margin-bottom:14px;
  text-align:center;padding-right:40px;
}
.table-modal-actions{
  display:flex;justify-content:center;gap:12px;margin-top:16px;
}
.table-modal-download{
  display:inline-flex;align-items:center;gap:6px;
  background:var(--mint);color:var(--white);
  border:none;border-radius:var(--radius-sm);
  padding:8px 18px;cursor:pointer;
  font-family:'Cairo',sans-serif;font-size:0.85rem;font-weight:600;
  transition:background .2s;
}
.table-modal-download:hover{background:#148F77;}
"""

# ── New JS to inject ──
NEW_JS = """
// ===== DERIVATION TOGGLES (visible by default) =====
(function(){
  document.querySelectorAll('.deriv-toggle').forEach(function(btn){
    var wrap = document.getElementById(btn.getAttribute('aria-controls'));
    if(!wrap) return;
    var arrow = btn.querySelector('.deriv-arrow');
    var label = btn.querySelector('.deriv-label');
    btn.addEventListener('click', function(){
      var isOpen = btn.getAttribute('aria-expanded') === 'true';
      if(isOpen){
        btn.setAttribute('aria-expanded','false');
        wrap.classList.add('is-hidden');
        if(arrow) arrow.textContent = '\\u25BC';
        if(label) label.textContent = 'Show Derivation';
      } else {
        btn.setAttribute('aria-expanded','true');
        wrap.classList.remove('is-hidden');
        if(arrow) arrow.textContent = '\\u25B2';
        if(label) label.textContent = 'Hide Derivation';
      }
    });
  });
})();

// ===== TABLE REFERENCE MODAL =====
(function(){
  // Table metadata
  var tables = {
    'table-3-3':  {src:'images/table-3-3.jpg',  title:'Table 3\\u20133: Efficiency of Common Fin Geometries'},
    'table-3-4':  {src:'images/table-3-4.png',  title:'Table 3\\u20134: Modified Bessel Function Values'},
    'table-3-8':  {src:'images/table-3-8.png',  title:'Table 3\\u20138: R-Values of Building and Insulating Materials'},
    'table-3-9':  {src:'images/table-3-9.png',  title:'Table 3\\u20139: Unit Thermal Resistance of Surfaces'},
    'table-3-10': {src:'images/table-3-10.png', title:'Table 3\\u201310: Emissivities and Effective Emissivities'},
    'table-3-11': {src:'images/table-3-11.png', title:'Table 3\\u201311: Thermal Resistance of Sealed Air Spaces'}
  };

  // Create modal overlay once
  var overlay = document.createElement('div');
  overlay.className = 'table-modal-overlay';
  overlay.innerHTML =
    '<div class="table-modal-content">' +
    '<button class="table-modal-close" aria-label="Close">&times;</button>' +
    '<div class="table-modal-title"></div>' +
    '<img src="" alt="">' +
    '<div class="table-modal-actions">' +
    '<button class="table-modal-download">\\u2B07 Download Image</button>' +
    '</div>' +
    '</div>';
  document.body.appendChild(overlay);

  var content   = overlay.querySelector('.table-modal-content');
  var closeBtn  = overlay.querySelector('.table-modal-close');
  var titleEl   = overlay.querySelector('.table-modal-title');
  var imgEl     = overlay.querySelector('.table-modal-content img');
  var dlBtn     = overlay.querySelector('.table-modal-download');
  var currentSrc = '';

  function openModal(key){
    var t = tables[key];
    if(!t) return;
    titleEl.textContent = t.title;
    imgEl.src = t.src;
    imgEl.alt = t.title;
    currentSrc = t.src;
    overlay.classList.add('is-active');
    document.body.style.overflow = 'hidden';
    closeBtn.focus();
  }
  function closeModal(){
    overlay.classList.remove('is-active');
    document.body.style.overflow = '';
  }

  closeBtn.addEventListener('click', closeModal);
  overlay.addEventListener('click', function(e){
    if(e.target === overlay) closeModal();
  });
  document.addEventListener('keydown', function(e){
    if(e.key === 'Escape' && overlay.classList.contains('is-active')) closeModal();
  });

  // Download button
  dlBtn.addEventListener('click', function(){
    if(!currentSrc) return;
    var a = document.createElement('a');
    a.href = currentSrc;
    a.download = currentSrc.split('/').pop();
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  });

  // Bind all table-ref-btn buttons
  document.querySelectorAll('.table-ref-btn').forEach(function(btn){
    btn.addEventListener('click', function(){
      var key = btn.getAttribute('data-table');
      if(key) openModal(key);
    });
  });
})();
"""

# ── Inject CSS ──
# Find the closing </style> tag in the <head> (inline styles)
css_inject_marker = '</style>'
css_inject_pos = html.find(css_inject_marker)
if css_inject_pos > 0:
    html = html[:css_inject_pos] + NEW_CSS + '\n' + html[css_inject_pos:]
    print("CSS injected successfully")
else:
    print("WARNING: Could not find </style> to inject CSS")

# ── Rebuild lines after CSS injection ──
lines = html.split('\n')

# ── Re-find section boundaries after CSS injection ──
sec11_start = None
sec13_end   = None

for i, line in enumerate(lines):
    if '<!-- ==================== SECTION 11 ====================' in line:
        sec11_start = i
    if sec11_start is not None and i > sec11_start:
        if '<!-- ==================== KEY RELATIONS SUMMARY ====================' in line:
            sec13_end = i
            break

# If KEY RELATIONS marker not found exactly, search more broadly
if sec13_end is None:
    for i in range(len(lines)-1, max(0, (sec11_start or 0)), -1):
        if 'Key Relations Summary' in lines[i]:
            # Back up to find the start of this section block
            for j in range(i, max(0, (sec11_start or 0)), -1):
                stripped = lines[j].strip()
                if stripped.startswith('<!-- =====') or stripped.startswith('<section class="section">'):
                    sec13_end = j
                    break
            break

print(f"After CSS injection: Section 11 starts at line {sec11_start}, Key Relations at line {sec13_end}")

if sec11_start is None or sec13_end is None:
    raise RuntimeError("Could not find section boundaries!")

# ── Replace sections 11-13 ──
new_content = topic11.rstrip('\r\n') + '\n\n' + topic12.rstrip('\r\n') + '\n\n' + topic13.rstrip('\r\n') + '\n\n'

before = lines[:sec11_start]
after  = lines[sec13_end:]

html_new = '\n'.join(before) + '\n' + new_content + '\n'.join(after)

# ── Inject JS before the last </script> before </body> ──
# Find the last </script> tag
last_script_end = html_new.rfind('</script>')
if last_script_end > 0:
    html_new = html_new[:last_script_end] + '\n' + NEW_JS + '\n' + html_new[last_script_end:]
    print("JS injected successfully")
else:
    print("WARNING: Could not find </script> to inject JS")

# ── Update TOC entries for sections 11-13 ──
html_new = html_new.replace(
    '<a class="toc-item" href="#sec11"><span class="toc-num">11</span>Fin Effectiveness &amp; Efficiency</a>',
    '<a class="toc-item" href="#sec11"><span class="toc-num">11</span>Extended Surfaces — Fins</a>'
)
html_new = html_new.replace(
    '<a class="toc-item" href="#sec12"><span class="toc-num">12</span>Fin Design &amp; Heat Sinks</a>',
    '<a class="toc-item" href="#sec12"><span class="toc-num">12</span>Fin Effectiveness &amp; Design</a>'
)
html_new = html_new.replace(
    '<a class="toc-item" href="#sec13"><span class="toc-num">13</span>Heat Transfer: Walls &amp; Roofs</a>',
    '<a class="toc-item" href="#sec13"><span class="toc-num">13</span>Walls, Roofs &amp; Insulation</a>'
)

# ── Write output ──
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html_new)

# ── Stats ──
new_lines = html_new.split('\n')
print(f"\nDone! Output: {OUT}")
print(f"Original lines: {len(lines)}")
print(f"New lines: {len(new_lines)}")
print(f"File size: {len(html_new)} bytes ({len(html_new)/1024:.1f} KB)")
