# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git (session-by-session
phase 5 notes: `git show 1765c13:docs/status.md`).

- **Phase:** 8. QA in the emulator in progress (phase 7 done 2026-11-10, session 13; session 23 latest).
- **Phase 8 progress (session 23):** visual-QA verdicts by hand (codex out) for chunk_000-004 and the first 6 ids of
  chunk_005 (prize, prologue_f00): work/qa/verdicts/chunk_000..005.tsv. **Next worker: continue at chunk_005 id 7
  (prologue_f01/sheet) through chunk_010**, same method (EN sheet, JP under tour_jp when unsure). Issues found and
  fixed in gfx/text.tsv (build 2026-11-10 15:59 sha1 712aa806, smoke ok; tour rerun on it 36/36, manifest
  re-inited with --build: 49 sheets changed, verdicts for 4 of them in s23_fixed.tsv; the other 45 need a fresh look,
  many frames are shifted in time (texture sizes change load timing) and show wipe/dim strips: if a sheet looks torn,
  rerun its case with the machine idle; the tour ran beside check.py): 戦績 band label on every ending page = SEN_FONT 0,0 (drawn
  tinted, quads.lua misses it) -> "Record"; explore merchant speaker tag 商人 = CNAMEB254 -> "Merchant"; explore
  band "Exploration Pre" clipped (TREFONT rect 92..161) + JP stroke remnants; attract faction intro (OPK_WR / TM_M
  drawn at top x+60 / bottom x-59): titles + descriptions ran off screen -> TM_M box 60,0,136 maxw, OPK_WR maxw 160;
  SYSTEX Unit Info cells (prisoner, prize): Terra / Spee / Equ clipped -> Land / Speed / Gear (20-px cells), CIRCLE's
  E overwritten by the Thieves box -> box from x 169. Those sheets carry `issue` verdicts: after the rebuild, rerun
  the tour on the new build (`regen.py --list tools/debug/tour.txt --qa work/qa/tour --rom build/yggdra_en.nds`),
  `qa_gate.py init ... --build build/yggdra_en.nds` (unchanged sheets keep their verdicts), look at the changed ones
  (attract_op/sheet_3, ending_*, explore/sheet*, prisoner/sheet_2-3, prize/sheet*) and add `fixed` lines in a new
  verdict file. Still to fix from session 22: char_intro route (hold-only), battle route (tap units).
- **Phase 8 progress (session 22):** QA tour built and run. `tools/debug/tour.txt` = 36 cold-boot cases (35 scenes +
  `gameover`), warp.lua `TOUR='90-;6t128,100;..'` (route once the scene is reached) + `EVERY` (shot interval), regen.py
  `--list` / per-line `LUA=tools/lua/x.lua`; one sheet set per case (`<qa>/<case>/sheet*.png`, 8 tiles of top+bottom
  screen, 1024 x 768). Ran on build 159b2e59 -> work/qa/tour (106 sheets) and on rom/ -> work/qa/tour_jp.
  `qa_gate.py init work/qa/manifest.tsv work/qa/tour --glob "*/sheet*.png" --build build/yggdra_en.nds` done (106
  rows, build recorded); chunks of 10 in work/qa/chunks/chunk_000-010.txt. **No verdicts yet**: codex hit its usage
  limit (until 2026-11-11 13:07), so `sh tools/qareview.sh work/qa/chunks work/qa/verdicts` (codex, read-only, EN +
  tour_jp sheet per id, brief docs/visual-qa-brief.md) can't run today. Next worker: read each chunk's sheets yourself
  (EN, then the same path under tour_jp when unsure) and write work/qa/verdicts/chunk_NNN.tsv (`id<TAB>ok|issue<TAB>
  note`), ~1.5k tokens per sheet: about 6 chunks per worker, then hand back. Done: work/qa/verdicts/s22_main.tsv (5:
  card_select/sheet, territory/sheet, char_intro/sheet + sheet_2 ok; battle/sheet issue = the known stray mark after
  "Forest Army", polish "Phase 8"). Route fixes for the next tour round: char_intro's centre taps exit to the title
  after 2 characters (make it hold-only, `TOUR='2400-'`); battle needs taps on units (it idles on "Touch").
  Game over reached: `0x0207F04C(0)` via spmes.lua CALL (docs/re/scenes.md "Game over"): "Give it up?" Retry / Easy
  Retry / Back to Title English (work/qa/tour/gameover). Text coverage: `tools/lua/textcover.lua` logs `TEXT <hash>`
  (content hash at dialogue 0x020128B8, run, ctr, join parts) and `python -X utf8 tools/cover.py` writes
  build/strings.tsv (13,723 ids, same hash); first pass over the 36 tour cases (work/qa/cover, probe run): 113/13,723 shown (keys verified: 70 of 78
  logged hashes are string ids, the rest joined/number buffers). Coverage is the big remaining gate. Then
  `textcover.py work/qa/cover build/strings.tsv --waive docs/text_unshown.tsv`: add scenes for the big gaps (MESSAGE
  events via warp.lua MSG=n, SPMES via spmes.lua SPA/SPB, EDMES endings, TUTO pages), waive only unreachable ids.
  Still open for the done-when: verdicts, every gfx/text.tsv row seen English in a zoomed shot (session-19 list:
  BTLMN pause menu tap unknown, explore map TREFONT, prisoner ENETREFONT, save slots, 戦績 page; war-event `_unk`),
  inkbox on choice/centred boxes (gameover Retry rows, confirm OK/CANCEL, title menu), textcover exit 0.
