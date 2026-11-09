"""tex.py: decode Yggdra Unison DS textures (.PACK = NDS 3D texture parts) to RGBA images.

PACK parts (tools/sfs.unpack_pack): texels, palette (BGR555), 4x4 index data. Format is inferred:
  index part present and half the texel size -> 4x4-compressed (GBATEK "Texture Compression");
  else palette colours: <=4 -> 2bpp, <=16 -> 4bpp, else 8bpp (rows linear, low bits = left pixel).
Width is not stored in the PACK (the code or the .BI layout file holds it): guess() picks the power-of-two width
whose rows join most smoothly.

    python tools/tex.py work/sfs/TIT_LOGO.PACK out.png [--w 256]
"""
import struct
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sfs  # noqa: E402


def rgb(c):
    return ((c & 31) * 255 // 31, (c >> 5 & 31) * 255 // 31, (c >> 10 & 31) * 255 // 31, 255)


def colours(pal):
    return [rgb(c) for c in struct.unpack_from(f"<{len(pal) // 2}H", pal)]


def decode_4x4(tex, idx, pal, w):
    """GBATEK 4x4 compression: 4 bytes texels (2 bpp, one byte per row) + u16 index per block."""
    pw = struct.unpack_from(f"<{len(pal) // 2}H", pal)
    nb = len(tex) // 4
    bw = w // 4
    h = (nb + bw - 1) // bw * 4
    img = Image.new("RGBA", (w, h))
    px = img.load()
    for b in range(nb):
        v = struct.unpack_from("<H", idx, b * 2)[0] if b * 2 + 2 <= len(idx) else 0
        base, mode = (v & 0x3FFF) * 2, v >> 14

        def pc(i):
            return pw[base + i] if base + i < len(pw) else 0
        c0, c1 = pc(0), pc(1)
        if mode == 0:
            cs = [rgb(c0), rgb(c1), rgb(pc(2)), (0, 0, 0, 0)]
        elif mode == 1:
            a, b2 = rgb(c0), rgb(c1)
            cs = [a, b2, tuple((x + y) // 2 for x, y in zip(a, b2)), (0, 0, 0, 0)]
        elif mode == 2:
            cs = [rgb(c0), rgb(c1), rgb(pc(2)), rgb(pc(3))]
        else:
            a, b2 = rgb(c0), rgb(c1)
            cs = [a, b2, tuple((5 * x + 3 * y) // 8 for x, y in zip(a, b2)),
                  tuple((3 * x + 5 * y) // 8 for x, y in zip(a, b2))]
        x0, y0 = b % bw * 4, b // bw * 4
        for r in range(4):
            row = tex[b * 4 + r]
            for c in range(4):
                px[x0 + c, y0 + r] = cs[row >> (2 * c) & 3]
    return img


def decode_pal(tex, pal, w, bpp):
    cs = colours(pal) or [(0, 0, 0, 255)]
    per = 8 // bpp
    n = len(tex) * per
    h = (n + w - 1) // w
    img = Image.new("RGBA", (w, h))
    px = img.load()
    mask = (1 << bpp) - 1
    for i in range(n):
        v = tex[i // per] >> (bpp * (i % per)) & mask
        px[i % w, i // w] = cs[v] if v < len(cs) else (255, 0, 255, 255)
    return img


def parts(b):
    ps = sfs.unpack_pack(b)
    return [d if d is not None else r for r, d in ps]


def kind(tex, pal, idx):
    if idx and len(idx) * 2 == len(tex):
        return "4x4"
    n = len(pal) // 2
    return "2bpp" if n <= 4 else "4bpp" if n <= 16 else "8bpp"


def render(tex, pal, idx, w):
    k = kind(tex, pal, idx)
    if k == "4x4":
        return decode_4x4(tex, idx, pal, w)
    return decode_pal(tex, pal, w, {"2bpp": 2, "4bpp": 4, "8bpp": 8}[k])


def guess(tex, pal, idx):
    """Width with the smoothest vertical joins (texture widths are powers of two, 8..1024)."""
    k = kind(tex, pal, idx)
    bits = {"4x4": 2, "2bpp": 2, "4bpp": 4, "8bpp": 8}[k]
    npx = len(tex) * 8 // bits
    best = None
    for w in (32, 64, 128, 256, 512, 1024):
        if npx < w * 8 or npx % w:
            continue
        img = render(tex, pal, idx, w).convert("L")
        a = img.load()
        hh = img.height
        rows = range(3 if k == "4x4" else 0, hh - 1, 4 if k == "4x4" else max(1, hh // 64))
        cost = sum(abs(a[x, y] - a[x, y + 1]) for y in rows for x in range(0, w, 2)) / max(1, len(rows) * w)
        if best is None or cost < best[0]:
            best = (cost, w)
    return best[1] if best else 256


def main():
    b = Path(sys.argv[1]).read_bytes()
    tex, pal, idx = parts(b)
    w = int(sys.argv[sys.argv.index("--w") + 1]) if "--w" in sys.argv else guess(tex, pal, idx)
    img = render(tex, pal, idx, w)
    img.save(sys.argv[2])
    print(sys.argv[2], kind(tex, pal, idx), img.size)


if __name__ == "__main__":
    main()
