# Graphics text survey

All screen graphics are **NDS 3D textures** in `.PACK` files (DATA.SFS; format in `sfs.md`): texels + BGR555 palette +
4x4-compression index data. 1,863 of 2,497 are 4x4-compressed, the rest 2/4/8 bpp paletted. The width is not in the
PACK; `tools/tex.py` guesses it (power of two with the smoothest row joins), which was right on every text texture
seen. Fonts for runtime text are separate (`FONT_*.NTFT`, see `text.md`) and are text work, not graphics.

## How the survey was made
- **Static sweep (all of it):** `python tools/gfxsweep.py --packed --out work/gfx/packed` renders every named PACK and
  every PACK-shaped file in `work/sfs/_unk/` (2,497 rendered; 16 `_unk` files skipped as not-PACK, listed in
  `work/gfx/packed/skipped.tsv`) into 29 labelled pages, `index.tsv` maps file -> page. All 29 pages were read
  (2026-11-09; art-only pages at half size). Per-prefix pages: `python tools/gfxsweep.py` (work/gfx/sweep).
- **Not yet decoded right:** textures with 1-5 colour palettes render as noise/magenta (alpha formats A3I5/A5I3, or 2bpp
  with a different palette layout): CS_MA_00-35, CLEARNESS, EPI_FLAG00-11, IMPACT00-35, ITEM_WINDOW, OP_EFFECT,
  PRISONER, PRIZE, QUEST, TERAFONTTGA, TR_TGA, TR_TGA2, TUKOKU_TGA, WARRESULT, WR_TGA. Most are masks/effects; QUEST,
  PRIZE, PRISONER, *_TGA and WARRESULT show text-like strokes: **check each on screen** (phase 2 debug tool) and add
  rows below if Japanese.
- **Tour:** boot-to-title only so far (`work/qa/open1`, `work/qa/tit`). Runtime file names: `tools/lua/fileopen.lua`.

## Japanese graphics (to translate; D5: all of it)
Counts are files. "atlas" = many labels packed in one texture (needs the layout: `.BI` or code-side rects).

