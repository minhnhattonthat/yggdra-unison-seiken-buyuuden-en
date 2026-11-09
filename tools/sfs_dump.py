"""sfs_dump.py: extract DATA.SFS files whose names we know into work/sfs/<NAME>, unknown ones as work/sfs/_unk/<hash>_<sector>.bin.

Known names come from upper-case tokens and printf patterns in arm9 and the overlays (run tools/unpack.py first).
Prints a summary; never writes outside work/.
"""
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sfs  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


EXTS = ("", ".BIN", ".NTFT", ".NTFP", ".NTFI", ".NTFS", ".PACK", ".BI", ".LTFT")  # .PACK/.BI/.LTFT: runtime log


def expand(pat):
    """A printf pattern from the code -> every name it can produce (%d ranges guessed from the width)."""
    specs = re.findall(r"%0?(\d?)d", pat)
    if "%s" in pat or len(specs) > 2:
        return
    ranges = [range(10 ** int(w)) if w else range(1000) for w in specs]
    base = re.sub(r"%0?\d?d", "%s", pat)
    if not specs:
        yield pat
    elif len(specs) == 1:
        for i in ranges[0]:
            yield base % (f"{i:0{specs[0] or 1}d}",)
    else:
        for i in ranges[0]:
            for j in ranges[1]:
                yield base % (f"{i:0{specs[0] or 1}d}", f"{j:0{specs[1] or 1}d}")


def candidate_names():
    """Every upper-case token in arm9 and the overlays, expanded, with and without each extension."""
    pats = set()
    for f in [ROOT / "work/arm9.bin", *sorted((ROOT / "work").glob("ov9_*.bin"))]:
        pats |= {m.group(1).decode() for m in re.finditer(rb"([A-Z0-9_%.][A-Z0-9_%.ds]{2,})\x00", f.read_bytes())}
    for pat in sorted(pats):
        for n in expand(pat):
            stem = n.rsplit(".", 1)[0] if "." in n else n
            for ext in EXTS:
                yield stem + ext
            yield n


def main():
    arm9 = (ROOT / "work/arm9.bin").read_bytes()
    data = (ROOT / "work/fs/DATA.SFS").read_bytes()
    ents = sfs.read_dir(arm9, len(data))
    by_hash = {e[0]: e for e in ents}
    names = {}
    for n in candidate_names():
        h = sfs.name_hash(n)
        if h in by_hash and h not in names:
            names[h] = n
    out = ROOT / "work/sfs"
    if out.exists():
        shutil.rmtree(out)  # work/ only: stale names from an earlier run would duplicate files
    (out / "_unk").mkdir(parents=True)
    for h, size, sec in ents:
        raw = data[sec * sfs.SECTOR: sec * sfs.SECTOR + size]
        p = out / names[h] if h in names else out / "_unk" / f"{h:08x}_{sec:05d}.bin"
        p.write_bytes(raw)
    (out / "names.tsv").write_text("".join(f"{h:08x}\t{names.get(h, '')}\n" for h, _, _ in ents), encoding="utf-8")
    print(f"{len(ents)} files, {len(names)} named")


if __name__ == "__main__":
    main()
