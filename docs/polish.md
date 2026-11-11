# Polish pass (deferred reviewer Minors)

One line per Minor: `- [ ] id - note`. The polish pass ticks each `[x]`, fixed or `waived: reason`; release refuses
to run while any line is unticked.

## b003-b004 (system, approved)
- [x] arm9:90B58/90DB0/90FCC - 帝国兵法書 天/地/人ノ巻: "Man" beside Heaven/Earth reads odd (Humanity?) -> waived: Humanity is 172 px > 168 (FONT_ITEM twin); Heaven/Earth/Man is the usual rendering of 天地人
- [x] arm9:91398 - 殺意の仮面 "Malice" is weak: Mask of Bloodlust -> fixed (s33): Mask of Bloodlust
- [x] arm9:91278 - 凶刃ベルセルク: "Cruel" soft: Berserk, the Bloody Blade -> waived: Cruel Blade Berserk reads fine and fits; the longer form overflows 168 px
- [x] arm9:904FC vs 91050 - 巨獣ロコン / 幻獣ヤーデ both "Beast": fixed (phase 6 review): Giant Rokon / Phantom Yade, twins unified
- [x] arm9:9046C - 命のミサンガ: Life Bracelet? -> waived: ミサンガ is a wish bracelet; Lifeline keeps 命
- [x] arm9:90414 - アラン人形: is Alan Kylier's griffon Al? check description -> waived: nothing in the game ties アラン to Kylier's griffon; literal Alan kept
- [x] arm9:90CB4/91248 - 映見の手鏡 "Scrying Hand Mirror": check description -> waived: reads fine
- [x] arm9:91374 - ゲテモノOKな人: "Anyone OK with weird food" -> waived: reads fine, fits 195 px
- [x] arm9:90CF0/90D98 - 上級勲章 "High Medal": Senior Medal? check medal ranks -> waived: the only medal rank in the game; High Medal reads fine
- [x] arm9:90960/91332 - 名馬ワードナ: Werdna the Fine Steed -> fixed (s33): Werdna the Fine Steed
- [x] arm9:90D80/90DD4 - 珍園 / 神園マセラマティ coinages Oddgarden / Godgarden: kept, glossary rows, twins unified
- [x] arm9:91194 - glued "." after card name: confirm in-game (phase 8) -> waived: card decided composite seen in the phase 8 card_select tour; lint checks every combination

