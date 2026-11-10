-- unlockall.lua: show the unlock-terms page (使用条件, ov9_18) of every locked faction for textcover.
--   emu.py build/yggdra_en.nds --out D --script tools/debug/warp.lua --var "SCENE='faction_select'" --var NOUNLOCK=true
--     --var HOLD=30 --var "TOUR='60-;6t20,20;60-;6t128,182;2000-'" --script tools/lua/textcover.lua
--     --script tools/lua/unlockall.lua --frames 6000
-- The page draw takes the faction from 0x02042B34 (returns at 0x0211ED3C); its 6 rows are u32 pointers at
-- 0x0211F540 + 24 * faction (0 = no row). This sets r0 there, stepping every STEP frames through the factions
-- that have rows, and logs "terms f".
local F = { 0, 3, 4, 5, 6, 7, 8, 9, 10, 11 }
local step = STEP or 20
local i, k, live = 1, 0, false
L.on_exec(0x0211ED3C, function()
  live = true
  memory.setregister("arm9.r0", F[i])
end)
L.on_frame(function()
  -- the faction panel draws the terms page instead of the info page while [0x0211F720+0x19] ~= 0 (0x0211E254)
  if memory.readdword(0x0210E020) == 2 then memory.writebyte(0x0211F739, 1) end
  if not live then return end
  k = k + 1
  if k % step ~= 0 then return end
  L.log(string.format("terms %d", F[i]))
  L.shot(string.format("terms_%02d.png", F[i]))
  i = i + 1
  if i > #F then L.finish(0) end
end)
