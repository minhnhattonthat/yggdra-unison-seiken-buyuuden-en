# Scenes, game state and the debug warp

## Scene manager (verified: warp.lua drives every scene below from a cold boot, work/qa/warp/)
- Struct at **0x0210E010**: `+0x10` u32 current scene, `+0x14` previous, `+0x18` next, `+9` u8 phase (0 init, 1 running,
  2 leaving). `0x0200D13C(next)` = set next + phase 2. Writing `+0x18` and `+9 = 2` from Lua is a clean scene change.
- Scene table **0x0208F4D4**, 22 x 16 bytes `(init, main, exit, overlay id)` (overlay -1 = arm9). Ids:

| id | ov | scene | id | ov | scene |
|---|---|---|---|---|---|
| 0 | 5 | company logos | 11 | 8 | war report 戦況報告 |
| 1 | 0 | title | 12 | 2 | turn end ターン終了 |
| 2 | 18 | faction select (new game) | 13 | 19 | save |
| 3 | 16 | card select | 14 | 19 | load |
| 4 | 17 | sortie select 出撃先選択 (world map) | 15 | 9 | attract opening (prologue scroll) |
| 5 | arm9 | battle | 16 | 7 | attract character intro |
| 6 | 14 | territory expansion 領土拡大 | 17 | 9 | new-game opening (BEGIN + scroll) |
| 7 | 13 | explore preparation 探索準備 | 18 | 15 | ending 全土統一 -> epithets -> epilogue -> staff roll |
| 8 | 12 | prize 褒賞 | 19 | 6 | extra contents |
| 9 | 11 | prisoner 捕虜処遇 | 20 | 4 | faction prologue |
| 10 | 10 | medallion supply | 21 | 3 | tutorial |

- Jumping straight from the title to scene 2+ skips the new-game init (map unowned, all red): warp.lua goes through
  GAME START, then requests the target scene from sortie select (turn 1), where the game state is real.

## Game state (partly verified)
- Player faction: u8 **0x02119138** (`0x02043464` get / `0x02043688` set). Verified by tap tests (warp.lua log `player`).
- Selectable factions: u16 bits **0x0210E6E6** (new system data 0x0006 = factions 1, 2); 0x0FFF opens 0..11 (verified:
  all 11 map factions selectable). 0x0210E6E8 bits = "newly unlocked" flags ov18 clears; 0x0210E6E4 = cleared? (guess).
- Territories: 37 x 0x22-byte records at 0x02118C4E, low 5 bits of the u16 = owner faction (`0x02042B34`; guess from code).
- Faction ids (faction-select tap -> 0x02119138): 0 red north-west (帝国), 1 Fantasinia, 2 Milano, 3 light blue
  south-east, 4 white east, 6 green, 7 orange, 8 yellow, 9 small green in yellow, 10 pink (森林), 11 north-west chunk.
  5 owns no start territory.

## Text loaders
- Rumor screen 風聞 (verified s31): task `0x0208ED54(n)` (arm9, main 0x0208E75C) loads FUM_BG0-3, FUM_TI<faction
  %02d><'A'+n> (256 x 24 title) and FUM<faction><'A'+n> (256 x 240 paragraph); faction from 0x02043464; n 0/2 take
  one layout, 1/3/4 branch at 0x0208EE50. Callers: battle end 0x02080908 (n = byte +0xE) and 0x0204C2D4.
  Forced by tools/debug/fum.txt. Modes 1/3/4 (B/D/E) open a castle BG (FUM_BG2/3) + a bottom-screen dialogue; in the
  forced battle view they never draw the title/paragraph quads and a tap blacks the screen, so fum.txt shows their
  textures in the mode-0 layout (fumfac.lua LETTER= swaps the sprintf letter r5).
- MESSAGE%03d: `0x02078760(file, r1, r2, r3, [sp])`, ~70 call sites in arm9 and overlays 10-19 (per-scene events).
  Seen: faction select confirm -> MESSAGE000, card select -> 008, sortie -> 009.
