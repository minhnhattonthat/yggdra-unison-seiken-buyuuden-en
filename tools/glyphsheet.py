"""glyphsheet.py: zoomed sheet of 16x16 4bpp NTFT glyphs, ink dark on white, hex label under each cell.

    python -X utf8 tools/glyphsheet.py FONT.NTFT OUT.png FIRST_HEX COUNT [--cols 16 --zoom 3]
Used for reading kanji (tools/kanji.py sheet) and spot checks. Palette: index 1-8 = ink (darker = lower), F = outline.
"""
import argparse

from PIL import Image, ImageDraw

INK = {0: 255, 15: 225}


def glyph_img(raw, zoom=3):
    im = Image.new("L", (16, 16), 255)
    px = im.load()
    for i, byte in enumerate(raw):
        for k, v in enumerate((byte & 15, byte >> 4)):
            n = 2 * i + k
            px[n % 16, n // 16] = INK.get(v, min(200, 20 * v))
    return im.resize((16 * zoom, 16 * zoom), Image.NEAREST)


def sheet(cells, cols=16, zoom=3):
    """cells: [(label, raw128)] -> RGB image."""
    cw, ch = 16 * zoom + 6, 16 * zoom + 14
    rows = (len(cells) + cols - 1) // cols
    img = Image.new("RGB", (cols * cw + 4, rows * ch + 4), (255, 255, 255))
    d = ImageDraw.Draw(img)
    for k, (label, raw) in enumerate(cells):
        x, y = (k % cols) * cw + 4, (k // cols) * ch + 2
        img.paste(glyph_img(raw, zoom).convert("RGB"), (x, y))
        d.rectangle((x - 1, y - 1, x + 16 * zoom, y + 16 * zoom), outline=(180, 180, 255))
        d.text((x, y + 16 * zoom + 1), str(label), fill=(200, 0, 0))
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("font")
    ap.add_argument("out")
    ap.add_argument("first", type=lambda s: int(s, 16))
    ap.add_argument("count", type=int)
    ap.add_argument("--cols", type=int, default=16)
    ap.add_argument("--zoom", type=int, default=3)
    a = ap.parse_args()
    d = open(a.font, "rb").read()
    cells = [(f"{g:X}", d[g * 128:(g + 1) * 128]) for g in range(a.first, min(a.first + a.count, len(d) // 128))]
    sheet(cells, a.cols, a.zoom).save(a.out)


if __name__ == "__main__":
    main()
