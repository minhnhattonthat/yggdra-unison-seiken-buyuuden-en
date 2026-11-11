# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git (session-by-session
phase 5 notes: `git show 1765c13:docs/status.md`).

- **Phase:** 8. QA in the emulator in progress (phase 7 done 2026-11-10, session 13; session 32 latest).
- **Phase 8 progress (session 32):** **build 2026-11-11 15:02 sha1 76bd7aa5 (smoke ok)**; tour rerun 37/37 on it
  (new case `pause`), `qa_gate.py init ... --build` done; textcover exit 0 (13,637 + 86 waived; strings.tsv
  regenerated). **Battle pause menu found: Select**, gated by battle flags 0x0211A874 (deploy phase 0x2000);
  `tools/lua/pausemenu.lua` clears it (docs/re/scenes.md). BTLMN_FONT boxes re-cut to the game's own quads (quads.lua
  logs them under a stale name, gotcha logged): fixed clipped "Weapon Affini" / "Terrain Affini" / "apon Type W"
  headers, band titles bleeding neighbours ("ty~Weapon/Element~We"), class cells with neighbours' ink ("m Hunter",
  Assassin, Griffon Rider), weapon-row residue ("Lance/", "'Rock"), Duel Data "ses"/"0≤€" (回数 / 回 suffix cells
  blanked, → kept), header 各種記録 mistranslated ("Each Nation's Record" -> "~ Records of This War ~"); terrain page
  description arm9:94C94 3 lines over the buttons -> 2 lines. Seen against tour_jp in zoomed frames (work/qa/tour/
  pause). **Rumor modes B/D/E**: forced view never draws them (castle BG + dialogue; a tap blacks out), so fum.txt now
  shows their textures in the mode-A layout (`fumfac.lua LETTER=`): all 36 titles + paragraphs English
  (work/qa/fum_en/bde_0-2.png). Verdicts: s32_pause.tsv by hand; the 36 other changed sheets (timing shifts) went to
  codex (`sh tools/qareview.sh work/qa/chunks_s32 work/qa/verdicts_s32`, copied in as verdicts/s32_chunk_*.tsv).
  States regenerated on 76bd7aa5 (**stale again**: regen on bb4818f3 before using states). Then (session 32b) codex
  fixes: WD_N place names spilled past the sortie Targets frame (x 4-195; frame 12-188) -> `#! WD_N maxw=168 size=24`
  (5 long names size 20); territory "Expanding territory" (x fixed at 91, ran to 224) -> arm9:919E0 "Expanding"
  (centre 127 vs original 126.5). **Build 2026-11-11 15:45 sha1 bb4818f3 (smoke ok)**; reran sortie territory
  faction_select war_report card_select + ending_f01 (`--jobs 1`: the dark bands codex saw were parallel capture
  tears, gone alone), manifest re-inited on bb4818f3 (stale sortie/sheet_2 row dropped), textcover exit 0 on it.
  Codex prologue/prisoner wrap flags ruled ok by the controller (verdicts/s32_ruling.tsv, polish lines added).
  **Gate: 107 sheets, 2 issue** -> **next worker, in order:** (1) territory/sheet_2: capture composite (glossary.md
  "composite sentences": "Battle won! " + army + " took\n" + territory + "!", pieces arm9:919EC / ov9_14:1900 ' took\n'
  / ...) is a **mistranslation**: JP 激戦を制し…\n + army + より、 + territory + を占領！ = territory captured *from*
  that army; EN says the army took it. Also line 1 starts at x ~73 (count-based x, not lines_px) and runs off the
  right edge (tour_jp/territory t00540 vs tour). Reword so piece 1 ends in \n like the JP ("Battle won!\n" + "Took "
  ...? check every army x territory with lint) and/or move the caller to lines_px (text.md "Per-line centring
  counts"); rerun territory, re-verdict. (2) sortie/sheet tile 3: unit card top-left shows "Bounty Hunter" (codex
  wants "Mizer"): compare with tour_jp (JP card may show the epithet too) and verdict. (3) Tactician BTLMN cell never
  drawn (box guessed, polish). Then phase 8 done-when is met: set Phase 9.
