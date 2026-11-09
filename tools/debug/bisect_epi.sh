#!/bin/sh
# Marker-build bisect helper: build with the given --skip list (families or file-stem regexes), warp to a scene,
# print the warp result. Run one at a time (the build writes build/yggdra_marker.nds).
#   sh tools/debug/bisect_epi.sh "spmes,MESSAGE1.*" epilogue 1
set -e
S="$(python tools/skill.py)"
python -X utf8 tools/build.py --marker --skip "$1" > /dev/null
out=work/qa/bisect_$(printf %s "$1" | tr -c 'A-Za-z0-9' '_')
mkdir -p "$out"
cp build/yggdra_marker.nds "$out/rom.nds"
python -X utf8 "$S/scripts/emu.py" "$out/rom.nds" --out "$out" --script tools/debug/warp.lua \
  --var "SCENE='${2:-epilogue}'" --var FACTION="${3:-1}" --frames 30000 > /dev/null 2>&1 || true
echo "skip=$1: $(tail -1 "$out/log.txt")"
