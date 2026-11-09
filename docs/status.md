# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 2. Debug tool next (phase 1 recon done 2026-11-09). Last build: none yet.
- **Done:** Step 0. Phase 1 recon (docs/re/): DATA.SFS directory/hash/LZ and 3,846/4,001 file names (sfs.md); text encoding,
  fonts, control codes (FD/FF only), script string refs `30 xx u32` / `51 u32` with full coverage, EDMES record table,
  system text in arm9 (pool 0x8F000-0x95FFF) + overlays via u32 pointers (text.md); .PACK = NDS 3D textures, decoder,
  static sweep of all 2,497 textures read, Japanese graphics listed by group (graphics.md). Free space: ~9 MB at cart end;
  DATA.SFS is rebuilt with a re-laid directory (sfs.md). No prior fan patch exists.
- **Next (phase 2, debug tool):**
  1. Scene list `tools/debug/scenes.txt` + `tools/debug/warp.lua` (AGENTS.md warp command): title, faction select (one per
     faction), prologue scroll (OP_WR), a battle, world map, card/item menus, save/load, explore, war report, prisoner,
     tutorial, endings (EDMES/ED_N), epilogue (EPI_*), credits, game over.
  2. Find the game-state/scene variable and story flags (RAM search with `ramsearch.py`; the MESSAGE/SPMES script loader is a
     good anchor: log names with `tools/lua/fileopen.lua`, which also resolves the ~120 unnamed war-event textures).
  3. On the way, shoot the alpha-format textures listed in graphics.md (QUEST, PRIZE, PRISONER, *_TGA, WARRESULT) and add
     rows if Japanese; find what FONT_ITEM draws.
- **Later phases, known work:** kanji readings for FONT_MES/FONT_SYSTEM/FONT_END (transfer by bitmap hash, text.md);
  4x4 texture encoder; system-string relocation plan (phase 5); SPMES_WR sentence fragments.
- **Open bugs:** none.
- **Waiting on the user:** nothing.
