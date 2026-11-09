# Text engine

## Encoding (verified: draw loop arm9 0x02012A74, tutorial text checked on screen, whole script decodes)
- Shift-JIS appears only in debug labels (`ST%02d.BIN` stage names `ＳＴＡＧＥ００` at 0x16, never drawn as far as seen) and an SJIS table at arm9 0xFD249 (pairs, not a font list); all game text is glyph-index encoded.
- **Code = glyph index in the font the screen uses.** Every font is an NTFT file: 16x16 px, linear 4bpp rows of 8 bytes, 128 bytes/glyph (same layout as a 3D 16-colour texture), palette in the matching NTFP. Ink is the low palette indices (1-3 core, up to ~8 anti-alias), 0xF border = outline. Glyphs are read from the font file per character (0x01FFACDC with offset glyph*0x80), so the dialogue font never sits whole in RAM.
  - byte `00..EF` = glyph `b`;
  - `F1..F9, xx` = glyph `(b - 0xF0) * 0xF0 + xx` (**stride 0xF0**, `mla r0, r1, #0xF0, xx` at 0x02012B00; an older note said 0x100, which shifted every code from F2 on);
  - `FC xx` = colour (xx indexes the u16 table at 0x0209281C), `FD` = new line (y += 0x11), `FF` = end. Glyph advance is 0x0B px (fixed). No other codes appear in any string; names are spelled out.
- Control inventory (`tools/text.py` layout checks): MESSAGE/SPMES/TUTO/EDMES and the system pools hold only glyph codes, FD and FF (no FC seen yet). Item names in FONT_ITEM use the same F1 xx two-byte form.

### Fonts
| Font | Glyphs | Used by (verified by decoding with each font) |
|---|---|---|
| FONT_MES.NTFT | 0x56E | MESSAGE/SPMES/TUTO (tutorial on screen) |
| FONT_SYSTEM.NTFT | 0x398 | arm9 string pools, ov9_03 (help), ov9_05, ov9_15/16/19 (save, card prompt). Loaded at boot, sits in RAM at 0x0212E840 |
| FONT_END.NTFT | 0x582 | EDMES, ov9_02, ov9_06 (extras), ov9_07 (character profiles), ov9_18 (unlocks). First 697 glyphs = FONT_SYSTEM |
| FONT_ITEM.NTFT | 0x14A | bold display font, no fixed kana block (custom order). Used by the item names at field +C of the 225 item records (below). Read by aligning each record's FONT_SYSTEM name (+8) with its FONT_ITEM name: 328 of 330 glyphs, no conflicts (0x0D 開, 0x0F ず from the 4 records found later); 0x11A (unused by any record) and 0x149 (blank) left unread. Table `tbl/jp_item.tbl` |
| FONT_8X8.NTFT/.LTFT | - | debug / small labels (unread) |
- Glyphs 00-EB are the same in all three text fonts (MES, SYSTEM, END): 00-4F hiragana, 50-9F katakana with ヂ ヅ slots holding `・` and a blank, A0 ヴ, A1 ー, A2-AB 0-9, AC-C5 A-Z, C6-DF a-z, E0-EB `!?♪~「」()…—。、`. Kanji from EC differ per font (MES: order of first use 下 行 私 神...).
- **Kanji readings: done** (1,770 bitmaps, `tbl/kanji.tsv` keyed by bitmap hash, so a reading fills every font with the same pixels). Read by eye from `tools/kanji.py todo` sheets, look-alikes checked with `tools/kanji.py ctx`/`dupes`, then `tools/kanji_check.py` (janome tokenizer) flagged kanji never inside a dictionary word and unknown compounds: ~45 misreads fixed that way (選/遥, 願/顔, 賛/貿, 滅/減, 熟/熱...). Remaining risk: FONT_SYSTEM/END glyphs no script line uses were read without context.
- Fonts hold some kanji twice (e.g. 盗, 遣, 為); `tools/mkjptbl.py` writes the later copies with a variation selector (U+FE00+) so jp shows the char and still round-trips. Tables: `tbl/jp.tbl` (MES), `tbl/jp_sys.tbl`, `tbl/jp_end.tbl`, all generated.

