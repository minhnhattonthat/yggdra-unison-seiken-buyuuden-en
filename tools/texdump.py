"""texdump.py TEX.bin TEXIMAGE_PARAM.. [--out DIR]: decode textures from a texture-VRAM dump (tools/lua/texvram.lua:
banks A-D = slots 0-3, 128 KB each) by their TEXIMAGE_PARAM (tools/lua/gxtex.lua logs them), as index/alpha images.

4x4 (format 5) takes its index data from slot 1 (0x20000 + off/2 for slot 0, 0x30000 + (off-0x40000)/2 for slot 2);
paletted formats show the raw index (no palette in the dump). Output: DIR/tex_<param>.png, 4x zoom.

    python -X utf8 tools/texdump.py work/qa/tex/sortie/tex_002640.bin 74B0225A 76D00000 --out work/qa/texdump
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image


def decode(v, param):
    off = (param & 0xFFFF) * 8
    w, h = 8 << ((param >> 20) & 7), 8 << ((param >> 23) & 7)
    fmt = (param >> 26) & 7
    if fmt == 5:
        n = (w // 4) * (h // 4)
        tex = np.frombuffer(v[off:off + n * 4], np.uint32)
        ioff = 0x20000 + (off // 2 if off < 0x20000 else 0x10000 + (off - 0x40000) // 2)
        idx = np.frombuffer(v[ioff:ioff + n * 2], np.uint16)
        pix = np.stack([(tex >> (2 * k)) & 3 for k in range(16)], 1)
        transp = (pix == 3) & ((idx >> 14) < 2)[:, None]
        val = np.where(transp, 0, 80 + pix * 58).astype(np.uint8)
        return val.reshape(h // 4, w // 4, 4, 4).transpose(0, 2, 1, 3).reshape(h, w)
    bpp = {1: 8, 2: 2, 3: 4, 4: 8, 6: 8, 7: 16}[fmt]
    d = np.frombuffer(v[off:off + w * h * bpp // 8], np.uint8)
    if bpp < 8:
        per = 8 // bpp
        px = np.zeros(len(d) * per, np.uint8)
        for k in range(per):
            px[k::per] = (d >> (k * bpp)) & ((1 << bpp) - 1)
        return (px.reshape(h, w) * (255 // ((1 << bpp) - 1))).astype(np.uint8)
    return d[:w * h].reshape(h, w)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dump")
    ap.add_argument("params", nargs="+")
    ap.add_argument("--out", default="work/qa/texdump")
    a = ap.parse_args()
    v = open(a.dump, "rb").read()
    Path(a.out).mkdir(parents=True, exist_ok=True)
    for p in a.params:
        img = decode(v, int(p, 16))
        out = Path(a.out) / f"tex_{p.upper()}.png"
        Image.fromarray(img).resize((img.shape[1] * 4, img.shape[0] * 4), Image.NEAREST).save(out)
        print(out, img.shape[1], "x", img.shape[0])


if __name__ == "__main__":
    main()
