import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build  # noqa: E402
import sfs  # noqa: E402

needs_rom = pytest.mark.skipif(not build.ORIG.is_file(), reason="no ROM dump")


@needs_rom
def test_identity_build():
    assert build.build_rom({}) == build.ORIG.read_bytes()


@needs_rom
def test_identity_sfs_relayout():
    import ndspy.rom
    rom = ndspy.rom.NintendoDSRom.fromFile(build.ORIG)
    data, arm9 = rom.getFileByName("DATA.SFS"), bytes(rom.arm9)
    assert build.rebuild_sfs(data, arm9, {}) == (data, arm9)


@needs_rom
def test_replaced_file_relaid():
    import ndspy.rom
    rom = ndspy.rom.NintendoDSRom.fromFile(build.ORIG)
    data, arm9 = rom.getFileByName("DATA.SFS"), bytes(rom.arm9)
    grown = b"\x5a" * 0x1234
    new, new9 = build.rebuild_sfs(data, arm9, {"MESSAGE001.BIN": grown})
    ents = {h: (size, sec) for h, size, sec in sfs.read_dir(new9, len(new))}
    old = {h: (size, sec) for h, size, sec in sfs.read_dir(arm9, len(data))}
    assert len(ents) == len(old)
    size, sec = ents[sfs.name_hash("MESSAGE001.BIN")]
    assert new[sec * 0x200: sec * 0x200 + size] == grown
    for h, (size, sec) in old.items():  # every other file unchanged at its new place
        if h != sfs.name_hash("MESSAGE001.BIN"):
            nsize, nsec = ents[h]
            assert nsize == size and new[nsec * 0x200:][:size] == data[sec * 0x200:][:size]


@needs_rom
def test_english_build(tmp_path):
    """The English insert: builds, and romcheck (allowed writes, every string and pointer) is clean."""
    import romcheck
    repl, images = build.edits()
    out = tmp_path / "en.nds"
    out.write_bytes(build.build_rom(repl, images=images))
    errs, n, nsys = romcheck.run(out)
    assert not errs, errs[:20]
    assert n > 12000 and nsys > 1600
