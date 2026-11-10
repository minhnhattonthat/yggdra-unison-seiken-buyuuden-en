#!/bin/sh
# Text coverage for the battle tips (table 0x02100500, 8 tips) and the YOU WIN results screen, from battle.dst.
#   sh tools/debug/cover_battle.sh [ROM]   -> work/qa/cover2/tip_N, work/qa/cover2/results (textcover logs)
ROM=${1:-build/yggdra_en.nds}
SK=$(python tools/skill.py)
for n in 0 1 2 3 4 5 6 7; do
  rm -rf work/qa/cover2/tip_$n
  python -X utf8 "$SK/scripts/emu.py" "$ROM" --out work/qa/cover2/tip_$n --state-in work/states/battle.dst \
    --script tools/lua/textcover.lua --script tools/lua/spmes.lua --var CALL=0x02080388 \
    --script tools/lua/tips.lua --var TIP=$n --route-str "100 -;10 t16,152;600 -" --frames 900 > /dev/null 2>&1
  echo "tip $n exit $?"
done
rm -rf work/qa/cover2/results
python -X utf8 "$SK/scripts/emu.py" "$ROM" --out work/qa/cover2/results --state-in work/states/battle.dst \
  --script tools/lua/textcover.lua --script tools/lua/spmes.lua --var CALL=0x02081350 --var R0=8 \
  --route-str "100 -;10 t16,152;300 -;6 t128,100;300 -;6 t128,100;300 -;6 t128,100;300 -" --shot-every 150 \
  --frames 1800 > /dev/null 2>&1
echo "results exit $?"
