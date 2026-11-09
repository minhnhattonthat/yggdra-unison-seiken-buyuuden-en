"""Translation batches (docs/translator-brief.md): split untranslated text, check translator output, merge it back.

    python -X utf8 tools/batches.py split [--size 3500] [--family system,tuto]   work/tl/bNNN.tsv + build/terms_bNNN.txt
    python -X utf8 tools/batches.py check [bNNN ...]      a batch's .out.tsv; with no batch, all shipped English
    python -X utf8 tools/batches.py merge bNNN ... [--overwrite]   check, then write the English into script/
    python -X utf8 tools/batches.py fit ID "English"     px per line against ID's box (\\n = line break)
    python -X utf8 tools/batches.py wrap ID "English"    greedy-wrap to ID's box; prints the \\n form to paste

From the skill's assets/batches.py; ADAPTER fitted to script/<family>/*.json ("strings" rows, widths from
tools/lint.py). Identical JP in the same box kind is batched once (first id) and merged into every copy.
Batch TSV: id, speaker, form, limit, JP (line breaks as \\n). Output: work/tl/bNNN.out.tsv, id<TAB>English.
"""
import json
import re
import struct
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
TL = ROOT / "work/tl"
SCRIPT = ROOT / "script"
GLOSSARY = ROOT / "glossary.md"
MAX_ENTRIES = 150
FAMILY_ORDER = ["system", "tuto", "message", "spmes", "edmes"]

# ---- ADAPTER: this game's text format ----
TOKEN = re.compile(r"(?!)")  # no inline control codes in this game ([dm／2] in effect text is literal text)
FREE = set()
VARIABLE = r"\[var[^\]]*\]"
HONORIFICS = {"さん": "-san", "ちゃん": "-chan", "くん": "-kun", "殿": "-dono", "様": "-sama"}  # D1, after a name
DUMMY = re.compile(r"^[あいうえお\n]+$")  # MESSAGE000 test lines
JP = re.compile(r"[぀-ヿ一-鿿＀-￯]")


def docs():
    """(path, doc, entries) per script file, in FAMILY_ORDER."""
    paths = [p for p in SCRIPT.rglob("*.json") if p.name != "windows.json"]
    paths.sort(key=lambda p: (FAMILY_ORDER.index(p.parent.name) if p.parent.name in FAMILY_ORDER else 99, p.name))
    for path in paths:
        doc = json.loads(path.read_text(encoding="utf-8"))
        for e in doc["strings"]:
            e.setdefault("font", doc.get("font"))
        yield path, doc, doc["strings"]


def needs_english(entry):
    """Empty, test-file and no-Japanese strings (digits, 'P') are not translated."""
    jp = entry.get("jp", "")
    return bool(JP.search(jp)) and not DUMMY.match(jp) and not entry.get("en")


def rule(entry):
    import lint
    return lint.rule_for(entry["id"], entry["jp"], entry.get("font"))


def group_of(entry):
    """Same JP in the same box kind = one translation."""
    r = rule(entry)
    return (entry["jp"], entry.get("font"), r and r["match"], r and r.get("table"), r and r["box"])


def limit_label(entry):
    r = rule(entry)
    if not r:
        return "?"
    if r["status"] in ("composite", "unread"):
        return f"{r['px']}px x{r['lines']} ({r['status']})"
    return f"{r['px']}px x{r['lines']}"


def form_of(entry, path):
    fam = path.parent.name
    if fam in ("message", "spmes", "tuto"):
        return "dlg"
    if fam == "edmes":
        return "epilogue" if "\n" in entry["jp"] else "epithet"
    r = rule(entry)
    return (r["box"].split("(")[0].split(":")[0].strip()[:48] if r else "menu").replace("\t", " ")


def width_problems(entry, en):
    import lint
    errs, _ = lint.check_string({**entry, "en": en}, entry.get("font"))
    return [e for e in errs if not e.startswith("no glyph")]


def encodable(char):
    import lint
    return char in lint.widths()
# ---- end of ADAPTER ----


UNITS = None


def unit_names():
    """Unit table F5380 (stride 0x14, field +0) -> JP name per speaker id (opcode 33 <u16 id>)."""
    global UNITS
    if UNITS is None:
        import text
        arm9 = text.code_images()["arm9"]
        strs = {s["id"]: s for _, _, es in docs() for s in es}
        gl = {j: ens[0] for jps, ens, _ in glossary() for j in jps}
        UNITS = []
        for k in range(63):
            p = struct.unpack_from("<I", arm9, 0xF5380 + k * 0x14)[0] - text.ARM9_BASE
            s = strs.get(f"arm9:{p:X}")
            UNITS.append((s.get("en") or gl.get(s["jp"], s["jp"])) if s else "")
    return UNITS


