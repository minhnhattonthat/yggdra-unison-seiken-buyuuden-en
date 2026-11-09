"""blcalls.py: every BL to TARGET in arm9 and the overlays, with the next N instructions (does the caller use r0?).

python -X utf8 tools/blcalls.py 02012DF4 [N]   (reads work/arm9_02000000.bin, work/ov9_XX.bin from tools/unpack.py)
"""
import sys
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs

WORK = Path(__file__).resolve().parents[1] / "work"
target = int(sys.argv[1], 16)
n = int(sys.argv[2]) if len(sys.argv) > 2 else 4
cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
images = [("arm9", WORK / "arm9_02000000.bin", 0x02000000)]
images += [(p.stem, p, 0x0211B780) for p in sorted(WORK.glob("ov9_[0-9][0-9].bin"))]
for name, path, base in images:
    data = path.read_bytes()
    for off in range(0, len(data) - 3, 4):
        w = int.from_bytes(data[off:off + 4], "little")
        if (w >> 24) & 0xF != 0xB or w >> 28 == 0xF:
            continue
        imm = w & 0xFFFFFF
        imm = imm - (1 << 24) if imm & 0x800000 else imm
        if base + off + 8 + imm * 4 != target:
            continue
        after = " | ".join(f"{i.mnemonic} {i.op_str}" for i in cs.disasm(data[off + 4:off + 4 + 4 * n], base + off + 4))
        print(f"{name} {base + off:08X}: {after}")
