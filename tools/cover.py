"""cover.py: build/strings.tsv for the skill's textcover.py: one "id<TAB>hash" per string of the English build.

    python -X utf8 tools/cover.py [--jp]          (--jp: hashes of the original bytes, for a run on rom/)

The hash is the content key tools/lua/textcover.lua logs (strings sit in RAM buffers, so no fixed address):
fold of (h * 31 + byte + 1) mod 4294967291 over the bytes before FF. Then:
    python -X utf8 "$(python tools/skill.py)/scripts/textcover.py" work/qa/tour build/strings.tsv --waive docs/text_unshown.tsv
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import insert  # noqa: E402
import text  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def strhash(b):
    h = 0
    for x in b:
        h = (h * 31 + x + 1) % 4294967291
    return h


def rows(jp=False):
    """-> [(id, built bytes)] for every script-file and system string."""
    out = []
    for name, b in text.text_files().items():
        en = {r["id"]: r["en"] for r in text.load(name)["strings"]}
        for s, e in text.layout(name, b)[1]:
            sid = text.sid(name, s)
            out.append((sid, insert.encode(en[sid]) if en[sid] and not jp else b[s:e - 1]))
    images = text.code_images()
    for p in sorted((ROOT / "script/system").glob("*.json")):
        b = images[p.stem]
        for r in json.loads(p.read_text(encoding="utf-8"))["strings"]:
            off = int(r["id"].split(":")[1], 16)
            out.append((r["id"], insert.encode(r["en"]) if r["en"] and not jp else b[off:b.index(b"\xff", off)]))
    return out


def main():
    jp = "--jp" in sys.argv
    assert strhash(b"\x01\x02") == (2 * 31 + 3), "hash drifted from textcover.lua"
    out = ROOT / "build" / ("strings_jp.tsv" if jp else "strings.tsv")
    rs = rows(jp)
    out.write_text("".join(f"{i}\t{strhash(b):X}\n" for i, b in rs), encoding="utf-8")
    print(f"{len(rs)} strings -> {out}")


if __name__ == "__main__":
    main()