- **Phase 8 progress (session 21):** TU_* tutorial shots done: gfx/text.tsv has the labels of all 40 shots with
  Japanese (the other 17 have none; dump in work/gfx/tu, 256 x 100 4x4, shown 1:1 on the bottom screen). Dialogue
  uses the script's own English; names/terms from glossary + atlas rows. New: `tools/inkrects.py` (ink rects on a
  picture texture; atlas.py grows to the opaque panel), gen_gfx `clear=panel` (commonest border colour: diagrams
  with leader lines) and clear=fill on boxes touching the edge (test_gfx). Coordinates: read single-file zoom crops
  (px / N), never multi-tile sheets (they shrink: docs/skill-gotchas.md). Leftovers/guesses in docs/polish.md
  "TU_*". Seen English in game: Exploration topic (TU_T04_01/02/03/06, work/qa/s21_tuto.png; route: tutorial.dst,
  t75,78 then t60,107, then t80,165 per page). Build 2026-11-10 sha1 159b2e59 (smoke ok); work/states regenerated
  35/35 from 8dda782e (differs only in TU_*), tutorial.dst from 159b2e59.
  **Graphics text is now all in text.tsv.** **Next:** the session-19 on-screen list (battle pause menu BTLMN, explore
  map TREFONT, prisoner ENETREFONT, save slots, 戦績 page) as a QA tour: regen states, `qa_gate.py init
  work/qa/manifest.tsv work/qa/tour --build build/yggdra_en.nds`, tour_jp on the original, verdicts in a fresh
  read-only pass (no subagents in an Orca worker), inkbox on choice/centred boxes, textcover (needs build/strings.tsv
  + a TEXT hook log).
- **Phase 8 progress (session 20):** unnamed DATA.SFS files now go by `_unk_<hash8>.PACK` (text.sfs_files,
  sfs.name_hash; test in test_sfs), so text.tsv / gen_gfx / gfx.py / build take them. gfx/text.tsv gained all 60
  war-event titles (256 x 24) + 60 paragraphs (256 x 240, other factions' wars on the war report; read off the
  textures, translated by the controller: polish line for a story pass), credit line 制作・著作 (_unk_0addeae8),
  カード選択 banner (_unk_441d016e), the 3 logo variants (ruby smoothed out with new gen_gfx `clear=fill`, subtitle
  as TIT_LOGO), a "< Town of Tolstoy >" label. gen_gfx `rows=N` (fixed pitch), `gfx.py check NAME..` (fast).
  Sheets: work/gfx/unk/para_sheet*.png (originals), title_sheet*.png. War-event names are built at runtime
  (not in arm9/ov9_08 strings; hashes only in the SFS dir): to see one on screen, run tools/lua/hashlookup.lua
  over war_report turns on a later turn or find the war-event selector (ov9_08?), then warp. Not done this session:
  the session-19 "Next" on-screen list below, TU_* (57 tutorial shots), QA tour + verdicts, inkbox, textcover.
  Build 2026-11-10 sha1 8dda782e (smoke ok, check.py green: 22 passed, lint 0); work/states are older: regen first.
  hashlookup.lua logs every name looked up, so a war-report turn with an event will name the `_unk` files.
  Builds take ~20 min and check.py ~40 min now (every texture re-encoded): run both in the background.
