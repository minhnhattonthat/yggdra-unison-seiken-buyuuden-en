"""leftink.py [NAME..]: ink of the original atlas outside every gfx/text.tsv box of that NAME, grouped into rects.

An atlas row that was never given a box (a label the quads log never showed) stays Japanese in the build; this lists
the ink no box covers so each leftover can be looked at (`sheet.py work/gfx/ui/NAME.png --crop x,y,w,h --zoom 4`).
English, digits and art also show up: judge by eye. Default NAMEs: every name with box= rows.

    python -X utf8 tools/leftink.py FORSEL_FONT SYSTEX
"""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import gen_gfx, gfx  # noqa: E402


def groups(mask, gap=3):
    """Connected ink runs (8-neighbour after dilating by gap) -> [(x, y, w, h, px)]."""
    from collections import deque
    h, w = mask.shape
    seen = np.zeros_like(mask, bool)
    ys, xs = np.nonzero(mask)
    pts = set(zip(ys.tolist(), xs.tolist()))
    out = []
    for p in zip(ys.tolist(), xs.tolist()):
        if seen[p]:
            continue
        q, comp = deque([p]), []
        seen[p] = True
        while q:
            y, x = q.popleft()
            comp.append((y, x))
            for dy in range(-gap, gap + 1):
                for dx in range(-gap, gap + 1):
                    n = (y + dy, x + dx)
                    if n in pts and not seen[n]:
                        seen[n] = True
                        q.append(n)
        cy, cx = zip(*comp)
        out.append((min(cx), min(cy), max(cx) - min(cx) + 1, max(cy) - min(cy) + 1, len(comp)))
    return out


def main(argv):
    boxes = {}
    for name, en, o in gen_gfx.rows():
        if "box" in o:
            boxes.setdefault(name, []).append(tuple(map(int, o["box"].split(","))))
    for name in argv or sorted(boxes):
        img, _ = gfx.load(name + ".PACK")
        a = np.asarray(img.convert("RGBA")).astype(int)
        ink = (a[..., 3] > 0) & (a[..., :3].max(-1) > 120)
        for x, y, w, h in boxes.get(name, []):
            ink[y:y + h, x:x + w] = False
        for g in sorted(groups(ink), key=lambda g: (g[1], g[0])):
            if g[4] >= 12 and g[2] >= 6 and g[3] >= 5:
                print(f"{name}\t{g[0]},{g[1]},{g[2]},{g[3]}\t{g[4]} px")


if __name__ == "__main__":
    main(sys.argv[1:])
