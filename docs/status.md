# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 5. Marker build in progress (dialogue/TUTO/EDMES measured; system text relocated and packed into
  16 px cells; submenu tours under way: item encyclopedia + tutorial menu measured; rest + battle SPMES box next).
- **Phase 5 session 4 (2026-11-10):**
  - Tour kit: `tools/tour.py` (play.py step + systrace log per screen), `tools/drawsites.py` (all 106 system-text
    call sites, constant x/y), `tools/ptrtables.py` (string -> data table + field; lint rule key `"table"`),
    `tools/lua/extras_all.lua` (opens every card / sound / item entry: bits 0x0210E6F8..0x0210E71F).
  - Measured (windows.json): item name 168 (encyclopedia, smaller than the prize list), item effect 200 x 2, equip
    195, territory name 200, encyclopedia labels, BGM label 66, tutorial titles 130, descriptions 204 x 3.
  - Card select / card dictionary panels (不明, 未鑑定, timing / condition / effect) are CDS_* textures.
  - **Gotcha:** after a savestate load DeSmuME shots stay flat grey ~125 frames: play.py `--wait 60+` (tour.py
    defaults 90).
  - Battle (tour_bt): the diamond button and START did nothing in the paused pre-battle state; find how to open
    the battle menu / unit info (arm9 0x02080D88.. run sites x 40/197 y 48-133 = a status panel; 0x0208BB9C.. x 20
    y 38 = data pages 武器相性 / 地形相性 / 記録).
- **Next (phase 5 rest):** tour with tools/tour.py: battle menus + unit panel; sortie map (territory / faction
  names); territory ov9_14, explore ov9_13, medallion ov9_10, prize popup ov9_12, turn end ov9_02, war report
  ov9_08, faction select ov9_18 (unlock text), save/load ov9_19; then card names/one-liners (A7E44), unit names
  (F5380), class names (F5B88), F79D8 help strings. Rebuild the marker (new px) and regen states after.
  Last builds (2026-11-10 02:22): `build/yggdra_en.nds` sha1 bf09f342 (fonts + VWF + packing, Japanese text, smoke
  ok); `build/yggdra_marker.nds` sha1 c59da449 (smoke ok). States in work/states/ regenerated from that marker build.
- **Phase 5 session 3 (2026-11-10):**
  - **System text packed into 16 px cells** (engine.py `pack_run`/`pack_ctr` replace 0x02012DF4/0x020130AC; per-slot
    key cache `codes[slot] = 0xC000|key`, `slotkey[]`; slots past the pool cap not drawn; FC handled at real px;
    docs/re/text.md). 0x02013224 glyph count -> `count11` = ceil(px / 11) (overlay callers lay out 11 x n).
    35/35 warps; help bands, card_select, prize list, char_intro stats render. Profile ticker: every profile at
    900 px = 89/128 slots, scrolls through and restarts (work/qa/gate/tick3; was a crash at 130 chars).
  - `tools/blcalls.py TARGET [N]`: every BL to an address in arm9 + overlays with the next N instructions.
  - Prize item popup (FONT_ITEM name x 23 y 116, effects x 40 y 132 / x 3 y 167, ov9_12 0x0211EF00.., z 0x294,
    alpha 0x1ff9770(0xA)): systrace logs it drawn on any tap (item row, decide button), but no frame shows it: tap,
    120-frame hold, every-2-frames shots, decide, drag to the unit all tried (work/play/prize3). Next try: find who
    calls that ov9_12 function and its state flag (`tools/lua/callers.lua`), or the 3D poly/alpha attrs.
- **Phase 5 session 2 (2026-11-10):**
  - **System-string relocation done** (`tools/sysreloc.py`, docs/re/text.md): fits -> in place, else EXTRA block =
    new arm9 autoload section at 0x02123460 + main arena lo raised (OS_GetInitArenaLo literals, engine.ARENA_LO;
    ITCM arena lo raised past the VWF hooks too). Marker build relocates all 1,625 (39 KB) and reaches 35/35 warps.
  - Who draws what: `tools/lua/systrace.lua` + `tools/sysmap.py` (27 ids on landing screens); regen.py takes
    `--qa DIR --script X.lua --var N=V` for probe runs (states untouched).
  - Measured (windows.json/windows.md): centred help + CONFIRM bands 240 px x 3; prize list item names 208 px
    (lint rule key `item` = item record field); profile ticker (ov9_07) is a slot limit: 82 chars ok, 130 crash.
- **Next (phase 5, rest), in order:** (1) tour the submenus with play.py + systrace and turn each guess rule into
  a measured one (prize item popup, above; help menu ov9_03; extras ov9_06 + unlocks ov9_18; explore help pages
  arm9 0x958EC+; save prompts ov9_15/19; medallion line arm9:9222C). Centred option menu at 0x0201038C centres by
  a stored glyph count (r5+0x12) with an 11 x n highlight bar: check it on screen, centre by px if off.
  (2) battle SPMES box (debug-tool gap). (3) FONT_ITEM look. (4) maybe redraw p/q. Packed cells at x < -12 are
  culled by 0x02012C10 (ticker left edge loses up to 4 px early): cosmetic.
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
