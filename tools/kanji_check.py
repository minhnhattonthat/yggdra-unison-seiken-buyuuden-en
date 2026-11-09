"""kanji_check.py: flag kanji readings the script never uses inside a dictionary word (likely misreads).

    python -X utf8 tools/kanji_check.py [--min 1]   -> work/kanji/suspect.tsv: char, uses, uses inside known words,
                                                       sample lines
Tokenizes every jp line with janome (pip install janome). A kanji that only ever lands in unknown tokens or as a
lone one-kanji token is suspect: check it with `tools/kanji.py ctx` and fix with `tools/kanji.py set`.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from janome.tokenizer import Tokenizer

ROOT = Path(__file__).resolve().parents[1]
KANJI = re.compile(r"[一-鿿々]")


def main():
    tk = Tokenizer()
    uses, good, sample = defaultdict(int), defaultdict(int), defaultdict(list)
    for p in sorted((ROOT / "script").glob("*/*.json")):
        for row in json.loads(p.read_text(encoding="utf-8"))["strings"]:
            line = re.sub(r"[︀-️]", "", row["jp"]).replace("\n", "")
            for t in tk.tokenize(line):
                s = t.surface
                known = t.reading != "*" and (len(s) > 1 or t.part_of_speech.split(",")[0] in ("動詞", "形容詞", "接頭詞"))
                for c in KANJI.findall(s):
                    uses[c] += 1
                    good[c] += known
                    if len(sample[c]) < 2:
                        sample[c].append(line[:40])
    runs = defaultdict(int)  # kanji compounds the dictionary can't split into known words
    for p in sorted((ROOT / "script").glob("*/*.json")):
        for row in json.loads(p.read_text(encoding="utf-8"))["strings"]:
            for run in re.findall(r"[一-鿿々]{2,}", re.sub(r"[︀-️]", "", row["jp"])):
                runs[run] += 1
    bad = [r for r in runs if any(t.reading == "*" or (len(t.surface) == 1 and t.part_of_speech.startswith("名詞,一般"))
                                  for t in tk.tokenize(r))]
    (ROOT / "work/kanji/compounds.tsv").write_text("".join(f"{r}\t{runs[r]}\n" for r in sorted(bad)),
                                                   encoding="utf-8")
    print(f"{len(bad)} of {len(runs)} kanji compounds unknown -> work/kanji/compounds.tsv")
    rows = sorted((c for c in uses if good[c] == 0), key=lambda c: -uses[c])
    out = ROOT / "work/kanji/suspect.tsv"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(f"{c}\t{uses[c]}\t{good[c]}\t{' | '.join(sample[c])}\n" for c in rows), encoding="utf-8")
    print(f"{len(uses)} kanji used, {len(rows)} never inside a known word -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