def speakers(fname):
    """{string offset: speaker} for a bytecode file: the last `35 id id` (speaker), else `33 id expr` (portrait),
    between the previous show and this one (ids = unit table F5380; checked on MESSAGE020/084/100, SPMES005036).
    shortcut: a byte scan, not a bytecode walk; good enough as a translator hint, wrong after jumps."""
    import text
    b = text.sfs_files({fname}).get(fname)
    if not b or not text.family(fname) or text.family(fname)[0] == "edmes":
        return {}
    sa, strs, refs, tail = text._bytecode(b)
    out, prev = {}, 0
    names = unit_names()
    for a, t in sorted(refs):
        seg = b[prev:a - 2]
        ids = list(re.finditer(rb"\x35([\x00-\x3e])\1", seg)) or list(re.finditer(rb"\x33([\x00-\x3e])[\x00-\x09]", seg))
        if ids:
            out.setdefault(t, names[ids[-1].group(1)[0]])
        prev = a + 4
    return out


def kind(char):
    if "぀" <= char <= "ゟ":
        return "hiragana"
    if "゠" <= char <= "ヿ":
        return "katakana"
    if "一" <= char <= "鿿" or char == "々":
        return "kanji"
    return "other"


def has_term(jp, term):
    """term occurs as a whole kana or kanji run: ミン isn't in タイミング, くも isn't in ぼくも."""
    for m in re.finditer(re.escape(term), jp):
        a, b = m.start(), m.end()
        if (a == 0 or kind(jp[a - 1]) != kind(term[0])) and (b == len(jp) or kind(jp[b]) != kind(term[-1])):
            return True
    return False


def glossary():
    """[(JP forms, EN forms, avoid forms)] from glossary.md's | JP | EN | max | notes | Avoid | tables."""
    rows = []
    if not GLOSSARY.exists():
        return rows
    for line in GLOSSARY.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("|") and len(cells) >= 2 and cells[0] not in ("JP", "") and not set(cells[0]) <= set("-: "):
            avoid = [x.strip() for x in cells[4].split("/") if x.strip()] if len(cells) > 4 else []
            rows.append(([x.strip() for x in cells[0].split("/")], [x.strip() for x in cells[1].split("/")], avoid))
    return rows


PRONOUNS = ("オレ", "オイラ", "ワシ", "ボク", "アタシ", "アタイ", "アンタ", "オマエ", "テメェ", "キサマ", "オラ")


def honorific_after_name(jp, form):
    """form right after a katakana run that isn't a pronoun (オレ様 is a self-title, not a name)."""
    for m in re.finditer(form, jp):
        a = m.start()
        while a > 0 and kind(jp[a - 1]) == "katakana":
            a -= 1
        if a < m.start() and not jp[a:m.start()].endswith(PRONOUNS) and \
                (m.end() == len(jp) or kind(jp[m.end()]) != kind(form[-1])):
            return True
    return False


def problems(entry, en, terms):
    """Every rule, on one line of English."""
    jp = entry["jp"]
    if not en.strip():
        return ["empty English"]
    out = []
    plain = TOKEN.sub("", en)
    if bad := sorted({c for c in plain if not encodable(c) and c != "\n"}):
        out.append(f"unencodable characters {bad}")
    if re.search(r"\\u[0-9a-fA-F]{4}", en) or "\t" in en or "\\n" in en:
        out.append("escape sequence or tab in the English")
    want = Counter(t for t in TOKEN.findall(jp) if t not in FREE)
    have = Counter(t for t in TOKEN.findall(en) if t not in FREE)
    if want != have:
        out.append(f"control codes differ: JP {dict(want)} EN {dict(have)}")
    if re.search(VARIABLE + r"(st|nd|rd|th)\b", en):
        out.append('ordinal suffix after a variable (write "No. [var]")')
    jp_plain = TOKEN.sub("", jp)
    for jps, ens, avoid in terms:
        if any(has_term(jp_plain, j) for j in jps) and not any(e.lower() in en.lower() for e in ens):
            out.append(f"glossary: {jps[0]} -> {ens[0]}")
        out += [f"glossary Avoid: {a}" for a in avoid if re.search(rf"\b{re.escape(a)}\b", en)]
    for jp_form, en_form in HONORIFICS.items():
        if honorific_after_name(jp_plain, jp_form) and en_form.lower() not in en.lower():
            out.append(f"honorific {jp_form} after a name needs {en_form}")
    return out + width_problems(entry, en)