- **Phase 8 progress (session 19):** gfx/text.tsv gained the last UI atlases: TR_FONT (Medallion Supply, Exploration
  Report, Rarity), TUKOKU_FONT (Expansion, Dismissal x2), CDSKILLFNT0/1 (Card Skill Activated / Card Appraisal),
  ENETREFONT (prisoner: New Recruit! / Refused! / Banished! drawn straight, Prisoners = the 捕虜処遇 band), TREFONT
  (explore prep + map, 41 labels), BTLMN_FONT (battle pause menu, affinity pages, duel data, 42), SYSTEX (unit info /
  card panel / HUD army names / classes / elements, 48). SYSTEX2 is art. None drawn on a warp scene (quads.lua), so
  boxes are ink rects read off zoomed grids and snapped to ink + 1 px; the 王国軍 on the battle HUD top-left is SYSTEX
  drawn by another path (not in the quads log). Squeezes flagged in docs/polish.md "Phase 8". UI atlases are now all
  in text.tsv. Title logo: TIT_LOGO ruby cleared, subtitle "~ Legend of the Holy Sword ~" (dark on the ribbon: new
  gen_gfx `fill=r,g,b` / `outline=r,g,b`); SAVE_BG0 ruby + 6-px subtitle blended out (new `clear=vert`: text over
  art). Seen English on screen: title subtitle (work/qa/s19_title.png), battle HUD "Royal Army" (work/qa/s19_hud.png;
  a 2-px mark above its R = the 白薔薇軍 cell's bottom row inside the game's rect: polish). Build 2026-11-10 sha1
  d229fa1a (smoke ok, check.py green); work/states are from build 038ac7cc (differs only in SYSTEX): regen first.
  **Next:** see on screen: battle HUD army name (work/states/battle.dst top screen), battle pause menu (BTLMN: find the
  MENU tap), explore map (TREFONT: from explore.dst), prisoner result (ENETREFONT), SAVE slot names, 戦績 page, title
  logo subtitle (TU_T01_00 and `_unk` logo variants still Japanese); then `_unk` PACKs (war-event titles/paragraphs, credit line: needs hash keys in
  build.rebuild_sfs), TU_* (57 tutorial shots, late); then QA tour + verdicts, inkbox, textcover.
- **Phase 8 progress (session 18):** gfx/text.tsv gained CN_N_00-36 (territory leaders on the sortie Targets panel,
  = unit epithet strings; seen Japanese there before: tap t155,65 from work/states/sortie.dst), BTLFONT (残存戦力 +
  terrain / move-type / speed cells, 20 px wide, squeezed 0.53-0.8; War Result, Terrain View, Unit Sortie!,
  Deployed!, Retreated, Active), EXTRA_FONT (menu + big copies + title headers), SAVE_FONT (prompts, faction names,
  Lands, Play Time, Next/Back), TEND_FONT, TUTO_FONT, SEN_FONT (戦績 page: Loyalty / Retreats / Merit, Btl KO Kill
  cells, 回 blanked, Low/Avg/High), OP_FONT, GMOVERFONT, TERAGGFONT, HELP_MAT, WR_FONT, PRIZE_FONT. Most of those
  rects are ink rects (`atlas.py --region x,y,w,h` new: segment inside a region), not seen drawn: none of
  BTLMN_FONT SYSTEX SYSTEX2 TREFONT ENETREFONT TR_FONT TUKOKU_FONT WR_FONT PRIZE_FONT TERAGGFONT OP_FONT HELP_MAT
  CDSKILLFNT0/1 GMOVERFONT is drawn on any of the 35 warp scenes (HOLD=600). Glossary: atlas terms line.
  Abbreviations flagged for polish (docs/polish.md "Phase 8"). Build 2026-11-10 sha1 6b3ebc6a (smoke ok, check.py
  green, states regenerated 35/35 from it). Seen English on screen (work/qa/s18_sheet.png): sortie leader plate
  (CN_N), turn_end menu (TEND), save prompt, extras menu, tutorial menu (TUTO book buttons squeezed but readable).
  Still Japanese there: the title-logo ruby + subtitle on the save top screen (TIT_LOGO / SAVE_BG0).
  **Next:** see on screen: save slot faction names (SAVE, needs a save), 戦績 page (SEN), battle HUD (BTLFONT terrain cells: tap a square in battle); then BTLMN_FONT, SYSTEX,
  TREFONT, ENETREFONT, TR_FONT, TUKOKU_FONT, CDSKILLFNT0/1, SYSTEX2 (dump + ink rects; drive the scenes that show
  them with emu.py taps from work/states), 捕虜処遇, `_unk` PACKs, TU_*; then QA tour + verdicts, inkbox, textcover.
