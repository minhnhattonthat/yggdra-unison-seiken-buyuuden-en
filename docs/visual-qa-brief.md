# Visual-QA reviewer brief - Yggdra Unison: Seiken Buyuuden (NDS)

You review contact sheets from a translated build's QA tour and give each one a verdict. Read-only on everything
except your one verdict file: no edits to the repo, no git, no subagents. (Orca workers can't start subagents:
`tools/qareview.sh` runs this brief through `codex exec -s read-only`, one run per chunk, and the verdict lines are
its final message.)

## Inputs
- A chunk: sheets of the English build (`work/qa/tour/<case>/sheet*.png`, id = `<case>/sheet..`), each followed by
  the original ROM's sheet of the same case (`work/qa/tour_jp/...`) when one exists. Each tile is one frame: the DS
  top screen above the bottom screen (256 x 384). Tiles run left to right, top to bottom, in time order.
- `glossary.md` for names.

## Judge
An `issue` is any of:
- Japanese still visible (kana/kanji) in the English sheet;
- text overflowing a box, clipped by a frame, or running off screen;
- text off-centre where the original centres it: an option in its selection box, a label, a bubble;
- garbage tiles, wrong or missing glyphs, a strike or stray pixels across letters;
- broken line breaks: a word split mid-line, a page ending mid-sentence, a one-word last line;
- an empty box where text belongs;
- a name that differs from `glossary.md`.

Standing non-bugs, `ok`:
- text still typing out, a box mid-fade or mid-scroll, black or half-faded frames between scenes;
- a map or scene still loading after a warp;
- anything identical in the original's sheet (including English the original already had: GAME OVER, ENTRY OK!,
  Touch, TIME, staff roll, logos);
- lowercase p and q drawn as small capitals ("exPand", "ExPanding"): the English font has no descender room;
- a frozen battle screen with the "Touch" prompt: the battle waits for a touch;
- the vertical "Occupation" art on the territory screen's left edge.

## Verdicts
One line per English sheet id: `id<TAB>ok|issue<TAB>what and where` (for an issue: which tile, which text, what is
wrong). Output only these lines.