- **Phase 8 progress (session 31b):** **build 2026-11-11 12:40 sha1 5056ec2f (smoke ok); QA gate green on it**
  (`qa_gate.py check work/qa/manifest.tsv work/qa/verdicts` exit 0, 105 sheets). States regenerated 35/35 on
  c2cf9a8f (5056ec2f differs only in EXTRA_FONT + FUM_TI textures, none loaded by a saved scene). Tour rerun on
  c2cf9a8f: 31 changed sheets verdicted by hand (work/qa/verdicts/s31.tsv; codex out until 13:07). On 5056ec2f only
  extras was rerun (work/qa/tour/extras); the other sheets are the reviewed c2cf9a8f ones (verdicts re-issued in
  s31c.tsv: a second tour flip-flops timing variants of fades and the gate's verdicts are time-based, so each rerun
  re-asks for sheets already seen). **War-event `_unk` titles = the rumor screen 風聞**: FUM_TI<faction %02d><A-E>
  title + FUM<faction><A-E> paragraph, task 0x0208ED54(n) (arm9; called after a story battle at 0x02080908,
  faction from 0x02043464). Forced from battle via `tools/debug/fum.txt` (60 cases; spmes.lua CALL + new
  `tools/lua/fumfac.lua` FAC=): modes A and C (24) show title + paragraph English on screen
  (work/qa/fum_en/mosaic_NN.png; battle HUD bleeds into the strip there, the original does the same); modes B/D/E
  take another path whose layers the battle BG hides in this forced view. **Fixes:** 28 titles ran x 1-254 over the
  frame pillars (x 244+; original ink 24-233) -> maxw=216 on all 60 (now x 20-237); paragraphs all end <= x 240
  (original 240). EXTRA_FONT menu labels were align=l in quads the game centres on the buttons: Sound Mode 10 px,
  Back to Title 6 px left of the original -> align=c, now within 2 px (tools/inkx.py vs tour_jp, zoom checked).
  Title menu and FILE tabs are the original's own English (pixel-identical). **Left for the done-when:** (1) battle
  pause menu (BTLMN_FONT Resume / Back to Title / Retry): trigger still unknown (start, top-left diamond, X do
  nothing on the deploy or Touch screens; docs/re/scenes.md:60): find the pause task (BTLMN_FONT.PACK loader via
  hashlookup.lua + xref) and inkx it; (2) rumor modes B/D/E on screen (follow 0x0208EE50, or force from a calmer
  scene than battle). Then phase 9. Polish items added in docs/polish.md.
