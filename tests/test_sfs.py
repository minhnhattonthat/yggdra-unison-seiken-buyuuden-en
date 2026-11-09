import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import sfs  # noqa: E402


def test_decompress_literal_and_backref():
    # out = AB CD AB CD AB CD: 2 literal halfwords, then copy 4 halfwords from 2 back (len field 2 -> 4)
    src = (12).to_bytes(4, "little") + (2).to_bytes(2, "little") + (2).to_bytes(2, "little") \
        + (0x8000 | (2 << 10) | 2).to_bytes(2, "little") + bytes.fromhex("abcdabcd")
    out, size, _ = sfs.decompress(src)
    assert out == bytes.fromhex("abcdabcd" * 3) and size == 12


@pytest.mark.skipif(not (ROOT / "rom/yggdra.nds").is_file(), reason="no ROM dump")
def test_directory_finds_known_names():
    import ndspy.rom
    rom = ndspy.rom.NintendoDSRom.fromFile(ROOT / "rom/yggdra.nds")
    data = rom.getFileByName("DATA.SFS")
    ents = sfs.read_dir(bytes(rom.arm9), len(data))
    assert len(ents) == 4001
    by_hash = {h: (size, sec) for h, size, sec in ents}
    assert sfs.name_hash("FONT_MES.NTFT") in by_hash
    size, sec = by_hash[sfs.name_hash("MESSAGE001.BIN")]
    assert data[sec * 0x200 + 0x240: sec * 0x200 + 0x243] == bytes([0x0A, 0x00, 0xEB])  # "さあ、"
