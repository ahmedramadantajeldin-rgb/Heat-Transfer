with open('scratch/enhance.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace("FILE_PATH = 'chapter3.html'", "FILE_PATH = 'scratch/test_chapter3.html'")
code = code.replace("BAK_PATH = 'chapter3.html.bak'", "BAK_PATH = 'scratch/test_chapter3.html.bak'")

with open('scratch/test_enhance.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Created scratch/test_enhance.py")
