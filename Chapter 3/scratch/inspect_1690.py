with open('chapter3.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1690, 1740):
    print(f"{i+1}: {repr(lines[i])}")
