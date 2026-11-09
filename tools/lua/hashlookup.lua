-- hashlookup.lua: log every name passed to the DATA.SFS directory lookup (ITCM 0x01FFAD88, r0 = name; docs/re/sfs.md).
-- Catches opens that skip the 0x0200A540 wrapper (fileopen.lua). emu.py ... --script tools/lua/hashlookup.lua [--var ALL=true]
local frame = 0
L.on_frame(function(n) frame = n end)
local seen = {}
L.on_exec(0x01FFAD88, function()
  local p = memory.getregister("arm9.r0")
  local s = {}
  for i = 0, 63 do
    local c = memory.readbyte(p + i)
    if c == 0 or c > 126 or c < 32 then break end
    s[#s + 1] = string.char(c)
  end
  local name = table.concat(s)
  if not seen[name] or ALL then
    seen[name] = true
    L.log("lookup " .. frame .. " " .. name .. " lr=" .. string.format("%08X", memory.getregister("arm9.r14")))
  end
end)
