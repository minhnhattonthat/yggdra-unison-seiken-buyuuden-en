# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 5. Marker build next (phase 4 extract done 2026-11-10).
  Last build: `build/yggdra_en.nds` = original (no edits yet).
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
- **Next (phase 5, marker build):** font/VWF decision (fixed 0x0B advance now; FONT_ITEM needs English glyphs too),
  insert `[id]` markers in every family (text.rebuild for script files; system strings > `max` need relocation +
  pointer rewrite), boot, find the Japanese that stays (code-built strings), width gate per box variant. Item names
  exist twice (sys +8 and item +C): translate them as one.
- **Done:** Step 0, phases 1-4 (recon docs/re/, warp tool 35 scenes, identity build, extract + roundtrip tests).
- **Debug-tool gaps (add before phase 8 QA):** game over; stage/SPMES selector and per-faction battles; specific
  MESSAGE events (`MSG=n`, untested on screen); 38 EDMES ending variants and 10 more epilogues; faction 5 has no
  start territory. `work/play/tuto` is a play.py session inside the tutorial (TUTO00_01 text on screen).
- **Later phases, known work:** 4x4 texture encoder; system-string relocation (phase 5); SPMES_WR sentence
  fragments; alpha-format textures (QUEST, PRIZE, PRISONER, *_TGA, WARRESULT) to shoot for graphics.md.
- **Open bugs:** none.
- **Waiting on the user:** nothing.
