# Translator brief - Yggdra Unison: Seiken Buyuuden (NDS, 2009)

You translate part of the Japanese script of Yggdra Unison (a Yggdra Union spin-off: real-time war game, a cast of
~36 generals, mostly short battle barks, duel conversations, menus and help) into English for a fan patch.
Work only on the batches named in your dispatch, one at a time in the order given, each to a passing check before
the next. Do all translation yourself; do not dispatch subagents.

## Read first
1. `docs/style-reference.md` - character voices and approved example pairs. Match this voice.
2. `build/terms_<batch>.txt` - binding glossary rows for this batch (full table in `glossary.md` if you need more).
3. `docs/synopsis.md` - who is who and where each kind of text appears.

## Input: `work/tl/<batch>.tsv`
`id<TAB>speaker<TAB>form<TAB>limit<TAB>Japanese`.
- speaker: best guess from the script bytecode (blank when unknown); usually right, sometimes wrong after a jump -
  trust the line's own speech style over it.
- form: dlg (bubble), epilogue / epithet (ending), or for system text a description of the screen it sits on
  (item name, card description, help page body...).
- limit: `142px x2` = the box is 142 px wide and 2 lines; `(composite)` = a piece the game glues to other pieces
  (keep it short; a line break only where the JP has one); `(unread)` = no screen shows it, translate plainly.
- `\n` in the Japanese is a line break in the box. Lines are in file order: neighbours give context.
- Identical Japanese lines in the same box kind were folded into one row: your English goes to every copy.

## Output: `work/tl/<batch>.out.tsv`, written with your file-write tool (not a shell heredoc)
`id<TAB>English`, every input id exactly once, same order. Write a line break as the two characters `\n`.
Plain ASCII only: straight quotes, `...`, no tabs inside the English, no Japanese or fullwidth characters. The font
has letters, digits, space and `. , ' - : ; " / % + & * ! ? ( ) ~` and nothing else (no [ ] < > _ # @ =).

## Fitting (hard limits, checked)
- Every line must fit the box's px width and line count. Letters average ~6 px (i/l 3-4, m/w 9-10), so a 142 px
  line holds ~22-26 characters; 184 px ~30-34.
- `python -X utf8 tools/batches.py wrap <id> "your English"` breaks text into lines for that id's box and prints the
  `\n` form plus px per line; `fit` does the same without re-wrapping. Use them instead of guessing.
- Fit by rephrasing tighter (contractions, shorter synonyms, reorder), never by abbreviating ("Lv.", "HP" are fine
  only where the JP uses them) and never by dropping information. If it truly cannot fit, keep the most meaning
  that fits and report `CUT: id - what was dropped`.
- System text pieces (`composite`): keep the JP's line breaks exactly where they are.

## Validate
Run `python -X utf8 tools/batches.py check <batch>` from the repo root and fix every reported id until it prints OK.

## Style
- Faithful: keep the information and order of ideas; adapt idiom, not meaning. Don't add details the Japanese doesn't
  state; don't summarise or skip. Adapt wordplay so the joke still lands (no translator notes).
- Keep the speaker audible. JP register markers carry voice and must turn into English devices, not vanish:
  old men's じゃ/のう/わし ("eh?", "sonny", "heh"), rough men's ぜ/ねぇ/やがる ("ain't", "ya", "damn", clipped
  grammar), feminine かしら/わよ/のね ("I wonder...", "you know", "dear"), archaic 拙者/そなた/ぞ (light "thee"),
  polite です/ます (no contractions, formal words). A line any speaker could have said is a mistake.
- Use names and terms exactly as in the glossary (the check enforces them). Honorifics after a name stay:
  ジルヴァ様 -> Zilva-sama, エミリオ殿 -> Emilia-dono, ミラノさん -> Milanor-san (check enforces). 陛下 -> Your
  Majesty / His Majesty, 殿下 -> Your Highness, 王女/姫様 -> Princess, お兄様/兄様 -> Big Brother / brother.
- Punctuation: 「」 -> "...", … and ・・・ -> `...`, ！？ -> `?!`, ♪ -> `~` or `!`, stretched ー -> repeated
  letters ("Nooo!"). Laughs and roars become English sounds of similar length (glossary rulings).
- Item names: the same item appears twice (system font +8, display font +C, `item name in FONT_ITEM`): translate
  both identically. Item "who can equip" lines are often jokes about the character: keep the joke.
- Help/tutorial text: clear instructions, game terms from the glossary, "you" addressing the player.
- Notes from earlier batches (reviewers): オレ様/俺様 = "the great me" everywhere (never "Inzaghi-sama", not "yours
  truly"); "dear" only for Mistel and Amareus (not Eudy or soldiers); "sonny" only for Dort; Nietzsche always speaks
  of herself in the third person; Nessiah's teasing ませんよ? -> "..., you know?" keep the question; かしら is not
  always "I wonder" (use "hmm?", "shall we?" where it is rhetorical); keep !? vs ?! as the JP has it.
- Mistakes earlier projects made (avoid): ordinal glued to a number ("1th"); a name off by one letter; stock phrases
  like "TIPS ... GET!"; a joke losing its punchline; an old man or a brat speaking neutral English.

## Consistency
Never edit `glossary.md`. For a recurring name or term not in it, pick a form, use it consistently, and report it.

## Report (reply with only this, short)
Files written and entry count; then any lines: `NEW TERM: jp -> en`, `UNSURE: id - note`, `CUT: id - note`.
