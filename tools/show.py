"""show.py: print script entries by id (or a JP/EN regex) with their box budget.

    python -X utf8 tools/show.py ID [ID ...]          id, budget, JP, EN
    python -X utf8 tools/show.py --grep REGEX [--file PREFIX]   every entry whose JP or EN matches
    python -X utf8 tools/show.py --ctx N ID           the entry with N neighbours either side (same file)
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import batches


def show(e):
    r = batches.rule(e)
    print(f">> {e['id']}  [{r['px']}px x{r['lines']}]  {e['jp']!r}\n   {e.get('en', '')!r}")


def main(argv):
    if not argv:
        sys.exit(__doc__)
    if argv[0] == "--grep":
        pat, pre = re.compile(argv[1]), argv[argv.index("--file") + 1] if "--file" in argv else ""
        for e in batches.index().values():
            if e["id"].startswith(pre) and (pat.search(e["jp"]) or pat.search(e.get("en", ""))):
                show(e)
        return 0
    ctx = 0
    if argv[0] == "--ctx":
        ctx, argv = int(argv[1]), argv[2:]
    ids = list(batches.index())
    idx = batches.index()
    for eid in argv:
        i = ids.index(eid)
        f = eid.split(":")[0]
        for j in range(max(0, i - ctx), min(len(ids), i + ctx + 1)):
            if ids[j].split(":")[0] == f:
                show(idx[ids[j]])
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
