"""inkx.py: horizontal extent and centre of near-white text fill inside rects of a screenshot.

inkbox.py takes the rect's commonest colour as background, which fails on the game's gradient buttons; the text
fill here is white, so this measures only pixels whose channels are all > --min. Compare with the original ROM's
shot of the same frame (work/qa/tour_jp) to judge centring:

    python -X utf8 tools/inkx.py SHOT.png x,y,w,h [x,y,w,h ..] [--min 215]
"""
import argparse

from PIL import Image


def extent(im, rect, lo):
    x, y, w, h = rect
    xs = [i for i in range(x, x + w) for j in range(y, y + h) if min(im.getpixel((i, j))) > lo]
    return (min(xs), max(xs)) if xs else None


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("png")
    p.add_argument("rects", nargs="+")
    p.add_argument("--min", type=int, default=215)
    a = p.parse_args()
    im = Image.open(a.png).convert("RGB")
    for r in a.rects:
        e = extent(im, tuple(map(int, r.split(","))), a.min)
        print(r, *(e + ((e[0] + e[1]) / 2,) if e else ("none",)))


if __name__ == "__main__":
    main()
