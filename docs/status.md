# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 4. Extract next (phase 3 identity build done 2026-11-09). Last build: `build/yggdra_en.nds` = original
  (sha1 ef4d5e4f..., no edits yet).
- **Phase 3:** `tools/build.py` re-lays DATA.SFS (`rebuild_sfs`, replacements via `edits()` {name: bytes}) and
  patches the arm9 directory, then fixes the ndspy quirks; tests/test_build.py: no-edit build byte-identical, relaid
  archive keeps every other file. A grown-file ROM booted and warped fine (sfs.md "Rebuild, done").
- **Done:** Step 0. Phase 1 recon (docs/re/: sfs.md, text.md, graphics.md). Phase 2 debug tool: `tools/debug/warp.lua`
  drives the game's own touch flow by the scene manager (docs/re/scenes.md: 22 scene ids, player faction, faction
  unlock bits, text loaders, touch coords); `tools/debug/scenes.txt` lists 35 scenes (title, attract, opening, faction
  select, 11 faction prologues, card/sortie select, battle, territory, explore, prize, prisoner, medallion, war report,
  turn end, save, load, char intro, extras, tutorial, ending x2, epilogue x2, credits); `tools/debug/regen.py` reached
  35/35 from cold boot on the original ROM (states `work/states/<name>.dst`, proof `work/qa/warp/sheet*.png`).
- **Next (phase 4, extract):** dump MESSAGE/SPMES/TUTO/EDMES etc. (text.md "Text files") and system strings
  (arm9/overlay pointer fields, text.md "System text": decide per table/field) into `script/` JSON with jp via
  `tbl/jp.tbl` (unknown kanji as `[XX]` codes until readings are done); roundtrip test (re-encode == original bytes)
  and coverage test against the original ROM. Kanji readings (text.md) are needed for translators: do them here.
- **Debug-tool gaps (add before phase 8 QA):** game over (B_GAMEOVER in arm9 battle code; needs a lost battle: find
  unit HP / lord-defeat state); stage/SPMES selector and per-faction battles (ATTACK_TAP is set for faction 1 only);
  specific MESSAGE events (`MSG=n` retargets the next MESSAGE load, untested on screen); the 38 EDMES ending variants
  and the other 10 epilogues (`FACTION=n` should select them: add rows); faction 5 has no start territory. Text
  coverage (phase 8) will list the rest.
- **Later phases, known work:** kanji readings for FONT_MES/FONT_SYSTEM/FONT_END (transfer by bitmap hash, text.md);
  4x4 texture encoder; system-string relocation plan (phase 5); SPMES_WR sentence fragments; alpha-format textures
  (QUEST, PRIZE, PRISONER, *_TGA, WARRESULT) now reachable by warp: shoot them for graphics.md.
- **Open bugs:** none.
- **Waiting on the user:** nothing.
