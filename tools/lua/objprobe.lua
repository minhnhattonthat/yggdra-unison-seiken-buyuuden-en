-- objprobe.lua: log each distinct script obj / file base the interpreter loop (0x02005798) runs, and every DATA.SFS
-- open by name (0x0200A540). Hooks those addresses: don't combine with msgall.lua (one callback per address).
local seen = {}
L.on_exec(0x02005798, function()
  local o = memory.readdword(0x02101D64 + 8)
  local b = memory.readdword(o)
  local k = string.format("%08X %08X", o, b)
  if not seen[k] then seen[k] = true; L.log(string.format("obj %s frame %d pc %08X", k, L.frame, memory.getregister("arm9.r1"))) end
end)
L.on_exec(0x0200A540, function()
  local p, s = memory.getregister("arm9.r0"), {}
  for i = 0, 31 do local c = memory.readbyte(p + i); if c == 0 then break end; s[#s + 1] = string.char(c) end
  L.log("open " .. table.concat(s) .. " frame " .. L.frame)
end)
