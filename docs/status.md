# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 5. Marker build in progress (dialogue/TUTO/EDMES width gate measured + torture line ok; system-text
  field budgets, battle SPMES box, system slot capacity, relocation plan next).
  Last builds (2026-11-10): `build/yggdra_en.nds` sha1 90503cd0 (English fonts + VWF engine, Japanese text, smoke ok);
  `build/yggdra_marker.nds` sha1 5d838803 (smoke ok; `regen.py --rom build/yggdra_marker.nds` re-run after the
  overlay hook, 35/35 warps). States in work/states/ are from the marker build.
- **Phase 5 this session (2026-11-10):**
  - Clipped dialogue letters in old warp shots were a stale savestate (old code); cold boot is clean. Always regen.
  - Width gate: `docs/re/windows.md` + `script/windows.json` (budgets per id regex, measured/guess) read by
    `tools/lint.py` (now in `tools/check.py`: encodable, no Japanese, lines, px). Measured: MESSAGE bubbles 142 px x 2
    (portrait left and right), SPMES_TRE box 184 x 2, TUTO 144 x 2, EDMES paragraphs 208 x 4. Verified by
    `sh tools/debug/widthgate.sh` (stress build `build/yggdra_gate.nds`, `MARKER_QA="ID=#px x lines|ID=text"`
    in tools/marker.py, shots work/qa/gate/). Torture line (all 82 glyphs, double spaces) ok.
  - EDMES paragraphs had no VWF (ov9_15 advanced x by a fixed 11): hooked (`engine.OV_SITES`, `ov_adv`), test added.
  - jp_left on the marker build (`tools/ptrslots.py` -> `--slots`): found 6 explore help pages after arm9 pool 2
    (pool end 0x958EB -> 0x95C09); script re-dumped (arm9 1,389 strings). Every other arm9/overlay hit is code or
    table noise (ov9_06 0x427A = kana sort table, not text). DATA.SFS non-script files not scanned (no pointer form known).
  - New helpers: `tools/rowscan.py` (box edges in px), `tools/lua/callers.lua` (distinct callers of a function).
- **Next (phase 5, rest):** (1) system-text budgets: map strings to screens and measure list fields with the longest
  name (unit/class/item/card names, menu labels, char-intro profile lines ov9_07 with 50-char lines, unlocks ov9_18,
  extras ov9_06, tutorial yellow description at x 50); move those rules from guess to measured in windows.json.
  (2) battle SPMES box: reach a battle event (debug-tool gap) and measure, or confirm the explore window is reused.
  (3) system text still takes one slot per glyph (pool capacity 112 free in the ending): check long help/menu strings
  against their scene's pool, else pack cells there too. (4) FONT_ITEM English look (palette-mapped MES glyphs, may
  be too tall). (5) system strings longer than `max`: relocation plan (ITCM ~14 KB left above 0x01FFC6A0, arm9 pools
  24 KB can be re-laid). Item names exist twice (sys +8 and item +C): translate them as one. (6) maybe redraw the
  game's lowercase p/q (no descender, read as P / 9).
- **Seen in the tours, graphics phase:** dialogue name tags = CNAMEC%02d textures; battle HUD 王国軍/残存戦力, turn-end,
  tutorial and extras buttons, epithet title bar (ED_H), faction prologue / epilogue / card / banner text: textures
  (graphics.md).
- **Phase 4 end (2026-11-10):** FONT_ITEM read (326/330, `tbl/jp_item.tbl`); 221 item-name rows `"font": "item"`;
  4-byte data block at arm9 0x8F9C0 split off (`text.POOL_DATA`); 22 FONT_SYSTEM/END kanji misreads fixed.
  `tools/text.py dump [--force]` writes `script/` (message 221 files / 7,920 strings, spmes 407 / 3,348, tuto 28 / 214,
  edmes 38 / 612, system 10 images / 1,625). Encoding, fonts, kanji: docs/re/text.md.
- **Done:** Step 0, phases 1-4 (recon docs/re/, warp tool 35 scenes, identity build, extract + roundtrip tests).
- **Debug-tool gaps (add before phase 8 QA):** game over; stage/SPMES selector and per-faction battles (battle warp
  stops on the map, no event dialogue); specific MESSAGE events (`MSG=n`, untested on screen); 38 EDMES ending
  variants and 10 more epilogues; faction 5 has no start territory. `work/play/tuto` is a play.py session (original
  ROM) inside the tutorial; widthgate.sh replays its presses from work/states/tutorial.dst.
- **Later phases, known work:** 4x4 texture encoder; system-string relocation; SPMES_WR sentence fragments;
  alpha-format textures (QUEST, PRIZE, PRISONER, *_TGA, WARRESULT) to shoot for graphics.md.
- **Open bugs:** none.
- **Waiting on the user:** nothing.
