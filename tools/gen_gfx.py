"""gen_gfx.py: draw the English texture labels of gfx/text.tsv into gfx/<NAME>.png (tools/gfx.py encodes them).

gfx/text.tsv: NAME <TAB> English (\\n = new line) <TAB> options. One row per label; several rows may share a NAME
(atlas: each with its own box). Options (space separated, key=value):
  box=x,y,w,h   rect to clear and draw in (default: bbox of the original's opaque pixels)
  font=serif-b  serif-b serif sans-b sans (fonts/, docs/fonts.md)
  size=N        px (default: the largest that fits the box height per line, capped by width after squeezing)
  align=c       l / c / r inside the box;  wide=N  how far the text may spread past the box (default: to the edge)
  stroke=1      outline px;  min_x=0.7  narrowest horizontal squeeze before the size shrinks
  clear=row     repaint the box row by row with the pixel left of it (text on a panel) instead of transparency
Colours come from the original: fill = per-row brightest opaque colour in the box (keeps gradients), outline =
the darkest common opaque colour. Alpha is binary (4x4 textures have no partial alpha).

    python -X utf8 tools/gen_gfx.py [NAME ..]        all rows, or those NAMEs; prints each fit
"""
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import gfx  # noqa: E402

FONTS = {"serif-b": "LiberationSerif-Bold.ttf", "serif": "LiberationSerif-Regular.ttf",
         "sans-b": "LiberationSans-Bold.ttf", "sans": "LiberationSans-Regular.ttf"}
TSV = ROOT / "gfx/text.tsv"


def rows():
    out = []
    for line in TSV.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        name, en, *opt = line.split("\t")
        o = dict(kv.split("=", 1) for kv in (opt[0].split() if opt else []))
        out.append((name, en.replace("\\n", "\n"), o))
    return out


def bbox(a):
    ys, xs = np.nonzero(a[..., 3] > 0)
    return (int(xs.min()), int(ys.min()), int(xs.max()) - int(xs.min()) + 1, int(ys.max()) - int(ys.min()) + 1)


def colours(a, box):
    x, y, w, h = box
    sub = a[y:y + h, x:x + w]
    op = sub[..., 3] > 0
    lum = sub[..., :3].sum(-1)
    dark = Counter(tuple(c) for c in sub[op & (lum < 200)][:, :3]).most_common(1)
    outline = np.array(dark[0][0] if dark else (0, 0, 0))
    fill = []
    bright = lum[op].max() // 2  # rows with only panel/outline colours take the brightest inked row's fill
    for r in range(h):
        m = op[r] & (lum[r] >= bright)
        fill.append(sub[r][m][lum[r][m].argmax()][:3] if m.any() else None)
    top = max((f for f in fill if f is not None), key=lambda f: int(f.sum()))
    fill = [f if f is not None else top for f in fill]
    return outline, np.array(fill)


def font(name, size):
    return ImageFont.truetype(str(ROOT / "fonts" / FONTS[name]), size)


def layout(text, o, box, maxw):
    """-> (font, xscale, line height) fitting len(lines) lines in box height and maxw width."""
    lines = text.split("\n")
    stroke = int(o.get("stroke", 1))
    _, _, _, h = box
    lh = h / len(lines)
    size = int(o["size"]) if "size" in o else None
    for s in ([size] if size else range(int(lh * 1.6), 5, -1)):
        f = font(o.get("font", "serif-b"), s)
        ink = [f.getbbox(ln) for ln in lines]
        top, bot = min(b[1] for b in ink), max(b[3] for b in ink)
        if size is None and bot - top + 2 * stroke > lh:
            continue
        w = max(f.getlength(ln) for ln in lines) + 2 * stroke
        xs = min(1.0, maxw / w)
        if xs >= float(o.get("min_x", 0.7)) or size:
            return f, xs, lh, top, bot
    raise ValueError(f"{text!r} does not fit {box}")


def draw(a, text, o):
    """Clear the label's box in RGBA array a and draw text there."""
    box = tuple(map(int, o["box"].split(","))) if "box" in o else bbox(a)
    x, y, w, h = box
    H, W = a.shape[:2]
    outline, fill = colours(a, box)
    wide = int(o["wide"]) if "wide" in o else None
    align = o.get("align", "c")
    if wide is not None:
        maxw = w + 2 * wide
    elif align == "c":
        maxw = 2 * min(x + w / 2, W - x - w / 2) - 2
    else:
        maxw = W - x - 1 if align == "l" else x + w - 1
    f, xs, lh, top, bot = layout(text, o, box, maxw)
    stroke = int(o.get("stroke", 1))
    lines = text.split("\n")
    tw = max(f.getlength(ln) for ln in lines)
    cw = int(tw + 2 * stroke + 4)
    ch = int(round(lh)) * len(lines) + 4
    outer = Image.new("L", (cw, ch))
    inner = Image.new("L", (cw, ch))
    for n, ln in enumerate(lines):
        dx = {"c": (tw - f.getlength(ln)) / 2, "r": tw - f.getlength(ln)}.get(align, 0)  # each line aligned
        pos = (stroke + 2 + dx, n * lh + (lh - (bot - top)) / 2 - top + 2)
        ImageDraw.Draw(outer).text(pos, ln, font=f, fill=255, stroke_width=stroke, stroke_fill=255)
        ImageDraw.Draw(inner).text(pos, ln, font=f, fill=255)
    nw = max(1, round(cw * xs))
    outer, inner = (np.array(im.resize((nw, ch), Image.LANCZOS)) / 255.0 for im in (outer, inner))
    if o.get("clear") == "row":  # text on a panel: repaint each row with the panel colour left of the box
        a[y:y + h, x:x + w] = a[y:y + h, x - 1:x]
    else:
        a[y:y + h, x:x + w] = 0
    if align == "c":
        ox = round(x + w / 2 - nw / 2)
    elif align == "l":
        ox = x - stroke - 2
    else:
        ox = x + w - nw + stroke + 2
    oy = y - 2
    for r in range(ch):
        for c in range(nw):
            X, Y = ox + c, oy + r
            if not (0 <= X < W and 0 <= Y < H) or outer[r, c] < 0.5:
                continue
            fc = fill[min(max(Y - y, 0), len(fill) - 1)]
            t = min(1.0, inner[r, c])
            a[Y, X, :3] = np.round(outline * (1 - t) + fc * t)
            a[Y, X, 3] = 255
    return box, f.size, xs


def main(argv):
    want = set(argv)
    by_name = {}
    for name, en, o in rows():
        if not want or name in want:
            by_name.setdefault(name, []).append((en, o))
    for name, labels in by_name.items():
        img, _ = gfx.load(name + ".PACK")
        a = np.array(img.convert("RGBA"), dtype=np.int32)
        for en, o in labels:
            box, size, xs = draw(a, en, o)
            print(f"{name}: {en!r} box {box} size {size} xscale {xs:.2f}")
        Image.fromarray(a.astype(np.uint8)).save(gfx.GFX / f"{name}.png")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
