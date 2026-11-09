"""text.py: game text files <-> script/<family>/<FILE>.json. Formats in docs/re/text.md.

    python -X utf8 tools/text.py dump [--force]   original ROM -> script/*.json. Without --force only missing files are
                                                  written; --force refreshes every jp (after new kanji readings) and
                                                  keeps every en by id.
    python -X utf8 tools/text.py stats            strings / translated per family

Families: MESSAGE/SPMES/TUTO (bytecode script, FONT_MES), EDMES (ending records, FONT_END). A string's id is
FILE:OFFSET (hex, original file). jp/en use "\n" for the FD line break and {col:XX} for the FC colour code.
rebuild() re-lays a file's string area with new strings and rewrites every pointer to them (insertion, phase 7).
"""
import json
import re
import struct
import sys
from functools import cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mkjptbl  # noqa: E402
import sfs  # noqa: E402
from tbl import Table  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ORIG = ROOT / "rom/yggdra.nds"
SCRIPT = ROOT / "script"
FAMILIES = [("message", r"MESSAGE\d{3}\.BIN", "mes"), ("spmes", r"SPMES\w+\.BIN", "mes"),
            ("tuto", r"TUTO\d\d_\d\d\.BIN", "mes"), ("edmes", r"EDMES\d\d\.BIN", "end")]
UNREF_OK = {"MESSAGE000:0A78"}  # test-file line no op reaches (text.md)


@cache
def names():
    """{hash: name} for the 3,846 named DATA.SFS files (tbl/sfs_names.tsv, from tools/sfs_dump.py)."""
    rows = (ln.split("\t") for ln in (ROOT / "tbl/sfs_names.tsv").read_text(encoding="utf-8").splitlines() if ln)
    return {int(h, 16): n for h, n in rows}


@cache
def _rom(rom_path):
    import ndspy.rom
    return ndspy.rom.NintendoDSRom.fromFile(rom_path)


@cache
def _sfs(rom_path):
    rom = _rom(rom_path)
    return rom.getFileByName("DATA.SFS"), bytes(rom.arm9)


@cache
def code_images(rom_path=ORIG):
    """{"arm9": bytes, "ov9_NN": bytes}: arm9 runs at 0x02000000, every overlay at 0x0211B780 (none compressed)."""
    rom = _rom(Path(rom_path))
    out = {"arm9": bytes(rom.arm9)}
    for i, o in sorted(rom.loadArm9Overlays().items()):
        out[f"ov9_{i:02d}"] = bytes(o.data)
    return out


def sfs_files(wanted=None, rom_path=ORIG):
    """{name: bytes} of the named DATA.SFS files (all, or those in wanted) of a ROM."""
    data, arm9 = _sfs(Path(rom_path))
    nm = names()
    out = {}
    for h, size, sec in sfs.read_dir(arm9, len(data)):
        n = nm.get(h)
        if n and (wanted is None or n in wanted):
            out[n] = data[sec * sfs.SECTOR: sec * sfs.SECTOR + size]
    return out


def family(name):
    for fam, pat, font in FAMILIES:
        if re.fullmatch(pat, name):
            return fam, font
    return None


@cache
def table(font):
    return Table.load(ROOT / mkjptbl.TABLES[font])


def decode(font, raw):
    """String bytes (no FF) -> text."""
    return table(font).decode(raw, 0, len(raw))[0].replace("{br}", "\n")


def encode(font, s):
    """Text -> string bytes (no FF)."""
    return table(font).encode(s.replace("\n", "{br}"))


# --- file layouts: (string area start, [(start, end incl. FF)], [(u32 field pos, target)], tail) ---

def _split(b, sa):
    out, i = [], sa
    while i < len(b) and b.find(b"\xff", i) >= 0:
        j = b.find(b"\xff", i)
        out.append((i, j + 1))
        i = j + 1
    return out, b[i:]


def _bytecode(b):
    """MESSAGE/SPMES/TUTO: `30 0x <u32 off>` shows a string, `51 <u32 off>` passes one; strings follow the bytecode."""
    cand = []
    for m in re.finditer(rb"\x30[\x00\x01]|\x51", b):
        a = m.start() + (2 if b[m.start()] == 0x30 else 1)
        if a + 4 <= len(b):
            t = struct.unpack_from("<I", b, a)[0]
            if m.start() < t < len(b):
                cand.append((b[m.start()], a, t))
    shown = [t for op, a, t in cand if op == 0x30]
    sa = min(shown) if shown else len(b)
    strs, tail = _split(b, sa)
    starts = {s for s, _ in strs}
    refs = [(a, t) for op, a, t in cand if a < sa and (op == 0x30 or t in starts)]
    return sa, strs, refs, tail


