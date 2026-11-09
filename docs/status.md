# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git (session-by-session
phase 5 notes: `git show 1765c13:docs/status.md`).

- **Phase:** 6. Translate in progress (76 batches work/tl/b001-b076 from `tools/batches.py split`; wave 1 b001-b032
  dispatched session 8; merged batches listed below).
- **Phase 6 kit (session 8):** `tools/batches.py` split/check/merge/fit/wrap/terms (identical JP in the same box kind
  batched once, merge copies it to every id; speaker from bytecode opcode `35 id id` / `33 id expr`, ids = unit
  table F5380), `tools/pairs.py` (reviewer input), glossary.md (official Atlus names), docs/style-reference.md,
  docs/synopsis.md, docs/translator-brief.md, docs/reviewer-brief.md. work/tl is gitignored: merged English lives in
  script/.
- **Batch state (session 8):** merged + reviewed (+ fixes): b001-b004, b013-b032. Translated, check OK, NOT
  reviewed: b005-b008 (help/system; composite joins set). Translating when session 8 ended (all dispatched):
  b009-b012, b033-b076; their reports also go to work/tl/b0NN.report.txt for b057+. Next: check each, pairs.py +
  reviewer per 2 batches, fix Critical/Important (and Minors in the same round), merge, commit. Resume: `batches.py check bNNN` each; merge the reviewed ones;
  `pairs.py bA bB` -> reviewer agent (compact: Critical/Important only, Minors applied by the translator in the
  same fix round); docs/polish.md holds the Minors from the first 4 reviews.
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
- **Phase 7 to-do (engine/insert):**
  - 0x02013274 per-line glyph counts x 11 centre the HINT! tips (0x02080258 / 0x020802E8) and the medallion line
    (ov9_10 0x0211C004): make it px-based like count11 (0x02013224), else English sits left of centre.
  - Option menu 0x0201038C centres by a stored glyph count (unlock message line 2 at x 46): centre by px.
  - Faction conditions header count digit at fixed x 162 (ov9_18 near 0x0211EE48, an immediate): set after translation.
  - Item encyclopedia value x 46 after レア：/装備： is hard-coded in ov9_06: move it if the English labels need more.
- **Debug-tool gaps (add before phase 8 QA):** game over; real battle play (moves: drag + tap, unverified); specific
  MESSAGE events (`MSG=n`, untested on screen); 38 EDMES ending variants and 10 more epilogues; faction 5 has no
  start territory; explore unit-select info-band composites not seen on screen (budget = the measured band).
  `work/play/tuto` is a play.py session inside the tutorial; widthgate.sh replays it from work/states/tutorial.dst.
- **Later phases, known work:** 4x4 texture encoder; SPMES_WR sentence fragments; alpha-format textures (QUEST,
  PRIZE, PRISONER, *_TGA, WARRESULT) to shoot for graphics.md; textures seen Japanese in tours (faction_select top,
  save/load band, turn_end buttons, battle HUD, name tags CNAMEC, ED_H/ED_N epithets): graphics.md; lowercase p/q
  maybe redrawn (no descender room).
- **Gotchas this session** (docs/skill-gotchas.md): states from an older build hang the emulator on the first touch
  (regen after every build); DeSmuME registerexec = one callback per address; setregister r15 does not jump.
- **Open bugs:** none.
- **Waiting on the user:** nothing.
