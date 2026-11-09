"""rowscan.py: colour runs along a row (or column) of a shot, to read box edges and text extents in pixels.

    python tools/rowscan.py SHOT.png y [y..] [--x0 0 --x1 256] [--min 3] [--col]
    python tools/rowscan.py SHOT.png --ink x,y,w,h      -> first/last column and row with outline (black) ink

Each run: x0-x1 and its RGB (runs shorter than --min px are merged into "~"). Used for the width gate (docs/re/windows.md).
"""
import argparse

from PIL import Image


def runs(px, lo, hi, minlen, tol=24):
    out, start = [], lo
    for x in range(lo + 1, hi + 1):
        if x == hi or max(abs(a - b) for a, b in zip(px(x), px(start))) > tol:
            out.append((start, x - 1, px(start)))
            start = x
    merged = []
    for r in out:
        if r[1] - r[0] + 1 < minlen:
            if merged and merged[-1][2] == "~":
                merged[-1] = (merged[-1][0], r[1], "~")
            else:
                merged.append((r[0], r[1], "~"))
        else:
            merged.append(r)
    return merged


def ink(im, x, y, w, h, dark=40):
    cols = [cx for cx in range(x, x + w) for cy in range(y, y + h) if max(im.getpixel((cx, cy))) <= dark]
    rows = [cy for cx in range(x, x + w) for cy in range(y, y + h) if max(im.getpixel((cx, cy))) <= dark]
    return (min(cols), max(cols), min(rows), max(rows)) if cols else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("shot")
    ap.add_argument("pos", nargs="*", type=int)
    ap.add_argument("--x0", type=int, default=0)
    ap.add_argument("--x1", type=int)
    ap.add_argument("--min", type=int, default=3)
    ap.add_argument("--col", action="store_true", help="scan columns (pos = x) instead of rows")
    ap.add_argument("--ink")
    a = ap.parse_args()
    im = Image.open(a.shot).convert("RGB")
    if a.ink:
        print("ink x %s-%s y %s-%s" % ink(im, *map(int, a.ink.split(","))))
        return
    for p in a.pos:
        if a.col:
            f, hi = (lambda v, p=p: im.getpixel((p, v))), a.x1 or im.height
        else:
            f, hi = (lambda v, p=p: im.getpixel((v, p))), a.x1 or im.width
        print(p, " ".join(f"{r[0]}-{r[1]}:{'~' if r[2] == '~' else '%02x%02x%02x' % r[2]}" for r in runs(f, a.x0, hi, a.min)))


if __name__ == "__main__":
    main()