## Text files (DATA.SFS, raw, not compressed)
| Files | Count | Bytes | Layout |
|---|---|---|---|
| MESSAGE000-220.BIN | 221 | 371 KB | bytecode script (below); 7,920 strings. MESSAGE000 = test file (あいうえお lines) |
| SPMES%03d%03d.BIN, SPMES_APP00-02, SPMES_TRE, SPMES_WR | 407 | 221 KB | bytecode script; 3,348 strings. SPMES_WR builds sentences from fragments (place name + 「にて、」 + event): translate as a set |
| TUTO00_*, TUTO01_* | 28 | 9 KB | bytecode script; 214 strings |
| EDMES%02d.BIN | 38 | 30 KB | `u32 id, u32 n, u32 table_off`, n x u32 -> 8-byte records `(u32 str, u32 str)` (0 = none), strings FF-terminated after the records; 612 strings (ending epithets "ナマクラ聖剣士ラッセル" + epilogue paragraphs). **verified**: every string start is referenced by a record, nothing else |
| P04..P50.BIN | 18 | - | battle map data (opened with P%02d.PACK/.BI); FF-runs in them are not text |
| ST00-89.BIN | 90 | - | stage data; only an SJIS debug label |

## Bytecode script files (MESSAGE/SPMES/TUTO) - verified by coverage
- Header: `u32 ?` (0/1/file id), `u32 n`, `u32 table_off` (0xC), then n x u32 entry offsets into the bytecode (event entry points; each entry ends with opcode `01`). Bytecode follows; strings follow the bytecode, FF-terminated, to EOF (zero padding allowed).
- Strings are referenced only by absolute file offsets in two opcodes:
  - `30 xx <u32 off>` (xx = 00/01): show message.
  - `51 <u32 off>`: string argument (SPMES_WR fragment table; 105 refs).
