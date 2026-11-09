-- scenejump.lua (recon): once the title scene (1) has run 30 frames, request scene JUMP through the scene manager
-- (0x0210E010: +0x10 current, +0x18 next, +9 phase; 0x0200D13C sets next = r0, phase = 2). Logs every scene change.
local M = 0x0210E010
local last, t1, done = -1, 0, false
L.on_frame(function(n)
  local cur = memory.readdword(M + 0x10)
  if cur ~= last then L.log(string.format("scene %d %d phase %d", n, cur, memory.readbyte(M + 9))); last = cur end
  if cur == 1 and memory.readbyte(M + 9) == 1 then t1 = t1 + 1 else t1 = 0 end
  if JUMP and not done and t1 >= 30 then
    if PRE then PRE() end
    memory.writedword(M + 0x18, JUMP); memory.writebyte(M + 9, 2); done = true
    L.log("jump " .. n .. " " .. JUMP)
  end
end)
