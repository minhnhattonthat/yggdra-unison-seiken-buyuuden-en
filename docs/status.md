# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 5. Marker build in progress (dialogue/TUTO/EDMES measured; system-text relocation done; system-text
  cell packing + submenu budgets + battle SPMES box next).
  Last builds (2026-11-10 02:05): `build/yggdra_en.nds` sha1 ce5dc47c (fonts + VWF, Japanese text, smoke ok);
  `build/yggdra_marker.nds` sha1 dff43712 (every system string filled to its budget and relocated; smoke ok).
  States in work/states/ are from the marker build one step earlier (same code, older fill widths; 35/35).
- **Phase 5 session 2 (2026-11-10):**
  - **System-string relocation done** (`tools/sysreloc.py`, docs/re/text.md): fits -> in place, else EXTRA block =
    new arm9 autoload section at 0x02123460 + main arena lo raised (OS_GetInitArenaLo literals, engine.ARENA_LO;
    ITCM arena lo raised past the VWF hooks too). Marker build relocates all 1,625 (39 KB) and reaches 35/35 warps.
  - Who draws what: `tools/lua/systrace.lua` + `tools/sysmap.py` (27 ids on landing screens); regen.py takes
    `--qa DIR --script X.lua --var N=V` for probe runs (states untouched).
  - Measured (windows.json/windows.md): centred help + CONFIRM bands 240 px x 3; prize list item names 208 px
    (lint rule key `item` = item record field); profile ticker (ov9_07) is a slot limit: 82 chars ok, 130 crash.
- **Next (phase 5, rest), in order:** (1) **pack system text into 16 px cells** (one slot per glyph now: queue
  fill in 0x02012DF4/0x020130AC + per-glyph upload 0x02012130 + run draw 0x02012C10 with hook_step) so long
  profiles / help pages fit the 128-slot pools; re-test `work/qa/gate/ticker` (130 chars) after. (2) tour the
  submenus with play.py + systrace (prize: tap an item -> popup with FONT_ITEM name x 23 and effects x 40 / x 3 drawn
  at frame ~92 but not seen in the shot yet; help menu ov9_03; extras ov9_06 + unlocks ov9_18; explore help pages
  arm9 0x958EC+; save prompts ov9_15/19; medallion line arm9:9222C) and turn each guess rule into a measured one.
  (3) battle SPMES box (debug-tool gap). (4) FONT_ITEM look. (5) maybe redraw p/q.
- **Seen this session:** faction_select top screen (王都パルティナを中心に..., 領主, 領土数, 難易度), save/load band
  (セーブファイルを選択してください) and turn_end buttons stay Japanese in the marker build: textures (check graphics.md
  survey covers them).
- **Phase 5 session 1 (2026-11-10):**
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
  - Still open from session 1: tutorial yellow description at x 50; item names exist twice (sys +8 and item +C):
    translate them as one.
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