def index():
    return {e["id"]: e for _, _, entries in docs() for e in entries}


def item_twins(entries):
    """Each item record (arm9 0x100640, 225 x 0x18) names the item at +8 (system font) and +C (FONT_ITEM):
    both must carry the same English, or one item shows two names (docs/re/text.md)."""
    by_ptr = {p: e for e in entries.values() for p in e.get("ptrs", [])}
    out = []
    for i in range(225):
        rec = 0x100640 + i * 0x18
        a, b = by_ptr.get(f"arm9:{rec + 8:X}"), by_ptr.get(f"arm9:{rec + 0xC:X}")
        if a and b and a.get("en") != b.get("en"):
            out.append(f"{a['id']} / {b['id']}: item name twins differ: {a.get('en')!r} / {b.get('en')!r}")
    return out


def read_tsv(path):
    return [line.split("\t") for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def out_rows(path):
    """id -> English from a .out.tsv; a literal \\n is a line break."""
    return [(r[0], "\t".join(r[1:]).replace("\\n", "\n")) for r in read_tsv(path)]


def existing():
    return sorted(TL.glob("b[0-9][0-9][0-9].tsv"))


def split(size, families=None):
    """Numbers on from the last batch and leaves out ids already batched, so a repeat run can't duplicate work."""
    TL.mkdir(parents=True, exist_ok=True)
    (ROOT / "build").mkdir(exist_ok=True)
    taken = {r[0] for p in existing() for r in read_tsv(p)}
    taken_groups = set()
    idx = index()
    for i in taken:
        if i in idx:
            taken_groups.add(group_of(idx[i]))
    n = max((int(p.stem[1:]) for p in existing()), default=0)
    rows, seen = [], set(taken_groups)
    for path, _, entries in docs():
        if families and path.parent.name not in families:
            continue
        spk = speakers(path.stem + ".BIN") if path.parent.name in ("message", "spmes", "tuto") else {}
        for e in entries:
            g = group_of(e)
            if needs_english(e) and e["id"] not in taken and g not in seen:
                seen.add(g)
                off = int(e["id"].split(":")[1], 16)
                rows.append((path.stem, e, spk.get(off, ""), form_of(e, path)))
    batches, cur, chars, cur_file = [], [], 0, None
    for fname, e, spk, form in rows:
        c = len(e["jp"])
        if cur and (chars + c > size or len(cur) >= MAX_ENTRIES):
            batches.append(cur)
            cur, chars = [], 0
        cur.append((e, spk, form))
        chars += c
    if cur:
        batches.append(cur)
    for batch in batches:
        n += 1
        name = f"b{n:03d}"
        path = TL / f"{name}.tsv"
        if path.exists():
            sys.exit(f"{path} already exists")
        lines = [f"{e['id']}\t{spk}\t{form}\t{limit_label(e)}\t{e['jp'].replace(chr(10), chr(92) + 'n')}"
                 for e, spk, form in batch]
        path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    write_terms()
    print(f"{len(batches)} new batches in {TL}, {len(taken)} ids already batched")


def write_terms():
    """build/terms_bNNN.txt: the glossary rows whose JP occurs in the batch (rerun after glossary edits)."""
    terms = glossary()
    for path in existing():
        jps = " ".join(r[4] for r in read_tsv(path) if len(r) > 4)
        used = [(j, ens[0]) for jpl, ens, _ in terms for j in jpl if has_term(jps, j)]
        (ROOT / f"build/terms_{path.stem}.txt").write_text("".join(f"{j}\t{e}\n" for j, e in used)
                                                           or "(no glossary terms in this batch)\n", encoding="utf-8",
                                                           newline="\n")


def check_batch(batch, entries, terms):
    want = [r[0] for r in read_tsv(TL / f"{batch}.tsv")]
    rows = out_rows(TL / f"{batch}.out.tsv")
    bad = []
    if [r[0] for r in rows] != want:
        got = [r[0] for r in rows]
        dup = sorted(i for i, c in Counter(got).items() if c > 1)
        bad.append(f"ids differ: missing {sorted(set(want) - set(got))[:8]} extra {sorted(set(got) - set(want))[:8]} "
                   f"duplicate {dup[:8]} (order must match too)")
    for eid, en in rows:
        if eid in entries:
            bad += [f"{eid}: {p}: {en!r}" for p in problems(entries[eid], en, terms)]
    return bad, dict(rows)


def expand(new, entries):
    """Copy each batched translation to every entry with the same JP in the same box kind."""
    by_group = {}
    for e in entries.values():
        by_group.setdefault(group_of(e), []).append(e["id"])
    out = {}
    for eid, en in new.items():
        for other in by_group.get(group_of(entries[eid]), [eid]):
            out[other] = en
    out.update(new)
    return out


def merge(new, overwrite):
    """Refuses to replace different English unless told to, before anything is written."""
    new = expand(new, index())
    if not overwrite:
        for _, _, entries in docs():
            for e in entries:
                if e["id"] in new and e.get("en") and e["en"] != new[e["id"]]:
                    sys.exit(f"{e['id']} would lose {e['en']!r}: pass --overwrite if that is meant")
    changed = 0
    for path, doc, entries in docs():
        touched = False
        for e in entries:
            if e["id"] in new and e.get("en") != new[e["id"]]:
                e["en"] = new[e["id"]]
                touched = True
                changed += 1
        if touched:
            for e in entries:
                if e.get("font") == doc.get("font"):
                    del e["font"]  # docs() filled it in; only per-row overrides are stored
            path.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"merged: {changed} entries changed")


