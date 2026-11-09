# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 5. Marker build in progress (engine spike done; width gate + leftover-Japanese survey next).
  Last builds (2026-11-10): `build/yggdra_en.nds` = English fonts + VWF engine, Japanese text (smoke ok);
  `python -X utf8 tools/build.py --marker` -> `build/yggdra_marker.nds` (all 35 warps reach their scene, regen.py).
- **Phase 5 so far (2026-11-10):** font decision made and proven on screen: game's own Latin glyphs + new ASCII
  punctuation (`tools/enfont.py`, `tbl/en.tbl`), VWF hooks in ITCM (`tools/engine.py`; text.md "English font + VWF").
  Dialogue is packed into 16 px cells, because each scene's glyph-slot pool is sized for the Japanese (ending
  dialogue: 32 slots; one slot per letter hung the ending). Marker build (`tools/marker.py`): script lines ->
  `(M154:240) The quick brown fox...` at 250 px per line (JP line count kept; ids: M=MESSAGE, S=SPMES, T=TUTO,
  E=EDMES + file + offset); system strings in place -> base-36 code + filler to `max`, codes in work/marker_ids.tsv.
  `--skip fam,REGEX` and `MARKER_PX` / `MARKER_SAME` / `MARKER_GROW` env vars exist for bisecting
  (`tools/debug/bisect_epi.sh`). `tools/lua/glyphslots.lua` logs the slot pools.
- **Seen in the marker tour, not yet handled:** dialogue name tags (王女ユグドラ, yellow) stay Japanese (source not found:
  texture SHOOTNAME*.PACK or a system string? check); faction prologue / epilogue / card / banner text are textures
  (graphics.md, later phase); dialogue bubble text runs past the bubble's right edge at 250 px (measure).
- **Phase 4 end (2026-11-10):** FONT_ITEM read (326/330, by aligning item record +8 sys names with +C item names;
  `tbl/jp_item.tbl`, mkjptbl font "item"); 221 item-name rows in arm9.json have `"font": "item"` (`text.ITEM_RECS`);
  4-byte data block at arm9 0x8F9C0 split off (`text.POOL_DATA`), so ドゼウ (0x8F9C4) is its own row. 22 FONT_SYSTEM/END
  kanji misreads fixed from system-text context (text.md). No other non-text rows found in the pools, so no
  `"data"` rows yet; tests check system rows encode back in their font and script/system matches the ROM.
- **Phase 4 so far (2026-11-10):** `tools/text.py dump [--force]` writes `script/` from the ROM: message 221 files /
  7,920 strings, spmes 407 / 3,348, tuto 28 / 214, edmes 38 / 612, system 10 images / 1,619 (pools in `text.POOLS`).
  tests/test_text.py: family counts, decode->encode == bytes for every string, file re-lay == original, system pools
  roundtrip, script/ in sync with the tables. Encoding corrected (text.md): codes F1-F9 + xx = (b-0xF0)*0xF0+xx,
  FC xx colour; all fonts share glyphs 00-EB (FONT_MES has ヴー at A0/A1 too); EDMES and ov9_02/06/07/18 use
  FONT_END. Kanji: 1,770 bitmaps read (`tbl/kanji.tsv`), tables `tbl/jp.tbl`, `jp_sys.tbl`, `jp_end.tbl` generated
  by `tools/mkjptbl.py`; misreads checked with `tools/kanji_check.py` (janome; `pip install janome`).
- **Next (phase 5, rest):** (1) width gate: measure every box variant in px and lines from zoomed marker shots
  (dialogue bubble with/without portrait, name tag, narration, choices, tutorial, EDMES epithet/epilogue, menus,
  item/unit/card names, help) and record them in a window-data file the lint will read; torture line (all ASCII).
  (2) system text still takes one slot per glyph (pool capacity 112 free in the ending): check long help/menu
  strings against their scene's pool, else pack cells there too. (3) `jp_left.py` on the marker build + list the
  Japanese that stays (name tags, code-built strings). (4) FONT_ITEM English look (palette-mapped MES glyphs, may
  be too tall). (5) system strings longer than `max`: relocation plan (ITCM has ~14 KB left above 0x01FFC6A0, arm9
  pools 24 KB can be re-laid). Item names exist twice (sys +8 and item +C): translate them as one.
- **Done:** Step 0, phases 1-4 (recon docs/re/, warp tool 35 scenes, identity build, extract + roundtrip tests).
- **Debug-tool gaps (add before phase 8 QA):** game over; stage/SPMES selector and per-faction battles; specific
  MESSAGE events (`MSG=n`, untested on screen); 38 EDMES ending variants and 10 more epilogues; faction 5 has no
  start territory. `work/play/tuto` is a play.py session inside the tutorial (TUTO00_01 text on screen).
- **Later phases, known work:** 4x4 texture encoder; system-string relocation (phase 5); SPMES_WR sentence
  fragments; alpha-format textures (QUEST, PRIZE, PRISONER, *_TGA, WARRESULT) to shoot for graphics.md.
- **Open bugs:** none.
- **Waiting on the user:** nothing.