def _edmes(b):
    """EDMES: u32 id, u32 n, u32 table_off; n u32 -> 8-byte records (u32 str, u32 str), 0 = none; strings after."""
    _, n, toff = struct.unpack_from("<3I", b, 0)
    refs = []
    for r in struct.unpack_from(f"<{n}I", b, toff):
        for k in (0, 4):
            t = struct.unpack_from("<I", b, r + k)[0]
            if t:
                refs.append((r + k, t))
    sa = min(t for _, t in refs)
    strs, tail = _split(b, sa)
    return sa, strs, refs, tail


def layout(name, b):
    lay = _edmes(b) if family(name)[0] == "edmes" else _bytecode(b)
    check_layout(name, *lay)
    return lay


def check_layout(name, sa, strs, refs, tail):
    """Coverage: every ref on a string start, every string referenced (bar UNREF_OK), only zero padding after."""
    starts = {s for s, _ in strs}
    bad = [f"{name}: ref at {a:X} -> {t:X} not a string start" for a, t in refs if t not in starts]
    hit = {t for _, t in refs}
    bad += [f"{name}: string {s:X} unreferenced" for s in sorted(starts - hit) if sid(name, s) not in UNREF_OK]
    if tail.strip(b"\0"):
        bad.append(f"{name}: non-zero bytes after the last string")
    if bad:
        raise ValueError("; ".join(bad))


def rebuild(name, b, new):
    """Re-lay the string area of file b with new[i] (bytes, no FF) for its i-th string; rewrite every ref."""
    sa, strs, refs, tail = layout(name, b)
    assert len(new) == len(strs), (name, len(new), len(strs))
    out, where = bytearray(b[:sa]), {}
    for (s, _), raw in zip(strs, new):
        where[s] = len(out)
        out += raw + b"\xff"
    if len(out) == len(b) - len(tail):
        out += tail
    else:
        out += bytes(-len(out) % 4)
    for a, t in refs:
        struct.pack_into("<I", out, a, where[t])
    return bytes(out)


# --- system text: string pools in arm9 / overlays, reached by absolute u32 pointers (docs/re/text.md) ---
ARM9_BASE, OVL_BASE = 0x02000000, 0x0211B780
POOLS = [  # (image, start, end, font); end = after the last FF. Found by tools/systext.py + pointer scan.
    ("arm9", 0x8F98C, 0x9281C, "sys"), ("arm9", 0x92830, 0x95C09, "sys"),  # 958EC-95C08: explore help pages (jp_left on the marker build)
    ("ov9_02", 0x1690, 0x169D, "end"), ("ov9_02", 0x16BC, 0x17A8, "end"),
    ("ov9_03", 0x2BB0, 0x2D45, "sys"), ("ov9_03", 0x2D70, 0x316A, "sys"),
    ("ov9_05", 0x340, 0x36D, "sys"),
    ("ov9_06", 0x3ED8, 0x427A, "end"), ("ov9_06", 0x431C, 0x432C, "end"),
    ("ov9_07", 0x1DEC, 0x2654, "end"),
    ("ov9_15", 0x46DC, 0x4742, "sys"),  # 46D0-46DB: struct bytes before the first string
    ("ov9_16", 0x1024, 0x104B, "sys"),
    ("ov9_18", 0x3740, 0x3D95, "end"),
    ("ov9_19", 0x1BE8, 0x1C62, "sys"),  # 1BE4-1BE7: struct bytes
]


ITEM_RECS = (0x1006A0, 221, 0x18)  # arm9 item records: +8 name (sys), +C name (FONT_ITEM), +10 effect, +14 who


def item_strings(arm9):
    """arm9 offsets of the FONT_ITEM item names (field +C of each item record; each is pointed at only from there)."""
    at, n, size = ITEM_RECS
    return {struct.unpack_from("<I", arm9, at + i * size + 0xC)[0] - ARM9_BASE for i in range(n)}


def base_of(img):
    return ARM9_BASE if img == "arm9" else OVL_BASE


def pointer_sites(images, img, lo, hi):
    """{offset: ["image:site", ...]} for aligned u32s pointing into img[lo:hi]. arm9 strings can be pointed at from
    any image; an overlay's strings only from that overlay (they all share one load address)."""
    base = base_of(img)
    srcs = list(images) if img == "arm9" else [img]
    out = {}
    for s in srcs:
        b = images[s]
        for o in range(0, len(b) - 3, 4):
            v = struct.unpack_from("<I", b, o)[0] - base
            if lo <= v < hi:
                out.setdefault(v, []).append(f"{s}:{o:X}")
    return out


