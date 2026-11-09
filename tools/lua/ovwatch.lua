-- ovwatch.lua: log which arm9 overlay sits at 0x0211B780 (all 20 load there; docs/re/sfs.md) whenever it changes,
-- and dump main RAM DUMP_AFTER frames after each change (for ramsearch / scene-variable hunting).
-- emu.py ... --script tools/lua/ovwatch.lua --var "OVDIR=[[H:/.../work]]" [--var DUMP=true]
-- log.txt: "ov <frame> <id>" (-1 = none matched)
local sig = {}
for i = 0, 19 do
  local f = io.open(string.format("%s/ov9_%02d.bin", OVDIR, i), "rb")
  local d = f:read(64); f:close()
  sig[i] = { d:byte(1, 64) }
end
local function which()
  for i = 0, 19 do
    local ok = true
    for k = 1, 64, 4 do
      if memory.readbyte(0x0211B780 + k - 1) ~= sig[i][k] then ok = false; break end
    end
    if ok then return i end
  end
  return -1
end
local cur, due = -2, nil
L.on_frame(function(n)
  if n % 10 == 0 then
    local w = which()
    if w ~= cur then cur = w; L.log("ov " .. n .. " " .. w); due = n + (DUMP_AFTER or 60) end
  end
  if DUMP and due and n == due then L.dump_ram(string.format("ram_%06d_ov%d.bin", n, cur)); due = nil end
end)
