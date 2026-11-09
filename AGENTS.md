# Yggdra Unison: Seiken Buyuuden (NDS) English translation

Skill: translate-retro-game; `python tools/skill.py` prints its folder. Read its SKILL.md before ROM, text or QA work. `"$(python tools/skill.py)"` works in bash and PowerShell; never paste a `plugins/cache/<hash>` path.

## Commands (run from repo root)
- Build:    `python -X utf8 tools/build.py`        -> build/yggdra_en.nds (checks the dump against `rom.sha1` first)
- Marker:   `python -X utf8 tools/build.py --marker` -> build/yggdra_marker.nds (ids for every line; `tools/marker.py`)
- Check:    `python -X utf8 tools/check.py`  (tests + lint; the pre-commit hook runs this; `git config core.hooksPath tools/hooks` once per clone)
- Smoke:    `python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/yggdra_en.nds --out work/qa/smoke --route tools/routes/boot.txt --smoke`
- Warp:     `python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/yggdra_en.nds --out work/qa/warp --script tools/debug/warp.lua --var "SCENE='<scene>'" [--var FACTION=n] --frames 30000` (stops itself at the scene, shot `final.png`; vars per entry in `tools/debug/scenes.txt`, RAM map `docs/re/scenes.md`; never ask the user to play to a scene)
- All states: `python -X utf8 tools/debug/regen.py [--rom build/yggdra_en.nds] [names]` -> `work/states/<name>.dst` + `work/qa/warp/sheet.png`; rerun after code/font/graphics changes
- Release:  `python -X utf8 tools/release.py` (xdelta patch + verify; never publish without the user)
- Clean:    `python -X utf8 tools/clean.py` (published projects: lists rebuildable/downloadable files; `--yes` deletes)

## Paths
- Original ROM: `rom/yggdra.nds` (gitignored; SHA-1 in `rom.sha1`, checked by `tools/check_rom.py`). Emulator: DeSmuME QA fork in `tools/desmume/desmume-qa/` (release `qa-2`, `gh release download qa-2 -R minhnhattonthat/desmume`; gitignored; GUI settings in `tools/emu-config/`). Savestates: `work/states/`.
- Text: `script/`. Tables: `tbl/`. Glossary: `glossary.md`. RE notes index: `docs/re/README.md`. Fonts and their licences: `docs/fonts.md`.

## Rulings
- Edit source files (.py .lua .asm .tbl .json) only with the file-edit tool; scripts here read and analyse, never `.replace()` and write back.
- Subagents: dispatch the `.claude/agents/` types (translator, reviewer, visual-qa, playtester), never general-purpose: their short tool list cuts each agent's start-up context from ~43k to ~9k tokens.
- The user's decisions, with the options and reasons: `docs/decisions.md`. Read it before asking the user anything; add each new ruling there the same session.
- Player bug reports: GitHub issues (`gh issue list --label bug`). Copy the attached save into `work/states/`, reproduce in the emulator, fix, commit with `Fixes #N`, and update `docs/status.md`.
- Names: official Atlus English names from Yggdra Union (GBA/PSP) where they exist (`glossary.md`).
- `fetch_emu.py` fails here with an SSL cert error; download emulator releases with `gh release download`.

## Status
`docs/status.md`: done, next, open bugs. Update it at the end of every session.