- **Phase 8 progress (session 17):** UV rects found: ITCM 0x01FF9AD0 draws every 2D quad (r0 x, r1 y, r3 w, stack
  h, u0, v0, u1, v1), 0x01FF966C binds a slot, 0x01FF89B4 loads NAME into a slot. `tools/lua/quads.lua` logs
  "quad NAME u,v,w,h at x,y"; all 35 scenes: `regen.py --rom build/yggdra_en.nds --qa work/qa/quads --script
  tools/lua/quads.lua --var HOLD=600` (slotN = loaded by another loader; odd 0,0,16,15 rects are mislabelled glyph
  draws). `tools/atlas.py NAME --quads work/qa/quads/*/log.txt` outlines those rects on the atlas (no --quads:
  ink segmentation). gen_gfx: `maxw=N`, `#! PREFIX opts` defaults. Done: FORSEL_FONT (faction/sortie panel labels;
  colons are own cells), BUTTON (all 19 labels; 9 rects inferred from ink, not seen drawn), PRO_FONT プロローグ,
  CDSEL_MAT 未鑑定 + カード選択 (inferred rect). OP_WR is 26 strips 192 x 16: was clipped at 192, now fits
  (size 12, lines 0/2 reworded). MS_PRO maxw 222 (touched the frame), EPI_MES maxw 221, EPI_TIT maxw 218 (both
  were clipped by the frame window). Seen English on screen: Factions/Lord panel, OP_WR, EPI_TIT.
  Build 2026-11-10 sha1 093dab00 (smoke ok, check.py green, states regenerated 35/35 from it).
  **Next:** FORSEL 23-px labels (Leader/Guard/Troops/Capital) squeeze 0.6: see the sortie panel on screen, widen
  the rects in ov9_17/18 code if unreadable; see BUTTON inferred labels + カード選択 on screen; then BTLFONT,
  EXTRA_FONT, SAVE_FONT, TEND_FONT, TUTO_FONT (rects in work/qa/quads, rerun the probe), then the other atlases
  (rerun quads.lua on scenes that show them: explore, turn_end, game over, prisoner...), 捕虜処遇, `_unk` PACKs,
  TU_*; then QA tour + visual-QA verdicts, inkbox, textcover.
