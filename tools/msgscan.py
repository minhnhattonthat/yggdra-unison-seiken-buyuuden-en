"""msgscan.py: string refs in bytecode text files (MESSAGE/SPMES/TUTO); recon + coverage report.

    python -X utf8 tools/msgscan.py [--verbose]

Header: u32 ?, u32 n, u32 table_off, n x u32 entry offsets into bytecode. Bytecode refers to a string with
`30 xx <u32 file offset>`; strings are FF-terminated after the bytecode. See docs/re/text.md.
Reports per family: files, strings, refs, strings no `30` op reaches, refs not on a string start, and
the non-glyph bytes seen inside strings.
"""
import re
import struct
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SFS = ROOT / "work/sfs"
FAMILIES = [("MESSAGE", r"MESSAGE\d+\.BIN"), ("SPMES", r"SPMES.*\.BIN"), ("TUTO", r"TUTO.*\.BIN")]


def header(b):
    _, n, toff = struct.unpack_from("<3I", b, 0)
    return list(struct.unpack_from(f"<{n}I", b, toff)) if toff + 4 * n <= len(b) else []


def refs(b):
    """(op_pos, target) for every `30 0x u32` (message) or `51 u32` (string arg) whose target falls inside the
    file past the op. 51 hits are kept only when they land on a string start (checked by the caller)."""
    out = []
    for m in re.finditer(rb"\x30[\x00\x01]|\x51", b):
        p = m.start()
        a = p + (2 if b[p] == 0x30 else 1)
        if a + 4 <= len(b):
            t = struct.unpack_from("<I", b, a)[0]
            if p < t < len(b):
                out.append((p, t))
    return out


def string_area(b, rs):
    """Start of the string area: the lowest `30` ref target; strings run FF-terminated to EOF (zero pad allowed)."""
    ts = [t for p, t in rs if b[p] == 0x30]
    return min(ts) if ts else len(b)


def split_strings(b, start):
    out, i = [], start
    while i < len(b):
        j = b.find(b"\xff", i)
        if j < 0:
            break
        out.append((i, j + 1))
        i = j + 1
    return out, b[i:]


def controls(seg):
    """Non-glyph bytes in a string (F1-F5 take one argument byte)."""
    c, i = Counter(), 0
    while i < len(seg):
        x = seg[i]
        if 0xF1 <= x <= 0xF5:
            i += 2
            continue
        if x >= 0xF0:
            c[x] += 1
        i += 1
    return c


def main():
    verbose = "--verbose" in sys.argv
    for fam, pat in FAMILIES:
        files = sorted(p for p in SFS.iterdir() if re.fullmatch(pat, p.name))
        tot = Counter()
        ctl = Counter()
        bad = defaultdict(list)
        for p in files:
            b = p.read_bytes()
            rs = refs(b)
            sa = string_area(b, rs)
            strs, tail = split_strings(b, sa)
            starts = {s for s, _ in strs}
            rs = [(p, t) for p, t in rs if b[p] == 0x30 or (t in starts and p < sa)]
            hit = {t for _, t in rs}
            tot["files"] += 1
            tot["strings"] += len(strs)
            tot["refs"] += len(rs)
            for s, e in strs:
                ctl.update(controls(b[s:e - 1]))
                if s not in hit:
                    bad["unref"].append(f"{p.name}:{s:X}")
            for op, t in rs:
                if t not in starts:
                    bad["offstart"].append(f"{p.name}:{op:X}->{t:X}")
            if tail.strip(b"\0"):
                bad["tail"].append(f"{p.name}:{len(b) - len(tail):X}")
            if any(e >= sa for e in header(b)):
                bad["entry_in_strings"].append(p.name)
        print(f"{fam}: {dict(tot)} controls={ {f'{k:02X}': v for k, v in sorted(ctl.items())} }")
        for k, v in bad.items():
            print(f"  {k}: {len(v)}  {v[:8] if not verbose else v}")


if __name__ == "__main__":
    main()
