"""msgcover.py: run tools/lua/msgall.lua over a list of script files, restarting after any file that hangs.

    python -X utf8 tools/msgcover.py OUT FILES [--kind SPMES] [--jobs 3] [--rom build/yggdra_en.nds]
    FILES: msgall syntax ("0-220", "SPMES_WR,TUTO00_01", SPMES numbers "1014,1,3" with --kind SPMES),
           or "@path" = one entry per line.

Each job gets a slice of FILES and runs emu.py from work/states/battle.dst; when a run stops before
"msgall all done" (msgall exits 3 on a stuck file), the next run of that job starts after the file it was on.
Logs land in OUT/<job>_<run>/log.txt (TEXT lines for textcover.py); stuck files are listed in OUT/stuck.txt.
"""
import argparse
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill import SKILL  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def expand(spec):
    if spec.startswith("@"):
        spec = ",".join(Path(spec[1:]).read_text(encoding="utf-8").split())
    out = []
    for part in filter(None, re.split(r"[,\s]+", spec)):
        m = re.fullmatch(r"(\d+)-(\d+)", part)
        out += [str(i) for i in range(int(m[1]), int(m[2]) + 1)] if m else [part]
    return out


def job(k, files, args, out):
    stuck, run = [], 0
    while files:
        d = out / f"{k}_{run}"
        cmd = [sys.executable, "-X", "utf8", str(Path(SKILL) / "scripts" / "emu.py"), args.rom, "--out", str(d),
               "--state-in", str(ROOT / "work/states/battle.dst"),
               "--script", str(ROOT / "tools/lua/textcover.lua"), "--script", str(ROOT / "tools/lua/msgall.lua"),
               "--var", f"FILES='{','.join(files)}'", "--var", f"KIND='{args.kind}'",
               "--frames", str(2500 * len(files) + 3000), "--timeout", str(args.timeout)]
        with open(d.with_suffix(".out"), "w") as f:
            subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, cwd=ROOT)
        log = (d / "log.txt").read_text(encoding="utf-8", errors="replace") if (d / "log.txt").exists() else ""
        if "msgall all done" in log:
            break
        if re.search(r"^final frame", log, re.M) and not re.search(r"STUCK", log):
            print(f"job {k}: out of frames, raise the budget", flush=True)
        done = re.findall(r"^msgall (\S+) done", log, re.M)
        last = done[-1] if done else None
        # resume after the file that was running (stuck / crashed), or after the last finished one
        cur = re.findall(r"^msgall (\S+) STUCK", log, re.M)
        at = cur[-1] if cur else None
        if at is None:
            nxt = files.index(last) + 1 if last in files else 0
            at = files[nxt] if nxt < len(files) else None
        if at is None:
            break
        stuck.append(at)
        print(f"job {k}: stopped on {at}", flush=True)
        files = files[files.index(at) + 1:]
        run += 1
    return stuck


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("files")
    ap.add_argument("--kind", default="MESSAGE")
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--rom", default=str(ROOT / "build/yggdra_en.nds"))
    ap.add_argument("--timeout", type=int, default=3600)
    args = ap.parse_args()
    files = expand(args.files)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    n = args.jobs
    slices = [files[i::n] for i in range(n)]
    with ThreadPoolExecutor(n) as ex:
        res = list(ex.map(lambda a: job(a[0], a[1], args, out), enumerate(slices)))
    stuck = [s for r in res for s in r]
    (out / "stuck.txt").write_text("".join(s + "\n" for s in stuck), encoding="utf-8")
    print(f"{len(files)} files, {len(stuck)} stopped: {' '.join(stuck)}")


if __name__ == "__main__":
    main()
