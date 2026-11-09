"""marker.py: phase-5 marker text. Every script line becomes "[id] filler" at full box width; every system string a
short code that fits its slot (system strings stay in place until relocation exists).

    python -X utf8 tools/build.py --marker      -> build/yggdra_marker.nds, work/marker_ids.tsv (code -> id)

Script ids: M012:1A4 = MESSAGE012 offset 0x1A4, S001002:40 = SPMES001002, T00-01:40 = TUTO00_01, E05:40 = EDMES05.
System codes: base-36 index into work/marker_ids.tsv, then ":" and filler to the slot size.
"""
import os
import re
import struct
import sys
from functools import cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import text  # noqa: E402
from tbl import Table  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
FILL = "The quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs. "
LINE_PX = int(os.environ.get("MARKER_PX", 250))  # filler per line (wider than any box, so the clip edge shows)


@cache
def en():
    return Table.load(ROOT / "tbl/en.tbl")


@cache
def widths():
    import enfont
    files = text.sfs_files({"FONT_MES.NTFT"})
    return {ch: adv for ch, (_, _, adv) in enfont.glyphs(files["FONT_MES.NTFT"]).items()}


def encode(s):
    return en().encode(s.replace("\n", "{br}"))


def fill(head, px):
    """head + filler up to px wide."""
    out, w, i = head, sum(widths()[c] for c in head), 0
    while True:
        c = FILL[i % len(FILL)]
        if w + widths()[c] > px:
            return out
        out, w, i = out + c, w + widths()[c], i + 1


def short_id(name, off):
    stem = name.rsplit(".", 1)[0].replace("_", "-")
    m = re.fullmatch(r"(MESSAGE|SPMES|TUTO|EDMES)(.+)", stem)
    return f"{m.group(1)[0]}{m.group(2).lstrip('0') or '0' if m.group(1) == 'MESSAGE' else m.group(2)}:{off:X}"


def qa_lines():
    """MARKER_QA="MESSAGE166:0240=text|..." overrides single lines (width gate, torture line); "\\n" = new line.
    "#142x2" = 2 lines of filler, each as close to 142 px as the glyphs allow (the exact-limit test)."""
    out = {}
    for item in filter(None, os.environ.get("MARKER_QA", "").split("|")):
        k, v = item.split("=", 1)
        if m := re.fullmatch(r"#(\d+)x(\d+)", v):
            v = "\n".join(fill(f"{n + 1}W", int(m.group(1))) for n in range(int(m.group(2))))
        out[k] = v.replace("\\n", "\n")
    return out


def script_line(name, off, jp):
    qa = qa_lines().get(text.sid(name, off))
    if qa is not None:
        return encode(qa)
    lines = jp.split("\n")
    # ( ) not [ ]: the font has no brackets
    out = [fill(f"({short_id(name, off)}) ", LINE_PX)] + [fill(f"{n + 2}", LINE_PX) for n in range(len(lines) - 1)]
    return encode("\n".join(out))


def b36(n):
    s = ""
    while True:
        n, r = divmod(n, 36)
        s = "0123456789abcdefghijklmnopqrstuvwxyz"[r] + s
        if not n:
            return s


def system_line(code, jp, room):
    """code, then filler, in room bytes (FF excluded); keeps the JP line count when there is room."""
    nl = jp.count("\n")
    if room - nl < len(code) + 2:
        return encode(code[:room])
    per = (room - nl) // (nl + 1)
    parts = [(code + ":" + FILL)[:per]] + [(f"{n + 2}" + FILL)[:per] for n in range(nl)]
    return encode("\n".join(parts))


def script_files(skip=()):
    """{name: marker bytes} for every MESSAGE/SPMES/TUTO/EDMES file, bar families in skip (bisecting a hang)."""
    out = {}
    for name, b in text.text_files().items():
        if text.family(name)[0] in skip or any(re.fullmatch(p, name.rsplit(".", 1)[0]) for p in skip):
            continue
        sa, strs, refs, tail = text.layout(name, b)
        font = text.family(name)[1]
        new = [script_line(name, s, text.decode(font, b[s:e - 1])) for s, e in strs]
        if os.environ.get("MARKER_SAME"):  # experiment: same byte length, so no string moves
            new = [n[:e - 1 - s].ljust(e - 1 - s, encode("x")) for n, (s, e) in zip(new, strs)]
        out[name] = text.rebuild(name, b, new) + bytes(int(os.environ.get("MARKER_GROW", "0"), 16))
    return out


def system_images():
    """{image: bytes} with every pool string replaced in place by its code; writes work/marker_ids.tsv."""
    images = {k: bytearray(v) for k, v in text.code_images().items()}
    rows, n = [], 0
    for img, doc in text.system_docs().items():
        for r in doc["strings"]:
            code = b36(n)
            n += 1
            rows.append(f"{code}\t{r['id']}\t{r['jp']}")
            off = int(r["id"].split(":")[1], 16)
            raw = system_line(code, r["jp"], r["max"] - 1)
            images[img][off:off + r["max"]] = (raw + b"\xff").ljust(r["max"], b"\0")
    (ROOT / "work").mkdir(exist_ok=True)
    (ROOT / "work/marker_ids.tsv").write_text("\n".join(rows) + "\n", encoding="utf-8")
    return {k: bytes(v) for k, v in images.items()}


def selftest():
    assert short_id("MESSAGE012.BIN", 0x1A4) == "M12:1A4" and short_id("SPMES001002.BIN", 0x40) == "S001002:40"
    assert b36(0) == "0" and b36(36) == "10"
    assert len(system_line("a1", "あ\nい", 3)) <= 3 and len(system_line("a1", "あ\nい", 20)) == 19
    assert struct  # keep import for callers


if __name__ == "__main__":
    selftest()
    print("ok")
