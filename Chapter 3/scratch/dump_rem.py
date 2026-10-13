import sys

sys.stdout.reconfigure(encoding='utf-8')

for name in ['sol-ex3-7', 'sol-ex3-8', 'sol-ex3-9', 'sol-ex3-10', 'sol-ex3-11', 'sol-ex3-12', 'sol-ex3-13', 'sol-ex3-18', 'sol-ex3-19']:
    with open(f'scratch/sols/{name}.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    with open(f'scratch/current_{name}.txt', 'w', encoding='utf-8') as f_out:
        f_out.write(text)

print("Dumped current solutions.")
