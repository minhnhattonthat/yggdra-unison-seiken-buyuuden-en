-- spmes.lua: on the battle screen, call any battle function once (default: open battle event file SPMES<SPA><SPB>).
--   emu.py build/yggdra_marker.nds --state-in work/states/battle.dst --script tools/lua/spmes.lua --var SPA=1 --var SPB=14
--          --route-str "100 -;10 t16,152;600 -" ...                      (width gate for the battle SPMES box)
--   --var CALL=0x02080388 [--var R0=n --var R1=n]                         (any other function: tips, results ...)
-- Battle events normally start at a duel between two given units (0x0206F1E0 asks 0x02077134, then 0x02077910 makes
-- the SPMES task 0x020771FC, whose sprintf at 0x020772E8 names the file from *(battle+0x34), *(battle+0x38)).
-- Here the CAUTION draw call (tap your own castle: BL 0x020130AC at 0x02010BA4) is patched once into BL CALL with
-- r0 = R0, r1 = R1; the sprintf hook swaps in SPA/SPB. Gotchas: setregister r15 does not redirect in DeSmuME, and
-- memory.registerexec keeps one callback per address (a second script hooking SITE or SITE+4 breaks this one).
local SITE, TARGET, ORIG = 0x02010BA4, CALL or 0x02077910, nil
local function bl(at, to) return 0xEB000000 + ((to - at - 8) / 4) % 0x1000000 end  -- Lua 5.1: no bit ops
local state = 0
L.on_frame(function()
  if state == 0 then
    ORIG = memory.readdword(SITE)
    memory.writedword(SITE, bl(SITE, TARGET))
    state = 1
  end
end)
L.on_exec(SITE, function()
  if state ~= 1 then return end
  state = 2
  L.log(string.format("spmes: call %08X", TARGET))
  memory.setregister("arm9.r0", R0 or 0)
  memory.setregister("arm9.r1", R1 or 0)
end)
L.on_exec(SITE + 4, function()
  if state == 2 then state = 3; memory.writedword(SITE, ORIG) end
end)
L.on_exec(0x020772E8, function()
  L.log(string.format("spmes %03d%03d -> %03d%03d", memory.getregister("arm9.r2"), memory.getregister("arm9.r3"),
    SPA or -1, SPB or -1))
  if SPA then memory.setregister("arm9.r2", SPA); memory.setregister("arm9.r3", SPB) end
end)
