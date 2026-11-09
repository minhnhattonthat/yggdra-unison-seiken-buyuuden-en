"""code_sections.py: write arm9 autoload sections (ITCM, DTCM, ...) to work/arm9_<ramaddr>.bin so disasm.py can read them by RAM address."""
from pathlib import Path

import ndspy.code
import ndspy.rom

ROOT = Path(__file__).resolve().parents[1]
rom = ndspy.rom.NintendoDSRom.fromFile(ROOT / "rom/yggdra.nds")
arm9 = ndspy.code.MainCodeFile(rom.arm9, rom.arm9RamAddress)
for s in arm9.sections:
    print(hex(s.ramAddress), hex(len(s.data)), "bss", hex(s.bssSize), "implicit" if s.implicit else "")
    (ROOT / f"work/arm9_{s.ramAddress:08x}.bin").write_bytes(s.data)
