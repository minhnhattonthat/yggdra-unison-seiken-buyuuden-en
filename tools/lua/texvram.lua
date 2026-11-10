-- Dump texture VRAM (banks A-D, 512 KB) at frame TEX_AT to <out>/tex_<frame>.bin: maps the banks to LCDC for one
-- read and restores VRAMCNT, so the frame after may glitch. Bank order A B C D = file offsets 0, 0x20000, 0x40000,
-- 0x60000; vramcnt.txt has the original VRAMCNT_A..D (MST 3 = texture slot = OFS). Find what a 3D quad samples.
--   regen.py --list tools/debug/tour.txt --qa work/qa/x --script tools/lua/texvram.lua --var TEX_AT=2640 NAME
local at = TEX_AT or 0
L.on_frame(function(f)
  if f ~= at then return end
  local cnt = {}
  for b = 0, 3 do cnt[b] = memory.readbyte(0x04000240 + b) end
  for b = 0, 3 do memory.writebyte(0x04000240 + b, 0x80) end
  local fh = assert(io.open(OUT .. string.format("tex_%06d.bin", f), "wb"))
  for p = 0x06800000, 0x06880000 - 1, 4 do
    local v = memory.readdword(p)
    fh:write(string.char(v % 256, math.floor(v / 256) % 256, math.floor(v / 65536) % 256, math.floor(v / 16777216) % 256))
  end
  fh:close()
  for b = 0, 3 do memory.writebyte(0x04000240 + b, cnt[b]) end
  local t = assert(io.open(OUT .. "vramcnt.txt", "w"))
  t:write(string.format("%02X %02X %02X %02X\n", cnt[0], cnt[1], cnt[2], cnt[3]))
  t:close()
end)
