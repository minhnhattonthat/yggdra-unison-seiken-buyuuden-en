"""sysmap.py: which system string is drawn where (width gate, docs/re/windows.md "System text").

Reads systrace.lua logs from a marker-build run (each drawn string starts with its base-36 marker code,
work/marker_ids.tsv) and writes work/sysmap.tsv: id, scene, kind (run / ctr), x, y, font, caller, jp.

    python -X utf8 tools/debug/regen.py --rom build/yggdra_marker.nds --qa work/qa/sys --script tools/lua/systrace.lua
    python -X utf8 tools/sysmap.py [work/qa/sys]      -> work/sysmap.tsv + summary (drawn ids per image)
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tbl import Table  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
LINE = re.compile(r"sys (\d+) (run|ctr) lr=(\w+) x=(-?\d+) y=(-?\d+) font=(\d+) scene=(\d+) ptr=(\w+) (\w+)")


def parse(line):
    m = LINE.match(line)
    if not m:
        return None
    f, kind, lr, x, y, font, scene, ptr, hexb = m.groups()
    return dict(frame=int(f), kind=kind, lr=lr, x=int(x), y=int(y), font=int(font), scene=int(scene), ptr=ptr,
                raw=bytes.fromhex(hexb))


def code_of(text):
    """marker text -> base-36 code (before ':' or the first non-code char); None for non-marker text."""
    m = re.match(r"([0-9a-z]+)(:|$|\n)", text)
    return m.group(1) if m else None


def main():
    qa = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "work/qa/sys"
    en = Table.load(ROOT / "tbl/en.tbl")
    ids = {}
    for row in (ROOT / "work/marker_ids.tsv").read_text(encoding="utf-8").splitlines():
        code, sid, jp = row.split("\t", 2)
        ids[code] = (sid, jp)
    rows, other = set(), set()
    for log in sorted(qa.glob("*/log.txt")):
        for line in log.read_text(encoding="utf-8", errors="replace").splitlines():
            d = parse(line)
            if not d:
                continue
            raw = d["raw"].split(b"\xff")[0]
            text = en.decode(raw, length=len(raw))[0].replace("{br}", "\n")
            code = code_of(text)
            if code in ids:
                sid, jp = ids[code]
                rows.add((sid, log.parent.name, d["kind"], d["x"], d["y"], d["font"], d["lr"], jp.replace("\n", "/")))
            else:
                other.add((log.parent.name, d["kind"], d["x"], d["y"], d["lr"], text[:40].replace("\n", "/")))
    out = ROOT / "work/sysmap.tsv"
    out.write_text("".join("\t".join(map(str, r)) + "\n" for r in sorted(rows)), encoding="utf-8")
    drawn = {r[0] for r in rows}
    per = {}
    for sid in drawn:
        per[sid.split(":")[0]] = per.get(sid.split(":")[0], 0) + 1
    print(f"{len(drawn)} system ids drawn ({len(rows)} draws) -> {out}; by image: {per}")
    print(f"{len(other)} draws without a marker code (runtime-built text):")
    for o in sorted(other)[:60]:
        print("  ", *o)


if __name__ == "__main__":
    main()
