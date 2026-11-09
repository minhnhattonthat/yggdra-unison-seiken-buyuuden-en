"""bytefind.py: find a hex byte pattern in arm9, overlays and every DATA.SFS file (recon helper).

    python tools/bytefind.py "00 01 02 03" [--max 20]
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def targets():
    w = ROOT / "work"
    yield from [w / "arm9.bin", *sorted(w.glob("ov9_*.bin")), *sorted(w.glob("arm9_0*.bin"))]
    yield from sorted(p for p in (w / "sfs").rglob("*") if p.is_file() and p.suffix != ".tsv")


def main():
    pat = bytes.fromhex(sys.argv[1].replace(" ", ""))
    mx = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 20
    n = 0
    for p in targets():
        b = p.read_bytes()
        i = b.find(pat)
        while i >= 0 and n < mx:
            print(f"{p.relative_to(ROOT / 'work')}\t{i:#x}\t{b[max(0, i - 8):i + len(pat) + 16].hex(' ')}")
            n += 1
            i = b.find(pat, i + 1)
    print(f"{n} hits")


if __name__ == "__main__":
    main()