- SPMES%03d%03d: `0x020771FC`, numbers from bytes at `*(battle+0x34)`, `*(battle+0x38)` (battle object from 0x0206F9D4).
  These are **duel events**: the duel init 0x0206F1E0 stores the two units at +0x34/+0x38 and asks 0x02077134(a, b, 0)
  (modes 1/2 at 0x02076728.. during the duel); yes -> 0x02077910 creates the event task. Numbers = unit ids (guess).
- **Forcing battle-only screens** (`tools/lua/spmes.lua`, from work/states/battle.dst, route `100 -;10 t16,152;600 -`
  = tap your own castle): the CAUTION draw call (BL at 0x02010BA4) is patched once into BL CALL. Default CALL
  0x02077910 + `SPA/SPB` = any SPMES file (DUEL EVENT box); `CALL=0x02080388` (+ tips.lua `TIP=n`) = HINT! popup;
  `CALL=0x02081350 R0=8` = YOU WIN + War Result page. DeSmuME: `setregister("arm9.r15")` does not redirect, and
  `memory.registerexec` keeps one callback per address (two scripts hooking one address: the last wins).
- Battle moves (unverified): dragging from the unit (play.py presses with `--gap 0`) draws a 2-square path box; a tap
  on its end square spent 2 TIME but the unit did not visibly move (work/play/tour_bt3 0006-0007).
- File open by name: 0x0200A540 (r0 = name); warp.lua waits on it for the epilogue (EPI_MES_nn) and credits (STAFFROLL).

## Input facts
- Almost everything is touch: A does not advance dialogue or skip the attract loop; a tap does. Title menu: GAME
  START (128,58), CONTINUE (128,91), TUTORIAL (128,124). Confirm dialogs: OK (75,180), CANCEL (187,180). Faction /
  sortie bottom bar: 戻る (35,182), 戦力確認 (128,182), 決定 (218,182). Help popup at new game: CANCEL = no help.
- Battle TIME (300) only drops while moving, not with time.

## Game over (verified 2026-11-10, session 22)
- `0x0207F04C(r0)` starts it (battle state 0x0211A874 |= 0x20, +8 = 4, then 0x0207EF6C: B_GAMEOVER banner task
  0x0207EB44, fade, then 0x0207FAA0 loads GMOVERBG / GMOVERFONT: "Give it up?" Retry / Easy Retry / Back to Title,
  plus a HINT! tip). Callers 0x0207CEBC (r0 0, battle end code 0x0E) and 0x0207CED0 (r0 1, code 9).
- Warp: tour.txt `gameover` = battle + spmes.lua `CALL=0x0207F04C R0=0`, tap own castle (t16,152).
- Battle: the bottom screen waits on "Touch" (no animation at all while idle).
- **Battle pause menu (BTLMN_FONT, verified s32):** Select. Input handler 0x0204DF98..0x0204E01C: `0x0204BE78(1, id)`
  = keypad test (id 6 -> mask 4 Select, 5 -> 8 Start, 4 -> 0x300 L/R ...); Select calls the menu loader 0x02089728
  only while battle flags 0x0211A874 == 0 (or has 0x1000). The warp's battle sits in the deploy phase: flags 0x2000
  (set at 0x02057598 by task 0x02057278, cleared at 0x02057BB0 when the deploy ends). `tools/lua/pausemenu.lua`
  clears it once, then Select works (TIME starts running). Tour case `pause` walks Weapon Affinity, Unit Info >
  Weapon/Element (UNIT 2 t162,86), Terrain Affinity (UNIT 2, Terrain 2 t162,113), Duel Data, Retry confirm.
  quads.lua logs its quads under a stale slot name ("MS_PRO_001") after `load .. BTLMN_FONT`.

## Not reached yet
- Specific stages / SPMES events, specific MESSAGE events, per-faction battles (ATTACK_TAP is set for faction 1) and
  the 38 EDMES ending variants are reached only as far as the default flow goes; phase 8 text coverage will list what
  is missing. `MSG=n` retargets the next MESSAGE load (dialogue viewer; untested beyond logging).
