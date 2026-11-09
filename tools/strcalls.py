"""strcalls.py: for system string ids, the code that loads each string's address and the calls right after it.

Width gate helper (docs/re/windows.md): tells which draw routine a guessed string reaches without a tour.
Known targets are named (run, ctr, band = info band 0x0200FC88, join = 0x020132E0, menu = 0x0201038C ...).

    python -X utf8 tools/strcalls.py ID.. [--n 12]       (ids like arm9:92740 ov9_06:3FA4; reads work/*.bin)
    python -X utf8 tools/strcalls.py --stdin             (ids one per line, first column)
"""
import struct
import sys
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import drawsites  # noqa: E402

NAMES = {0x02012DF4: "run", 0x020130AC: "ctr", 0x0200FC88: "band", 0x020102F8: "bandctr", 0x020132E0: "join",
         0x0201038C: "menu", 0x02011168: "help", 0x020111AC: "helpbody", 0x02013224: "count11",
         0x02012FFC: "glyph"}


def addr_of(sid):
    img, off = sid.split(":")
    return int(off, 16) + (0x02000000 if img == "arm9" else drawsites.OV_BASE)


def calls(images, target, n):
    """-> [(image, load addr, [call names])] for every ldr-literal of target in any image."""
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    out = []
    for name, data, base in images:
        word = struct.pack("<I", target)
        pos = data.find(word)
        pools = set()
        while pos >= 0:
            if pos % 4 == 0:
                pools.add(base + pos)
            pos = data.find(word, pos + 1)
        if not pools:
            continue
        for pool in pools:
            # an ARM ldr rX,[pc,#imm] reaches up to 4 KB back
            for at in range(max(base, pool - 4096), pool, 4):
                w = struct.unpack_from("<I", data, at - base)[0]
                if (w & 0x0F7F0000) != 0x051F0000 or at + 8 + ((w & 0xFFF) if w & 0x800000 else -(w & 0xFFF)) != pool:
                    continue
                seq = []
                for ins in md.disasm(data[at - base + 4:at - base + 4 + n * 4], at + 4):
                    if ins.mnemonic in ("bl", "blx") and ins.op_str.startswith("#"):
                        t = int(ins.op_str[1:], 16)
                        seq.append(NAMES.get(t, f"{t:08X}"))
                out.append((name, at, seq))
    return out


def main():
    args = sys.argv[1:]
    n = 12
    if "--n" in args:
        i = args.index("--n")
        n = int(args[i + 1])
        del args[i:i + 2]
    ids = [ln.split()[0] for ln in sys.stdin if ln.strip()] if args == ["--stdin"] else args
    images = drawsites.images()
    for sid in ids:
        rows = calls(images, addr_of(sid), n)
        if not rows:
            print(f"{sid}\t-")
        for name, at, seq in rows:
            print(f"{sid}\t{name}:{at:08X}\t{' '.join(seq)}")


if __name__ == "__main__":
    main()