- **Phase 8 progress (session 31):** **textcover exit 0: 13,637/13,723 shown + 86 waived, 0 failing**
  (`textcover.py work/qa build/strings.tsv --waive docs/text_unshown.tsv`). build/strings.tsv was stale (built
  before the ov9_18 header's 5th space): rerun `tools/cover.py` after any script edit. The 180 code-loaded prompts,
  composite parts, unit names (F5380+0), card names (A7E44+0) and 3 faction names were **forced in the battle
  CAUTION box** (new `tools/forcelist.py IDS OUT.lua` = each id's built address via its pointer + `tools/lua/
  forceband.lua`: swaps r2 of the CAUTION draw 0x02010BA4 for each entry, 12 castle taps; run line in its header;
  log work/qa/cover2/force): coverage of glyphs only, not their own screens (3-line band prompts show 2 lines
  there; real sites: info band 240 x 3, widths gated by lint). "Touch a sound." shown on its own screen via
  `tools/lua/soundnone.lua` (index -1). Waived ov9_02:1698 (war-data digit template copied to the stack).
  strcalls.py misses `ldr rX,[pc,#-n]` loads placed after their pool (ov9_06:2360 is one).
  **Save slots with data seen** (work/states/save1.dsv, gitignored: save.dst route `60 -;6 t225,182;90 -;6
  t75,180;600 -` = FILE 1 saved; DeSmuME writes `tools/desmume/desmume-qa/Battery/yggdra_en.dsv`, **delete it after**
  or every later run boots with that save). Load screen: `emu.py ... --sav work/states/save1.dsv --script
  tools/debug/warp.lua --var "SCENE='load'"`. Fix: SAVE_FONT Play Time box 91,40 overwrote the time colon cell
  (91,42,4,6: "0+00", label read "lay Time") and its top row bled under "load" (the prompt quad draws one row past
  v 39) -> box 96,41,45,10; seen clean (work/qa/s31_load_slot.png). **Build 2026-11-11 10:09 sha1 c2cf9a8f (smoke
  ok)**; work/states are older (regen before graphics checks).
  (Its "next worker" list was done in session 31b above.)
- **Phase 8 progress (session 30):** textcover **13,038 -> 13,429/13,723 + 111 waived (183 failing)**:
  `textcover.py work/qa build/strings.tsv --waive docs/text_unshown.tsv` (work/qa/cover2/* logs). **States
  regenerated 35/35 on build 23:44** (all were older: old RAM text). New forcers (each header has its run line):
  `tools/lua/helpall.lua` (all 36 HELP popup topics x pages, faction_select HELP=true), `tutoall.lua` (tutorial menu
  both books, route `tools/routes/tuto_heaven.txt`), `profall.lua` (37 char_intro profiles), `unlockall.lua`
  (unlock-terms page of each locked faction: UNLOCK_BITS=6, tap t20,20 then Profile t128,182), `saveall.lua` +
  `tools/routes/saveall.txt` (Back prompt, Overwrite via slot-in-use word, FAIL=1 = save fault injection),
  `loadfail.lua` (boot load fault), `unlock.lua` now writes on the title (boot overwrote the frame-1 write) + CLEAR=
  (☆ CLEAR), war data both pages `tools/routes/wardata.txt` (turn_end.dst), item catalog row 4 `tools/routes/
  items_row3.txt` (y 118 hit row 5: rows 4 were never shown), `tools/debug/cover_battle.sh` (tips 0-7: all 8 shown; results
  screen: Clear Time / Points Earned / Allies Retreated / Foes Fled shown, 101CAC Guard / Kill Out / Unison Attack /
  Highest Damage not: a later results page or the 戦績 record page). Waived (docs/text_unshown.tsv): 110 unread table fields (F5380+4, F5B88+0,
  A7E44+4: windows.json status unread, single pointer each) + ov9_06:431C digit template. **Fix:** unlock-terms header
  count digit touched "of" ("any 4of"): header got a 5th space and engine.OV_SITES ov9_18 0x0211EE38 x 162 -> 161;
  seen centred on screen (work/qa/cover2/terms_zoom.png). Build 2026-11-11 sha1 c407236e (smoke ok); states are
  from the 23:44 build (differs only in ov9_18). The QA manifest was inited on c55aa58a: rerun the tour +
  `qa_gate.py init ... --build` before release (faction_select sheets may change). **Left (183):** 80 code-loaded arm9
  prompts (battle: Not enough points / Sortie limit / can't control / out of move range / restart war / abandon;
  explore ov9_13: prep prompts, steps, chest, deserters; prize ov9_12 held-by; prisoner ov9_11 refused + 'has joined';
  war report ov9_08 nothing-to-report / disaster lines; territory ov9_14 'Battle won!', continent rises, Mistel joins;
  card ov9_16 used card / strategy card composite; system save fail arm9:94948 (FAIL-style injection in ov9_03?);
  tutorial book intros 95664/94CC8; battle menu descriptions 94918/94BC4/94C94/94ED0/94CFC), F5380+0 unit names
  (63, 52 of them one 'Nameless Soldier' hash: likely composite parts, e.g. prisoner 'X has joined'), A7E44+0 card
  names (36: card select strategy-card composite, force the card index), A7D00+0 3 faction names, 101CAC results labels (4), ov9_06:3FD4 'Touch a sound.' (no load site found: table?).
  `tools/strcalls.py ID` gives each load site + the draw call after it.
- **Phase 8 progress (session 29):** textcover **8,097 -> 13,038/13,723** (685 left, all system text): **all SPMES
  (3,282) + TUTO + SPMES_APP / TRE / WR + all 612 EDMES (456/456 records ok) + item catalog / sound titles shown.** msgall.lua loads them through the MESSAGE loader by name (FILE name swap kept on all run) and
  `duelnop` rewrites, in RAM, every op but 30 / 51 into the 1-byte no-op 1D and 39 into end 01, one start per line
  (op lengths for all 435 SPMES*/TUTO* files in its LEN table; 14 = 8-byte branch, 06 = goto). Run:
  `python -X utf8 tools/msgcover.py work/qa/cover2/spmes @work/qa/cover2/spmes_names.txt --jobs 3` (~20 min),
  `... work/qa/cover2/names @work/qa/cover2/names.txt --jobs 2`. KIND='SPMES' mode (duel task) freezes: kept for
  probing only. **EDMES**: new `tools/lua/edall.lua` (from work/states/ending_f01.dst, regenerated on this build:
  an older state crashes once the ending advances) forces every (file, record) at each unit load of the ending
  (ov9_15 sprintf 0x0211D254 r2, record r1 at 0x0211D278 / beq 0x0211D274 for page type 4: exec hooks at
  0x0211D280-88 never fire), taps only after the epithet is drawn (the record page timer needs ~300 frames; a tap
  ends it). Run: 3 jobs `FILES='0-12' / '13-25' / '26-37'`, `--var MAXIDLE=1200 --frames 500000` (~25 min), logs
  work/qa/cover2/ed_*. **Extras**: item catalog all 5 pages x 50 cells (`tools/lua/extras_all.lua` unlocks; page
  arrow t213,162; cells x 22 + 22.9c, y 45 + 24.3r), sound mode 8 x 5 cells (x 18 + 24c, y 45 + 24r), card catalog
  9 x 4 (card texts were already covered), locked run without the unlock (work/qa/cover2/ex_*; routes in this
  session's commit message). Menu taps (extras.dst): items t128,66, sound t128,98, cards t128,130, back t20,182.
  **Next worker, in order** (`textcover.py work/qa build/strings.tsv` lists them; work/qa/sysmiss.txt has the text):
  (a) help menu ov9_03 + arm9 "About Duels n" / "Moving Units n" / "About Prisoners n" pages and their bodies
  (find where the help menu opens: battle pause BTLMN or the title option menu); (b) ov9_07 character profiles
  (char_intro ticker: one per leader, force each); (c) ov9_18 unlock terms "1. Clear with Ortega ..." (faction select
  with locked factions: unlock.lua NEW=0 / clear 0x0210E6E6 bits); (d) arm9 item / unit / card-name copies kind
  'sys' (e.g. 'Dragon Boots', 'Nameless Soldier' x many: per-unit tables, prize lists, equip screens, battle card
  list), battle prompts ('Not enough points!', 'Sortie limit already reached!'); (e) ov9_06 3FD4 'Touch a sound.',
  4034 'You do not have that item yet.', 431C '000:'; ov9_15 save prompt, ov9_19 save prompts (save with data).
  Waive only provably unreachable ids (empty '' / lone punctuation pool entries: check refs first) in
  docs/text_unshown.tsv. Exec hooks under JIT can miss instructions in a branch-target block: hook the branch.
- **Phase 8 progress (session 28):** textcover **113 -> 8,097/13,723** (`textcover.py work/qa build/strings.tsv`;
  strings.tsv regenerated by `tools/cover.py`). **All 7,920 MESSAGE strings shown** by a script-driving viewer: new
  `tools/lua/msgall.lua` (from work/states/battle.dst, castle tap patched into the MESSAGE loader 0x02078760, hooks
  the interpreter loop 0x02005798, queues every switch-op-19 target, starts the file once per block; logs TEXT at op
  30/51) + `tools/msgcover.py OUT FILES --jobs 3` (parallel, restarts after a stuck file). Run: `python -X utf8
  tools/msgcover.py work/qa/cover2/msgX 0-220` (~10 min). Logs kept in work/qa/cover2/msg_0-73, msg_74-147, msg3,
  msg4 (MESSAGE150 hangs the battle scene after its lines: listed stuck, all its strings shown). Interpreter RE in
  docs/re/text.md "Interpreter". battle.dst regenerated (the old one ignored the patched call: gotcha logged).
  **Next worker, in order:** (1) SPMES (3,282 strings): `KIND='SPMES'` mode in msgall (duel task 0x02077910, sprintf
  swap 0x020772E8, heap script obj) **hangs the emulator** (no frames after ~850; TRACE shows op 05 = wait-N-frames
  at +21 of SPMES001014): likely the hook on 0x02005798 firing in a tight game loop or a heap obj check; spmes.lua
  alone + tools/lua/objprobe.lua ran fine. Try hooking only op 30 (0x0200628C, r0 = pc+1: string at base + u32) instead
  of the loop, and queue entries 0-3 via the task's r0 mode. List: work/qa/cover2/spmes.txt (402 numbers aaabbb).
  (2) TUTO (214) + SPMES_APP/TRE/WR (66): `FILES='@work/qa/cover2/names.txt'` (MESSAGE mode renames MESSAGE001.BIN
  at 0x0200A540; untested end to end). (3) EDMES 612 (38 endings x unit epithets: force the record choice in ov9_15).
  (4) system text 1,629 (work/qa/sysmiss.txt: item names/effects/who-can-equip, card skills, unit names, help pages
  "About Duels n", ov9_03 help menu, ov9_06 sound titles, ov9_07 character profiles, ov9_18 unlock terms, ov9_19 save
  prompts): extras Item Catalog / Card Catalog / Sound Mode with unlock flags (find them), help menu pages. Waive only
  unreachable ids in docs/text_unshown.tsv. Still open from s27: save slots with data, war-event `_unk` titles on
  screen, inkbox on choice/centred boxes.
- **Phase 8 progress (session 27):** **visual-QA gate green: `qa_gate.py check work/qa/manifest.tsv work/qa/verdicts`
  exit 0, 106/106 sheets ok on build 2026-11-10 ~23:45 sha1 c55aa58a** (smoke ok). Verdicts by hand (codex out until
  2026-11-11 13:07): work/qa/verdicts/s27.tsv (the 68 left on 49b4f05c) + s27_c55a.tsv (39 changed by the rerun).
  Fix: SYSTEX Unit Info 特殊 cell "Special" was squeezed into the game's 20-px rect (read "Speciali") -> "Trait"
  size=10 maxw=19 (seen clean on prisoner / prize frames). Method for rerun sheets: `work/qa/tour_prev` = copy of the
  previous run's sheets; each changed sheet diffed against it (scratch diff, bbox at threshold 24): sub-threshold
  ones and the timing-only shifts of screens without SYSTEX (tutorial, extras, epilogue_f02, credits/sheet_3) took
  the earlier verdict with that note, not a fresh read: re-read tutorial/sheet* in the story/release pass if in doubt.
  **Dark bands / black strips at fixed rows** (epilogue, credits, battle, attract_op) are capture tears from 6
  parallel emulators: epilogue_f01 alone (`--jobs 1`, work/qa/bandtest_en) has the original's row-luminance profile
  (docs/skill-gotchas.md). Polish: faction_select description "...centered on the royal capital Paltina" fills the
  band edge to edge and lacks its period. **Next worker: rest of the done-when**: save slots with data (make a save
  via turn_end "Save and End Turn", reboot with the .sav, tour the load screen), war-event `_unk` titles on screen
  (war_report on a later turn), inkbox on choice/centred boxes if not all done, then textcover (113/13,723: scenes
  for MESSAGE via warp.lua MSG=n, SPMES via spmes.lua, EDMES endings, TUTO pages; waive only unreachable ids). Any
  rebuild re-hashes ~25-50 sheets: rerun the tour with the machine idle, keep a tour_prev copy and diff.
- **Phase 8 progress (session 26):** session 25's work committed. Verdicts by hand for the 59 sheets left on acf6a790
  (work/qa/verdicts/s26.tsv; prologue / opening / load / extras not re-read). Fixes: **game p q g glyphs were drawn
  raised** (bowl above x-height: "uPon", "sPoils", "amon9" in every dialogue / system line) -> `tools/enfont.py DROP`
  moves them 2 rows down (descender to row 14 like y, widths unchanged; docs/re/windows.md); TREFONT "Exploration Prep"
  band box 92,31,79,21 (the original's outline top at row 31 left dark dashes above it); SYSTEX Unit Info: "Speed"
  maxw 19 (the game's 20-px rect cut its d), "Move Type" -> "Movement" box h 11 + "Weakness" box from y 68 (outline
  row 68 left dashes above it); `#! CNAMEC maxw=56` (prize UNIT LIST plates cut "Nameless Soldier"'s r at col ~60).
  Seen fixed on tour frames: p descenders, Speed, Movement, Nameless Soldier plate, no dashes above Exploration Prep /
  Weakness. Also fixed: gfx/text.tsv row CNAMEB000 had lost its tab (s25), so it kept the pre-maxw render. Build
  2026-11-10 21:55 sha1 49b4f05c (smoke ok); tour rerun on it 36/36 + `qa_gate.py init ... --build` done: 68 sheets
  lack a current verdict, so **next worker: verdicts for every sheet `qa_gate.py check` lists** (codex back after
  2026-11-11 13:07: `sh tools/qareview.sh` after `qa_gate.py todo`; else by hand, ~1k tokens per sheet, ~60 per
  worker). Then the rest of the done-when: save slots with data, textcover (113/13,723), war-event `_unk` on screen.
  Note: never regenerate gfx/*.png while check.py runs (test_english_build builds from them: a mid-run edit fails it).
- **Phase 8 progress (session 25):** verdicts by hand for the 30 sheets session 24 left (work/qa/verdicts/s25.tsv:
  17 ok, 13 issue) and fixes for every issue: SYSTEX boxes clipped to each label's own ink (Land / Speed cells left a
  dashed row and cut letters; army-name boxes ate the neighbours; Griffon Rider marks; Skeleton cut by the Griffon
  box; Valkyrie / Time / Nessiah's Army top rows); CNAMEB `#! CNAMEB maxw=110` (war-report VS screen shows the
  right fighter from x ~143: "Bewitching Amareus" ran off screen); composite piece arm9:919EC "Battle won! " got its
  trailing space back; tutorial top line arm9:93494 -> one line "I'll teach you how to win wars." (wrapped line ran
  over the band); SEN_FONT 称号 blanked (38,0,30,13: the epithet run covers that spot since session 12).
  **戦力確認 on the sortie UNIT LIST header was FORSEL_FONT's right column, not SYSTEX**: the label is drawn by the
  path quads.lua misses; found with new probes `tools/lua/gxtex.lua` (TEXIMAGE_PARAM writes), `texvram.lua` (texture
  VRAM dump), `tools/texdump.py` (decode by TEXIMAGE_PARAM), also `ppuevery.lua` + `tools/oamlist.py`,
  `ramat.lua`. FORSEL_FONT gained Check Forces / Player Faction / Lords & Leaders / Unlock Terms. New
  `tools/leftink.py` lists original ink no text.tsv box covers: run on all 23 UI atlases, the EN atlases were read
  (work/qa/s25_atlases_0/1.png): no other Japanese left in them. Build 2026-11-10 19:20 sha1 acf6a790 (smoke ok);
  tour rerun 36/36 on it, manifest re-inited with --build. Spot check of the fixes on the new tour frames
  (work/qa/s25_spot.png): sortie header "Check Forces", prisoner Land / Speed / VIT clean, VS names fit, tutorial
  line one row. **Next worker: 59 sheets lack a current verdict** (most only shifted in time; `qa_gate.py check
  work/qa/manifest.tsv work/qa/verdicts | grep "NO VERDICT"`; prisoner, prize, sortie, territory, tutorial,
  war_report, char_intro carry this session's fixes). Codex is back after 2026-11-11 13:07: then
  `sh tools/qareview.sh` (re-chunk with `qa_gate.py todo`). Then the rest of the done-when: save slots with data,
  textcover (113/13,723), war-event `_unk` on screen. Theocracy Army / Embellian Army SYSTEX cells come out ~7 px
  (41-px cells): readable on the VS label, small on the HUD (polish).
- **Phase 8 progress (session 24):** build 2026-11-10 17:43 sha1 7fc5f325 (smoke ok). Verdicts by hand (codex out
  until 2026-11-11 13:07) in work/qa/verdicts/s24.tsv: all prologue_f01-f11 (sheet_2/3 of f02-f11 are pixel-identical
  to f01 outside the leader bubble: bubbles checked on one crop sheet), ending_f01/f02, epilogue_f01, credits,
  medallion, faction_select, card_select, attract_op 1-2, gameover/sheet_2, turn_end/sheet. Fixes: battle HUD
  "Forest Army" had 森林軍 remnants at both ends (SYSTEX box 177,78,44,11); End Turn menu labels (TEND_FONT) drawn
  12-14 px left of the original's centre -> new gen_gfx `dx=N` (shift after align; test in test_gfx); gameover Easy
  Retry / Back to Title 7 px right -> dx=-7, stray dot left of Easy Retry = atlas column 159 not cleared (box from
  159). New `tools/inkx.py` (centre of white text fill: inkbox.py misreads the gradient buttons; compare with the
  tour_jp frame): CONFIRM OK / CANCEL and confirm messages match the original, gameover rows now match. char_intro
  tour case is hold-only (`EVERY=90 TOUR='2400-'`): its tour_jp sheets are from the old route, rerun
  `regen.py --list tools/debug/tour.txt --qa work/qa/tour_jp char_intro` (original ROM default) before judging it.
  Reran battle char_intro gameover explore turn_end prize prisoner on 7fc5f325, manifest re-inited with --build
  (3 stale ids of vanished sheets dropped). **Next worker: 30 sheets still lack verdicts** (`qa_gate.py check
  work/qa/manifest.tsv work/qa/verdicts | grep "NO VERDICT"`): battle, char_intro 1-5, explore 1-3, prisoner 1-3,
  prize 1+3, save 1-3, sortie, territory 2-3, title, turn_end 2-3, tutorial 1-3, war_report 1-3, gameover/sheet.
  Then the rest of the done-when: graphics-text rows seen in zoomed shots (BTLMN pause menu, explore map TREFONT,
  prisoner ENETREFONT, save slots, war-event `_unk`), textcover (113/13,723 strings shown: needs MESSAGE / SPMES /
  EDMES / TUTO scenes).
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
