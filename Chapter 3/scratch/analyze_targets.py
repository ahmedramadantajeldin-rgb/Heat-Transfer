import sys
import re

def analyze_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_m = re.search(r'<h3>(.*?)</h3>', content)
    title = title_m.group(1) if title_m else "None"
    
    prob_m = re.search(r'<div class="problem-statement">([\s\S]*?)</div>', content)
    prob = prob_m.group(1).strip() if prob_m else "None"
    
    # Check fig
    fig_m = re.search(r'<div class="fig-container[^"]*">([\s\S]*?)</div>\s*</div>', content)
    fig = fig_m.group(0) if fig_m else "None"
    
    # Check sol-inner
    sol_inner_m = re.search(r'<div class="sol-inner">([\s\S]*?)</div>\s*</div>\s*</div>', content)
    sol_inner = sol_inner_m.group(1).strip() if sol_inner_m else "None"
    
    # Check sections in sol_inner: Given, Assumptions, Properties, Solution, Final Answer, Discussion
    sections = []
    if 'given-section' in sol_inner or '<h4>Given</h4>' in sol_inner:
        sections.append("Given")
    if 'Assumptions' in sol_inner:
        sections.append("Assumptions")
    if 'Properties' in sol_inner:
        sections.append("Properties")
    if 'solution-steps' in sol_inner:
        sections.append("Solution")
    if 'final-answer' in sol_inner:
        sections.append("Final Answer")
    if 'discussion-box' in sol_inner:
        sections.append("Discussion")
        
    return {
        'title': title,
        'has_fig': fig != "None",
        'fig_tag': fig[:100] if fig != "None" else "None",
        'sections': sections,
        'sol_len': len(sol_inner),
        'prob_len': len(prob)
    }

for name in ['sol-ex3-5', 'sol-ex3-6', 'sol-ex3-7', 'sol-ex3-8', 'sol-ex3-9', 'sol-ex3-10', 'sol-ex3-11', 'sol-ex3-12', 'sol-ex3-13', 'sol-ex3-18', 'sol-ex3-19']:
    info = analyze_file(f'scratch/ex/{name}.html')
    print(f"File: {name}")
    print(f"  Title: {info['title']}")
    print(f"  Has Fig: {info['has_fig']}")
    print(f"  Sections in solution: {', '.join(info['sections'])}")
    print(f"  Problem len: {info['prob_len']} chars | Solution len: {info['sol_len']} chars")
    print()
