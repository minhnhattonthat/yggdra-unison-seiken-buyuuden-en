"""kanji_zoom.py: zoom a few todo numbers from work/kanji/todo.tsv side by side (look-alike checks).

    python -X utf8 tools/kanji_zoom.py OUT.png N [N ...] [--zoom 6]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mkjptbl  # noqa: E402
from glyphsheet import sheet  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
args = sys.argv[1:]
zoom = 6
if "--zoom" in args:
    i = args.index("--zoom")
    zoom = int(args[i + 1])
    del args[i:i + 2]
out, nums = args[0], set(args[1:])
cells = []
for line in (ROOT / "work/kanji/todo.tsv").read_text(encoding="utf-8").splitlines():
    n, _, where = line.split("\t")[:3]
    if n in nums:
        font, g = where.split(":")
        g = int(g, 16)
        cells.append((n, mkjptbl.font_bytes(font)[g * 128:(g + 1) * 128]))
sheet(cells, min(len(cells), 8), zoom).save(out)
