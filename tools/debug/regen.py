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


def scenes():
    out = []
    for line in (ROOT / "tools/debug/scenes.txt").read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            name, *vars_ = line.split()
            out.append((name, vars_))
    return out


def run(rom, name, vars_):
    out = ROOT / "work/qa/warp" / name
    state = (ROOT / "work/states" / f"{name}.dst").as_posix()
    cmd = [sys.executable, "-X", "utf8", str(Path(SKILL) / "scripts/emu.py"), str(rom), "--out", str(out),
           "--script", str(ROOT / "tools/debug/warp.lua"), "--frames", "30000", "--timeout", "600",
           "--var", f"STATE=[[{state}]]"]
    for v in vars_:
        cmd += ["--var", v]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    log = out / "log.txt"
    ok = log.exists() and "warp ok" in log.read_text(encoding="utf-8", errors="replace")
    return name, ok, r.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom", default=str(ROOT / "rom/yggdra.nds"))
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("names", nargs="*")
    a = ap.parse_args()
    todo = [s for s in scenes() if not a.names or s[0] in a.names]
    (ROOT / "work/states").mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(a.jobs) as ex:
        res = list(ex.map(lambda s: run(a.rom, *s), todo))
    bad = [n for n, ok, _ in res if not ok]
    for n, ok, rc in res:
        print(f"{'ok  ' if ok else 'FAIL'} {n} (exit {rc})")
    shots = [str(ROOT / "work/qa/warp" / n / "final.png") for n, ok, _ in res if ok]
    if shots:
        subprocess.run([sys.executable, "-X", "utf8", str(Path(SKILL) / "scripts/sheet.py"), *shots, "--cols", "8",
                        "--max", "16", "--out", str(ROOT / "work/qa/warp/sheet.png")])
    print(f"{len(res) - len(bad)}/{len(res)} scenes reached" + (f"; failed: {' '.join(bad)}" if bad else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
