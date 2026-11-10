"""oamlist.py PREFIX [--engine a|b] [--at x,y]: list the visible OBJs of a ppuevery.lua / L.dump_ppu dump.

Prints DISPCNT and each OBJ: x, y, w x h, tile, palette, 8bpp, the byte offset of its first tile in the dump's
.vram.bin (1D mapping, boundary from DISPCNT) and the 32/64 tile bytes there (to search the ROM for its source).
--at x,y keeps only OBJs covering that screen point.

    python -X utf8 tools/oamlist.py work/qa/ppu_s25/sortie/ppu_002640 --engine b --at 160,4
"""
import argparse
import struct

SIZES = {0: [(8, 8), (16, 16), (32, 32), (64, 64)], 1: [(16, 8), (32, 8), (32, 16), (64, 32)],
         2: [(8, 16), (8, 32), (16, 32), (32, 64)]}
OBJ_BASE = {"a": 0xA0000, "b": 0xE0000}  # offsets in .vram.bin (desmume_lib L.dump_ppu layout)


def objs(prefix, engine):
    io = open(prefix + ".io.bin", "rb").read()
    oam = open(prefix + ".oam.bin", "rb").read()
    disp = struct.unpack_from("<I", io, 0 if engine == "a" else 0x60)[0]
    base = 0 if engine == "a" else 0x400
    bound = 32 << ((disp >> 20) & 3) if disp & 0x10 else 32  # 1D tile mapping boundary
    out = []
    for n in range(128):
        a0, a1, a2 = struct.unpack_from("<HHH", oam, base + n * 8)
        rs, off = a0 & 0x100, a0 & 0x200
        if not rs and off:
            continue
        shape = a0 >> 14
        if shape == 3:
            continue
        w, h = SIZES[shape][a1 >> 14]
        x, y = a1 & 0x1FF, a0 & 0xFF
        x -= 512 if x >= 256 else 0
        y -= 256 if y >= 192 else 0
        tile, pal, bpp8 = a2 & 0x3FF, a2 >> 12, bool(a0 & 0x2000)
        out.append(dict(n=n, x=x, y=y, w=w, h=h, tile=tile, pal=pal, bpp8=bpp8, voff=OBJ_BASE[engine] + tile * bound))
    return disp, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prefix")
    ap.add_argument("--engine", default="b")
    ap.add_argument("--at")
    a = ap.parse_args()
    disp, os_ = objs(a.prefix, a.engine)
    vram = open(a.prefix + ".vram.bin", "rb").read()
    print(f"DISPCNT {disp:08X}")
    for o in os_:
        if a.at:
            px, py = map(int, a.at.split(","))
            if not (o["x"] <= px < o["x"] + o["w"] and o["y"] <= py < o["y"] + o["h"]):
                continue
        tb = vram[o["voff"]:o["voff"] + (64 if o["bpp8"] else 32)]
        print(f'#{o["n"]:3d} at {o["x"]},{o["y"]} {o["w"]}x{o["h"]} tile {o["tile"]} pal {o["pal"]} '
              f'{"8bpp" if o["bpp8"] else "4bpp"} vram+{o["voff"]:X} {tb.hex()}')


if __name__ == "__main__":
    main()