- **Phase 8 progress (session 16):** gfx/text.tsv gained the prose textures, read off the originals (zoomed contact
  sheets; codex was out of quota): OP_WR (26-line prologue scroll), OPK_WR_00-11 (faction select, 7 lines),
  MS_PRO_000-011 (faction prologues; a blank line = paragraph gap), MS_N_00-36 (territory descriptions; MS_M + MS_N
  now all size 14), EPI_TIT/EPI_MES_00-11 (epilogues), EPI_WAKU0 全土統一 pill label (new gen_gfx `clear=row`:
  repaint a panel instead of punching a transparent hole), OBJSTR00-13 (title + 3 lines, two boxes), CDS_000-035
  (card panels: name + 9 lines; ★ -> •, not in Liberation). Glossary: Yggdra Yuril Artwaltz, Baroi, Barabasa, Aries,
  Lombard, Asura Gate, Rodney Road / Alwin River / Karna Canal. TM_M faction names were clipped on screen (texture
  drawn at x - 33): now left-aligned in box 50,0. Build 2026-11-10 07:19 sha1 0ddc741c (smoke ok, check.py green);
  work/states regenerated 35/35 from build 7b781960 (same code, only TM_M differs): regen before graphics checks.
  faction_select still shows Japanese 勢力選択 / 領主: / 領土数: / 難易度: (FORSEL_FONT?) and 戻る / 戦力確認 / 決定
  (BUTTON). OPK_WR did not appear on faction select or its confirm box: probably the new-game opening (scene 17).
  **Next:** see these on screen (OPK_WR, prologue_fNN MS_PRO, opening OP_WR scroll with KEEP=true,
  epilogue EPI, territory/sortie MS_N, card_select CDS, battle map OBJSTR help); then the UI atlases (BTLFONT,
  BTLMN_FONT, SYSTEX, TREFONT 探索準備, EXTRA_FONT, SAVE_FONT, BUTTON, SEN_FONT, ENETREFONT, TUTO_FONT, TR_FONT,
  TUKOKU_FONT, WR_FONT, PRIZE_FONT, PRO_FONT, TERAGGFONT, OP_FONT, HELP_MAT, CDSEL_MAT, CDSKILLFNT0/1, FORSEL_FONT,
  GMOVERFONT, TEND_FONT: dumps in work/gfx/ui via `gfx.py dump NAME --out work/gfx/ui`): each label needs its rect
  (connected components of the atlas, or the .BI / code rects) and a `box=` row; English must fit the same rect.
  Then 捕虜処遇 bottom band (probably an atlas above), ゴーレム in char_intro, `_unk` PACKs, TU_* last.
- **Phase 8 progress (session 15):** gfx/text.tsv now also has (mapping in its `#` comments): IN_PRO/TM_M/EVSFORCE
  (faction table), CN_M leaders, MS_M descriptions (read off the texture), CARDNAMEA/CS_M (card table), IT_EF001-225
  (73 distinct labels, read off; IT_EF113 decodes as noise: untouched, check), ED_N/ED_H (306, = EDMEScc string v /
  6+v), CNAMEA/B/C (00-36 unit table, 37-71 generic types read off CNAMEA; B098/099/253), EVSFONT/EVSFONTSB event
  goals, BATTLEOUT1-3, SELSORTIE, SHOOTNAME99, WR_SHN00-05. Seen English on screen: prologue IN_PRO, CNAMEA
  (char_intro), CNAMEB speaker tags (prisoner, ending). Tools: gfx.py paletted colour 0 = transparent, `WIDTH`
  override (CNAMEC is 64x16), gen_gfx per-line centring. New Johaim (ヨハイム, pope) in MS_M_08: add to glossary.
  `_unk` PACKs need hash keys in build.rebuild_sfs. EVSFONT lowercase lines follow a force name: check the join on
  screen (war events).
- **Phase 8 (session 14):** texture pipeline (docs/re/graphics.md "Pipeline"): add rows to `gfx/text.tsv`,
  `python -X utf8 tools/gen_gfx.py [NAMEs]`, `python -X utf8 tools/gfx.py check`, look at work/gfx/enc/ (sheet.py),
  build. SHOOTNAME00-11, WD_N_00-36 (= territory table A71F0+0). Long WD_N names fill 256 px: check on screen.
- **regen.py defaults to the original ROM:** pass `--rom build/yggdra_en.nds`.
- **Phase 7 review fixes (session 14):** lint fails a stub last line (< 6 chars, previous line not a sentence end;
  stat lines ATK+1 and composite parts exempt, composites checked per combination), leading/trailing blanks must
  match the Japanese (composite parts exempt); `MESSAGE000:*` keeps only あいうえお filler rows. `batches.py wrap`
  is balanced now; `batches.py widows NAME` re-balances every widow: 250 rows merged (work/tl/fix7b).
  Open minor: romcheck passes `romdiff.check` an empty write log (no per-write original-byte check yet).
