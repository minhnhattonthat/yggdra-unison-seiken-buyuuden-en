-- saveall.lua: reach every save-screen prompt (ov9_19) from work/states/save.dst for textcover.
--   emu.py build/yggdra_en.nds --out D --state-in work/states/save.dst --route tools/routes/saveall.txt
--          --script tools/lua/textcover.lua --script tools/lua/saveall.lua --frames 3000
-- ov9_19 0x0211BAF8: the slot is "in use" when u16 [0x0210E970 + slot * 0x98C] ~= 0 -> "Overwrite the data?".
-- This marks slot 1 (FILE 1) in use. FAIL=n: the n-th save result read (0x02014434 -> r0 at 0x0211BD20; >0 done,
-- 0 busy, -1 failed) is forced to -1 -> "Failed to save..." (fault injection: the card never fails here).
local fails = 0
L.on_frame(function()
  if memory.readdword(0x0210E020) == 13 then memory.writeword(0x0210E970, 1) end
end)
L.on_exec(0x0211BD20, function()
  local r0 = memory.getregister("arm9.r0")
  if FAIL and r0 > 0 then
    fails = fails + 1
    if fails == FAIL then memory.setregister("arm9.r0", 0xFFFFFFFF); L.log("save forced to fail") end
  end
end)
