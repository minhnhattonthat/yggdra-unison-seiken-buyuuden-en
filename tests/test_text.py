"""Extraction roundtrip and coverage against the original ROM (docs/re/text.md)."""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import text  # noqa: E402

needs_rom = pytest.mark.skipif(not text.ORIG.is_file(), reason="no ROM dump")


@pytest.fixture(scope="module")
def files():
    return text.text_files()


@needs_rom
def test_families_found(files):
    counts = {}
    for n in files:
        counts[text.family(n)[0]] = counts.get(text.family(n)[0], 0) + 1
    assert counts == {"message": 221, "spmes": 407, "tuto": 28, "edmes": 38}


@needs_rom
def test_roundtrip(files):
    """decode -> encode gives every string's bytes back, and re-laying the file from them gives the file back."""
    for name, b in files.items():
        font = text.family(name)[1]
        _, strs, _, _ = text.layout(name, b)  # raises on any coverage gap
        new = []
        for s, e in strs:
            raw = b[s:e - 1]
            assert text.encode(font, text.decode(font, raw)) == raw, (name, hex(s))
            new.append(raw)
        assert text.rebuild(name, b, new) == b, name


@needs_rom
def test_rebuild_moves_refs(files):
    name = "MESSAGE001.BIN"
    b = files[name]
    sa, strs, refs, _ = text.layout(name, b)
    new = [b"\x00" * 40 for _ in strs]
    out = text.rebuild(name, b, new)
    assert out[:sa] != b[:sa] or not refs
    _, strs2, refs2, _ = text.layout(name, out)
    assert len(strs2) == len(strs) and all(out[s:e] == b"\x00" * 40 + b"\xff" for s, e in strs2)
    assert sorted(a for a, _ in refs2) == sorted(a for a, _ in refs)


@needs_rom
def test_system_pools_roundtrip():
    """Every pool byte is a string, zero padding or a POOL_DATA block; each string re-encodes (in its row's font)
    to its bytes; every item record's FONT_ITEM name is a row in font "item"; script/system matches the ROM."""
    ims = text.code_images()
    docs = text.system_docs(ims)
    for img, lo, hi, _ in text.POOLS:
        b = ims[img]
        strs = text.pool_strings(b, lo, hi, set(text.pointer_sites(ims, img, lo, hi)), img)
        used = sum(e - s for s, e in strs) + sum(n for (i, o), n in text.POOL_DATA.items() if i == img and lo <= o < hi)
        assert used + b[lo:hi].count(0) - sum(b[s:e].count(0) for s, e in strs) >= hi - lo, (img, hex(lo))
    for img, doc in docs.items():
        b = ims[img]
        for r in doc["strings"]:
            s = int(r["id"].split(":")[1], 16)
            assert text.encode(r["font"], r["jp"]) == b[s:b.index(b"\xff", s)], r["id"]
        on_disk = json.loads((text.SCRIPT / "system" / f"{img}.json").read_text(encoding="utf-8"))["strings"]
        assert [(r["id"], r["font"], r["jp"]) for r in on_disk] == [(r["id"], r["font"], r["jp"]) for r in doc["strings"]]
    items = {f"arm9:{o:X}" for o in text.item_strings(ims["arm9"])}
    assert items == {r["id"] for r in docs["arm9"]["strings"] if r["font"] == "item"} and len(items) == 221


@needs_rom
def test_script_in_sync(files):
    """script/ has a JSON per text file, same ids, and jp matches the ROM under the current tables."""
    for name, b in files.items():
        doc = json.loads(text.json_path(name).read_text(encoding="utf-8"))
        rows = text.extract(name, b)
        assert [r["id"] for r in doc["strings"]] == [r["id"] for r in rows], name
        assert [r["jp"] for r in doc["strings"]] == [r["jp"] for r in rows], name
