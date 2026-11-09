-- tips.lua: force the battle tip popup (table 0x02100500, drawn by the task at 0x0207FD6C).
--   emu.py build/yggdra_marker.nds --state-in work/states/battle.dst --script tools/lua/systrace.lua
--          --script tools/lua/tips.lua [--var TIP=n] ...
-- The battle calls 0x02080388 (picks tip 0..3 from battle state) only while byte [0x0210E6AC+0xF] < 5;
-- this hook zeroes that byte at the check and, with TIP set, starts the tip task with that index instead.
local logged = false
L.on_exec(0x0207ED80, function()
  if not logged then
    logged = true
    L.log(string.format("tipcheck byte=%d", memory.readbyte(0x0210E6BB)))
  end
  memory.writebyte(0x0210E6BB, 0)
end)
if TIP then
  -- 0x020803D0 starts the task with r4 = tip index
  L.on_exec(0x020803D0, function() memory.setregister("arm9.r4", TIP) end)
end
L.on_exec(0x02080388, function() L.log("tip task start") end)
-- battle banner / cut-in task (0x0207CEFC, r0 = type; its end hook 0x0207CE20: 0xE / 9 turn start, 8 results)
L.on_exec(0x0207CEFC, function() L.log(string.format("banner %d", memory.getregister("arm9.r0"))) end)
L.on_exec(0x0208119C, function() L.log("results task") end)
-- No real turn start in reach: start the tip task with tools/lua/spmes.lua --var CALL=0x02080388 (tap own castle).
-- FORCE_TURN=1: the battle state machine (0x0207CEAC, byte [r4+1]) starts the turn-start task 0x0207F04C at
-- state 0xE; the pre-battle warp state never gets there, so set it once.
if FORCE_TURN then
  local done = false
  L.on_exec(0x0207CEAC, function()
    local r4 = memory.getregister("arm9.r4")
    if not done then
      done = true
      L.log(string.format("battle state %d -> 14", memory.readbyte(r4 + 1)))
      memory.writebyte(r4 + 1, 0x0E)
    end
  end)
end
