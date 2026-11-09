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
| ending results bubble (戦績, name under it) | MESSAGE168 | - | - | 142 | guess: not measured, same rule |
| explore / shop box | SPMES_TRE | 40 | 239 (fill); page arrow 225-236 on line 2 | 184 px x 2 | verified: `#184x2`, SPMES_TRE:0160 |
| battle event dialogue | SPMES*** | - | - | 184 px x 2 | guess: no battle event reached yet (warp stops on the map; debug-tool gap) |
| tutorial bubble (portrait right) | TUTO | 8 | 159 (fill); arrow 154-162 under line 2 | 144 px x 2 | verified: `#144x2`, TUTO00_01:007B |

## EDMES (ending, scene 18, ov9_15)
- Paragraphs (3-4 lines) draw over the character art, one glyph per call to 0x02012FFC from ov9_15 0x0211DC88; the
  overlay advanced x by a fixed 11 (`add r4,r4,#0xB` at 0x0211DC8C), now `bl ov_adv` (tools/engine.py OV_SITES) =
  VWF advance from the width table (font id in fp). Pen x 32, panel frame from 242: **208 px x 4 lines**, verified
  with the torture line (EDMES07:0100, last line 206 px). The game fades the text where it crosses the portrait
  (the Japanese does the same).
- One-line epithets (ナマクラ聖剣士ラッセル): the title bar on that screen is the ED_H texture with the same words;
  where the string itself is drawn is not seen yet. Guess 140 px.

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
| character profile ticker (char_intro, y 4, scrolls left) | run, ov9_07 0x0211BC3C | 520 px (slot limit) | measured: 82 chars ok (114/128 slots), 130 chars crashes |
| item name, system font, prize item list (x 30, scrollbar at 242) | run, prize overlay 0x0211E524/E6A4 | 208 px | measured (work/play/prize2/0003.png) |
| item name FONT_ITEM, item popup (x 23 y 116), effect lines (x 40 y 132; x 3 y 167 built in a heap buffer) | run | guess | drawn in prize after tapping an item, not visible in the shot yet |
| medallion line (arm9:9222C, x = 0x80000000 at entry: set later) | run | guess | |
| everything else (help menu ov9_03, extras ov9_06, unlocks ov9_18, explore pages, item effects / equip lines, save prompts) | | 240 x 3 / 100 x 1 guesses | screens not toured yet |

**Glyph slots:** system text takes one slot per glyph (pool at 0x0210E768; cap 128 in most scenes, 256 tutorial).
Landing screens with every string at full budget peak at 117/128 (medallion), 114 (char_intro). Long profiles
overflow: pack system text into 16 px cells like dialogue (engine work, next).

**Unit / class names in lists** (prize UNIT LIST, unit status: ヴァルキリー, 王女ユグドラ, 時間帯, 地形 ...) are textures
(CNAME*, graphics phase), not system strings.

## Glyph torture line (verified 2026-11-10, work/qa/gate/epilogue f000900)
All 82 English glyphs (` !"%&'()*+,-./0-9:;?~—…A-Za-z`) and double spaces render with VWF spacing. The game's own
lowercase p and q have no descender room (p reads like a small P, q like 9): legible, candidates for a redraw.

## Not text windows (graphics phase)
Dialogue name tags (王女ユグドラ, 商人) are CNAMEC%02d textures (fileopen.lua in prize/explore); the battle HUD
(王国軍 残存戦力), turn-end / tutorial / extras buttons and the epithet title bar are textures too.
