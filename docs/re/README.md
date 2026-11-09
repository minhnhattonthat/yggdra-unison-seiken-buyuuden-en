# Reverse-engineering notes

One file per subsystem (text engine, pointers, compression, font, graphics). Mark every finding with how far it is
proven, so a later session doesn't build on a guess:

- **verified** - and how: a decoded known string, a corrupt-and-boot test, a breakpoint hit on the drawing path, a
  passing roundtrip test. Name the test or savestate.
- **guess** - and why it seems likely (byte pattern, another game, an earlier patch's notes). Promote it to verified
  before code depends on it.

Addresses are for the dump in `rom.sha1` unless a note says otherwise.

| File | Covers | State |
|---|---|---|
| sfs.md | ROM layout, DATA.SFS directory (in arm9), name hash, LZ, free space | verified (LZ usage guessed) |
| text.md | encoding (stride-0xF0 codes, FC/FD/FF), fonts per text family, script files + refs, EDMES, system pools, draw routines, glyph slots, English font + VWF | verified (draw code, on-screen tutorial, roundtrip tests); kanji read; FONT_ITEM read (item names, aligned with FONT_SYSTEM) |
| graphics.md | textures (.PACK), static sweep, list of Japanese graphics | sweep read; alpha textures to check on screen |
| scenes.md | scene manager + ids, game state (player faction, unlock bits), text loaders, touch coordinates, warp | verified by warp runs |

Recon helpers: `tools/unpack.py` (NitroFS + overlays to work/), `tools/code_sections.py` (ITCM/DTCM), `tools/sfs_dump.py`
(DATA.SFS files to work/sfs/), `tools/fontsheet.py` (glyph sheets), `tools/ygdecode.py` (decode bytes), `tools/textscan.py`,
`tools/mkjptbl.py` (-> tbl/jp*.tbl from fonts + tbl/kanji.tsv), `tools/kanji.py` (kanji sheets, add/set readings, ctx,
dupes), `tools/kanji_check.py` (janome misread check), `tools/glyphsheet.py`/`kanji_zoom.py` (zoomed glyphs),
`tools/text.py` (extract/dump script/, layouts, rebuild, system pools), `tools/systext.py` (system strings via pointers),
`tools/lua/hashlookup.lua` (log DATA.SFS directory lookups), `tools/bytefind.py` (pattern search over all
images/files), `tools/tex.py` + `tools/gfxsweep.py` (texture decode / sweep pages), `tools/lua/fileopen.lua` (log opened
file names). No prior fan patch found (web search 2026-11-09).
