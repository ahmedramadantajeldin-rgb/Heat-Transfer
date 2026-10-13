with open('scratch/current_sol-ex3-18.txt', 'w', encoding='utf-8') as f:
    pass

for ex in ['3-1', '3-2', '3-3', '3-4']:
    with open(f'scratch/sols/sol-ex{ex}.txt', 'r', encoding='utf-8') as f:
        print(f"=== Example {ex} ===")
        lines = f.readlines()
        print(''.join(lines[:15]))
