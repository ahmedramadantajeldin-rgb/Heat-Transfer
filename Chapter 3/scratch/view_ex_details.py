import sys

sys.stdout.reconfigure(encoding='utf-8')

for name in ['sol-ex3-5', 'sol-ex3-6', 'sol-ex3-7', 'sol-ex3-8', 'sol-ex3-9', 'sol-ex3-10', 'sol-ex3-11', 'sol-ex3-12', 'sol-ex3-13', 'sol-ex3-18', 'sol-ex3-19']:
    print(f"\n==================== {name} ====================")
    with open(f'scratch/ex/{name}.html', 'r', encoding='utf-8') as f:
        print(f.read())
