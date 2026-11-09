"""build.py: original ROM -> build/yggdra_en.nds.

Re-lays DATA.SFS (docs/re/sfs.md "Rebuild plan") with any replaced files, patches the arm9 directory, saves via
ndspy and undoes ndspy's two quirks (size word at 0x1000, no 0xFF pad to cart size). With no replacements the
output is byte-identical to the original (tests/test_build.py).
"""
import hashlib
import struct
import sys
from pathlib import Path

import ndspy.rom

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_rom  # noqa: E402
import sfs  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ORIG = ROOT / "rom/yggdra.nds"
OUT = ROOT / "build/yggdra_en.nds"


def rebuild_sfs(data, arm9, repl):
    """repl: {name: bytes}. Unchanged files keep their original bytes up to the next file (gap included);
    replaced ones are zero-padded to a sector. Returns (new DATA.SFS, new arm9)."""
    arm9 = bytearray(arm9)
    ents = sfs.read_dir(bytes(arm9), len(data))
    idx = {h: i for i, (h, _, _) in enumerate(ents)}
    by_hash = {}
    for name, b in repl.items():
        h = sfs.name_hash(name)
        if h not in idx:
            raise KeyError(f"{name}: not in DATA.SFS directory")
        by_hash[h] = b
    order = sorted(ents, key=lambda e: e[2])
    out = bytearray()
    for n, (h, size, sec) in enumerate(order):
        start = sec * sfs.SECTOR
        end = order[n + 1][2] * sfs.SECTOR if n + 1 < len(order) else len(data)
        new_sec = len(out) // sfs.SECTOR
        if h in by_hash:
            size = len(by_hash[h])
            out += by_hash[h] + bytes(-size % sfs.SECTOR)
        else:
            out += data[start:end]
        struct.pack_into("<3I", arm9, sfs.DIR_OFF + 12 * idx[h], h, size, new_sec)
    return bytes(out), bytes(arm9)


def build_rom(repl=None, orig_path=ORIG, images=None):
    """repl: {DATA.SFS name: bytes}; images: {"arm9" | "ov9_NN": bytes} replacing arm9 / overlays (same size)."""
    orig = orig_path.read_bytes()
    rom = ndspy.rom.NintendoDSRom(orig)
    for img, b in (images or {}).items():
        if img == "arm9":
            rom.arm9 = b
        else:
            ov = rom.loadArm9Overlays()[int(img[4:])]
            assert len(b) == len(ov.data), f"{img}: size changed"
            rom.files[ov.fileID] = b
    if repl:
        rom.files[rom.filenames.idOf("DATA.SFS")], rom.arm9 = rebuild_sfs(rom.getFileByName("DATA.SFS"), rom.arm9, repl)
    out = bytearray(rom.save())
    out[0x1000:0x1004] = orig[0x1000:0x1004]  # ndspy writes a size word into this zero gap
    out += b"\xff" * (len(orig) - len(out))  # ndspy trims to used size; the cart is 0xFF-padded
    return bytes(out)


def edits(marker=False):
    """(DATA.SFS {name: bytes}, code images {image: bytes}): English fonts + VWF, then text (marker or English)."""
    import enfont
    import engine
    import text
    fonts, wtab = enfont.patched_fonts(text.sfs_files(set(enfont.FONTS)))
    repl, images = dict(fonts), {}
    if marker:
        import marker as mk
        skip = sys.argv[sys.argv.index("--skip") + 1].split(",") if "--skip" in sys.argv else ()
        repl |= mk.script_files(skip)
        images = mk.system_images()
    orig = text.code_images()
    arm9 = images.get("arm9", orig["arm9"])
    images["arm9"] = engine.patch_arm9(arm9, wtab)
    images |= engine.patch_overlays({**orig, **images}, engine.entries(orig["arm9"]))
    return repl, images


def main():
    check_rom.check()
    marker = "--marker" in sys.argv
    repl, images = edits(marker)
    out = build_rom(repl, images=images)
    dst = OUT.with_name("yggdra_marker.nds") if marker else OUT
    dst.parent.mkdir(exist_ok=True)
    dst.write_bytes(out)
    print(dst.relative_to(ROOT), hex(len(out)), hashlib.sha1(out).hexdigest())


if __name__ == "__main__":
    main()
