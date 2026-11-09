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

## System text (arm9 / overlay pools; 0x02012DCC runs, 0x020130AC centred)
- Help lines centred under each scene banner (sortie, territory, card select, prize, war report, explore...) sit on
  a screen-wide band: 240 px, 2-3 lines (guess per string until each string's screen is mapped).
- Everything else (unit/class/item names, list fields, labels) is a guess: 100 px x 1. Phase 6 must measure list
  fields with the longest name (the next thing drawn on the row minus the field x) before translating names.
- System strings are still in place (`max` bytes): English longer than `max` needs the relocation step (status.md).

## Glyph torture line (verified 2026-11-10, work/qa/gate/epilogue f000900)
All 82 English glyphs (` !"%&'()*+,-./0-9:;?~—…A-Za-z`) and double spaces render with VWF spacing. The game's own
lowercase p and q have no descender room (p reads like a small P, q like 9): legible, candidates for a redraw.

## Not text windows (graphics phase)
Dialogue name tags (王女ユグドラ, 商人) are CNAMEC%02d textures (fileopen.lua in prize/explore); the battle HUD
(王国軍 残存戦力), turn-end / tutorial / extras buttons and the epithet title bar are textures too.