- **Phase 7 done (session 13):** English insert `tools/insert.py` (script files re-laid, system strings in place or
  relocated, empty en = original bytes, only ids in `script/keep_jp.txt`: MESSAGE000 filler + 7 symbol strings; lint
  enforces it). `tools/romcheck.py` (also tests/test_build.py, builds its own ROM): code-image writes only at string
  slots / pointer words / engine sites / SFS dir / module params, every pointer reads its English, no stale pointer
  to a vacated slot, other SFS files identical, every script string = script/ (12,056 + 1,629 checked, 0 errors;
  no control codes but {br} exist, JP/EN multisets equal). 54 ellipsis-only lines -> "..." (work/tl/fix7a).
  SPMES_WR war-report composites (6 forms, "id|id" alternatives in lint part_texts) fit 184 x 2. Engine:
  `lines_px` / `lines_px12` replace 0x02013274 at 7 centring callers (text.md "Per-line centring counts"): seen
  centred in English: territory capital-taken, HINT! tip 0, confirm band, faction unlock message.
  Item encyclopedia labels (Rare / For:) fit the x 46 value column: no code change.
- **Next (phase 8):** graphics text (textures still Japanese: prologue scrolls OP_WR / OPK_WR / MS_PRO, scene banners,
  faction info panel, battle HUD 王国軍 / 残存戦力, CNAME name plates, buttons 戻る / 決定, tutorial topics, レア度 in
  the Get Item! popup, ED_H/ED_N, 戦績 BG label 称号：): references/graphics.md + docs/re/graphics.md; then the QA
  tour, visual-QA verdicts (do them yourself, read-only pass, no subagents in an Orca worker), inkbox, textcover.
  Phase-7 leftovers to see on screen: docs/polish.md "Phase 7".
- **Builds session 13 (2026-11-10 ~05:55):** `build/yggdra_en.nds` sha1 f56f2adb (smoke ok, English text, 35/35
  warps reached on this build, states regenerated from it); `build/yggdra_marker.nds` sha1 67f7db67 (states NOT
  from it: regen before using marker states).
- **Phase 6 done (session 12):** all 76 batches merged into script/ and reviewed (b069-b076 by the controller: codex
  out, no subagents in an Orca worker); `batches.py check` = 13723 entries, 0 problems; check.py 17 passed, lint 0
  errors. Session 12 fixes: Luciana addressee SPMES036004:01D4, Nessiah taunt SPMES036000:01DA, Kylier "!?"
  SPMES036019:01FB, Mistel APP01:0113, EDMES03:0180. Minors for the polish pass in docs/polish.md. Glossary gained
  Fallen Angel / Prophet / Pope / Cardinal / Mage / Bounty Hunter (EDMES epithets).
  Kit: `tools/batches.py` split/check/merge/fit/wrap/terms, `tools/pairs.py`, `tools/codex_review.sh bA bB`,
  docs/translator-brief.md, docs/reviewer-brief.md, docs/style-reference.md. work/tl is gitignored.
- **EDMES epithet run widened (session 12, D4 engine first):** ov9_15 0x0211E004 `mov r0,#0x66` -> `#0x42`
  (engine.OV_SITES, now also takes an instruction string): run x 66, budget 186 px (was 150), on screen in
  work/qa/epi_mk f000900. It now overlaps the 称号： label, part of the 戦績 page BG (no text call in ov9_15):
  **graphics phase must blank that label** (and translate 忠誠度 / 戦果 / 戦線離脱 / 戦功 on the same BG). Russell's
  epithets keep "Astral Fencer" (悲運 -> Tragic); ranks cut in b073-b076 restored (Bounty Hunter Mizer, Black Rose
  King/Emperor Roswell, White Rose Queen/Empress Rosary, Fallen Angel Nessiah, Full-Time Housewife Mistel,
  "Best"/Peerless/Global/Galactic/Cosmic Mage Pamela-sama). ED_H/ED_N textures carry the same words.
