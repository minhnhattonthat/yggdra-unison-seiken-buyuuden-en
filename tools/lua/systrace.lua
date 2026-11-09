-- systrace.lua: log each distinct system-text draw (docs/re/text.md "Draw routines") with its position and bytes.
--   emu.py ROM --out D --script tools/debug/warp.lua --var "SCENE='prize'" --script tools/lua/systrace.lua
-- Lines: "sys <frame> <kind> lr=<caller> x=<x> y=<y> font=<id> scene=<id> ptr=<addr> <hex bytes up to FF>"
--   kind run = 0x02012DF4 (r0 x, r1 y, r3 string, [sp] font); ctr = 0x020130AC (centred; r0 y, r2 string, r3 font)
--   y may be in a sprite space past 192 (e.g. 979); lines are y += 15.
-- Read by tools/sysmap.py (marker build: the bytes decode to marker codes -> string ids).
local frame = 0
L.on_frame(function(n) frame = n end)
local seen = {}
local function bytes(p)
  local t = {}
  for i = 0, 95 do
    local b = memory.readbyte(p + i)
    t[#t + 1] = string.format("%02X", b)
    if b == 0xFF then break end
  end
  return table.concat(t)
end
local function r(n) return memory.getregister("arm9.r" .. n) end
local function hook(addr, kind, preg, xyf)
  L.on_exec(addr, function()
    local p = r(preg)
    local x, y, font = xyf()
    local k = string.format("%s lr=%08X x=%d y=%d font=%d scene=%d ptr=%08X %s", kind, r(14), x, y, font,
      memory.readdword(0x0210E020), p, bytes(p))
    if not seen[k] then
      seen[k] = true
      L.log(string.format("sys %d %s", frame, k))
    end
  end)
end
hook(0x02012DF4, "run", 3, function() return r(0), r(1), memory.readbyte(r(13)) end)
hook(0x020130AC, "ctr", 2, function() return 128, r(0), r(3) end)  -- centred on x 128 (0x80 - width / 2)
