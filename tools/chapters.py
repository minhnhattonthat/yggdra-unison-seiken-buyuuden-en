"""chapters.py: story-pass input (docs/story-reviewer-brief.md): one file per "chapter" in work/qa/story/chapters/.

    python -X utf8 tools/chapters.py      -> work/qa/story/chapters/<chapter>.txt, then
    python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" init work/qa/story/manifest.tsv work/qa/story/chapters --glob "*.txt"

The game has no linear plot (docs/synopsis.md), so a chapter is a run of script files in file order: battle barks
(MESSAGE, 20 files each), duel events grouped by first character (SPMESxxx), endings (EDMES), the tutorial, and
the prose drawn as textures (gfx/text.tsv: English only, the JP is in the image). Lines with no English
(unused placeholders) are left out. Speaker = the batch TSV's hint (work/tl), blank when unknown.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "work/qa/story/chapters"
PROSE = re.compile(r"^(MS_PRO|IN_PRO|OPK_WR|EPI_MES|EPI_TIT|CS_M|MS_M|CN_M|TM_M|_unk_)")
SPMES_CAP = 40000  # chars of JP+EN per duel chapter


def flat(s):
    return s.replace("\\n", " / ").replace("\n", " / ")


def speakers():
    out = {}
    for p in (ROOT / "work/tl").glob("b*.tsv"):
        if p.name.endswith(".out.tsv"):
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            r = line.split("\t")
            if len(r) > 1 and r[1]:
                out[r[0]] = r[1]
    return out


def lines(paths, spk):
    out = []
    for p in paths:
        for s in json.loads(p.read_text(encoding="utf-8"))["strings"]:
            if s.get("en"):
                out += [f">> {s['id']} | {spk.get(s['id'], '')} | {flat(s['jp'])}", f"   {flat(s['en'])}"]
    return out


def chapters():
    s = ROOT / "script"
    msg = sorted((s / "message").glob("*.json"))
    starts = list(range(0, len(msg) - 10, 20))  # the last group takes a short tail (MESSAGE220)
    yield from ((f"msg_{i:03d}", msg[i:j]) for i, j in zip(starts, starts[1:] + [len(msg)]))
    duel, cur, size = [], [], 0
    for p in sorted((s / "spmes").glob("*.json")):
        n = p.stat().st_size
        if cur and size + n > SPMES_CAP * 2 and p.stem[5:8] != cur[-1].stem[5:8]:  # json ~2x the text
            duel.append(cur)
            cur, size = [], 0
        cur.append(p)
        size += n
    duel.append(cur)
    yield from ((f"duel_{c[0].stem[5:8]}-{c[-1].stem[5:8]}", c) for c in duel)
    ed = sorted((s / "edmes").glob("*.json"))
    yield "ending_a", ed[:19]
    yield "ending_b", ed[19:]
    yield "tutorial", sorted((s / "tuto").glob("*.json"))


def main():
    spk = speakers()
    OUT.mkdir(parents=True, exist_ok=True)
    for name, paths in chapters():
        (OUT / f"{name}.txt").write_text("\n".join(lines(paths, spk)) + "\n", encoding="utf-8", newline="\n")
    prose = []
    for line in (ROOT / "gfx/text.tsv").read_text(encoding="utf-8").splitlines():
        r = line.split("\t")
        if len(r) > 1 and PROSE.match(r[0]):
            prose += [f">> {r[0]} | | (texture, JP in the image)", f"   {flat(r[1])}"]
    (OUT / "textures.txt").write_text("\n".join(prose) + "\n", encoding="utf-8", newline="\n")
    for p in sorted(OUT.glob("*.txt")):
        print(p.name, p.stat().st_size)


if __name__ == "__main__":
    main()
