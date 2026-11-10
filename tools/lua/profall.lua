-- profall.lua: show every character-profile ticker line (ov9_07 table 0x0211DDE0, 37 pointers) for textcover.
--   emu.py build/yggdra_en.nds --out D --state-in work/states/char_intro.dst --script tools/lua/textcover.lua
--          --script tools/lua/profall.lua --frames 3000
-- The ticker draw (ov9_07 0x0211BC20 ldrb r2,[r8,#6] -> run 0x02012DF4) takes the profile from [r8+6]; this
-- overwrites it before the read, stepping every STEP frames, and logs "prof n".
local N, step = 37, STEP or 20
local i, k, live = 0, 0, false
L.on_exec(0x0211BC1C, function()
  live = true
  memory.writebyte(memory.getregister("arm9.r8") + 6, i)
end)
L.on_frame(function()
  if not live then return end
  k = k + 1
  if k % step ~= 0 then return end
  L.log(string.format("prof %d", i))
  i = i + 1
  if i >= N then L.shot("final.png"); L.finish(0) end
end)
