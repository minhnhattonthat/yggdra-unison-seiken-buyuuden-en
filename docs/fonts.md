# Fonts

Every font or glyph sheet the build reads ends up inside the released patch, so its licence must allow that. One row
per file; a font with no known licence doesn't go into a release.

| File | Source (URL, version) | Licence | Redistributable in a patch | Used for | Changes made |
|---|---|---|---|---|---|
| (in-game Latin glyphs + tools/enfont.py PUNCT) | the game's own FONT_* glyphs; punctuation drawn for this project | game / MIT | yes | dialogue + system VWF | outline added, shifted to column 0 |
| fonts/LiberationSerif-Bold.ttf, -Regular.ttf, fonts/LiberationSans-Bold.ttf, -Regular.ttf | github.com/liberationfonts/liberation-fonts 2.1.5 | SIL OFL 1.1 (fonts/LICENSE-Liberation.txt) | yes, as rendered pixels | texture lettering (tools/gfx.py) | none |
