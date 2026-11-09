"""romcheck.py: ROM-level checks of an English build against the original (pipeline.md "Checks").

    python -X utf8 tools/romcheck.py [build/yggdra_en.nds]      exit 1 on any error

- Code images (arm9 main section, every overlay): romdiff.check with the allowed bytes from the sources: system
  string slots (`max` bytes), their pointer words (`ptrs`), engine.SITES / OV_SITES, the arena-lo literals. Other
  arm9 sections are unchanged except ITCM growing (the hook blob); the only new section is the EXTRA block.
- System strings: every pointer word of a row reaches a string that decodes to the row's en (or its original
  bytes when en is empty), and no word in any built image still points at a vacated slot.
- DATA.SFS: every file but the fonts and the script files is byte-identical. Each script file's bytecode is the
  original bar its string refs, and its strings decode to script/ en in order (control codes and line breaks
  included); the count written equals the count of strings with English.
"""
import json
import struct
import sys
from pathlib import Path

import ndspy.code

sys.path.insert(0, str(Path(__file__).resolve().parent))
import engine  # noqa: E402
import enfont  # noqa: E402
import insert  # noqa: E402
import romdiff  # noqa: E402
import sfs  # noqa: E402
import sysreloc  # noqa: E402
import text  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def sections(arm9):
    return {s.ramAddress: s for s in ndspy.code.MainCodeFile(arm9, 0x02000000).sections}


def system_rows():
    for p in sorted((ROOT / "script/system").glob("*.json")):
        yield from json.loads(p.read_text(encoding="utf-8"))["strings"]


def allowed_code(rows):
    """{image: set of offsets the build may change}."""
    ok = {}
    for r in rows:
        img, off = r["id"].split(":")
        ok.setdefault(img, set()).update(range(int(off, 16), int(off, 16) + r["max"]))
        for p in r["ptrs"]:
            pimg, poff = p.split(":")
            ok.setdefault(pimg, set()).update(range(int(poff, 16), int(poff, 16) + 4))
    for site, _, _ in engine.SITES:
        ok["arm9"].update(range(site - 0x02000000, site - 0x02000000 + 4))
    for a in engine.ARENA_LO:
        ok["arm9"].update(range(a - 0x02000000, a - 0x02000000 + 4))
    ok["arm9"].update(range(0xBA0, 0xBA8))  # module params: autoload list start / end (ndspy, new sections)
    data, arm9 = text._sfs(text.ORIG)
    for n in range(len(sfs.read_dir(arm9, len(data)))):  # DATA.SFS directory: size + sector of each entry (build.rebuild_sfs), not the hash
        ok["arm9"].update(range(sfs.DIR_OFF + 12 * n + 4, sfs.DIR_OFF + 12 * n + 12))
    for img, site, _, _ in engine.OV_SITES:
        ok.setdefault(img, set()).update(range(site - engine.OV_BASE, site - engine.OV_BASE + 4))
    return ok


def check_code(orig, new, rows):
    errs = []
    so, sn = sections(orig["arm9"]), sections(new["arm9"])
    for ram in sorted(set(so) | set(sn)):
        if ram not in so:
            if ram != sysreloc.EXTRA:
                errs.append(f"arm9: unexpected new section at {ram:#x}")
        elif ram not in sn:
            errs.append(f"arm9: section {ram:#x} gone")
        elif ram == engine.ITCM:
            if bytes(sn[ram].data)[:len(so[ram].data)] != bytes(so[ram].data):
                errs.append("arm9: ITCM original code changed")
        elif ram != 0x02000000 and bytes(sn[ram].data) != bytes(so[ram].data):
            errs.append(f"arm9: section {ram:#x} changed")
    main_o, main_n = bytes(so[0x02000000].data), bytes(sn[0x02000000].data)
    ok = allowed_code(rows)
    pairs = [("arm9", main_o, main_n)] + [(k, orig[k], new[k]) for k in orig if k != "arm9"]
    for img, a, b in pairs:
        if len(a) != len(b):
            errs.append(f"{img}: size {len(a):#x} -> {len(b):#x}")
            continue
        e, _ = romdiff.check(a, b, ok.get(img, set()), [])
        errs += [f"{img}: {m}" for m in e]
    return errs