| Group | Files | What | Notes |
|---|---|---|---|
| TIT_LOGO, SAVE_BG0, TU_T01_00, several `_unk` logo variants | ~6 | title logo: ruby ユグドラ・ユニゾン + ~聖剣武勇伝~ under the English "Yggdra Unison" | D5: no official English title for this game; keep "Yggdra Unison", replace ruby + subtitle (e.g. ~Legend of the Holy Sword~) |
| OP_WR | 1 | opening prologue scroll (~26 lines) | tall 256-wide texture |
| OPK_WR_00-11, MS_PRO_000-011 | 24 | faction-select descriptions (7 lines) and faction prologues (10-14 lines) | |
| MS_M_00-11, MS_N_00-36 | 49 | faction / territory descriptions (2 lines) | |
| IN_PRO_000-011, TM_M_00-11, EVSFORCE00-11, ED_H_90928/91928/92928 | ~40 | faction and force names (~新生ブロンキア帝国~, 帝国軍 ...) | |
| WD_N_00-36 | 37 | world-map place names (ブロンキア城 帝都フレアヴェルク ...) | names per glossary |
| CN_M_00-11, CN_N_00-36, CNAMEA00-71, CNAMEB000-254, CNAMEC00-71 | ~270 | character / class name plates (1-line, 2-line title+name, tiny strips) | CNAMEC is 2bpp |
| CARDNAMEA00-35, CDS_000-035, CS_M_00-35, CDSEL_MAT, CDSKILLFNT0/1 | ~110 | card names (small), card description panels, card effect one-liners, 未鑑定カード選択, カードスキル発動 / カード鑑定 | CARDNAMEB is already English |
| IT_EF001-225 | 225 | item effect one-liners (HPが徐々に回復 ...) | 2bpp |
| ED_N_000-375, ED_H_030-375 | ~310 | ending epithets (ナマクラ魔剣士ラッセル ...) | same wording as the EDMES title strings: translate once, use for both |
| EPI_TIT_00-11, EPI_MES_00-11, EPI_WAKU0 | 25 | epilogue titles, epilogue paragraphs (8-10 lines), 全土統一 frame label | |
| `_unk` war-event textures (~120, hashes in index.tsv) | ~120 | war-event titles (蛮賊団、支配領域拡大! ファンタジニア王国侵攻戦 ...) and story paragraphs; カード選択 banner | done (session 20) as `_unk_<hash>` rows; titles 256 x 24, paragraphs 256 x 240 (war report: other factions' wars); not seen on screen yet |
| `_unk` 0addeae8_01421 | 1 | credit line 制作・著作 株式会社スティング | rest of credits (STAFFROLL) is English already |
| SHOOTNAME00-11,99, WR_SHN00-05, WR_FONT, EVSFONT00-17, EVSFONTSB00-07, BATTLEOUT1-3, SELSORTIE, TERAGGFONT | ~55 | phase banners (勢力選択 カード選択 出撃先選択 戦況報告 探索 ...), war report (戦争勃発 占領成功 ... 疫病発生, 勝利 敗北), event goals (が都市を制圧 ... タイムオーバー), battle outs (戦線離脱 敵兵退却 敵兵戦死), 選択ユニット出撃! | |
| OBJSTR00-13 | 14 | map-object help panels (title + 3 lines) | |
| BTLFONT, BTLMN_FONT, BUTTON, SYSTEX, SYSTEX2, FORSEL_FONT, SAVE_FONT, SEN_FONT, TREFONT, TEND_FONT, TR_FONT, TUKOKU_FONT, TUTO_FONT, GMOVERFONT, EXTRA_FONT, ENETREFONT, HELP_MAT, OP_FONT, PRO_FONT, PRIZE_FONT | 20 | UI label atlases (menus, battle HUD, buttons, save/load, explore, turn end, game over, extras, prisoner, help) | atlas: needs the label rects before redraw |
| TU_C01_00-TU_C17_00, TU_T01_00-TU_T11_01 | ~57 | tutorial screenshots with baked Japanese (UI, tables, dialogue) | session 21: labels overlaid in gfx/text.tsv (40 shots; the rest have no Japanese), boxes from `tools/inkrects.py` / zoom-4 crops (px / 4); dialogue = the script's own English |

## Already English (no work)
STAFFROLL00-14 (credits), B_GAMECLEAR/B_GAMEOVER/B_START, BEGIN, BEATOUT, CARDNAMEB00-35, CI_ATLOGO, CI_STLOGO,
CONF_TAG, CRITICAL, DLT_ATTACK/DLT_CLEAR, END_CONG, ENEUNIT, EPI_MAT ("Fin."), FAIL, GMOVERBG, GUARD, INPUTOK,
KILLOUT, OP2_FONT, PLYUNIT, PRO_AFT, SEN_BG0/1, SMASHHIT, STCANCEL, SUCCESS, TIT_FONT, TOUCH, UNISON, EXTRA_SOUND,
CAUTION/CHECK/NOTICE (`_unk`).

## Art, no text
BTLBG*, BUST*, EPI_BUST*, FACE*/FACEALL/FACEEVE/FACEUP/FACEHOL, FLAG*, FS_FLAG*, FMAP_*, WD_00-67, WORLDMAP_A/B, P04-P50
(unit sprite sheets), MUNIT*, ICON*, ICON_ITEM, ICD_*, EV_BG*, EVESIMG*, SHOOTIMG*, TREBG*, OBJIMG*, OP*FIRE*, OP_BG*,
TIT_BG0/1, ST_BG*, STSORBG*, CDSKILLBG*, MSGFRAME, DMGFRAME, etc. ED_NESIA and ICON18-20 have small lettering-like
marks: confirm on screen.

## Pipeline (phase 8, session 14: works in game, SHOOTNAME00 "Faction Select" seen at faction_select)
- `gfx/text.tsv` (NAME, English, options) -> `tools/gen_gfx.py` draws gfx/NAME.png (clears the original's text bbox
  or `box=`, Liberation font from fonts/, fill = per-row brightest colour of the original, outline = its darkest,
  binary alpha) -> `tools/gfx.py` encodes into a PACK with the original palette untouched (4x4: best palette
  offset + mode per block; paletted: nearest colour), parts raw, flags 0x100 -> build.py `repl`.
  `gfx.py check` writes the re-decoded result to work/gfx/enc/ (look at that, not gfx/). romcheck: a changed PACK
  must equal the encode of its gfx/ PNG. tests/test_gfx.py: an unedited decode re-encodes pixel-identical.
- The game tints some textures itself (the SHOOTNAME banner shows white texels as a yellow gradient).
- Unnamed files are `_unk_<hash8>.PACK` (text.sfs_files; sfs.name_hash reads the hash back), so gfx/text.tsv,
  gen_gfx, gfx.py and build take them like named ones (session 20: 60 war-event titles + 60 paragraphs, credit
  line, カード選択 banner, 3 logo variants, a town label). Not handled yet: textures needing a new palette.

## Edit plan (phase 5+)
- Re-encode: 4x4 compression encoder needed (or switch a texture to a paletted format only if the loader reads the format
  from data, not from code - check the texture params at the load call). Paletted/2bpp ones re-import directly.
- Most text textures are text on a flat panel: render English with a committed OFL font (`docs/fonts.md`), 4x4-encode,
  keep each texture's size.
- Same text twice: ED_N/ED_H vs EDMES strings; faction/place names in textures vs system strings; logo in TIT_LOGO,
  SAVE_BG0, tutorial and `_unk` variants.
