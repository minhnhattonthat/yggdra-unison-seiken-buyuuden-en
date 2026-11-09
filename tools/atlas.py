"""atlas.py: label rects of a UI atlas texture (rows of ink split into bands, bands split at column gaps).

    python -X utf8 tools/atlas.py NAME.. [--gap 4] [--zoom 3] [--out work/gfx/atlas] [--quads work/qa/quads/*/log.txt]

--region x,y,w,h (repeatable): segment inside each region only (label rows that touch merge otherwise).
--quads: the rects the game draws (tools/lua/quads.lua over the warp scenes: regen.py --qa work/qa/quads
--script tools/lua/quads.lua --var HOLD=600) instead of segmenting; only labels on those screens show up.

Ink = opaque and bright (sum RGB > 300: the white/grey lettering, not its black outline). Prints one `x,y,w,h` per
label (reading order; the rect grown to the opaque outline around the ink) and writes <out>/NAME.png: the decode
zoomed, each rect outlined in red with its number, to read the labels and pick `box=` values for gfx/text.tsv.
A label whose characters sit further apart than --gap splits in two: join those by eye.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import gfx  # noqa: E402


def runs(v, gap=1):
    """[(start, end)) of True runs in bool vector v, joining runs separated by < gap False cells."""
    out = []
    for i in np.nonzero(v)[0]:
        if out and i - out[-1][1] < gap:
            out[-1][1] = i + 1
        else:
            out.append([i, i + 1])
    return [tuple(map(int, r)) for r in out]


def rects(ink, opaque, gap=4):
    out = []
    for y0, y1 in runs(ink.any(1)):
        for x0, x1 in runs(ink[y0:y1].any(0), gap):
            op = opaque[max(y0 - 1, 0):y1 + 1, max(x0 - 1, 0):x1 + 1]  # take in the 1 px outline
            ys, xs = np.nonzero(op)
            bx, by = max(x0 - 1, 0) + int(xs.min()), max(y0 - 1, 0) + int(ys.min())
            out.append((bx, by, max(x0 - 1, 0) + int(xs.max()) + 1 - bx, max(y0 - 1, 0) + int(ys.max()) + 1 - by))
    return out


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="+")
    ap.add_argument("--gap", type=int, default=4)
    ap.add_argument("--zoom", type=int, default=3)
    ap.add_argument("--out", default="work/gfx/atlas")
    ap.add_argument("--quads", nargs="+", help="quads.lua log files: use the drawn rects instead of segmenting")
    ap.add_argument("--region", action="append", type=lambda s: tuple(map(int, s.split(","))),
                    help="x,y,w,h (repeatable): segment only inside it, for label rows with no blank row between")
    a = ap.parse_args(argv)
    out = ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    for name in a.names:
        img, _ = gfx.load(name + ".PACK")
        rgba = img.convert("RGBA")
        px = np.array(rgba).astype(int)
        opaque = px[..., 3] > 0
        if a.quads:  # rects the game really draws (tools/lua/quads.lua log lines "quad NAME u,v,w,h ...")
            rs = sorted({tuple(map(int, ln.split()[2].split(","))) for p in a.quads
                         for ln in Path(p).read_text(encoding="utf-8").splitlines()
                         if ln.startswith("quad " + name + " ")}, key=lambda r: (r[1], r[0]))
        else:
            ink = opaque & (px[..., :3].sum(-1) > 300)
            rs = []
            for x, y, w, h in a.region or [(0, 0, rgba.width, rgba.height)]:
                rs += [(rx + x, ry + y, rw, rh) for rx, ry, rw, rh in
                       rects(ink[y:y + h, x:x + w], opaque[y:y + h, x:x + w], a.gap)]
        print(f"{name} {rgba.size}")
        for i, r in enumerate(rs):
            print(f"  {i:2d} {','.join(map(str, r))}")
        z = a.zoom
        bg = Image.new("RGBA", rgba.size, (40, 40, 60, 255))
        big = Image.alpha_composite(bg, rgba).resize((rgba.width * z, rgba.height * z), Image.NEAREST)
        d = ImageDraw.Draw(big)
        for i, (x, y, w, h) in enumerate(rs):
            d.rectangle((x * z - 1, y * z - 1, (x + w) * z, (y + h) * z), outline=(255, 0, 0, 255))
            d.text((x * z + 1, y * z + 1), str(i), fill=(0, 255, 0, 255))
        big.save(out / f"{name}.png")
    return 0


if __name__ == "__main__":
    assert runs(np.array([1, 0, 0, 1, 1, 0], bool), 3) == [(0, 5)]
    assert runs(np.array([1, 0, 0, 1, 1, 0], bool), 2) == [(0, 1), (3, 5)]
    sys.exit(main(sys.argv[1:]))
