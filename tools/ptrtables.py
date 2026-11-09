"""ptrtables.py: group system strings by the data table that points at them (record start, stride, field offset).

A record table = a run of pointer slots in arm9 data with one stride; each string row's `ptrs` (script/system) is
placed in the table and field it sits in. One field = one box variant, so measuring one string of a field on
screen covers every string of it (docs/re/windows.md).

    python -X utf8 tools/ptrtables.py            -> table list: start, stride, count, field: n strings, sample jp
    python -X utf8 tools/ptrtables.py --tsv OUT  -> id, table start, field (hex) per string (read by tools/lint.py)
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODE_END = 0x8F000  # arm9 pointers below this are literal pools in code, not tables


def rows():
    out = {}
    for p in sorted((ROOT / "script/system").glob("*.json")):
        for s in json.loads(p.read_text(encoding="utf-8"))["strings"]:
            out[s["id"]] = s
    return out


def tables(strings):
    """[(start, stride, n, {field: [ids]})] from arm9 data pointer slots >= CODE_END."""
    slots = {}
    for sid, s in strings.items():
        for p in s["ptrs"]:
            img, a = p.split(":")
            if img == "arm9" and int(a, 16) >= CODE_END:
                slots[int(a, 16)] = sid
    addrs = sorted(slots)
    sys.path.insert(0, str(ROOT / "tools"))
    import text
    item_at, _, item_size = text.ITEM_RECS  # known stride: the generic scan merges its 4 consecutive fields
    out, i = [], 0
    while i < len(addrs):
        best = None
        if (addrs[i] - item_at) % item_size == 8 and abs(addrs[i] - item_at) < 0x200:
            n = 1
            while addrs[i] + n * item_size in slots:
                n += 1
            best = (item_size, n)
        for stride in [] if best else (4, 8, 0xC, 0x10, 0x14, 0x18, 0x1C, 0x20, 0x24, 0x28, 0x2C, 0x30, 0x34, 0x38, 0x3C, 0x40):
            n = 1
            while addrs[i] + n * stride in slots:
                n += 1
            if n >= 3 and (best is None or n > best[1]):  # most records wins: 0x18 x 221, not 0x30 x 113
                best = (stride, n)
        if not best:
            i += 1
            continue
        stride, n = best
        start, end = addrs[i], addrs[i] + n * stride
        fields = defaultdict(list)
        for a in addrs:
            if start <= a < end + stride - 4 and a >= start:
                rec = (a - start) // stride
                if rec < n + (1 if a >= end else 0):
                    fields[(a - start) % stride].append(slots[a])
        out.append((start, stride, n, dict(fields)))
        while i < len(addrs) and addrs[i] < end + stride - 4:
            i += 1
    return out


def main():
    strings = rows()
    tabs = tables(strings)
    if "--tsv" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--tsv") + 1])
        lines = [f"{sid}\t{start:X}\t{f:X}\n" for start, _, _, fl in tabs for f, ids in fl.items() for sid in ids]
        out.write_text("".join(lines), encoding="utf-8")
        print(f"{len(lines)} rows -> {out}")
        return
    covered = set()
    for start, stride, n, fields in tabs:
        print(f"arm9 {start:X} stride {stride:X} x {n}")
        for f, ids in sorted(fields.items()):
            covered |= set(ids)
            print(f"   +{f:X}: {len(set(ids))} strings  " + " | ".join(strings[i]["jp"][:12].replace("\n", "/")
                                                                     for i in ids[:4]))
    print(f"{len(covered)} of {len(strings)} strings in a table")


if __name__ == "__main__":
    main()
