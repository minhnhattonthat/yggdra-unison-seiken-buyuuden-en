# Text windows and width budgets (width gate, phase 5)

Machine-readable budgets: `script/windows.json` (read by `tools/lint.py`, run by `tools/check.py`). Line px = sum of
the VWF advances + 1. Pen origin and box edges read from cold-boot shots with `tools/rowscan.py` (colour runs per row;
`--ink x,y,w,h` = outline extent). Verified by `sh tools/debug/widthgate.sh`: a stress build (`build/yggdra_gate.nds`)
with lines filled to each budget (`MARKER_QA="ID=#<px>x<lines>"`, tools/marker.py) plus the glyph torture line,
booted cold to each box -> `work/qa/gate/gate.png`.

## Dialogue text objects (0x020128B8; MESSAGE via 0x02006324, SPMES via 0x02006F78)
Both create the object at x = -1; the scene sets the position, so the box is per scene. 2 lines (FD, y += 0x11).

| Box | Family | Pen x | Last usable x | Budget | State |
|---|---|---|---|---|---|
| bubble, portrait left (prize, ending, medallion...) | MESSAGE | 98 | 244 (cloud edge, line 2) | 142 px x 2 | verified: `#142x2` fits, MESSAGE154:0240 in prize |
| bubble, portrait right (prisoner) | MESSAGE | 11 | 154 | 142 px x 2 | verified: `#142x2` fits, MESSAGE130:04ED (right at the edge) |
| ending results bubble (戦績, name under it) | MESSAGE168 | 7 | ~165 (portrait) | 142 px x 2 | measured: work/qa/m168_zoom.png |
| explore / shop box | SPMES_TRE | 40 | 239 (fill); page arrow 225-236 on line 2 | 184 px x 2 | verified: `#184x2`, SPMES_TRE:0160 |
| battle duel event (DUEL EVENT, top screen) | SPMES*** | 40 | ~238; page arrow 228-236 under line 2 | 184 px x 2 | verified: `#184x2`, SPMES001014:0160 (work/qa/gate/spmes_zoom.png, forced by tools/lua/spmes.lua) |
| tutorial bubble (portrait right) | TUTO | 8 | 159 (fill); arrow 154-162 under line 2 | 144 px x 2 | verified: `#144x2`, TUTO00_01:007B |

## EDMES (ending, scene 18, ov9_15)
- Paragraphs (3-4 lines) draw over the character art, one glyph per call to 0x02012FFC from ov9_15 0x0211DC88; the
  overlay advanced x by a fixed 11 (`add r4,r4,#0xB` at 0x0211DC8C), now `bl ov_adv` (tools/engine.py OV_SITES) =
  VWF advance from the width table (font id in fp). Pen x 32, panel frame from 242: **208 px x 4 lines**, verified
  with the torture line (EDMES07:0100, last line 206 px). The game fades the text where it crosses the portrait
  (the Japanese does the same).
- One-line epithets (ナマクラ聖剣士ラッセル, record +0): the top title bar is the ED_H texture with the same words;
  the string itself is drawn on the bottom 戦績 page after 称号： (ov9_15 0x0211E010, run x 102 y 35): 150 px in the
  original. `mov r0,#0x66` at 0x0211E004 is now `#0x42` (engine.OV_SITES): run x 66, over the 称号： label (part of
  the page BG, no text call: blank it in the graphics phase), clipped at 256: **186 px** (work/qa/epi_mk f000900).

## System text (arm9 / overlay pools; 0x02012DF4 runs, 0x020130AC centred)
Which string draws where: `tools/lua/systrace.lua` logs every call (x, y, font, caller, bytes); on the marker build
the bytes are marker codes, so `python -X utf8 tools/sysmap.py work/qa/<dir>` maps them to ids (work/sysmap.tsv).
All 35 warps: `regen.py --rom build/yggdra_marker.nds --qa work/qa/sys2 --script tools/lua/systrace.lua` (27 ids;
most system text sits in submenus, still to tour). The marker build fills every system string to its rule's px and
relocates it (`MARKER_SYS=slot` = old short codes in place); `MARKER_QA` overrides system ids too.

