-- tutoall.lua: show every tutorial-menu topic title + description (ov9_03 tables 0x0211E908 Book of Heaven, 11
-- entries; 0x0211E960 Book of Earth, 18; 8 bytes each = title, description) for textcover.
--   emu.py build/yggdra_en.nds --out D --state-in work/states/tutorial.dst --script tools/lua/textcover.lua
--          --script tools/lua/tutoall.lua --frames 3000
-- The menu draw (ov9_03 0x0211CB74..0x0211CBF4) takes the book from [r5+7] and the entry from [sp+0x68]; this
-- overwrites both before they are read, stepping every STEP frames, and logs "tuto b e".
local N = { [0] = 11, [1] = 18 }
local step = STEP or 20
local b, e, k, live = 0, 0, 0, false
L.on_exec(0x0211CB74, function()
  live = true
  memory.writebyte(memory.getregister("arm9.r5") + 7, b)
end)
L.on_exec(0x0211CBA8, function() memory.writedword(memory.getregister("arm9.r13") + 0x68, e) end)
L.on_frame(function()
  if not live then return end
  k = k + 1
  if k % step ~= 0 then return end
  L.log(string.format("tuto %d %d", b, e))
  if e == 0 then L.shot(string.format("tuto_%d.png", b)) end
  e = e + 1
  if e >= N[b] then b, e = b + 1, 0 end
  if b > 1 then L.shot("final.png"); L.finish(0) end
end)
