"""release.py: build, gate and package a release (references/pipeline.md "Release"). Stops at the first failure.

    python -X utf8 tools/release.py VERSION [--force] [--skip-tests]
        -> release/v<VERSION>/Yggdra_Unison_EN_v<VERSION>.xdelta, README.txt, Yggdra_Unison_EN_v<VERSION>.zip

Steps: build -> tests + lint (check.py, ~1 h; --skip-tests only when the commit hook just ran it on this tree)
-> smoke -> romcheck -> jpleft (code images) -> qa_gate check on every work/qa/**/manifest.tsv (verdicts in the
sibling verdicts/ dir) -> textcover -> no unticked docs/polish.md line -> no template placeholder in README.md ->
debug tool off -> xdelta3 patch -> re-apply to the original and compare -> zip (patch + README.txt, stored).
The debug tool is Lua run by the emulator (tools/debug/), never in the ROM: "off" = the build is build.py's normal
output (not the --marker build) and README.txt says nothing of it. Never publishes (`gh release create` is the
user's call). Refuses to overwrite an existing version without --force.
"""
import argparse
import hashlib
import re
import subprocess
import sys
import zipfile
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill import SKILL  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ORIG = ROOT / "rom/yggdra.nds"
BUILT = ROOT / "build/yggdra_en.nds"
MARKER = ROOT / "build/yggdra_marker.nds"
PY = [sys.executable, "-X", "utf8"]
SK = Path(SKILL) / "scripts"


def sha1(p):
    return hashlib.sha1(Path(p).read_bytes()).hexdigest()


def step(name, cmd):
    print(f"== {name}: {' '.join(str(c) for c in cmd)}", flush=True)
    if subprocess.call([str(c) for c in cmd], cwd=ROOT) != 0:
        sys.exit(f"release stopped: {name} failed")


def fail(msg):
    sys.exit(f"release stopped: {msg}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("version")
    ap.add_argument("--force", action="store_true", help="overwrite this version's files")
    ap.add_argument("--skip-tests", action="store_true", help="skip check.py (the commit hook ran it on this tree)")
    a = ap.parse_args()
    out = ROOT / f"release/v{a.version}"
    base = f"Yggdra_Unison_EN_v{a.version}"
    if out.exists() and any(out.iterdir()) and not a.force:
        fail(f"{out} exists (use --force to overwrite)")

    step("build", PY + ["tools/build.py"])
    if not a.skip_tests:
        step("tests + lint", PY + ["tools/check.py"])
    step("smoke", PY + [SK / "emu.py", BUILT, "--out", "work/qa/smoke", "--route", "tools/routes/boot.txt", "--smoke"])
    step("romcheck", PY + ["tools/romcheck.py", BUILT])
    step("jp_left", PY + ["tools/jpleft.py", BUILT])
    manifests = sorted((ROOT / "work/qa").rglob("manifest.tsv"))
    if not manifests:
        fail("no work/qa/**/manifest.tsv")
    for m in manifests:
        step(f"qa_gate {m.parent.name}", PY + [SK / "qa_gate.py", "check", m, m.parent / "verdicts"])
    step("strings.tsv", PY + ["tools/cover.py"])
    step("textcover", PY + [SK / "textcover.py", "work/qa", "build/strings.tsv", "--waive", "docs/text_unshown.tsv"])

    open_lines = [ln for ln in (ROOT / "docs/polish.md").read_text(encoding="utf-8").splitlines()
                  if ln.startswith("- [ ]")]
    if open_lines:
        fail(f"{len(open_lines)} unticked docs/polish.md lines, first: {open_lines[0][:80]}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    ph = re.findall(r"<(?:Game title|platform|publisher|year|repo|file|size|sha1|game|ext|Translated[^>]*|none known[^>]*)>", readme)
    if ph:
        fail(f"README.md template placeholders left: {sorted(set(ph))}")
    if MARKER.exists() and sha1(MARKER) == sha1(BUILT):
        fail("build/yggdra_en.nds is the marker build")
    rel = ROOT / "docs/release-readme.txt"
    if not rel.exists():
        fail("docs/release-readme.txt missing (the zip README)")

    out.mkdir(parents=True, exist_ok=True)
    patch = out / f"{base}.xdelta"
    if patch.exists():
        patch.unlink()
    step("patch", ["xdelta3", "-e", "-9", "-S", "djw", "-s", ORIG, BUILT, patch])
    check = out / "verify.nds"
    step("re-apply", ["xdelta3", "-d", "-f", "-s", ORIG, patch, check])
    if sha1(check) != sha1(BUILT):
        fail("re-applied patch differs from the build")
    check.unlink()
    txt = (rel.read_text(encoding="utf-8").replace("@PATCH@", patch.name).replace("@PATCHED_SHA1@", sha1(BUILT))
           .replace("@PATCHED_CRC32@", f"{zlib.crc32(BUILT.read_bytes()):08X}"))
    if re.search(r"@[A-Z0-9_]+@", txt):
        fail(f"docs/release-readme.txt placeholder left: {re.findall(r'@[A-Z0-9_]+@', txt)}")
    (out / "README.txt").write_text(txt, encoding="utf-8", newline="\r\n")
    z = out / f"{base}.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_STORED) as zf:
        zf.write(patch, patch.name)
        zf.write(out / "README.txt", "README.txt")
    print(f"release ok: {z} (build sha1 {sha1(BUILT)}, patch {patch.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
