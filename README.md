# Yggdra Unison: Seiken Buyuuden English translation

Unofficial English fan translation of **Yggdra Unison: Seiken Buyuuden** (ユグドラ・ユニゾン 聖剣武勇伝; Nintendo DS,
Sting, 2009): the source text and tools
that build the patch.

**Just want to play?** Download the patch from [Releases](../../releases) and follow its README. This repository holds
no game data you can play; you need your own dump of the Japanese game.

**Found a bug?** [Report it](../../issues/new/choose): untranslated text, typos, overflow, crashes. Attaching a savestate
helps most.

## Translation status

| Part | Status |
|---|---|
| Battle barks, duel events, prisoner / reward talk, tutorial | Translated |
| Menus, items, cards, skills, help, system messages | Translated |
| Prologues, faction intros, rumors, banners, HUD and menu graphics | Translated (redrawn textures) |
| Endings: epithets, epilogues, Hall of Fame, credits | Translated |
| Name entry | None in the game |

Names follow Atlus's English Yggdra Union where one exists (`glossary.md`).

Known issues (cosmetic; see also [Issues](../../issues)): some labels in small fixed cells are squeezed or short
("Btl / KO / Kill" on the record page, "Land" / "Gear" in Unit Info, battle HUD army names at 8 px); a few 6-px labels
inside the tutorial's illustration shots stay Japanese (illegible at that size in either language).

## What's here

| Path | What it is |
|---|---|
| `script/` | Every text block: original Japanese and English. Translation fixes go here. |
| `glossary.md` | Binding names, terms and style rules. |
| `tools/` | Python build chain: extract, insert, lint, release. |
| `tests/` | pytest suite (ROM-dependent tests skip when the ROM is absent). |
| `docs/re/` | Reverse-engineering notes. |
| `docs/decisions.md`, `docs/status.md` | Rulings with their reasons; current progress and open bugs. |
| `docs/fonts.md` | Fonts used and their licences. |
| `AGENTS.md` | Instructions for coding agents (`CLAUDE.md` points to it). |
| `.claude/agents/` | Subagent types (translator, reviewer, visual QA, playtester) with only the tools each needs. |

## Build your own patched ROM

Needs Python 3.12+ and your own dump of the Japanese game.

```sh
git clone https://github.com/minhnhattonthat/yggdra-unison-seiken-buyuuden-en
cd yggdra-unison-seiken-buyuuden-en
# copy your dump to: rom/yggdra.nds  (No-Intro "Yggdra Unison - Seiken Buyuuden (Japan).nds")
#   (33554432 bytes, CRC32 B077FF01, MD5 63270f61c87f5f558f7ac3e63e495956,
#    SHA-1 ef4d5e4fe56f9a0d3d114c0bd395db20d8dcb7f5; the build refuses any other dump, see rom.sha1)
python -X utf8 tools/build.py                          # -> build/yggdra_en.nds
python -X utf8 tools/check.py                          # tests + text lint
```

## Support

If you enjoy this translation, you can support my work on Ko-fi:

[![Support me on Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/minhnhattonthat)

## Licence

Tools and English translation: MIT. The original Japanese text in `script/` is Sting's and is included only so
the translation can be checked against it. Yggdra Unison: Seiken Buyuuden is (c) Sting; this project is not affiliated with them.
Do not share patched ROMs.

The translation was made with extensive AI assistance (Claude by Anthropic). Corrections are very welcome.
