-- forceband.lua: draw each listed system string in the battle CAUTION box, for textcover (code-loaded prompts,
-- composite parts and table names no warp scene reaches).
--   python -X utf8 tools/forcelist.py IDS.txt work/qa/force_list.lua
--   emu.py build/yggdra_en.nds --out D --state-in work/states/battle.dst --script tools/lua/textcover.lua
--          --var "LISTFILE='work/qa/force_list.lua'" --script tools/lua/forceband.lua
--          --route-str "100 -;10 t16,152;3000 -" --frames 3200
-- Tapping your own castle opens a CAUTION box; its draw call (BL 0x020130AC at 0x02010BA4, r2 = string) runs every
-- frame while it shows. This swaps r2 for the next list entry every STEP frames, logs "force <id>", and finishes
-- after the last one. The box is the CAUTION band (240 px, centred), not each string's own screen: coverage only.
dofile(LISTFILE)
local SITE, step = 0x02010BA4, STEP or 6
local i, k, f = 1, 0, 0
L.on_frame(function(n) f = n end)
L.on_exec(SITE, function()
  if i > #LIST then return end
  local e = LIST[i]
  memory.setregister("arm9.r2", e[2])
  k = k + 1
  if k == 1 then L.log("force " .. e[1] .. " " .. e[3] .. " f" .. f) end
  if k == 2 and i % 20 == 1 then L.shot(string.format("force_%03d.png", i)) end
  if k >= step then
    i, k = i + 1, 0
    if i > #LIST then L.log("force done"); L.finish(0) end
  end
end)
