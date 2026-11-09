"""tour.py: one play.py step of a submenu tour that keeps the systrace log (width gate, docs/re/windows.md).

    python -X utf8 tools/tour.py SCREEN --new STATE [--script X.lua]..   new session work/play/tour_SCREEN (marker build)
    python -X utf8 tools/tour.py SCREEN t20,48 a "down*4" [--wait 90]   one step

Appends the step's _run/log.txt to work/qa/tour/SCREEN/log.txt (read by tools/sysmap.py work/qa/tour OUT.tsv) and
prints the step's shot plus the distinct draws it logged (caller, x, y, marker code), not the raw log.
--wait defaults to 90: DeSmuME shots stay flat grey for ~125 frames after a state load (play.py warms 90).
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from skill import SKILL  # noqa: E402

args = sys.argv[1:]
screen, rest = args[0], args[1:]
sess = ROOT / "work/play" / f"tour_{screen}"
cmd = [sys.executable, "-X", "utf8", str(Path(SKILL) / "scripts/play.py"), str(sess)]
if rest and rest[0] == "--new":
    cmd += ["--rom", str(ROOT / "build/yggdra_marker.nds"), "--state", rest[1], "--script",
            str(ROOT / "tools/lua/systrace.lua")] + rest[2:]
else:
    cmd += rest
if "--wait" not in cmd:
    cmd += ["--wait", "90"]
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode:
    sys.exit(res.stdout[-2000:] + res.stderr[-2000:])
log = (sess / "_run/log.txt").read_text(encoding="utf-8", errors="replace")
out = ROOT / "work/qa/tour" / screen
out.mkdir(parents=True, exist_ok=True)
with open(out / "log.txt", "a", encoding="utf-8") as f:
    f.write(log)
seen = {}
for m in re.finditer(r"^sys \d+ (\w+) lr=(\w+) x=(-?\d+) y=(-?\d+) font=(\d+) \S+ \S+ (\w{0,12})", log, re.M):
    k = (m[1], m[2], m[4])
    seen.setdefault(k, (m[3], m[5], m[6]))
for (kind, lr, y), (x, font, hexb) in sorted(seen.items()):
    print(f"  {kind} lr={lr} x={x} y={y} font={font} {hexb}")
print(res.stdout.strip().splitlines()[-1])
