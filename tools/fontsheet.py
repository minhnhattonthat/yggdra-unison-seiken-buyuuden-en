"""fontsheet.py: render a linear 4bpp font (NTFT: rows of W px, low nibble = left pixel) as a labelled glyph sheet.

    python -X utf8 tools/fontsheet.py work/sfs/FONT_MES.NTFT work/font_mes.png --w 16 --h 16 [--first 0 --count 256 --cols 16 --zoom 2]
"""
import argparse

from PIL import Image, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("dst")
ap.add_argument("--w", type=int, default=16)
ap.add_argument("--h", type=int, default=16)
ap.add_argument("--first", type=int, default=0)
ap.add_argument("--count", type=int, default=256)
ap.add_argument("--cols", type=int, default=16)
ap.add_argument("--zoom", type=int, default=2)
a = ap.parse_args()
data = open(a.src, "rb").read()
gsize = a.w * a.h // 2
count = min(a.count, len(data) // gsize - a.first)
rows = (count + a.cols - 1) // a.cols
cw, ch = a.w + 2, a.h + 10
img = Image.new("RGB", (a.cols * cw + 2, rows * ch + 2), (40, 40, 90))
d = ImageDraw.Draw(img)
for k in range(count):
    g = a.first + k
    x0, y0 = (k % a.cols) * cw + 2, (k // a.cols) * ch + 10
    d.text((x0, y0 - 10), f"{g:x}", fill=(255, 200, 0))
    base = g * gsize
    for y in range(a.h):
        for x in range(a.w):
            b = data[base + (y * a.w + x) // 2]
            v = (b >> 4) if x & 1 else (b & 15)
            c = 255 - v * 16
            img.putpixel((x0 + x, y0 + y), (c, c, c) if v else (0, 0, 0))
img = img.resize((img.width * a.zoom, img.height * a.zoom), Image.NEAREST)
img.save(a.dst)
print(a.dst, f"glyphs {a.first:#x}..{a.first + count - 1:#x} of {len(data) // gsize:#x}")
