#!/bin/sh
# gfxreview.sh: independent read-only review of graphics-sweep pages with codex (one codex run per chunk of pages).
#   sh tools/gfxreview.sh work/gfx/sweep work/gfx/review [CHUNK=10] [PARALLEL=4]
# Writes <out>/chunk_NN.tsv: page, label, JP|EN|MIXED|NONE, text read, what it is. Reviewers see only the images.
src=$1; out=$2; chunk=${3:-10}; par=${4:-4}
mkdir -p "$out"
ls "$src"/*.png | sort > "$out/pages.txt"
split -l "$chunk" -d -a 2 "$out/pages.txt" "$out/list_"
prompt='You are reviewing contact sheets of game textures from a Japanese Nintendo DS game (Yggdra Unison) for a fan translation. Each attached image is one sheet; each texture on it has a small yellow label (its file name) above it. For EVERY texture that contains any readable text, output one line: <sheet file name><TAB><label><TAB><JP|EN|MIXED><TAB><the text as you read it, kana/kanji exactly, "?" for unreadable><TAB><short description: name plate, menu label, banner, card name, title, font sheet, etc>. A texture whose glyphs are a font sheet (many single characters in a grid) is "font sheet". Do not list textures without text (portraits, art, effects, icons with no letters); after the lines, add one line per sheet: <sheet><TAB>*<TAB>NONE<TAB><count of textures with no text><TAB>-. Output only these TSV lines, no prose. Read carefully: small text counts.'
for l in "$out"/list_*; do
  n=${l##*_}
  set --
  for f in $(cat "$l"); do set -- "$@" -i "$f"; done
  (codex exec -s read-only --skip-git-repo-check -o "$out/chunk_$n.tsv" "$@" -- "$prompt" > "$out/chunk_$n.log" 2>&1; echo "done $n $?") &
  while [ "$(jobs -r | wc -l)" -ge "$par" ]; do wait -n 2>/dev/null || sleep 5; done
done
wait
echo all done
