import glob
import os

with open('scratch/read_sols_out.txt', 'w', encoding='utf-8') as out_f:
    files = glob.glob('scratch/sols/*.txt')
    for fpath in sorted(files):
        fname = os.path.basename(fpath)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        out_f.write(f"***** {fname} ({len(content)} chars) *****\n")
        lines = content.splitlines()
        for l in lines[:40]:
            out_f.write(l + "\n")
        if len(lines) > 40:
            out_f.write(f"... ({len(lines)-40} more lines) ...\n")
            for l in lines[-15:]:
                out_f.write(l + "\n")
        out_f.write("\n" + "="*50 + "\n\n")

print("Wrote scratch/read_sols_out.txt")