def check_system(orig, new, rows):
    errs = []
    sn = sections(new["arm9"])
    mem = [(ram, bytes(s.data)) for ram, s in sn.items()]

    def at(img, addr):
        if img != "arm9" and sysreloc.OVL_BASE <= addr < sysreloc.OVL_BASE + len(new[img]):  # EXTRA sits above
            return new[img], addr - sysreloc.OVL_BASE
        for ram, d in mem:
            if ram <= addr < ram + len(d):
                return d, addr - ram
        raise KeyError(f"{addr:#x} in no arm9 section")

    vacated = {}
    for r in rows:
        img, off = r["id"].split(":")
        off = int(off, 16)
        o = orig[img]
        want = insert.encode(r["en"]) if r["en"] else o[off:o.index(b"\xff", off)]
        for p in r["ptrs"]:
            pimg, poff = p.split(":")
            buf = main_or(new, pimg)
            addr = struct.unpack_from("<I", buf, int(poff, 16))[0]
            d, i = at(pimg, addr)
            got = d[i:d.index(b"\xff", i)]
            if got != want:
                errs.append(f"{r['id']}: pointer {p} -> {addr:#x} reads {got.hex()}, want {want.hex()}")
            if addr != sysreloc.base(img) + off:
                vacated.setdefault(img, set()).add(off)
    for img, offs in vacated.items():
        lo, hi = min(offs), max(offs) + 1
        imgs = {k: main_or(new, k) for k in new}
        for v, sites in text.pointer_sites(imgs, img, lo, hi).items():
            if v in offs:
                errs.append(f"{img}:{v:X} vacated, still pointed at from {sites}")
    return errs


def main_or(images, img):
    """arm9 -> its main section bytes (offsets match the original arm9); overlays as they are."""
    return bytes(sections(images["arm9"])[0x02000000].data) if img == "arm9" else images[img]


def check_sfs(orig_files, new_files):
    errs = []
    if set(orig_files) != set(new_files):
        errs.append(f"DATA.SFS: named files differ: {sorted(set(orig_files) ^ set(new_files))[:5]}")
    script = text.text_files(orig_files)
    written = expected = 0
    for name, b in orig_files.items():
        nb = new_files.get(name)
        if nb is None or name in enfont.FONTS:
            continue
        if name not in script:
            if nb != b:
                errs.append(f"{name}: changed (not a font or script file)")
            continue
        sa, strs, refs, _ = text.layout(name, b)
        # no check_layout: UNREF_OK names strings by their original offset
        nsa, nstrs, nrefs, _ = (text._edmes if text.family(name)[0] == "edmes" else text._bytecode)(nb)
        fields = {a for a, _ in refs}
        if nsa != sa or [a for a, _ in nrefs] != [a for a, _ in refs] or \
                any(nb[i] != b[i] for i in range(sa) if not any(f <= i < f + 4 for f in fields)):
            errs.append(f"{name}: bytecode changed outside string refs")
            continue
        rows = {r["id"]: r for r in text.load(name)["strings"]}
        if len(nstrs) != len(strs):
            errs.append(f"{name}: {len(nstrs)} strings, original {len(strs)}")
            continue
        old_of = {s: n for n, (s, _) in enumerate(strs)}
        new_of = {s: n for n, (s, _) in enumerate(nstrs)}
        if [old_of[t] for _, t in refs] != [new_of[t] for _, t in nrefs]:
            errs.append(f"{name}: a ref points at a different string")
        for (s, e), (ns, ne) in zip(strs, nstrs):
            r = rows[text.sid(name, s)]
            expected += bool(r["en"])
            want = insert.encode(r["en"]) if r["en"] else b[s:e - 1]
            if nb[ns:ne - 1] != want:
                errs.append(f"{r['id']}: built bytes differ from script/")
            else:
                written += bool(r["en"])
    if written != expected:
        errs.append(f"script files: {written} strings in English, {expected} expected")
    return errs, written


def selftest():
    rows = [{"id": "ov9_01:10", "max": 4, "ptrs": ["arm9:20"]}]
    ok = allowed_code(rows)
    assert set(range(0x10, 0x14)) <= ok["ov9_01"] and 0x23 in ok["arm9"] and 0x24 not in ok["arm9"]


def run(built):
    """-> (errors, script strings checked, system strings checked) for the built ROM at path built."""
    selftest()
    rows = list(system_rows())
    orig, new = text.code_images(), text.code_images(built)
    errs = check_code(orig, new, rows) + check_system(orig, new, rows)
    e, n = check_sfs(text.sfs_files(), text.sfs_files(rom_path=built))
    return errs + e, n, len(rows)


def main():
    errs, n, nsys = run(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "build/yggdra_en.nds")
    for m in errs[:100]:
        print(m)
    print(f"romcheck: {n} script strings + {nsys} system strings checked, {len(errs)} errors")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
