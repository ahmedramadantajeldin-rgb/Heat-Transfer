import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('chapter3.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

def print_range(start, end, label):
    print(f"=== {label} (Lines {start}-{end}) ===")
    for i in range(start-1, min(end, len(lines))):
        print(f"{i+1}: {lines[i]}", end='')
    print("\n" + "="*50 + "\n")

# Let's inspect Example 3-5 (around 1731 to 1852)
print_range(1730, 1853, "Example 3-5")

# Example 3-6 (around 1853 to 1950)
print_range(1853, 1960, "Example 3-6 start")
