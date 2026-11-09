"""drawsites.py: every call to the system-text draw routines with the constant args a short back-scan can see.

Width gate helper (docs/re/windows.md "System text"): one row per call site = one box variant to measure.
    run 0x02012DF4(r0 x, r1 y, r2 ?, r3 string, [sp] font)    ctr 0x020130AC(r0 y, r1 ?, r2 string, r3 font)
Register values come from mov/mvn/ldr-literal/add/sub with known operands in the 32 instructions before the BL
(straight-line guess, no branches followed): '?' = computed at run time. A string arg that lands on a script row
prints its id.

    python -X utf8 tools/drawsites.py [run|ctr|all]      (reads work/arm9_02000000.bin, work/ov9_XX.bin)
"""
import json
import struct
import sys
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from capstone.arm import ARM_OP_IMM, ARM_OP_MEM, ARM_OP_REG

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "work"
TARGETS = {0x02012DF4: ("run", 0, 1, 3), 0x020130AC: ("ctr", None, 0, 2)}  # kind, x reg, y reg, string reg
OV_BASE = 0x0211B780


def images():
    out = [("arm9", (WORK / "arm9_02000000.bin").read_bytes(), 0x02000000)]
    out += [(p.stem, p.read_bytes(), OV_BASE) for p in sorted(WORK.glob("ov9_[0-9][0-9].bin"))]
    return out


def string_ids():
    """{(image, address): id} for every script/system row."""
    ids = {}
    for p in (ROOT / "script/system").glob("*.json"):
        for s in json.loads(p.read_text(encoding="utf-8"))["strings"]:
            img, off = s["id"].split(":")
            base = 0x02000000 if img == "arm9" else OV_BASE
            ids[(img, base + int(off, 16))] = s["id"]
    return ids


def regs_at(cs, data, base, site, back=32):
    """Naive constant propagation over the straight line [site - back*4, site)."""
    start = max(0, site - base - back * 4)
    regs = {}
    for ins in cs.disasm(data[start:site - base], base + start):
        ops, m = ins.operands, ins.mnemonic
        if not ops or ops[0].type != ARM_OP_REG:
            continue
        d = ins.reg_name(ops[0].reg)
        if m.startswith("bl"):
            for r in ("r0", "r1", "r2", "r3", "r12", "lr"):
                regs.pop(r, None)
            continue
        val = None
        if m in ("mov", "mvn") and len(ops) == 2:
            if ops[1].type == ARM_OP_IMM:
                val = ops[1].imm & 0xFFFFFFFF
            elif ops[1].type == ARM_OP_REG:
                val = regs.get(ins.reg_name(ops[1].reg))
            if val is not None and m == "mvn":
                val = ~val & 0xFFFFFFFF
        elif m == "ldr" and len(ops) == 2 and ops[1].type == ARM_OP_MEM and ins.reg_name(ops[1].mem.base) == "pc":
            a = ins.address + 8 + ops[1].mem.disp - base
            if 0 <= a < len(data) - 3:
                val = struct.unpack_from("<I", data, a)[0]
        elif m in ("add", "sub") and len(ops) == 3 and ops[1].type == ARM_OP_REG and ops[2].type == ARM_OP_IMM:
            a = regs.get(ins.reg_name(ops[1].reg))
            if a is not None:
                val = (a + ops[2].imm if m == "add" else a - ops[2].imm) & 0xFFFFFFFF
        if m in ("str", "strb", "strh", "cmp", "tst", "push", "stm", "stmdb"):
            continue
        if val is None:
            regs.pop(d, None)
        else:
            regs[d] = val
    return regs


def sites(kind="all"):
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    cs.detail = True
    ids = string_ids()
    for name, data, base in images():
        for off in range(0, len(data) - 3, 4):
            w = struct.unpack_from("<I", data, off)[0]
            if (w >> 24) & 0xF != 0xB or w >> 28 == 0xF:
                continue
            imm = w & 0xFFFFFF
            imm = imm - (1 << 24) if imm & 0x800000 else imm
            t = base + off + 8 + imm * 4
            if t not in TARGETS or kind not in ("all", TARGETS[t][0]):
                continue
            k, xr, yr, sr = TARGETS[t]
            regs = regs_at(cs, data, base, base + off)

            def show(r):
                if r is None:
                    return "128"
                v = regs.get(f"r{r}")
                return "?" if v is None else str(v - (1 << 32) if v & 0x80000000 else v)
            s = regs.get(f"r{sr}")
            sid = ids.get(("arm9", s)) or ids.get((name, s)) if s is not None else None
            yield dict(image=name, site=base + off, kind=k, x=show(xr), y=show(yr),
                       string=sid or (f"{s:08X}" if s is not None else "?"))


def main():
    kind = sys.argv[1] if len(sys.argv) > 1 else "all"
    rows = list(sites(kind))
    for r in rows:
        print(f"{r['image']:6} {r['site']:08X} {r['kind']} x={r['x']:>4} y={r['y']:>4} str={r['string']}")
    print(f"{len(rows)} call sites")


if __name__ == "__main__":
    main()
