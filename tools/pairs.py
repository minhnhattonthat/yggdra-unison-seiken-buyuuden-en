"""pairs.py: reviewer input (docs/reviewer-brief.md) from translated batches.

    python -X utf8 tools/pairs.py bNNN [bNNN ...]   -> work/qa/pairs/<first>-<last>.txt

One block per entry, in batch (= file) order, so neighbours are the context: `>> id | speaker | JP` then `   EN`.
Line breaks show as ` / `.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TL = ROOT / "work/tl"


def rows(batch):
    src = [line.split("\t") for line in (TL / f"{batch}.tsv").read_text(encoding="utf-8").splitlines() if line]
    out = {}
    p = TL / f"{batch}.out.tsv"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            if line:
                i, _, en = line.partition("\t")
                out[i] = en
    return [(r[0], r[1], r[4], out.get(r[0], "")) for r in src]


def flat(s):
    return s.replace("\\n", " / ").replace("\n", " / ")


def main(batches):
    entries = [e for b in batches for e in rows(b)]
    lines = []
    for i, spk, jp, en in entries:  # file order: the neighbours are the context
        lines += [f">> {i} | {spk} | {flat(jp)}", f"   {flat(en)}"]
    out = ROOT / f"work/qa/pairs/{batches[0]}-{batches[-1]}.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(out, len(entries), "entries")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:]) if sys.argv[1:] else sys.exit(__doc__)