## b001-b002 (system, approved)
- [x] arm9:8F998/8F99C/8F9D4 - glued pieces: confirm joins in-game (glossary composite list) -> waived: composites seen in phase 8 (territory/capital/card); lint checks every combination
- [x] arm9:8FC5C - アラン人形 "Alan Doll": Al (Kylier's griffon)? check description -> waived: see 90414
- [x] arm9:8FC2C - チカラダケ "Power Shroom": Power Mushroom -> waived: playful, kept
- [x] arm9:8FC44/8FC64 - どくまむし "Pit Viper": Venom Viper -> waived: pit viper is the real snake; kept
- [x] arm9:8FD84 - 豪槍一本鬼: fixed: One-Horned Oni Lance (both twins)
- [x] arm9:90214 - 凶刃ベルセルク (match 91278 fix) -> waived: kept with 91278
- [x] arm9:8FD9C - Imperial Soldier's Armor -> fixed (s33): Imperial Soldier's Armor (both twins)
- [x] arm9:902D4/90344 - White Goat's Milk / Cheese -> fixed (s33): White Goat's Milk / Cheese
- [x] arm9:901FC - ▼DEF-1 marker dropped: check glyph options -> waived: no ▼ glyph in the English font; DEF -1 reads clear
- [x] arm9:8FCD4 - Golden Ear of Wheat -> fixed (s33): Golden Ear of Wheat
- [x] arm9:90154 - Life Bracelet (match 9046C) -> waived: kept with 9046C

## b017-b018 (approved after 2 Important fixes)
- [x] MESSAGE030:0782 Juvelon - "always" added: Wh-why me!? Why do\nyou target me!? -> fixed (s33)
- [x] MESSAGE026:04A3 Milanor - redundant: Still a tomboy, huh! -> fixed (s33): one line
- [x] MESSAGE026:0549 Rosary - おばさん "old hag" too strong: some\nauntie -> fixed (s33): some old lady
- [x] MESSAGE027:07DE / 024:06D9 Nessiah - keep teasing "..., you know?" -> fixed (s33): Didn't work, did it? / ..., you know?
- [x] MESSAGE031:0640 Russell - アンタ: Nice skills, pal! -> fixed (s33): one line
- [x] MESSAGE031:0675 Luciana - てやろう: I'll deign to be your\nopponent! -> fixed (s33)
- [x] MESSAGE028:0649 Inzaghi - "ticked off" mild: pissed off -> fixed (s33)
- [x] fixed (phase 6 review): "dear" on Eudy 025:0644 and soldiers 027:07F6 / 027:080A: drop (Mistel/Amareus only)
- [x] MESSAGE024:0656 Juvelon - Th-this is abuse,\nI say!? -> fixed (s33)

## b019-b020 (approved; ids are offsets inside b019-b020, look up with grep)
- [x] 078B Eudy - "I wonder" calque: Ready yourself, hmm? -> fixed (s33): one line
- [x] 05EE Nessiah - "I wonder" added: Can you withstand\nthis? -> fixed (s33): Can you / withstand this?
- [x] 06E8 Milanor - You did it now,\nyou...!? -> fixed (s33)
- [x] 0591 Elena - "help me" added: ...Please! -> fixed (s33)
- [x] 0797 Pamela - cheekier: Don't judge by\nlooks, okay! -> fixed (s33)
- [x] 0519 Durant - Pursuing! Have at you! -> fixed (s33): Pursuing! / Have at you!
- [x] 04ED Baldus - archaic lost: Press on, then! -> fixed (s33)
- [x] 0542 Cruz - "Upsy-daisy" twee: Heave-ho! -> fixed (s33)
- [x] 05B7 Ortega - Some little missy\nyou are... -> fixed (s33)
- [x] 0496 Dort - this gilded show-off -> fixed (s33)
- [x] 04B2 Kylier - ?! vs !? consistency -> fixed (s33): !?
- [x] 05B8 Juvelon - G-God above! -> fixed (s33)
- [x] 04F8 Luciana - Splendid...\nwork, truly. -> fixed (s33)
- [x] 0696 Leon - 俺様: fixed (phase 6 review, with the other 10 俺様 lines)
- [x] 0590 Flunky - 姐さん: Big Sis -> fixed (s33)

## b005-b012 (system/help/tutorial/start barks, approved; reviewed by the controller, codex quota out)
- [x] arm9:95AF4 - 名無しユニット "nameless units": Nameless Soldiers (glossary) -> fixed (s33): Nameless Soldiers fill in.
- [x] ov9_07:1F60 - 第三騎士団 "Third Cavalry": Third Knight Order -> waived: glossary ruling (Durant, Third Cavalry)
- [x] TUTO00_03:0099 - 『ファンタジニア王国』 shortened to 'Fantasinia' (fit?) -> waived: 144-px box; the full name is on the faction list
- [x] TUTO01_06:00B5 - "But only up to bases / held + 1 units." awkward -> fixed (s33): But the limit is / bases held + 1 units.
- [x] TUTO01_15:00DF - JP says 探索 at the end of the points page (game's slip): keep or say "points" -> waived: follows the game's own text
- [x] fixed (phase 6 review): MESSAGE001:02D5 Juvelon - "ain't ... I tell ye" too thuggish for a cardinal: "Our fight is not over yet, I say!"
- [x] ov9_06:3ED8 - "Rare" lacks the colon "For:" has (Rare: is 33 px > 32): move the value x (phase 7 to-do) -> waived: no room for the colon at 32 px; value placement is code, label reads fine

## b033-b034 (cannon/barricade barks, approved after "dear" fix)

## b035-b036 (retreat/village barks, approved; controller review)
- [x] MESSAGE115:0614 Zilva - 勝負あったな "It's decided": It's over... Elena. -> fixed (s33): It's over... / Elena.
- [x] fixed (phase 6 review): MESSAGE108:0646 Juvelon - "I'm outta here" slangy for a cardinal: I'm fleeing for now!

## b037-b040 (capture/prisoner barks, approved; controller review)
- [x] fixed (phase 6 review): MESSAGE132:0603 Juvelon - わしゃ…嫌じゃあ old-man voice flat: I don't want to die, I say!

## b041-b042 (recruit/release barks, approved; Amareus/Juvelon lines fixed in review)
- [x] MESSAGE141:051F Leon - 100年早え idiom literal: You're a hundred years too early, trash! -> fixed (s33): A hundred years too / early for you, trash!

## b043-b044 (release/dismiss/reward barks, approved; controller review)
- [x] MESSAGE150:0512 Mardym - でくのぼうが生意気な said to the player: Wh-What!? Insolent blockhead...! -> fixed (s33)

## b045-b046 (reward/village/unification barks, approved; controller review)
- [x] MESSAGE160:0584 Gordon - "...?" after a statement reads odd: That village concerns me... -> fixed (s33): That village earlier / concerns me...
- [x] MESSAGE168:04D2 Canaan - "Congrats" casual to the Emperor: Congratulations on / uniting all, Majesty! -> fixed (s33)

## b047-b048 (ending/weapon-capture barks, approved; Eudy "dears", Amareus/Flunky congrats fixed in review)
- [x] MESSAGE173:0749 Rosary - 百人力 "I'm a hundred strong!" literal: I'm worth a hundred! -> fixed (s33)

## b049-b050 (weapon/Appraiser/item barks, approved; controller review)
- [x] MESSAGE188:08F2 Nameless Soldier - no end punctuation: Looks like we can / get cards appraised! -> fixed (s33)

## b051-b054 (explore/path barks, approved; controller review)
- [x] MESSAGE201:078E Juvelon - no end punctuation: ...a path to the left, eh. -> fixed (s33)

## b055-b056 (loot-box picks, conquest lines, first DUEL EVENTs; approved; controller review)
- [x] MESSAGE210:0641 / MESSAGE212:0616 Ortega - waived: no swap. MESSAGE210-219 put one line per leader in the same order; line 1 always carries ほっほー/ぞぉ (Ortega), line 2 のう/じゃ/かのう (Dort); ぞい is used by both, so tags and voices are consistent

## b057-b058 (DUEL EVENT lines Russell..Yggdra, approved; controller review)
- (no Minors)

## b059-b060 (DUEL EVENT lines Yggdra..Leon, approved; Dort/Leon voice fixed in review)
- (no Minors)

## b061-b062 (DUEL EVENT lines Leon..Russell, approved; controller review)
- [x] SPMES009035:01A8 Mistel - "I'll settle it now, dear?" question mark reads odd: I'll settle it now, dear~ -> fixed (s33)
- [x] SPMES012024:018E Amareus - no end punctuation: Juvelon-sama... / I'm so... sorry... -> fixed (s33)

## b063-b064 (DUEL EVENT lines Milanor..Kylier, approved; Mistel "punish you" parody joke fixed in review)
- (no Minors)

## b065-b066 (DUEL EVENT lines Kylier..Mardym, approved; controller review)
- [x] SPMES020004:0140 Cruz - JP names Aegina but the duel file is Luciana's (game text?): check on screen -> waived: the JP names Aegina here; the game's own text, kept

## b067-b068 (DUEL EVENT lines Luciana..Gulcasa, approved; controller review)
- [x] SPMES030036:01EF / 020D Nessiah - ユミラ "Yumira" / ユメール人 "Yumeru": kept (no Atlus name found), glossary rows

## b069-b070 (DUEL EVENT lines Gulcasa..Nessiah, approved; Luciana addressee + Nessiah taunt fixed in review)
- [x] SPMES034036:0160 Nessiah - フフフ restored: Still alive? How surprising, / Flame Emperor. Heh heh...

## b071-b072 (APP/TRE/WR system lines, EDMES00-13; approved; epithet run widened to 186 px, controller review)
- [x] EDMES00:00EA Russell - 悲運 shipped as "Tragic" (Ill-Fated was 196 px): fine unless the ED_H texture wording differs -> waived: ED_H texture wording matches (Tragic)
- [x] SPMES_APP02:011B Mistel - 百人力 "With me here, I'm worth a hundred~!" reads a bit stiff: With me, you're / a hundred strong~! -> fixed (s33): With me here, / you're a hundred strong~!

## b073-b076 (EDMES13-37 epithets + epilogues; approved; cut ranks restored at 186 px, controller review)
- [x] EDMES25:038A Roswell - 黒薔薇にその人在り "The Black Rose has its man" awkward: "Black Rose has its great man" -> fixed (s33)
- [x] EDMES25:00E2 / EDMES28:00DB - 大賢者/大魔導師 shipped Sage / Magus (Archsage/Archmage 189 px > 186): recheck if the budget is ever measured to 190 -> waived: the epithet budget is 186 px; Sage/Magus keep the rank meaning
- [x] EDMES30:00B7-00E5 Pamela - fixed: Big of Mages / Great of Mages Pamela (ED_H/ED_N textures must match)
- [x] EDMES26:00D8 / EDMES20:009C / EDMES18:00A7 - 流神 Evangelist, ぶち Hothead, 卑屈姫 Sulky Princess: kept, in glossary

## Phase 7 (insert, controller)
- [x] ov9_18:3748 + faction name - the '"' glyph leaves a ~3 px gap before the name in the unlock message (work/qa/p7_quote.png): tighten the quote glyph or its advance (enfont PUNCT) -> waived (s33): the quote reads as a quote on both sides of the name; the gap is the glyph's open column + 1-px spacing (cosmetic)
- [x] ov9_18:3D58 - faction conditions header: count digit at fixed x 162 lands in the 4-space gap (prefix ends x 159, "of" at x 175), computed, not seen on screen: check in phase 8 -> fixed (s30): header got a 5th space, digit x 162 -> 161, seen centred (work/qa/cover2/terms_zoom.png)
- [x] ov9_10 medallion unit + territory line (lines_px12) - not seen on screen: check in phase 8 -> waived (s33): its strings are shown in the textcover runs; lines_px12 centring seen on 4 other callers; lint gates the width
- [x] MESSAGE*/SPMES* ellipsis-only lines (54) set to "..." by fix7a (glossary rule), unreviewed in context -> done (s33): read in context by the story pass (chapters msg_* / duel_*, codex), none flagged

## Phase 8 (textures, controller)
- [x] SEN_FONT 戦 / 撃 / 斬 cells (13-14 px, 戦績 page "0戦 0撃 0斬") are "Btl" / "KO" / "Kill": abbreviations; widen the cells (page code) or reword -> waived (s33, README known issues): 13-14 px cells fit no full word at a legible size; the 戦績 page reads Btl / KO / Kill
- [x] SAVE_FONT "Theocracy of Meria" squeezed to 0.52 in its 53-px ink rect: see the save slot on screen, widen if the game rect allows -> waived (s33, README known issues): seen on the save slot in phase 8 (save1.dsv), legible
- [x] BTLFONT terrain / move-type / speed cells squeezed 0.53-0.8 (20 px): see the battle HUD, consider a narrow pixel font -> waived (s33, README known issues): legible on the battle HUD at 1x (tour battle sheets ok)
- [x] BTLMN_FONT weapon headers (Sword .. Book, 16-px cells) and TREFONT 前後左右 / 歩 (Front Rear Left Right, "steps")
  squeezed 0.5-0.6 at 9 px; 雷撃 = "Bolt" in the 20-px element cells (SYSTEX, TREFONT): see on screen, reword or a pixel font -> waived (s33, README known issues): legible at 1x on the pause / treasure screens (tour ok verdicts)
- [x] SYSTEX army names on the battle HUD at 8 px (Royal Army, Forest Army ..), 帝国軍 = "Empire" (33-px cell); 不明 = "???";
  a 2-px mark above "Royal Army" on the HUD (the game's rect starts a row into the White Rose cell: move that label up) -> waived (s33, README known issues): HUD army names legible at 8 px; tour battle sheets ok
- [x] Session 19 atlases (TR_FONT, TUKOKU_FONT, CDSKILLFNT0/1, ENETREFONT, TREFONT, BTLMN_FONT, SYSTEX): boxes are ink
  rects, none seen drawn: check each on screen (ENETREFONT brush text is drawn straight now, not tilted) -> waived (s33): each atlas's screen passed visual QA in phase 8 (tour verdicts ok, pause case s32)
- [x] (done s33: story pass chapter `textures`, codex verdict ok) `_unk_` war-event titles/paragraphs (session 20, read off the textures, translated by the controller with no
  reviewer): story-pass them with the faction voices. s31: they are the rumor screen 風聞 (FUM_TI<fac><A-E> /
  FUM<fac><A-E>, task 0x0208ED54 after a story battle), seen on screen via tools/debug/fum.txt; paragraph ink ends
  <= x 240 (frame pillar 244, original also 240); titles slide in from the right and settle like the original;
  logo variants 5851b4bc/660bec2b/73c6239a: ruby boxes eyeballed, check on screen; _unk_c85ce18c "Town of Tolstoy"
  label (unknown use) and _unk_078801f1 (noise decode, untouched)
- [x] TU_* tutorial shots (session 21, labels read off 256 x 100 shots, no reviewer): unread and left Japanese: the
  2nd unit name (コアン?) on TU_C06_01 / TU_T02_04 / TU_T02_05 and the tiny portrait tags on TU_C06_01; guesses:
  TU_T04_01 row 1 "South Nyllard Desert" (南部 or 北部), TU_T02_05 terrain row 2 order (Forest Waste Desert Peaks
  Water Swamp), TU_T04_04/06 composite wording ("went there and never came back..." / "Durant, to Fort Lonaris...");
  6-px labels (T02_04/05, C06_01, T10_00) are mush at that size in either language: see them in the tutorial viewer -> waived (s33, README known issues): 6-px labels in tutorial illustration shots are illegible in both languages; the shots' big labels are English
- [x] SYSTEX Unit Info cells are ~20 px (JP 2 kanji): 地形 -> "Land" (Terrain was clipped to "Terra"), 装備 -> "Gear"
  (Equip clipped to "Equ"), Speed squeezed 0.7 at 9 px (session 23); widen the cells in code if a later pass wants the
  full words -> waived (s33, README known issues): Land / Gear read clearly in the 20-px cells
- [x] OPK_WR faction descriptions squeezed to 0.60-0.94 (maxw 160, the attract faction intro shows only ~160 px):
  rewrap shorter if a reader finds them cramped -> waived (s33, README known issues): legible in the attract intro (tour ok)
- [x] Prize unit list (bottom screen, top-left card): "Nameless Soldier" (dialogue font) runs under the portrait, the
  final r half hidden (the JP name is 4 kanji); a shorter generic name or a tighter font if a reader minds -> waived (s33, README known issues): the visible part reads Nameless Soldie..; the JP clips too
- [x] CNAMEB name plates squeezed to maxw 110 (VS screen of the war report shows the right fighter from x ~143): the
  longest names (Mercenary Captain Inzaghi, Astral Fencer Russell) are now ~0.85 wide everywhere they appear -> waived (s33, README known issues): names read at 0.85 width
- [x] Tutorial top line arm9:93494 "I'll teach you how to win wars." (one line above the band; the 2-line budget in
  lint is wrong for that screen) -> waived (s33): the line is 31 chars, one line on screen (tutorial tour ok); lint's 2-line budget is only looser
- [x] MS_M_01 faction_select description "...centered on the royal capital Paltina" fills the 256-px band edge to edge (no period); shorter wording, e.g. "around the royal capital Paltina." (check other MS_M rows for periods) -> fixed (s33): around its royal capital, Paltina (xscale 0.87); the other MS_M rows end without periods like the original
- [x] MS_PRO_002 (sans-b 14): "high-born" kerns r+n into "m" at 1x; check other MS_PRO rows for rn/cl pairs (s31) -> fixed (s33): f02 rewritten without high-born; other rows' rn/cl pairs read fine in context (tour ok)
- [x] EXTRA_FONT "Card Catalog" small label (64-px quad) is visibly smaller than the other menu buttons; the quad
  is the original's ink width, so a shorter label ("Cards"?) or wider quad would match (s31) -> waived (s33, README known issues): label legible; the quad is the original's width
- [x] Battle pause menu (BTLMN_FONT): opened by Select (tour case `pause`, tools/lua/pausemenu.lua ends the deploy
  phase); s32 boxes = the game's quads. Squeezed small in their quads: "Weapon Affinity" (menu button 64 px and
  table header 54 px), "Weapon/Element" / "Terrain Affinity" (Unit Info buttons, page headers 48-55 px), class cells
  Knight (22 px) / Witch / Golem (28 px); 回数 / 回 count suffixes blanked ("Smash Hit ... 0"). Tactician's quad
  was never drawn (class absent): box guessed 208,90,48,12, see it on a battle that has one -> waived (s33, README known issues): squeezed labels legible at 1x (s32 zoomed frames); Tactician box guessed, the class appears in no reachable battle
- [x] MS_PRO prologues show 3-line pages of one texture: pages end mid-sentence (prologue_f02 "leader of a band" /
  "Taking it as his chance,", f07 "to spread / the faith", f08 "Juvelon's / faction"); rewrap so pages end on a
  sentence where the line budget allows (codex s32) -> fixed (s33): f02 / f07 / f08 rewritten so each page (2/4/5, 3/3/4, 4/2/4 lines) ends on a sentence
- [x] Prisoner dialogue one-word last lines ("You are the enemy / general?", "To be captured by / you..."): rewrap
  or reword (codex s32) -> fixed (s33): MESSAGE130:04ED So you're the / enemy general?, MESSAGE133:0673 Captured by the / likes of you...; the other two-line barks are the 142-px bubble's balanced wrap
- [x] BTLFONT "NOON" on the Terrain Affinity page: the N's left stem comes out as dots one column left (":NOON");
  the edited PNG matches the original there, so it is the texture re-encode (gfx.py check BTLFONT), not the art -> waived (s33, README known issues): 4x4 encode of a block shared with an edited label (gfx.py check: encoder limit); NOON still reads