def fit(eid, en, wrap=False):
    import lint
    e = index()[eid]
    r = rule(e)
    en = en.replace("\\n", "\n")
    if wrap:
        lines, cur = [], ""
        for word in en.replace("\n", " ").split(" "):
            cand = f"{cur} {word}" if cur else word
            if cur and lint.line_px(cand) > r["px"]:
                lines.append(cur)
                cur = word
            else:
                cur = cand
        lines.append(cur)
        en = "\n".join(lines)
        print(en.replace("\n", "\\n"))
    for line in en.split("\n"):
        print(f"  {lint.line_px(line):4d}/{r['px']} px  {line}")
    errs = problems(e, en, glossary())
    print(f"{len(en.split(chr(10)))}/{r['lines']} lines; " + ("OK" if not errs else "; ".join(errs)))
    return 1 if errs else 0


def main(argv):
    if not argv:
        sys.exit(__doc__)
    cmd, args = argv[0], argv[1:]
    if cmd == "split":
        fam = args[args.index("--family") + 1].split(",") if "--family" in args else None
        return split(int(args[args.index("--size") + 1]) if "--size" in args else 3500, fam)
    if cmd == "terms":
        return write_terms()
    if cmd in ("fit", "wrap"):
        return fit(args[0], args[1], cmd == "wrap")
    overwrite = "--overwrite" in args
    names = [a for a in args if a != "--overwrite"]
    entries, terms = index(), glossary()
    if cmd == "check" and not names:
        bad = [f"{i}: {p}: {e['en']!r}" for i, e in entries.items() if e.get("en") for p in problems(e, e["en"], terms)]
        bad += item_twins(entries)
        print(f"{len(entries)} entries, {len(bad)} problems")
        print("\n".join(bad[:200]))
        return 1 if bad else 0
    if cmd not in ("check", "merge") or not names:
        sys.exit(__doc__)
    new, failed = {}, 0
    for batch in names:
        bad, rows = check_batch(batch, entries, terms)
        new.update(rows)
        failed += bool(bad)
        print(f"{batch}: " + ("OK" if not bad else f"{len(bad)} problems"))
        for line in bad:
            print("  " + line)
    if failed:
        return 1
    if cmd == "merge":
        merge(new, overwrite)
    return 0


def selftest():
    assert has_term("ミンが来た", "ミン") and not has_term("タイミング", "ミン")
    assert honorific_after_name("エミリオ殿、勝負", "殿") and not honorific_after_name("殿下", "殿")
    assert honorific_after_name("ミラノさん", "さん") and not honorific_after_name("おじさん", "さん")
    assert honorific_after_name("ユグドラ様の", "様") and not honorific_after_name("お姫様", "様")
    assert not honorific_after_name("オレ様の剣", "様")
    assert needs_english({"jp": "勝負"}) and not needs_english({"jp": "あいうえお\nあいう"})
    assert not needs_english({"jp": "P"}) and not needs_english({"jp": "勝負", "en": "Duel"})


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    selftest()
    sys.exit(main(sys.argv[1:]))
