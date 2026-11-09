"""unpack.py: dump NitroFS files, arm9.bin and decompressed arm9 overlays into work/ for recon."""
import os
import sys
from pathlib import Path

import ndspy.rom

ROOT = Path(__file__).resolve().parents[1]
rom = ndspy.rom.NintendoDSRom.fromFile(ROOT / "rom/yggdra.nds")
out = ROOT / "work/fs"
print(rom.name, rom.idCode, "arm9", len(rom.arm9), "ovl9", len(rom.arm9OverlayTable), "files", len(rom.files))
for fid in range(len(rom.files)):
    name = rom.filenames.filenameOf(fid)
    if name is None:
        continue
    p = out / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(rom.files[fid])
(ROOT / "work/arm9.bin").write_bytes(rom.arm9)
for i, o in rom.loadArm9Overlays().items():
    (ROOT / f"work/ov9_{i:02d}.bin").write_bytes(o.data)
    print("ov", i, hex(o.ramAddress), len(o.data), "compressed" if o.compressed else "")
if "-v" in sys.argv:
    print(rom.filenames)
