"""forcelist.py: Lua list of the built address of each system string id, for tools/lua/forceband.lua.

    python -X utf8 tools/forcelist.py IDS.txt OUT.lua [--rom build/yggdra_en.nds]

IDS.txt: one id per line (first column, e.g. the ids of `textcover.py` NEVER SHOWN lines). Each id's address is
read through its first pointer in the built ROM; only addresses in an arm9 section (always resident) are usable in
any scene, the rest are listed as skipped. Kind = "caution" when the original code passes the string to the battle
CAUTION task 0x02010BC8, else "band" (info band 0x0200FC88).
"""
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import drawsites  # noqa: E402
import romcheck  # noqa: E402
import strcalls  # noqa: E402
import text  # noqa: E402


def main():
    args = sys.argv[1:]
    rom = ROOT / "build/yggdra_en.nds"
    if "--rom" in args:
        i = args.index("--rom")
        rom = Path(args[i + 1])
        del args[i:i + 2]
    ids = [ln.split()[0] for ln in Path(args[0]).read_text(encoding="utf-8").splitlines() if ln.strip()]
    rows = {r["id"]: r for r in romcheck.system_rows()}
    new = text.code_images(rom)
    mem = [(ram, len(s.data)) for ram, s in romcheck.sections(new["arm9"]).items()]
    images = drawsites.images()
    out, skipped = [], []
    for sid in ids:
        r = rows[sid]
        pimg, poff = r["ptrs"][0].split(":")
        addr = struct.unpack_from("<I", romcheck.main_or(new, pimg), int(poff, 16))[0]
        if not any(ram <= addr < ram + n for ram, n in mem):
            skipped.append(f"{sid} {addr:#x}")
            continue
        seq = [c for _, _, s in strcalls.calls(images, strcalls.addr_of(sid), 12) for c in s]
        kind = "caution" if "02010BC8" in seq else "band"
        out.append(f'  {{"{sid}", 0x{addr:08X}, "{kind}"}},\n')
    Path(args[1]).write_text("LIST = {\n" + "".join(out) + "}\n", encoding="utf-8")
    print(f"{len(out)} ids -> {args[1]}; skipped (not in arm9): {len(skipped)}")
    for s in skipped:
        print("  skipped", s)


if __name__ == "__main__":
    main()
