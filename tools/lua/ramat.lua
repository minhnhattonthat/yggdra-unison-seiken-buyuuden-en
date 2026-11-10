-- Dump main RAM (4 MB) at frames RAM_AT (comma list) to <out>/ram_<frame>.bin: search it for a texture or string.
--   regen.py --list tools/debug/tour.txt --qa work/qa/x --script tools/lua/ramat.lua --var "RAM_AT='2640'" NAME
local at = {}
for n in tostring(RAM_AT or "0"):gmatch("%d+") do at[tonumber(n)] = true end
L.on_frame(function(f)
  if at[f] then L.dump_ram(string.format("ram_%06d.bin", f)) end
end)