| Box | Draw | Budget | State |
|---|---|---|---|
| centred help band under a scene banner (top screen, y 140) | ctr, overlay callers | 240 px x 3 | measured: 240 px x 2 = ink 9-248 (territory); 3rd line by y |
| CONFIRM / info band (bottom screen, full width, OK / CANCEL) | ctr, caller 0x020102F8 | 240 px x 3 | measured on card_select (band spans the screen) |
| character profile ticker (char_intro, y 4, scrolls left) | run, ov9_07 0x0211BC3C | 900 px (slots) | measured: packed cells, every profile at 900 px = 89/128 slots, scrolls through and restarts (work/qa/gate/tick3) |
| item name, system font, prize item list (x 30, scrollbar at 242) | run, prize overlay 0x0211E524/E6A4 | 208 px | measured (work/play/prize2/0003.png) |
| item name FONT_ITEM, item popup (x 23 y 116), effect lines (x 40 y 132; x 3 y 167 built in a heap buffer) | run | guess | drawn in prize after tapping an item, not visible in the shot yet |
| medallion line (arm9:9222C, x = 0x80000000 at entry: set later) | run | guess | |
| item encyclopedia (extras ov9_06, top screen): no. label x 41 / name x 85 y 12; レア： 装備： x 14 + value x 46; 効果： x 14 y 83 + effect x 41 y 96 (2 lines); 発見場所： x 14 y 136 + territory name x 41 y 152; panel frame 242 | run | name 168 (screen edge), effect 200 x 2, equip 195, territory 200, labels 32 / 227 / 44 | measured (work/play/tour_ex 0002; open every entry with `tools/lua/extras_all.lua`) |
| sound mode ticker (ov9_06, y 174, scrolls): BGM00： label, title at label x + 66 | run | label 66; title guess | measured label |
| card dictionary / card select info panels | - | - | textures (CDS_*, graphics.md), not system text |
| tutorial menu (ov9_03): topic list x 20 on a sloped bar (row top ends 152); page title x 67 y 115 (bar slope ~200); description x 49 y 135, 3 lines, to the screen edge | run | title 130, description 204 x 3 | measured (work/play/tour_tuto 0001-0002) |
| battle: sortie hint x 23 y 162 = 91F4C + digit + 91EDC (one run) | run 0x02051688 | 216 each, composite 225 | measured (tour_bt 0008) |
| battle CAUTION band (bottom y 161, 1 line) | ctr 0x02010BA4 | 240 x 1 | measured (tour_bt2 sheet) |
| battle data pages (SELECT menu > unit info / weapon affinity / duel data): description x 20 y 38 to the screen edge | run 0x0208BB9C.. | 228 x 3 | measured (tour_bt 0018-0026) |
| duel data labels (top x 30, number at x 198) = table 101CAC+0 | run 0x0208CEB0 | 164 | measured |
| territory (ov9_14): captured / capital-taken messages = composites (army / faction lands / territory tables), centred band y 81 | run, x from count11 | composite 240 x 2 | measured (tour_te 0002) |
| territory 'expanding' line + animated dots | run y 90 | 180 | measured |
| explore help pages (ov9_13): title x 5 y 7, body x 12 y 28 | run | title 240, body 236 x 7 | measured (tour_exp 0001) |
| war data (turn end > 戦争データ, ov9_02): label x 39, number to 217, unit x 217 | run | label 130, unit 37 | measured (tour_exp 0006) |
| medallion line (ov9_10) centred band y 90 | run | 240 x 1 | measured (tour_me 0002) |
| medallion Get Item! popup: item-font name, centred after the icon | run font 2 | 168 (= system-font copy) | measured |
| war report event line under the banner (top x 40/45 y 130) | run ov9_08 | 210 | measured (tour_wr 0004 sheet) |
| faction conditions page (使用条件, ov9_18): header 2 lines x 8 y 21 (count digit at fixed x 162!), rows x 8 y 57..147 | run | 240 x 2 / 240 | measured (tour_fs 0003) |
| faction unlock message (option menu 0x0201038C band y 80/96): 3748 + faction name + 3740, then 3750 | run | composite 240 | measured (tour_un 0004, tools/lua/unlock.lua) |
| save / load prompts (ov9_19, ov9_15, ov9_05) | ctr 0x020102F8 | 240 x 2 | measured (save band) |
| in-game HELP popup (help on at new game): title x 22 y 59, body x 24 y 76 x 3 lines, frame at 236 = table F79D8+0 | run 0x02011168 / 0x020111AC | 210 / 210 x 3 | measured (tour_hp 0006) |
| textures, no system text: battle menu (SELECT), L unit panel, unit status, unit lists, sortie territory panel, faction info panel, VS names | | | toured 2026-11-10 |
| battle HINT! popup (100500, task 0x0207FD6C): entry 2n white y 49, 2n+1 red y 82/97, yellow panel spans the screen; centred by per-line glyph count (0x02013274) x 11, not px: **phase 7 fix** | run | 220 x 2 | measured (work/qa/tip0_top.png; `spmes.lua --var CALL=0x02080388` + `tips.lua --var TIP=n`) |
| battle results (War Result page, 100554 labels x 40 y 48 + 21 n, digits from x 176) | run 0x02080D88 | 120 | measured (work/qa/res_final.png; `spmes.lua --var CALL=0x02081350 --var R0=8` = YOU WIN + results) |
| ending epithet one-liner (EDMES record +0): ov9_15 0x0211E010 run x 66 (was 102, after 称号：) y 35 bottom screen, bar count11*11+40 from x 66 | run | 186 | measured (work/qa/epi_mk f000900) |
| ending results bubble MESSAGE168 (戦績 page): pen x 7, cloud to ~165 | MESSAGE | 142 x 2 | measured (work/qa/m168_zoom.png) |
| info band messages (explore / prize / medallion / save..., `tools/strcalls.py`: load then BL 0x0200FC88) | band -> ctr 0x020102F8 | 240 x 3 | same band as card_select |
| battle CAUTION messages (load then BL 0x02010BC8 = the CAUTION task, as arm9:930D8) | ctr 0x02010BA4 | 240 x 1 | same band |
| extras (ov9_06): menu descriptions table 0x0211FA88 (ctr y 140 help band), prompts / not-yet (ctr y 89), sound titles table 0x0211FAAC (ticker) | ctr / run | 240 x 3 / 228 / 400 | code |
| medallion (ov9_10): report line 2 (buffer r4+0xA5, centred), warning popups x slide+72 / +50 | run | 240 x 2 / 180 / 200 | code |
| tutorial scroll descriptions (ov9_03 ctr y 120, 4 lines) | ctr | 240 x 4 | code |

