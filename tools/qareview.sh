#!/bin/sh
# qareview.sh: visual-QA verdicts with codex (read-only), one codex run per qa_gate chunk (Orca workers have no
# subagents). Brief: docs/visual-qa-brief.md. Each chunk's EN sheets go in with the tour_jp sheet of the same id.
#   python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" todo work/qa/manifest.tsv work/qa/verdicts --size 8 --out-dir work/qa/chunks
#   sh tools/qareview.sh work/qa/chunks work/qa/verdicts [PARALLEL=3]
# Writes <verdicts>/<chunk>.tsv (only "id<TAB>ok|issue<TAB>note" lines kept) and <verdicts>/raw/<chunk>.log.
chunks=$1; out=$2; par=${3:-3}
mkdir -p "$out/raw"
brief=$(cat docs/visual-qa-brief.md)
for c in "$chunks"/chunk_*.txt; do
  n=$(basename "$c" .txt)
  set --
  list=""
  i=0
  while IFS="$(printf '\t')" read -r id path; do
    [ -n "$id" ] || continue
    i=$((i + 1)); set -- "$@" -i "$path"; list="$list
image $i = English sheet, id $id"
    jp=$(echo "$path" | sed 's|work/qa/tour/|work/qa/tour_jp/|')
    if [ -f "$jp" ]; then i=$((i + 1)); set -- "$@" -i "$jp"; list="$list
image $i = original Japanese ROM, same case as $id (reference only, no verdict)"; fi
  done < "$c"
  prompt="$brief

Attached images, in order:$list

Give one verdict line per English sheet id, nothing else."
  (codex exec -s read-only --skip-git-repo-check -o "$out/raw/$n.txt" "$@" -- "$prompt" > "$out/raw/$n.log" 2>&1
   grep -P '^[^\t]+/sheet[^\t]*\t(ok|issue)\t' "$out/raw/$n.txt" > "$out/$n.tsv"; echo "done $n $(wc -l < "$out/$n.tsv") lines") &
  while [ "$(jobs -r | wc -l)" -ge "$par" ]; do sleep 5; done
done
wait
echo all done
