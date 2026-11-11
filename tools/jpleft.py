"""jpleft.py: the release's leftover-Japanese scan (pipeline.md "Release": jp_left.py on the release build).

    python -X utf8 tools/jpleft.py [build/yggdra_en.nds]      exit 1 if any code image has a Japanese run left

Script files (MESSAGE/SPMES/EDMES/TUTO) are checked string by string by tools/romcheck.py (every string = script/);
this covers the code images (arm9 + overlays), whose strings are reached by pointers. For each image: slots = every
aligned u32 of the *built* images that points into it (ptrslots.py does the same on the original), so text that was
relocated away is not reported; jp_left.py --orig keeps only runs whose bytes are unchanged from the original;
docs/jp_known.txt lists the runs checked and kept (decoded noise in tables, not text). Logs in work/jpleft/.
"""
import struct
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import text  # noqa: E402
from ptrslots import DATA_LO  # noqa: E402
from skill import SKILL  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "work/jpleft"
KNOWN = ROOT / "docs/jp_known.txt"
ARM9_TEXT = "8F000-95C0A"  # arm9 string pools (docs/re/text.md); past them are font/kanji maps and unit tables, which
# decode as 1,100+ noise runs (one-byte glyph indices: every byte is a kana)


def slots(img, built_imgs, size):
    base, lo = text.base_of(img), DATA_LO.get(img, 0)
    out = []
    for name, b in built_imgs.items():
        if img != "arm9" and name != img:
            continue  # overlay strings are only pointed at from the same overlay (text.md)
        for i in range(0, len(b) - 3, 4):
            t = struct.unpack_from("<I", b, i)[0] - base
            if lo <= t < size and not (name == img and i == t):
                out.append(f"{i:X} {t:X}" if name == img else f"{t:X} {t:X}")
    return out


def main(argv):
    built = Path(argv[0]) if argv else ROOT / "build/yggdra_en.nds"
    OUT.mkdir(parents=True, exist_ok=True)
    bi, oi = text.code_images(built), text.code_images()
    bad = 0
    for img, b in bi.items():
        (OUT / f"{img}.bin").write_bytes(b)
        (OUT / f"{img}.orig.bin").write_bytes(oi[img])
        (OUT / f"{img}.slots").write_text("\n".join(slots(img, bi, len(b))) + "\n", encoding="utf-8")
        cmd = [sys.executable, "-X", "utf8", str(Path(SKILL) / "scripts/jp_left.py"), str(OUT / f"{img}.bin"),
               "--orig", str(OUT / f"{img}.orig.bin"), "--tbl", str(ROOT / "tbl/jp_sys.tbl"),
               "--slots", str(OUT / f"{img}.slots"), "--limit", "100000"]
        if img == "arm9":
            cmd += ["--range", ARM9_TEXT]
        if KNOWN.exists():  # "IMG OFFSET note" lines -> this image's own --known file
            mine = [ln.split(None, 1)[1] for ln in KNOWN.read_text(encoding="utf-8").splitlines()
                    if ln.startswith(img + " ")]
            (OUT / f"{img}.known").write_text("\n".join(mine) + "\n", encoding="utf-8")
            cmd += ["--known", str(OUT / f"{img}.known")]
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        (OUT / f"{img}.txt").write_text(r.stdout + r.stderr, encoding="utf-8")
        last = (r.stdout.strip().splitlines() or ["?"])[-1]
        print(f"{img}: exit {r.returncode}: {last}")
        bad |= r.returncode != 0
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
