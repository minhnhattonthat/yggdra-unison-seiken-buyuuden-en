-- Log the GX texture state between GX_FROM and GX_TO: every TEXIMAGE_PARAM (0x040004A8) / PLTT_BASE (0x040004AC)
-- write with the PC that wrote it, plus DISPCAPCNT (0x04000064) once per frame. Finds the code and VRAM address of a
-- quad that tools/lua/quads.lua does not see (drawn by another path). Direct-port writes only: a game that DMAs packed
-- commands to GXFIFO 0x04000400 logs nothing here.
--   regen.py --list tools/debug/tour.txt --qa work/qa/x --script tools/lua/gxtex.lua --var GX_FROM=2640 --var GX_TO=2641 NAME
local from, to, frame = GX_FROM or 0, GX_TO or 1e9, 0
L.on_frame(function(f)
  frame = f
  if f >= from and f <= to then L.log(string.format("frame %d DISPCAPCNT %08X", f, memory.readdword(0x04000064))) end
end)
local function on(addr, name)
  L.on_write(addr, addr + 3, function(a, size, value)
    if frame >= from and frame <= to then
      L.log(string.format("%s %08X pc %08X lr %08X", name, value or memory.readdword(addr), L.pc(),
        memory.getregister("arm9.r14")))
    end
  end)
end
on(0x040004A8, "TEXIMAGE")
on(0x040004AC, "PLTT")
