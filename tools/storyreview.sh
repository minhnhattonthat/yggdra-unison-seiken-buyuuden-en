#!/bin/sh
# storyreview.sh: story-pass reports with codex (read-only), one codex run per chapter (Orca workers have no
# subagents). Brief: docs/story-reviewer-brief.md. Chapters: tools/chapters.py + qa_gate.py init (see its header).
#   sh tools/storyreview.sh [PARALLEL=3] [CHAPTER ...]     (default: every chapter qa_gate todo lists)
# Writes work/qa/story/reports/<chapter>.md and work/qa/story/verdicts/<chapter>.tsv ("chapter<TAB>ok|issue<TAB>note").
par=${1:-3}; shift 2>/dev/null
cd "$(dirname "$0")/.." || exit 1
rep=work/qa/story/reports; ver=work/qa/story/verdicts
mkdir -p "$rep" "$ver"
if [ $# -eq 0 ]; then
  set -- $(python -X utf8 "$(python tools/skill.py)/scripts/qa_gate.py" todo work/qa/story/manifest.tsv "$ver" --size 1 2>/dev/null \
    | grep -v '^#' | cut -f1)
fi
brief=$(cat docs/story-reviewer-brief.md)
for ch in "$@"; do
  prompt="$brief

Dispatch: chapter file work/qa/story/chapters/$ch.txt (read all of it, in parts). Also read docs/synopsis.md,
docs/style-reference.md and glossary.md. Speaker tags are a byte-scan hint and can be wrong after jumps; lines
in one file are alternatives the game picks from (attacker, win, loss, death), not one conversation, so judge
voice and consistency per character rather than line-to-line flow. The last line of your report must be
'Assessment: ok' or 'Assessment: issue - <one sentence>'."
  (codex exec -s read-only --skip-git-repo-check -o "$rep/$ch.md" -- "$prompt" > "$rep/$ch.log" 2>&1
   a=$(grep -iE '^[#* ]*Assessment' "$rep/$ch.md" | tail -1)
   case "$a" in
     *issue*) printf '%s\tissue\t%s\n' "$ch" "$(echo "$a" | sed 's/^[^-]*- *//')" > "$ver/$ch.tsv" ;;
     *ok*) printf '%s\tok\tcodex story pass\n' "$ch" > "$ver/$ch.tsv" ;;
     *) echo "no assessment in $rep/$ch.md" ;;
   esac
   echo "done $ch: $a") &
  while [ "$(jobs -r | wc -l)" -ge "$par" ]; do sleep 5; done
done
wait
echo all done
