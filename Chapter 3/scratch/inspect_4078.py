with open('chapter3.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(4074, 4095):
    print(f"{i+1}: {lines[i]}", end='')
