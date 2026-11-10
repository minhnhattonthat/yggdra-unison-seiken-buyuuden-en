-- Dump 2D engine VRAM / palettes / OAM / IO every PPU_EVERY frames (default 120) between PPU_FROM and PPU_TO to
-- <out>/ppu_<frame>.*.bin (layout: L.dump_ppu in the skill's desmume_lib.lua). Find 2D-drawn (non-texture) graphics.
-- The game alternates its one 3D screen each frame (the other shows a capture as bitmap OBJs): dump both parities.
--   regen.py --list tools/debug/tour.txt --qa work/qa/x --script tools/lua/ppuevery.lua --var PPU_EVERY=1 --var PPU_FROM=2640 --var PPU_TO=2641 NAME
--   python -X utf8 tools/oamlist.py work/qa/x/NAME/ppu_002640 --engine a
local every, from, to = PPU_EVERY or 120, PPU_FROM or 0, PPU_TO or 1e9
L.on_frame(function(f)
  if f >= from and f <= to and f % every == 0 then L.dump_ppu(string.format("ppu_%06d", f)) end
end)
