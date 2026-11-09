# DATA.SFS archive and ROM layout

Dump: `rom/yggdra.nds` (SHA-1 in `rom.sha1`), game code BYGJ, header name YGGDRAUNIZON.

## ROM
- NitroFS has 3 files: `DATA.SFS` (17.5 MB, all game data), `DS_YZD_BGM.sdat`, `DS_YZD_SE.sdat`. **verified** (ndspy, `tools/unpack.py`).
- arm9.bin 0x105838 bytes at 0x02000000, not compressed; autoload sections: ITCM 0x01FF8000 (0x3A60 + bss 0x360), DTCM 0x027E0000 (0x60). `tools/code_sections.py` writes them to `work/arm9_<addr>.bin` for disasm. **verified**.
- 20 arm9 overlays, all at 0x0211B780, none compressed. **verified** (ndspy).
- Cart 0x2000000 bytes, header used size 0x1737600: **~9 MB free** at the end, so DATA.SFS can grow on rebuild. **verified** (header 0x80).

## DATA.SFS
- Files back to back, each starting on a 0x200 sector boundary; padding between files is leftover memory (env strings), not zeros. **verified**.
- **Directory is in arm9.bin**, not in the archive: 4001 entries of 12 bytes at arm9 file offset **0x95C4C..0xA17D8** (RAM 0x02095C4C; the code reads the base/count from the struct at 0x0210E044 +8/+0xC). Entry = `u32 hash, u32 size, u32 sector` (offset = sector*0x200), sorted by hash and binary-searched by ITCM 0x01FFAD88. **verified** (disasm + `FONT_MES.NTFT` hash found, sizes match file spans).
- **Name hash** (ITCM 0x01FFAD88): basename after the last `/` or `\`, copied into a 16-byte zero buffer; `h = h*0x89 + (signed char)` over all 16 bytes in 64-bit; low 32 bits compared. Names longer than 16 chars collide on the first 16. `tools/sfs.py name_hash`. **verified**.
- File open by name: arm9 0x0200A540 (-> ITCM 0x01FFAFF4) returns a heap copy; 0x0200A5EC = open + decompress.
- **Compression** (arm9 0x0200A54C, used only by 0x0200A5EC callers): `u32 out_size, u16 n, n x u16 control, literal halfwords`. Control bit15 set: copy `((w>>10)&0x1F)+2` halfwords from `(w&0x3FF)` halfwords back; else copy `w` literal halfwords. `tools/sfs.py decompress`. Used inside .PACK parts (below), **verified**: all 2,358 named PACKs decompress to their stated sizes. Text files are stored raw.
- **.PACK** (graphics, 2,358 named + ~139 in `_unk`): `u32 flags, u32 size[3]`, then 3 parts back to back from 0x10 (sizes sum to the file length, **verified** on all). Flags bit i = part i LZ-compressed; flags 0x100 (raw), 0x101, 0x107 seen. Parts = NDS 3D texture: texels, palette (BGR555), 4x4-compression index data (empty for paletted formats). `tools/sfs.py unpack_pack`, `tools/tex.py` (format inferred, width guessed: see graphics.md). `.BI` files (608) are layout/cell info for some PACKs (format unread). Recompressing: literal-only LZ (control words < 0x8000) should be valid (**guess**, untested in game), or store the part raw and clear its flag bit (0x100 files prove raw parts load).
- Names: `tools/sfs_dump.py` hashes every upper-case token / printf pattern in arm9 + overlays with .BIN/.NTFT/.NTFP/.NTFI/.NTFS/.PACK/.BI/.LTFT and names **3,846 of 4,001** files; the rest go to `work/sfs/_unk/<hash>_<sector>.bin` (139 of those are PACKs by header). The extensions .PACK/.BI/.LTFT came from logging every name passed to the open call (`tools/lua/fileopen.lua`, exec hook on 0x0200A540, r0 = name) during a boot-to-title run.
- Rebuild plan: rewrite DATA.SFS with every file re-laid on 0x200 sectors and patch size/sector in the arm9 directory (hash order unchanged). Identity build must reproduce the padding bytes, so keep each gap from the original.
- **Rebuild, done** (`tools/build.py rebuild_sfs`): files in sector order, no overlaps, no shared sectors, every gap < 0x200; unchanged files keep their bytes up to the next file's sector, replaced ones are zero-padded. No-edit build is byte-identical (tests/test_build.py). **verified in game**: MESSAGE001.BIN grown by 0x600 (shifts 28k later files) boots, and opening/prologue/battle/ending warps are pixel-identical to the original; the game trusts the arm9 directory alone. Cart has ~9 MB spare, so growth is free.
