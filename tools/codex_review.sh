#!/bin/sh
# codex_review.sh bA bB: independent review of two translated batches with `codex exec` (read-only), then a
# second codex session as translator applies the findings to work/tl/bA.out.tsv bB.out.tsv until check is OK.
# Reports: work/qa/review/bA-bB.{review,fix}.md. Used when no reviewer/translator subagent can be dispatched.
set -e
cd "$(dirname "$0")/.."
A=$1; B=${2:-$1}; P=work/qa/pairs/$A-$B.txt; R=work/qa/review/$A-$B
mkdir -p work/qa/review
[ -f "$P" ] || python -X utf8 tools/pairs.py $A $B >/dev/null
REP=""; for b in $A $B; do [ -f work/tl/$b.report.txt ] && REP="$REP work/tl/$b.report.txt"; done

codex exec -s read-only --skip-git-repo-check -o "$R.review.md" "You are a read-only translation reviewer. Read docs/reviewer-brief.md and follow it for the pairs file $P (read ALL of it). Also read glossary.md and docs/style-reference.md; translator reports (unverified):${REP:- none}. Edit nothing. Your final message is the report in the brief's format. Keep it compact: every Critical and Important finding with its id; Minors only if clearly worth it, at most 15, one line each. Known flags to check: Temple Knight for 聖騎士; Duchy of Embellia for エンベリア公国; Bly for ブライ; Brongaa for ブロンガ; 'dear' only for Mistel and Amareus (never Eudy or soldiers); speaker tags can be wrong (Ortega/Dort swapped in MESSAGE210-219; Emilia uses ボク) - judge by the line's style; 戦意 = morale in system text." </dev/null >"$R.review.log" 2>&1
[ -s "$R.review.md" ] || { tail -2 "$R.review.log"; exit 1; }  # codex exits 0 on a usage-limit error

codex exec -s workspace-write --skip-git-repo-check -o "$R.fix.md" "You are the translator for batches $A and $B. Read docs/translator-brief.md (style, fitting, validation rules), glossary.md and docs/style-reference.md. Then read the review report $R.review.md and the batch inputs work/tl/$A.tsv work/tl/$B.tsv. Apply every Critical and Important finding, and each Minor you agree with, by editing ONLY work/tl/$A.out.tsv and work/tl/$B.out.tsv (keep the id<TAB>English format, \\n as two characters, plain ASCII). If you disagree with a finding, leave the line and say why. Run: python -X utf8 tools/batches.py check $A $B and fix until it prints OK for both (EDMES epithet LONG lines in b071 may stay LONG: report them). Edit no other file, no git. Final message, short: FIXED: id - what changed (one line each); REJECTED: id - why; MINOR LEFT: id - note (Minors not applied, one line each); then the last line of the check output." </dev/null >"$R.fix.log" 2>&1
python -X utf8 tools/batches.py check $A $B | tail -3