- **Review flags for QA:** speaker tags doubted (Ortega/Dort swapped MESSAGE210-219, Emilia "ボク" MESSAGE187/192).
- **Phase 6 history (session 11, 2026-11-10):** merged + reviewed (+ fixes): b001-b068.
  Session 11 fixes: Mistel/Milanor Sailor Moon parody SPMES014035:0197/01B6 ("tidy you up" / "punish you"); Dort
  old-man voice SPMES007017:0188/01B6, SPMES021017:017B; Leon おらおら SPMES008007:0204; Yggdra SPMES034003:019D.
  Session 10 fixes: Eudy "dears" MESSAGE179:075D; Amareus MESSAGE141:0644 / MESSAGE168:06E3; Juvelon
  MESSAGE142:062C; Flunky MESSAGE169:0593. Swept b049-b076 pairs: no Eudy dear/darling left.
  Session 9 already applied to the pending .out.tsv files: every "dear" on Eudy (dropped) / Rosary (-> darling),
  Brai -> Bly, Bronga -> Brongaa, holy knight -> Temple Knight; glossary rows now enforce Bly, Brongaa, Temple
  Knight (聖騎士), Duchy of Embellia (エンベリア公国) in `batches.py check`.
  Composite joins (territory captured, capital taken, card decided, item held) re-broken so every combination fits
  240 px: lint clean (check.py 0 errors). glossary.md "composite sentences" has the joins.
- **Phase 5 done (2026-11-10, session 7):**
  - Width gate closed: 0 strings on a guessed budget (lint). 13,399 strings measured on screen, 60 from code (x/y
    constants: small separators, medallion popups, extras prompts, sound titles, tutorial scroll text), 150 composite
    parts (the composite rule in `composites` governs), 114 in fields no code reads (unit epithet F5380+4, class
    F5B88, card one-liner A7E44+4: screens use textures). Tables: docs/re/windows.md.
  - Battle SPMES (3,337 strings) measured: DUEL EVENT box 184 x 2, `#184x2` verified (widthgate.sh now forces
    SPMES001014 via `tools/lua/spmes.lua`). HINT! tips 220 x 2, War Result labels 120, EDMES epithet one-liners 150
    (bottom 戦績 page, x 102), MESSAGE168 142 x 2.
  - `tools/lua/spmes.lua`: patches the CAUTION BL (tap own castle) into a call: SPMES file (SPA/SPB), tip popup
    (CALL=0x02080388 + tips.lua TIP=n), YOU WIN + results (CALL=0x02081350 R0=8). docs/re/scenes.md.
  - `tools/strcalls.py ID..`: each load of a string address + the BLs after it (run / ctr / band / CAUTION / join):
    classified the guessed system strings statically.
  - Extractor fix: item records start at 0x100640 (225, not 221): 4 FONT_ITEM names were decoded as system kana
    noise (しさうす...), now item font; FONT_ITEM 0x0D 開, 0x0F ず read. Script re-dumped, test updated.
  - Builds 2026-11-10 03:56: `build/yggdra_en.nds` sha1 bf09f342 (smoke ok, Japanese text); `build/yggdra_marker.nds`
    sha1 3906c0e9 (smoke ok). States regenerated from that marker build, 35/35.
- **Next (phase 6):** translate per references/translation.md with the `.claude/agents/translator` type (briefs:
  docs/translator-brief.md etc. as the skill sets up; glossary.md first: official Atlus Yggdra Union names, D2).
  Translate as sets: item name +8 and its FONT_ITEM twin +C alike; SPMES_WR fragments; composites (lint checks every
  combination); EDMES epithet one-liner = ED_N/ED_H texture wording (graphics phase).
- **Debug-tool gaps (add before phase 8 QA):** game over; real battle play (moves: drag + tap, unverified); specific
  MESSAGE events (`MSG=n`, untested on screen); 38 EDMES ending variants and 10 more epilogues; faction 5 has no
  start territory; explore unit-select info-band composites not seen on screen (budget = the measured band).
  `work/play/tuto` is a play.py session inside the tutorial; widthgate.sh replays it from work/states/tutorial.dst.
- **Later phases, known work:** 4x4 texture encoder; alpha-format textures (QUEST,
  PRIZE, PRISONER, *_TGA, WARRESULT) to shoot for graphics.md; textures seen Japanese in tours (faction_select top,
  save/load band, turn_end buttons, battle HUD, name tags CNAMEC, ED_H/ED_N epithets): graphics.md; lowercase p/q
  maybe redrawn (no descender room).
- **Gotchas this session** (docs/skill-gotchas.md): states from an older build hang the emulator on the first touch
  (regen after every build); DeSmuME registerexec = one callback per address; setregister r15 does not jump.
- **Open bugs:** none.
- **Waiting on the user:** nothing.