- `tools/text.py` layout checks (run by tests/test_text.py on every commit): every `30`-ref lands on a string start, every string (except MESSAGE000's unused test line at 0xA78) is referenced, no data after the last FF; re-laying each file from its decoded strings gives the file back. Other opcodes seen (lengths from examples, unverified): `33` 9 B, `35` 3 B, `36` 7 B, `39` 1 B, `20` 1 B, `44` 8 B, `55` 2 B, `01` end.
- **Insertion:** `text.rebuild(name, bytes, new_strings)` re-lays the string area (the file can grow, DATA.SFS is rebuilt) and rewrites the u32 of each `30`/`51` ref (EDMES: each record field). Bytecode and entry table do not move.

## System text (arm9 + overlays) - extracted to script/system/<image>.json
- FF-terminated, 00 padding between strings (a string may itself start with 00 = あ: pointer targets are kept as starts).
- Referenced by absolute u32 pointers: arm9 strings at 0x02000000+off (pointers in arm9 or any overlay), overlay strings at 0x0211B780+off (all 20 overlays load there; pointers only from the same overlay).
- **Pools** (`text.POOLS`, image, range, font): arm9 0x8F980-0x9281C (0x8F980-0x8F98B = one-glyph strings ・ … P,
  missed until 2026-11-10 by the >= 2-code filter; ov9_06 0x3ED4 — likewise; ov9_18 0x3734 "0" = A2 FF before struct
  bytes 0x3736-0x373F, left out: A2 is 0 in the English font too) and 0x92830-0x95C09 (1,389 strings: unit/class/item/card names, effects, help; 0x958EC-0x95C08 = 6 explore help pages pointed at from ov9_13, found by `jp_left.py --slots` (tools/ptrslots.py) on the marker build; the "NDS YGZ ver 1.00" tag follows), ov9_02 (2 pools, END), ov9_03 (help menu, 2 pools), ov9_05 (card error), ov9_06 (extras, END, 2 pools), ov9_07 (character profiles, END), ov9_15/ov9_19 (save prompts; a few struct bytes before the first string excluded), ov9_16 (card prompt), ov9_18 (unlock messages, END). Found by `tools/systext.py` (pointer scan) + a packed-run walk; every other pointer hit (285, mostly arm9 code < 0x8F000 and data tables at 0xA1000-0xA8FFF, 0xF5000-0xFFFFF, 0x100648) decodes as noise and is not text.
- JSON rows carry `ptrs` (every aligned u32 pointing at the string; some are false positives from data tables, e.g. arm9 0xA7xxx hits mid-string) and `max` (bytes in place incl. FF + trailing padding).
- **Item records** (`text.ITEM_RECS`): arm9 0x100640, 225 x 0x18 bytes (record 0's +0..+7 overlap the tail of "CNAMEB%03d"; the first 4 were missed until phase 5 session 7, their FONT_ITEM names had been decoded as system-font kana noise): +0/+4 stats, +8 name (FONT_SYSTEM), +C the same name in FONT_ITEM (each pointed at only from here; these were the "noise" strings), +10 effect, +14 who can equip. Rows at +C targets have `"font": "item"` in arm9.json (220 + one below); the item name and its +C twin must be translated alike.
- **Non-text inside a pool** (`text.POOL_DATA`): arm9 0x8F9C0, 4 bytes `0C 0C 0B 0C` read by code (literals at 0x12FF0/0x130A8), with no FF of its own: the item name ドゼウ at 0x8F9C4 follows it, so an FF split merged them. Skipped, not a row. Every other pointer that lands mid-string is a false positive (data tables at 0xA7xxx, odd addresses).
- **Kanji misreads fixed from system context** (item and help text, read without context before): 癒 録 塊 錆 勲 叉 響 冑 脈 穀 議 掴 籠 獪 男 卿 縛 劣 触 徴 箇 謎. Left as the game wrote them: 慚悔 (for 懺悔), 英雌 (coined, Yggdra), 順ずる.
- **Insertion / relocation (done, tools/sysreloc.py):** a string that fits `max` stays in place; a longer one goes
  into the EXTRA block, a new arm9 autoload section at main RAM 0x02123460 (= the overlay slot end, ov9_13, = the
  original main arena lo), deduplicated, and every pointer in `ptrs` is rewritten (asserted to hold the old
  address). `engine.patch_arm9(arm9, wtab, extra)` raises OS_GetInitArenaLo's literals (arm9 0x02025000 switch:
  main at 0x02025088, ITCM at 0x02025094, which also covered our hooks at 0x01FFBDC0) past what we add. Proven:
  the marker build relocates all 1,625 system strings (39 KB block), boots, and reaches all 35 warps. Other free
  RAM: every overlay but ov9_13 can grow up to 0x02123460 (bss turned into zeros, like the ITCM block).

## Draw routines (arm9, verified by disasm + marker build on screen)
- **Dialogue text object** `0x020128B8` (callers 0x02006324, 0x02006F78; FONT_MES): counts glyphs (0x02013274, also
  per-line counts for 2 lines at obj+0x2D), allocates per-glyph x/y/colour/alpha u16 arrays (obj+8/+C/+10/+14), then
  per glyph seeks/reads the 0x80-byte glyph from the font file (0x01FFACDC / 0x01FFAF1C) into the next **glyph slot**
  and stores x (obj+0x24, +0x0B per glyph) and y (obj+0x26, +0x11 per FD). Quads drawn per frame by 0x02012560..0x0201278C
  (`mov r3,#0xC` = quad width 12).
- **System text runs** `0x02012DCC` and **centred text** `0x020130AC`: queue glyph codes (`code | font << 12`) in the
  pool at 0x0210E768 (+0 glyph buffer, +4 codes, +8 capacity, +0xA used), then 0x02012C10 draws a run, x += font
  advance - 1. Advance per font id at arm9 0x0208F9C0 = `0C 0C 0B 0C` (the POOL_DATA block). Centring = 0x80 - 11*n/2.
- **Font ids**: 0 SYSTEM, 1 MES, 2 ITEM, 3 END (name table 0x020F7BB4).
- **Glyph slots (verified, tools/lua/glyphslots.lua):** each scene sizes the pool at 0x0210E768 for the Japanese: the
  ending (scene 18) has capacity 176, slots 0-31 reserved, dialogue objects start at slot 144 (u16 0x0210E7BA) = **32
  glyphs per dialogue**. One glyph per letter overflowed it and hung the ending (marker build, MESSAGE16x/17x).

## English font + VWF (phase 5, tools/enfont.py + tools/engine.py; verified on screen in the marker build)
- English reuses the game's Latin glyphs (A2-AB digits, AC-DF letters, E0 ! E1 ? E3 ~ E6/E7 ( ) E8 … E9 —) and adds
  ASCII punctuation in rare kana slots: 8A space (game blank), 39 . 3A , 47 ' 48 - 49 : 4A ; 4B " 97 / 98 % 99 + 9A & 9B *
  (`tbl/en.tbl`, generated). No [ ] < > glyphs. Every English glyph is shifted to column 0; advance = outline width - 1.
  The same glyphs go into all four fonts (FONT_ITEM palette-mapped: its outline is index 1; look not checked yet).
- Hook code + tables sit after the ITCM block's bss (0x01FFBDC0..0x01FFC6A0; ITCM data grows, bss 0, see engine.py):
  width table 4x256 (advance per font id, 0 = game advance), vtab 256 (visible px, FONT_MES), state, glyph buffer.
- **Dialogue = packed cells**: `cells_count` replaces the glyph count at 0x02012904 and `glyph_cell` the per-glyph
  path at 0x02012B0C: each line is blitted into 16 px cells (a cell opens only when a glyph's visible pixels reach it),
  quads widened to 16 (0x02012784). Slots used = sum over lines of ceil(px / 16), fewer than the Japanese used for the
  same width, so every scene's slot budget holds as long as a line fits its box. Typewriter reveal runs per cell.
- **System/centred text = packed cells too** (`pack_run` / `pack_ctr` replace 0x02012DF4 / 0x020130AC whole): each
  segment (text up to FD / FC / FF) is blitted into 16 px cells at VWF pen x, every block from 0 to the last one
  reached gets a slot, then 0x02012C10 draws them (`hook_step` steps 16 and `hook_qw` at 0x02012D08 widens the quad
  to 16 for a packed cell). The game redraws system text every frame and caches a slot by `codes[slot] == glyph`;
  a packed slot gets `codes[slot] = 0xC000 | key & 0x1FFF` (above every game code and every key 0x02012130's
  glyph search uses) plus a full 32-bit key in `slotkey[slot]` (FNV over code, font, x in the cell), so a cell is
  re-blitted only when its content changes. Slots past the pool capacity (+8) are not drawn (the original overran
  the pool and crashed). FC xx sets the colour and the line goes on at the real px. Return value = ceil(px / 11)
  (0x0201038C sizes a highlight bar as 11 x that). Single glyphs (0x02012FFC, EDMES) keep one slot each.
- **EDMES paragraphs** (ov9_15 0x0211DC88 -> 0x02012FFC, one glyph per call, x += 11 by the overlay): `ov_adv` hook
  at 0x0211DC8C (engine.OV_SITES, patched per overlay in build.edits). Only caller of 0x02012FFC. Budgets: windows.md.

## Not text (graphics)
- The title prologue scroll, faction names/banners, character name plates (CNAME*), card names (CARDNAME*), epilogue titles/messages (EPI_TIT_/EPI_MES_) and more are textures: see `graphics.md`.
