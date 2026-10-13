import re

with open("chapter3.html", "r", encoding="utf-8") as f:
    text = f.read()

proofs = re.findall(r'id=[\'"](proof-[^\'"]+)[\'"]', text)
print(f"Total proof bodies: {len(proofs)}")
for p in proofs:
    print(" ", p)

btn_controls = re.findall(r'aria-controls=[\'"](proof-[^\'"]+)[\'"]', text)
print(f"Total proof buttons: {len(btn_controls)}")
for b in btn_controls:
    print(" ", b)

assert len(proofs) == len(btn_controls)
for p, b in zip(proofs, btn_controls):
    assert p == b, f"Mismatch: {p} vs {b}"

print("All proof IDs and button aria-controls match 100% perfectly!")
