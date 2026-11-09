"""setval.py FILE ID VALUE: set one id's English in a .out.tsv exactly (keeps trailing spaces the Edit tool strips)."""
import sys
from pathlib import Path

p, eid, val = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
lines = p.read_text(encoding="utf-8").split("\n")
hits = [n for n, l in enumerate(lines) if l.split("\t")[0] == eid]
assert len(hits) == 1, hits
lines[hits[0]] = f"{eid}\t{val}"
p.write_text("\n".join(lines), encoding="utf-8", newline="\n")
print(repr(lines[hits[0]]))
