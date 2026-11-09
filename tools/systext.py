"""systext.py: system/menu strings (FONT_SYSTEM order) in arm9 and overlays, found through u32 pointers.

    python -X utf8 tools/systext.py      -> work/systext.tsv (image, offset, ptr count, ptr sites, text)

A string = FF-terminated run of valid codes (bytes < F0, F1-F3 + arg, FD) that some aligned u32 in the same image
(or in arm9, for overlay strings arm9 can't see: overlays only) points at. arm9 loads at 0x02000000, every
overlay at 0x0211B780. See docs/re/text.md §System text.
"""
import struct
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ygdecode  # noqa: E402
from mkjptbl import chars  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ARM9, OVL = 0x02000000, 0x0211B780


def images():
    w = ROOT / "work"
    yield "arm9", ARM9, (w / "arm9.bin").read_bytes()
    for p in sorted(w.glob("ov9_*.bin")):
        yield p.stem, OVL, p.read_bytes()


def run_end(b, i):
    """End (index of FF) of a valid text run starting at i, or -1. Empty runs (FF at i) are rejected."""
    j = i
    while j < len(b):
        c = b[j]
        if c == 0xFF:
            return j if j > i else -1
        if c < 0xF0 or c == 0xFD:
            j += 1
        elif 0xF1 <= c <= 0xF9 and j + 1 < len(b) and b[j + 1] < 0xF0:
            j += 2
        else:
            return -1
    return -1


def scan(name, base, b):
    """{offset: [ptr sites]} for pointers in b to valid runs in b."""
    hits = defaultdict(list)
    for o in range(0, len(b) - 3, 4):
        v = struct.unpack_from("<I", b, o)[0] - base
        if 0 <= v < len(b) and run_end(b, v) > 0:
            hits[v].append(o)
    return hits


def plausible(seg):
    """Reject code/data that happens to parse: need >= 2 codes and mostly kana/latin/kanji, no 00 00."""
    return len(seg) >= 2 and b"\0\0" not in seg


def main():
    ygdecode.CH = chars("sys")
    rows = []
    for name, base, b in images():
        for off, sites in sorted(scan(name, base, b).items()):
            e = run_end(b, off)
            if plausible(b[off:e]):
                txt = ygdecode.decode(b, off, e).replace("\n", "")
                rows.append((name, off, len(sites), " ".join(f"{s:X}" for s in sites[:6]), txt))
    out = ROOT / "work/systext.tsv"
    out.write_text("".join(f"{a}\t{b:X}\t{c}\t{d}\t{e}\n" for a, b, c, d, e in rows), encoding="utf-8")
    per = defaultdict(int)
    for r in rows:
        per[r[0]] += 1
    print(len(rows), "strings", dict(per))


if __name__ == "__main__":
    main()
