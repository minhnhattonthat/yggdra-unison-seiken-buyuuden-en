-- fileopen.lua: log every DATA.SFS file the game opens by name (arm9 0x0200A540, r0 = name; docs/re/sfs.md).
-- emu.py ... --script tools/lua/fileopen.lua  -> log.txt lines "open <frame> <name>"
local frame = 0
L.on_frame(function(n) frame = n end)
local seen = {}
L.on_exec(0x0200A540, function()
  local p = memory.getregister("arm9.r0")
  local s = {}
  for i = 0, 63 do
    local c = memory.readbyte(p + i)
    if c == 0 then break end
    s[#s + 1] = string.char(c)
  end
  local name = table.concat(s)
  if not seen[name] or ALL then
    seen[name] = true
    L.log("open " .. frame .. " " .. name)
  end
end)