POOL_DATA = {  # (image, offset): length of a non-text block inside a pool (skipped like padding, never translated)
    ("arm9", 0x8F9C0): 4,  # 0C 0C 0B 0C, read by code (literals at arm9 0x12FF0, 0x130A8); item name ドゼウ follows
}


def pool_strings(b, lo, hi, starts, img=None):
    """[(start, end incl. FF)] of a pool. Zero bytes between strings are padding, except at a pointer target
    (a string may begin with code 00 = あ); POOL_DATA blocks are skipped. Raises if the pool holds anything else."""
    out, p = [], lo
    while p < hi:
        if (img, p) in POOL_DATA:
            p += POOL_DATA[img, p]
            continue
        if b[p] == 0 and p not in starts:
            p += 1
            continue
        e = b.find(b"\xff", p, hi)
        if e < 0:
            raise ValueError(f"pool {lo:X}-{hi:X}: no FF after {p:X}")
        out.append((p, e + 1))
        p = e + 1
    return out


def system_docs(images=None):
    """{image: doc} for script/system/<image>.json (strings of every pool of that image, in address order)."""
    images = code_images() if images is None else images
    docs = {}
    items = item_strings(images["arm9"])
    for img, lo, hi, pool_font in POOLS:
        b = images[img]
        ptrs = pointer_sites(images, img, lo, hi)
        doc = docs.setdefault(img, {"file": img, "strings": []})
        for s, e in pool_strings(b, lo, hi, set(ptrs), img):
            font = "item" if img == "arm9" and s in items else pool_font
            row = {"id": f"{img}:{s:X}", "font": font, "jp": decode(font, b[s:e - 1]), "en": "",
                   "max": len(b[s:e]) + len(b[e:hi]) - len(b[e:hi].lstrip(b"\0")), "ptrs": ptrs.get(s, [])}
            if not row["ptrs"]:
                row["unref"] = True
            doc["strings"].append(row)
    return docs


def sid(name, off):
    return f"{name.rsplit('.', 1)[0]}:{off:04X}"


def extract(name, b):
    fam, font = family(name)
    sa, strs, refs, tail = layout(name, b)
    hit = {t for _, t in refs}
    out = []
    for s, e in strs:
        row = {"id": sid(name, s), "jp": decode(font, b[s:e - 1]), "en": ""}
        if s not in hit:
            row["unref"] = True
        out.append(row)
    return out


def json_path(name):
    return SCRIPT / family(name)[0] / (name.rsplit(".", 1)[0] + ".json")


def load(name):
    return json.loads(json_path(name).read_text(encoding="utf-8"))


def text_files(files=None):
    files = sfs_files() if files is None else files
    return {n: b for n, b in sorted(files.items()) if family(n)}


def all_docs():
    """(path, doc) for every script JSON, freshly extracted from the original ROM (en empty)."""
    for name, b in text_files().items():
        yield json_path(name), {"file": name, "font": family(name)[1], "strings": extract(name, b)}
    for img, doc in system_docs().items():
        yield SCRIPT / "system" / f"{img}.json", doc


def dump(force=False):
    wrote = kept = 0
    for p, doc in all_docs():
        rows = doc["strings"]
        if p.exists():
            if not force:
                continue
            old = {r["id"]: r for r in json.loads(p.read_text(encoding="utf-8"))["strings"]}
            for r in rows:
                o = old.get(r["id"], {})
                for k, v in o.items():  # translator fields survive; extracted ones (jp, ptrs, max...) refresh
                    if k == "en" or (k not in r and k != "unref"):
                        r[k] = v
                kept += bool(o.get("en"))
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
        wrote += 1
    print(f"wrote {wrote} files, kept {kept} translations")


def stats():
    tot = {}
    for p in sorted(SCRIPT.glob("*/*.json")):
        rows = json.loads(p.read_text(encoding="utf-8"))["strings"]
        t = tot.setdefault(p.parent.name, [0, 0, 0])
        t[0] += 1
        t[1] += len(rows)
        t[2] += sum(bool(r["en"]) for r in rows)
    for fam, (f, n, en) in tot.items():
        print(f"{fam}: {f} files, {n} strings, {en} translated")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stats"
    dump("--force" in sys.argv) if cmd == "dump" else stats()
