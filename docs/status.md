# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 1. Research and recon in progress. Last build: none yet (2026-11-09).
- **Done:** Step 0 (DeSmuME QA fork qa-2 in tools/desmume/, original boots and takes input, check + pre-commit gate, guard hook proven, AGENTS.md). Recon so far: DATA.SFS directory/hash/LZ (docs/re/sfs.md), text encoding + text file families + MESSAGE string refs (docs/re/text.md), partial tbl/jp.tbl (kana/latin/punct). No prior fan patch exists.
- **Next (phase 1, in order):**
  1. Control-code inventory over all MESSAGE/SPMES/EDMES/TUTO/P/WD strings (non-glyph bytes, arg counts); map MESSAGE header + opcodes enough to find every string pointer.
  2. Menu/unit/item/skill/place name tables: search arm9, overlays and `work/sfs/_unk` for FF-terminated tables; check if FONT_SYSTEM/FONT_ITEM share FONT_MES order.
  3. Resolve graphics file names (loader at 0x021023B0 builds `%s.NTFT/.NTFP/.NTFI`; log names at runtime with an on_exec hook on 0x0200A540).
  4. Graphics-text survey -> docs/re/graphics.md (title, faction banners, prologue scroll, faction descriptions, battle UI, game over, endings, credits) + static sweep of NTFT files.
  5. Kanji readings for tbl/kanji.tsv (~1154 glyphs EC-56D; sheets via tools/fontsheet.py; template matching failed) - can start phase 4 instead.
- **Open bugs:** none.
- **Waiting on the user:** nothing.
