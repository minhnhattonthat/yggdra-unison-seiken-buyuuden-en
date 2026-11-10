"""inkrects.py: text rects in a picture texture (tutorial shots: text over art or an opaque panel).

    python -X utf8 tools/inkrects.py PNG [--region x,y,w,h].. [--min 300] [--max 9999] [--gap 3]

Ink = pixels whose R+G+B is in [--min, --max] (white/yellow lettering; set --max to catch dark ink). Rows of ink
split into bands, bands into runs at column gaps >= --gap. Prints `x,y,w,h` per run (ink bbox, no outline grow:
pad it yourself or let gen_gfx clear a box 1-2 px larger). atlas.py grows rects to the opaque area, which on an
opaque panel is the whole texture.
"""
import argparse

import numpy as np
from PIL import Image


def runs(v, gap):
    out = []
    for i in np.nonzero(v)[0]:
        if out and i - out[-1][1] < gap:
            out[-1][1] = i + 1
        else:
            out.append([i, i + 1])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("png")
    ap.add_argument("--region", action="append", type=lambda s: tuple(map(int, s.split(","))))
    ap.add_argument("--min", type=int, default=300)
    ap.add_argument("--max", type=int, default=9999)
    ap.add_argument("--gap", type=int, default=3)
    a = ap.parse_args()
    im = np.asarray(Image.open(a.png).convert("RGBA")).astype(int)
    s = im[..., :3].sum(2)
    ink = (s >= a.min) & (s <= a.max) & (im[..., 3] > 0)
    for x0, y0, w, h in a.region or [(0, 0, im.shape[1], im.shape[0])]:
        sub = ink[y0:y0 + h, x0:x0 + w]
        for r0, r1 in runs(sub.any(1), 2):
            for c0, c1 in runs(sub[r0:r1].any(0), a.gap):
                ys = np.nonzero(sub[r0:r1, c0:c1].any(1))[0]
                print(f"{x0 + c0},{y0 + r0 + ys[0]},{c1 - c0},{ys[-1] - ys[0] + 1}")


if __name__ == "__main__":
    main()
