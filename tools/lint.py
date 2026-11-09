"""lint.py: text lint over script/ (run by tools/check.py). Exit 1 on any error.

Per string with English: every character encodable in tbl/en.tbl, no Japanese left, line count and pixel width
within the box budget from script/windows.json (first matching rule; line px = sum of VWF advances + 1, the outline
column of the last glyph). Lines held to a "guess" budget are counted in one summary line, not listed.

    python -X utf8 tools/lint.py [-v]      (-v lists the guess-budget lines too)
"""
import json
import re
import sys
from functools import cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
JP = re.compile(r"[぀-ヿ一-鿿＀-￯]")


@cache
def rules():
    return json.loads((ROOT / "script/windows.json").read_text(encoding="utf-8"))["rules"]


@cache
def widths():
    # shortcut: FONT_MES advances for every font (enfont puts the same English glyphs in all four); if FONT_ITEM's
    # palette-mapped glyphs get their own widths, read them per font here.
    import marker
    return marker.widths()


def rule_for(sid, jp, font):
    for r in rules():
        if not re.search(r["match"], sid):
            continue
        if r.get("multi") and "\n" not in jp:
            continue
        if r.get("font") and r["font"] != font:
            continue
        return r
    return None


def line_px(line):
    return sum(widths()[c] for c in line) + 1 if line else 0


def check_string(s, font):
    """-> (errors, guess_lines) for one script row."""
    en, errs = s.get("en", ""), []
    if not en:
        return errs, 0
    if JP.search(en):
        errs.append("Japanese left in en")
    bad = sorted(set(c for c in en if c != "\n" and c not in widths()))
    if bad:
        errs.append(f"no glyph for {''.join(bad)!r}")
        return errs, 0
    r = rule_for(s["id"], s["jp"], s.get("font", font))
    if r is None:
        return errs + ["no window rule"], 0
    lines = en.split("\n")
    if len(lines) > r["lines"]:
        errs.append(f"{len(lines)} lines > {r['lines']} ({r['box']})")
    for n, line in enumerate(lines, 1):
        if line_px(line) > r["px"]:
            errs.append(f"line {n} {line_px(line)} px > {r['px']} ({r['box']})")
    return errs, (len(lines) if r["status"] == "guess" else 0)


def selftest():
    s = {"id": "MESSAGE154:0240", "jp": "あ", "en": "Hi"}
    assert check_string(s, "mes") == ([], 0)
    assert check_string({**s, "en": "a\nb\nc"}, "mes")[0]
    assert any("px" in e for e in check_string({**s, "en": "W" * 40}, "mes")[0])
    assert check_string({**s, "en": "あ"}, "mes")[0]
    assert rule_for("EDMES07:0100", "a\nb", "end")["lines"] == 4 and rule_for("EDMES07:009C", "a", "end")["lines"] == 1
    assert rule_for("arm9:8F98C", "a", "item")["font"] == "item"


def main():
    selftest()
    errors, guess, done = [], 0, 0
    for p in sorted((ROOT / "script").rglob("*.json")):
        if p.name == "windows.json":
            continue
        doc = json.loads(p.read_text(encoding="utf-8"))
        for s in doc["strings"]:
            e, g = check_string(s, doc.get("font"))
            errors += [f"{s['id']}: {m}" for m in e]
            guess += g
            done += bool(s.get("en"))
    for e in errors:
        print(e)
    print(f"lint: {done} strings with English, {len(errors)} errors, {guess} lines held to guessed budgets")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
