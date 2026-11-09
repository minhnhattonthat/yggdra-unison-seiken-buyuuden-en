#!/bin/sh
# widthgate.sh: stress build for the width gate (docs/re/windows.md). Lines filled to each box's measured budget
# (#px x lines, tools/marker.py qa_lines) plus the glyph torture line, booted cold at each box; shots in work/qa/gate/.
#   sh tools/debug/widthgate.sh            -> build/yggdra_gate.nds, work/qa/gate/<box>/final.png + gate.png
set -e
cd "$(dirname "$0")/../.."
SKILL="$(python tools/skill.py)"
TORTURE=' !"%&'"'"'()*+,-./0123456789:;?  ~—…\nABCDEFGHIJKLMNOPQRS\nTUVWXYZ abcdefghijklmn\nopqrstuvwxyz  The quick brown'
export MARKER_QA="MESSAGE154:0240=#142x2|MESSAGE130:04ED=#142x2|SPMES_TRE:0160=#184x2|TUTO00_01:007B=#144x2|EDMES07:0100=$TORTURE"
python -X utf8 tools/build.py --marker
mv -f build/yggdra_marker.nds build/yggdra_gate.nds
unset MARKER_QA
python -X utf8 tools/build.py --marker >/dev/null
ROM=build/yggdra_gate.nds
OUT=work/qa/gate
warp() {  # name, scene, extra args
  n=$1; s=$2; shift 2
  python -X utf8 "$SKILL/scripts/emu.py" $ROM --out $OUT/$n --script tools/debug/warp.lua --var "SCENE='$s'" \
    --var "STATE=[[$(pwd -W 2>/dev/null || pwd)/$OUT/$n.dst]]" --frames 30000 --timeout 600 "$@" >/dev/null
}
warp prize prize & warp prisoner prisoner & warp explore explore & warp tutorial tutorial & warp ending ending --var FACTION=1 &
wait
TAPS=$(python -c "print(';'.join(['40 -;4 t128,300']*14)+';400 -')")  # through the ending dialogue to the first epithet
python -X utf8 "$SKILL/scripts/emu.py" $ROM --out $OUT/epilogue --state-in $OUT/ending.dst --route-str "$TAPS" --shots 700,900 >/dev/null
python -X utf8 "$SKILL/scripts/emu.py" $ROM --out $OUT/tuto --state-in $OUT/tutorial.dst \
  --route-str "90 -;30 -;90 -;6 t70,78;120 -;90 -;6 t80,38;200 -;90 -;6 a;120 -;90 -;6 t100,165;150 -" >/dev/null
python -X utf8 "$SKILL/scripts/sheet.py" $OUT/prize/final.png $OUT/prisoner/final.png $OUT/explore/final.png \
  $OUT/tuto/final.png $OUT/epilogue/f000900.png --div 1 --cols 5 --out $OUT/gate.png
