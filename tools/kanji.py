"""kanji.py: read the fonts' kanji once per bitmap. Readings go to tbl/kanji.tsv (key, char, first seen).

    python -X utf8 tools/kanji.py todo           -> work/kanji/todo.tsv + work/kanji/sheet_NN.png: every unread kanji
                                                    kanji bitmap of the three fonts, numbered, 160 per sheet,
                                                    with up to 3 script lines per glyph in todo.tsv for context
    python -X utf8 tools/kanji.py add FILE [START]  merge "N<TAB>char" lines (N = todo number) into tbl/kanji.tsv, or
                                                    with START, rows of chars read off a sheet from todo number START
    python -X utf8 tools/kanji.py dupes          chars read for two different bitmaps of one font (look-alike swaps)
    python -X utf8 tools/kanji.py set mes:182=栄 [...]   correct readings by font glyph
    python -X utf8 tools/kanji.py ctx mes:182 [...]      script lines using a glyph
Then run tools/mkjptbl.py and `tools/text.py dump --force`.
"""
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mkjptbl  # noqa: E402
import text  # noqa: E402
from glyphsheet import sheet  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "work/kanji"
PER_SHEET = 160


def glyphs(raw):
    i = 0
    while i < len(raw):
        c = raw[i]
        if 0xF1 <= c <= 0xF9:
            yield (c - 0xF0) * 0xF0 + raw[i + 1], i
            i += 2
        elif c == 0xFC:
            i += 2
        else:
            if c < 0xF0:
                yield c, i
            i += 1


def usage():
    """{font: {glyph: [sample string ids]}} over the script files."""
    use = {f: defaultdict(list) for f in mkjptbl.FONTS}
    for name, b in text.text_files().items():
        font = text.family(name)[1]
        _, strs, _, _ = text.layout(name, b)
        for s, e in strs:
            for g, _ in glyphs(b[s:e - 1]):
                if g >= mkjptbl.FIRST_KANJI and len(use[font][g]) < 3:
                    use[font][g].append((name, s))
    return use


def todo():
    rd = mkjptbl.readings()
    use = usage()
    files = text.text_files()
    seen, rows = set(), []
    for font in ("mes", "sys", "end"):
        data = mkjptbl.font_bytes(font)
        gs = range(mkjptbl.FIRST_KANJI, len(data) // 128)  # all: system text in arm9/overlays uses any font
        for g in gs:
            raw = data[g * 128:(g + 1) * 128]
            k = mkjptbl.key(raw)
            if k in rd or k in seen or not any(raw):
                continue
            seen.add(k)
            ctx = []
            for name, s in use[font].get(g, []):
                b = files[name]
                e = b.index(b"\xff", s)
                ctx.append(text.decode(font, b[s:e]).replace("\n", "/"))
            rows.append((k, font, g, raw, ctx))
    WORK.mkdir(parents=True, exist_ok=True)
    for old in WORK.glob("sheet_*.png"):
        old.unlink()
    with open(WORK / "todo.tsv", "w", encoding="utf-8", newline="\n") as f:
        for n, (k, font, g, raw, ctx) in enumerate(rows):
            f.write(f"{n}\t{k}\t{font}:{g:03X}\t" + " | ".join(ctx) + "\n")
    for p in range(0, len(rows), PER_SHEET):
        cells = [(str(n), rows[n][3]) for n in range(p, min(p + PER_SHEET, len(rows)))]
        sheet(cells, 16, 3).save(WORK / f"sheet_{p // PER_SHEET:02d}.png")
    print(f"{len(rows)} unread bitmaps -> {WORK.relative_to(ROOT)}/todo.tsv, {-(-len(rows) // PER_SHEET)} sheets")


def add(path, start=None):
    """path: "N<TAB>char" lines, or (with start) lines of chars read off a sheet in order from todo number start;
    ＿ = not read yet."""
    todo_rows = {}
    for line in (WORK / "todo.tsv").read_text(encoding="utf-8").splitlines():
        n, k, where = line.split("\t")[:3]
        todo_rows[n] = (k, where)
    kt = ROOT / "tbl/kanji.tsv"
    lines = kt.read_text(encoding="utf-8").splitlines() if kt.exists() else ["# key\tchar\tfirst seen (tools/kanji.py)"]
    have = {ln.split("\t")[0] for ln in lines}
    added = 0
    src = [ln for ln in Path(path).read_text(encoding="utf-8").splitlines() if ln.strip() and not ln.startswith("#")]
    if start is not None:
        chars = "".join(ln.strip() for ln in src)
        src = [f"{start + i}\t{c}" for i, c in enumerate(chars)]
    for line in src:
        n, c = line.split("\t")[:2]
        k, where = todo_rows[n.strip()]
        c = c.strip()
        if k not in have and c and c != "＿":
            lines.append(f"{k}\t{c}\t{where}")
            have.add(k)
            added += 1
    kt.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"added {added} readings ({len(lines) - 1} total)")


def set_reading(where, c):
    """Correct one reading: where = font:hex glyph (e.g. mes:182)."""
    font, g = where.split(":")
    g = int(g, 16)
    k = mkjptbl.key(mkjptbl.font_bytes(font)[g * 128:(g + 1) * 128])
    kt = ROOT / "tbl/kanji.tsv"
    lines = kt.read_text(encoding="utf-8").splitlines()
    hit = [i for i, ln in enumerate(lines) if ln.split("\t")[0] == k]
    if hit:
        old = lines[hit[0]].split("\t")
        lines[hit[0]] = "\t".join([k, c, *old[2:]])
    else:
        lines.append(f"{k}\t{c}\t{where}")
    kt.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"{where} -> {c}")


def ctx(where, n=4):
    """Script lines using one glyph, the glyph shown as 【c】."""
    font, g = where.split(":")
    g = int(g, 16)
    for name, b in text.text_files().items():
        if text.family(name)[1] != font:
            continue
        _, strs, _, _ = text.layout(name, b)
        for s, e in strs:
            raw = b[s:e - 1]
            for gg, i in glyphs(raw):
                if gg == g:
                    w = 1 if g < 0xF0 else 2
                    c = text.decode(font, raw[i:i + w])
                    print(where, text.decode(font, raw[:i]) + f"【{c}】" + text.decode(font, raw[i + w:]))
                    n -= 1
                    break
            if n <= 0:
                return


def dupes():
    for font in mkjptbl.FONTS:
        by = defaultdict(list)
        for g, c in mkjptbl.chars(font).items():
            if g >= mkjptbl.FIRST_KANJI:
                by[c].append(g)
        d = {c: gs for c, gs in by.items() if len(gs) > 1}
        print(font, len(d), " ".join(f"{c}:{','.join(f'{g:X}' for g in gs)}" for c, gs in sorted(d.items())))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "todo"
    if cmd == "ctx":  # font:hex, or a char: every glyph read as it
        for w in sys.argv[2:]:
            if ":" in w:
                ctx(w)
            else:
                for font in mkjptbl.FONTS:
                    for g, c in mkjptbl.chars(font).items():
                        if c == w and g >= mkjptbl.FIRST_KANJI:
                            ctx(f"{font}:{g:X}", 3)
    elif cmd == "set":
        for pair in sys.argv[2:]:  # font:hex=char ...
            set_reading(*pair.split("="))
    else:
        {"todo": todo, "dupes": dupes}.get(cmd, lambda: add(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else None))()
