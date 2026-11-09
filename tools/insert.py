"""insert.py: English text from script/ into the build (the non-marker path of tools/build.py).

Script files (MESSAGE/SPMES/TUTO/EDMES) are re-laid with text.rebuild; system strings go in place or into the
EXTRA block (tools/sysreloc.py), as the marker build does. A row with empty `en` keeps its original bytes: every
such row is listed in script/keep_jp.txt (lint fails on any other), and those glyphs (... - 0 P CLEAR, the kanji
star, MESSAGE000 debug filler) are untouched by enfont.
"""
import json
import sys
from functools import cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import text  # noqa: E402
from tbl import Table  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


@cache
def en():
    return Table.load(ROOT / "tbl/en.tbl")


def encode(s):
    return en().encode(s.replace("\n", "{br}"))


def script_files():
    """{name: English bytes} for every MESSAGE/SPMES/TUTO/EDMES file."""
    out = {}
    for name, b in text.text_files().items():
        rows = {r["id"]: r for r in text.load(name)["strings"]}
        sa, strs, refs, tail = text.layout(name, b)
        new = []
        for s, e in strs:
            r = rows[text.sid(name, s)]  # KeyError = script/ out of date with the extractor
            new.append(encode(r["en"]) if r["en"] else b[s:e - 1])
        out[name] = text.rebuild(name, b, new)
    return out


def system_images():
    """({image: bytes}, EXTRA block) with every system string in English."""
    import sysreloc
    images, rows = text.code_images(), []
    for img in images:
        p = ROOT / "script/system" / f"{img}.json"
        if not p.exists():
            continue
        b = images[img]
        for r in json.loads(p.read_text(encoding="utf-8"))["strings"]:
            off = int(r["id"].split(":")[1], 16)
            raw = encode(r["en"]) if r["en"] else b[off:b.index(b"\xff", off)]
            rows.append((r, raw))
    return sysreloc.relocate(images, rows)


if __name__ == "__main__":
    files = script_files()
    imgs, extra = system_images()
    print(f"{len(files)} script files, {len(imgs)} images, EXTRA {len(extra):#x} bytes")
