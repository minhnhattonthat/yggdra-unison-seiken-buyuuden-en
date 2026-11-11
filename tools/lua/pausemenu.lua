-- pausemenu.lua: lets Select open the battle pause menu (BTLMN_FONT, loader 0x02089728).
-- The battle input handler (0x0204DF98..0x0204E01C) opens it on Select (0x0204BE78(1,6) = keypad mask 4) only while the battle
-- state 0x0211A874 is 0 (or has 0x1000); the warp's battle sits in the deploy phase (0x2000, set by task 0x02057278).
-- This clears that bit once, so TIME runs and Select works. Tour: tools/debug/tour.txt `pause`.
local done = false
L.on_frame(function()
  if done then return end
  local v = memory.readdword(0x0211A874)
  if v == 0x2000 then
    memory.writedword(0x0211A874, 0)
    done = true
    L.log("pausemenu: battle flags 0x2000 -> 0")
  end
end)
