"""gfxsweep.py: static graphics-text sweep. Render every .PACK texture (tools/tex.py) into labelled pages per prefix.

    python tools/gfxsweep.py [PREFIX_REGEX] [--out work/gfx/sweep] [--zoom 1] [--packed]  (--packed: all prefixes share pages)

Pages: work/gfx/sweep/<prefix>_<n>.png (<= 1600 px wide, <= 1800 tall), index.tsv (file, kind, w, h, page).
Every PACK is either rendered or listed as skipped with the reason; none is dropped silently.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tex  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PW, PH = 1600, 1800


def prefix(name):
    return re.sub(r"[0-9]+.*$|\.PACK$", "", name).rstrip("_") or name


def pages(items, zoom):
    """Shelf-pack (label, img) into pages."""
    out, page, x, y, rowh = [], [], 0, 0, 0
    for label, img in items:
        if zoom != 1:
            img = img.resize((img.width * zoom, img.height * zoom), Image.NEAREST)
        w, h = min(img.width, PW), min(img.height, PH - 12) + 12
        if x + w > PW:
            x, y, rowh = 0, y + rowh + 4, 0
        if y + h > PH and page:
            out.append(page)
            page, x, y, rowh = [], 0, 0, 0
        page.append((x, y, label, img))
        x, rowh = x + w + 4, max(rowh, h)
    if page:
        out.append(page)
    return out


def main():
    pat = re.compile(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else None
    out = ROOT / (sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "work/gfx/sweep")
    zoom = int(sys.argv[sys.argv.index("--zoom") + 1]) if "--zoom" in sys.argv else 1
    out.mkdir(parents=True, exist_ok=True)
    groups, index, skipped = defaultdict(list), [], []
    unk = sorted((ROOT / "work/sfs/_unk").glob("*.bin"))  # unnamed files: PACKs by header, else skipped with reason
    for p in sorted((ROOT / "work/sfs").glob("*.PACK")) + unk:
        if pat and not pat.search(p.name):
            continue
        try:
            t, pal, idx = tex.parts(p.read_bytes())
            if not t:
                skipped.append((p.name, "empty texel part"))
                continue
            w = tex.guess(t, pal, idx)
            img = tex.render(t, pal, idx, w)
        except Exception as e:  # report, never drop
            skipped.append((p.name, f"{type(e).__name__}: {e}"))
            continue
        bg = Image.new("RGBA", img.size, (60, 60, 110, 255))
        bg.alpha_composite(img)
        g = "all" if "--packed" in sys.argv else "_unk" if p.parent.name == "_unk" else prefix(p.name)
        groups[g].append((p.stem, bg))
        index.append([p.name, tex.kind(t, pal, idx), img.width, img.height, ""])
    pageof = {}
    for g, items in sorted(groups.items()):
        for n, page in enumerate(pages(items, zoom)):
            W = max(x + min(i.width, PW) for x, _, _, i in page)
            H = max(y + min(i.height, PH - 12) + 12 for _, y, _, i in page)
            sheet = Image.new("RGB", (W, H), (20, 20, 20))
            d = ImageDraw.Draw(sheet)
            for x, y, label, img in page:
                d.text((x, y), label, fill=(255, 200, 0))
                sheet.paste(img.convert("RGB"), (x, y + 12))
                pageof[label] = f"{g}_{n}.png"
            sheet.save(out / f"{g}_{n}.png")
    for r in index:
        r[4] = pageof.get(r[0].rsplit(".", 1)[0], "")
    (out / "index.tsv").write_text("".join("\t".join(map(str, r)) + "\n" for r in index), encoding="utf-8")
    (out / "skipped.tsv").write_text("".join(f"{a}\t{b}\n" for a, b in skipped), encoding="utf-8")
    print(f"{len(index)} rendered, {len(skipped)} skipped, {len(set(pageof.values()))} pages -> {out}")


if __name__ == "__main__":
    main()
