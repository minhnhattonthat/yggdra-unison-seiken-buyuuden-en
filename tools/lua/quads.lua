-- quads.lua: log every textured quad the 2D layer draws, with the texture's name and its UV rect (atlas label rects).
--   emu.py ... --script tools/debug/warp.lua --script tools/lua/quads.lua  -> log.txt "quad NAME u,v,w,h at x,y z"
-- ITCM 0x01FF89B4 loads a texture: r0 = slot id, r1 = file name (no extension), r2/r3 = size.
-- ITCM 0x01FF966C binds slot r0 (0x01FF9770 is a wrapper). ITCM 0x01FF9AD0 draws: r0 x, r1 y, r2 z?, r3 w; stack h, u, v, u+w, v+h.
-- Each distinct (name, rect) is logged once; ALL=true logs every draw.
local names, cur, seen = {}, nil, {}
local function str(p)
  local s = {}
  for i = 0, 31 do
    local c = memory.readbyte(p + i)
    if c == 0 then break end
    s[#s + 1] = string.char(c)
  end
  return table.concat(s)
end
L.on_exec(0x01FF89B4, function()
  names[memory.getregister("arm9.r0")] = str(memory.getregister("arm9.r1"))
  L.log(string.format("load %d %s", memory.getregister("arm9.r0"), names[memory.getregister("arm9.r0")]))
end)
L.on_exec(0x01FF966C, function() cur = memory.getregister("arm9.r0") end)
L.on_exec(0x01FF9AD0, function()
  local r = function(n) return memory.getregister("arm9.r" .. n) end
  local sp = r(13)
  local h, u, v = memory.readdword(sp), memory.readdword(sp + 4), memory.readdword(sp + 8)
  local u1, v1 = memory.readdword(sp + 12), memory.readdword(sp + 16)
  local name = names[cur] or ("slot" .. tostring(cur))
  -- UV rect from the texcoords; screen size w x h (differs when the quad is scaled)
  local line = string.format("quad %s %d,%d,%d,%d at %d,%d size %dx%d z%d", name, u, v, u1 - u, v1 - v, r(0), r(1),
    r(3), h, r(2))
  if ALL or not seen[line] then
    seen[line] = true
    L.log(line)
  end
end)