**Static classification:** `python -X utf8 tools/strcalls.py ID..` lists each load of a string's address and the BLs
right after it (run / ctr / band / join / menu ...): how the "guess" system strings got their rules without a tour.

**Composites** (`composites` in windows.json, checked by lint): strings 0x020132E0 joins before one draw; lint tries every
combination of the parts (ids, `table:` fields, literal `'0`) line by line.

**Tables:** `tools/ptrtables.py` groups the 1,282 table-pointed strings by data table and field (territories
A71F0 +0, factions A7D00 +0/+4/+8, cards A7E44 +0 name / +4 one-liner, units F5380 +0 / +4, classes F5B88,
help F79D8, items 100648 = record +8..). A windows.json rule with `"table": "A71F0+0"` covers a whole field.
Tours: `tools/tour.py SCREEN --new STATE` then `tools/tour.py SCREEN <presses>` (play.py + systrace; logs to
work/qa/tour/SCREEN), `tools/sysmap.py work/qa/tour work/sysmap_tour.tsv` -> ids.

**Glyph slots:** system text is packed into 16 px cells (one slot per 16 px of line, text.md; pool at 0x0210E768,
cap 128 in most scenes, 256 tutorial); slots past the cap are not drawn instead of overrunning. Before packing
(one slot per glyph) landing screens peaked at 117/128 (medallion) and a 130-char profile crashed.

**Unit / class names in lists** (prize UNIT LIST, unit status: ヴァルキリー, 王女ユグドラ, 時間帯, 地形 ...) are textures
(CNAME*, graphics phase), not system strings.

## Glyph torture line (verified 2026-11-10, work/qa/gate/epilogue f000900)
All 82 English glyphs (` !"%&'()*+,-./0-9:;?~—…A-Za-z`) and double spaces render with VWF spacing. The game's own
lowercase p and q have no descender room (p reads like a small P, q like 9): legible, candidates for a redraw.

## Not text windows (graphics phase)
Dialogue name tags (王女ユグドラ, 商人) are CNAMEC%02d textures (fileopen.lua in prize/explore); the battle HUD
(王国軍 残存戦力), turn-end / tutorial / extras buttons and the epithet title bar are textures too.
