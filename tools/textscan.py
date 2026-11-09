"""textscan.py: rank files by how much game-encoded text they hold (FF-terminated runs, mostly kana/kanji codes).

    python -X utf8 tools/textscan.py [FILES...]   (default: work/sfs/**, work/arm9.bin, work/ov9_*.bin)
Writes work/textscan.tsv: file, strings, bytes, first string decoded.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ygdecode import decode  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def strings(b, min_chars=4):
    """FF-terminated runs that parse as text: glyph bytes, F1-F5 pairs, FD newlines; >= half kana."""
    out, i, n = [], 0, len(b)
    start = 0
    while i < n:
        c = b[i]
        if c == 0xFF:
            seg = b[start:i]
            if len(seg) >= min_chars and looks_text(seg):
                out.append((start, i + 1))
            i += 1
            start = i
        elif c < 0xF0 or c == 0xFD:
            i += 1
        elif 0xF1 <= c <= 0xF5 and i + 1 < n:
            i += 2
        else:
            i += 1
            start = i
    return out


PARTICLES = {0x18, 0x15, 0x19, 0x2C, 0x2E, 0x0F, 0x13, 0x28, 0x05, 0xEA, 0xEB, 0xE0, 0xE1, 0xE8}  # のにはをがたとるか。、!?…


def looks_text(seg):
    """Graphics and code also parse as glyph bytes; real lines have particles/punctuation, varied codes, no 00 00."""
    kana = sum(1 for c in seg if c < 0x4F or 0x50 <= c < 0xA0)
    if kana * 2 < len(seg) or b"\0\0" in seg or b"\xfd\xfd" in seg:
        return False
    if not PARTICLES & set(seg):
        return False
    return len(set(seg)) * 10 >= len(seg) * 4 or len(seg) < 8


def main():
    files = [Path(f) for f in sys.argv[1:]] or [
        *sorted(p for p in (ROOT / "work/sfs").rglob("*") if p.is_file() and p.suffix != ".tsv"),
        ROOT / "work/arm9.bin", *sorted((ROOT / "work").glob("ov9_*.bin"))]
    rows = []
    for f in files:
        b = f.read_bytes()
        s = strings(b)
        if s:
            first = decode(b, s[0][0], s[0][1]).replace("\n", " ")[:60]
            rows.append((f.relative_to(ROOT).as_posix(), len(s), sum(e - a for a, e in s), first))
    rows.sort(key=lambda r: -r[2])
    (ROOT / "work/textscan.tsv").write_text("".join(f"{a}\t{b}\t{c}\t{d}\n" for a, b, c, d in rows), encoding="utf-8")
    print(len(rows), "files with text,", sum(r[1] for r in rows), "strings,", sum(r[2] for r in rows), "bytes")


if __name__ == "__main__":
    main()
