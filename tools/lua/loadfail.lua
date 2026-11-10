-- loadfail.lua: fault injection for the boot data check (ov9_05, logos scene 0) -> "Failed to load data..." band.
--   emu.py build/yggdra_en.nds --out D --script tools/lua/textcover.lua --script tools/lua/loadfail.lua --frames 900
-- ov9_05 0x0211B92C calls 0x02013560 (= dword [0x0210E8C4 + 0xC], data loaded ok) and fails on 0. Exec hooks on
-- that block miss under JIT (a call-return target), so the flag itself is cleared every frame of scene 0.
L.on_frame(function()
  if memory.readdword(0x0210E020) == 0 then memory.writedword(0x0210E8D0, 0) end
end)
