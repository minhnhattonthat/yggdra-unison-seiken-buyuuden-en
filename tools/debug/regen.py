"""Warp to every scene in tools/debug/scenes.txt from a cold boot; save work/states/<name>.dst and the proof shot.

    python -X utf8 tools/debug/regen.py [--rom build/yggdra_en.nds] [--jobs 6] [names...]

Each run: emu.py ROM --out work/qa/warp/<name> --script tools/debug/warp.lua --var ... --var STATE=...
Pass = its log has "warp ok". Writes work/qa/warp/sheet*.png (one tile per scene, in list order) and exits 1 if
any scene failed. Regenerate after any code, font or graphics change (states keep the old VRAM and code).
"""
import argparse
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from skill import SKILL  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent


def scenes(path=ROOT / "tools/debug/scenes.txt"):
    out = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            name, *vars_ = line.split()
            out.append((name, vars_))
    return out


def run(rom, name, vars_, qa="work/qa/warp", extra=()):
    out = ROOT / qa / name
    state = (ROOT / "work/states" / f"{name}.dst").as_posix()
    cmd = [sys.executable, "-X", "utf8", str(Path(SKILL) / "scripts/emu.py"), str(rom), "--out", str(out),
           "--script", str(ROOT / "tools/debug/warp.lua"), "--frames", "30000", "--timeout", "600"]
    if qa == "work/qa/warp":  # probe runs (--qa elsewhere) leave the states alone
        cmd += ["--var", f"STATE=[[{state}]]"]
    for v in vars_:  # LUA=tools/lua/x.lua in a list line = an extra --script for that entry
        cmd += ["--script", str(ROOT / v[4:])] if v.startswith("LUA=") else ["--var", v]
    cmd += list(extra)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    log = out / "log.txt"
    ok = log.exists() and "warp ok" in log.read_text(encoding="utf-8", errors="replace")
    return name, ok, r.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom", default=str(ROOT / "rom/yggdra.nds"))
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--qa", default="work/qa/warp", help="output dir; anything else = probe run, states untouched")
    ap.add_argument("--script", action="append", default=[], help="extra Lua probe (repeatable)")
    ap.add_argument("--var", action="append", default=[], help="extra NAME=LUA for every scene (repeatable)")
    ap.add_argument("--list", default=str(ROOT / "tools/debug/scenes.txt"),
                    help="scene list; tools/debug/tour.txt = QA tour (TOUR routes, one sheet per case)")
    ap.add_argument("names", nargs="*")
    a = ap.parse_args()
    todo = [s for s in scenes(a.list) if not a.names or s[0] in a.names]
    extra = [x for s in a.script for x in ("--script", s)] + [x for v in a.var for x in ("--var", v)]
    (ROOT / "work/states").mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(a.jobs) as ex:
        res = list(ex.map(lambda s: run(a.rom, *s, a.qa, extra), todo))
    bad = [n for n, ok, _ in res if not ok]
    for n, ok, rc in res:
        print(f"{'ok  ' if ok else 'FAIL'} {n} (exit {rc})")
    for n, ok, _ in res:  # tour cases (TOUR=): one contact sheet per case from its t*.png shots
        d = ROOT / a.qa / n
        if ok and any(d.glob("t*.png")):
            for old in d.glob("sheet*.png"):
                old.unlink()
            subprocess.run([sys.executable, "-X", "utf8", str(Path(SKILL) / "scripts/sheet.py"), str(d / "t*.png"),
                            "--changed", "0.02", "--div", "1", "--cols", "4", "--max", "8", "--out",
                            str(d / "sheet.png")], capture_output=True)
    shots = [str(ROOT / a.qa / n / "final.png") for n, ok, _ in res if ok]
    if shots:
        subprocess.run([sys.executable, "-X", "utf8", str(Path(SKILL) / "scripts/sheet.py"), *shots, "--cols", "8",
                        "--max", "16", "--out", str(ROOT / a.qa / "sheet.png")])
    print(f"{len(res) - len(bad)}/{len(res)} scenes reached" + (f"; failed: {' '.join(bad)}" if bad else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
