# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 4. Extract in progress (script files + system pools extracted, kanji read; FONT_ITEM strings left).
  Last build: `build/yggdra_en.nds` = original (no edits yet).
- **Phase 4 so far (2026-11-10):** `tools/text.py dump [--force]` writes `script/` from the ROM: message 221 files /
  7,920 strings, spmes 407 / 3,348, tuto 28 / 214, edmes 38 / 612, system 10 images / 1,619 (pools in `text.POOLS`).
  tests/test_text.py: family counts, decode->encode == bytes for every string, file re-lay == original, system pools
  roundtrip, script/ in sync with the tables. Encoding corrected (text.md): codes F1-F9 + xx = (b-0xF0)*0xF0+xx,
  FC xx colour; all fonts share glyphs 00-EB (FONT_MES has ヴー at A0/A1 too); EDMES and ov9_02/06/07/18 use
  FONT_END. Kanji: 1,770 bitmaps read (`tbl/kanji.tsv`), tables `tbl/jp.tbl`, `jp_sys.tbl`, `jp_end.tbl` generated
  by `tools/mkjptbl.py`; misreads checked with `tools/kanji_check.py` (janome; `pip install janome`).
- **Next (finish phase 4):**
  1. FONT_ITEM: ~48 arm9 strings at field +12 of the 0x18-byte records from 0x1006A0 are FONT_ITEM-encoded (text.md
     "Not text in the arm9 pool"). Read FONT_ITEM's 330 glyphs (`tools/glyphsheet.py work/sfs/FONT_ITEM.NTFT ...`;
     add an "item" font to mkjptbl.FONTS/TABLES and kanji.py), decide per field which records use it, set those rows'
     font, and re-dump. Check for FONT_ITEM text elsewhere (other record tables, overlays).
  2. Mark non-text rows in system JSON (data pointed at by records) as `"data": true` once FONT_ITEM is decoded.
  3. Optional: re-read FONT_SYSTEM/END kanji that no script line uses (read without context) once system strings
     give context (`tools/kanji_check.py` covers script/ only; extend it to script/system).
  4. Then phase 5 (marker build): width gate, relocation plan for system strings longer than `max`.
- **Done:** Step 0, phases 1-3 (recon docs/re/, warp tool 35 scenes, identity build).
- **Debug-tool gaps (add before phase 8 QA):** game over; stage/SPMES selector and per-faction battles; specific
  MESSAGE events (`MSG=n`, untested on screen); 38 EDMES ending variants and 10 more epilogues; faction 5 has no
  start territory. `work/play/tuto` is a play.py session inside the tutorial (TUTO00_01 text on screen).
- **Later phases, known work:** 4x4 texture encoder; system-string relocation (phase 5); SPMES_WR sentence
  fragments; alpha-format textures (QUEST, PRIZE, PRISONER, *_TGA, WARRESULT) to shoot for graphics.md.
- **Open bugs:** none.
- **Waiting on the user:** nothing.
