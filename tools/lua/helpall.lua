-- helpall.lua: show every in-game HELP popup page (table arm9 0x020F79D8, docs/re/windows.md) for textcover.
--   emu.py build/yggdra_en.nds --out D --script tools/debug/warp.lua --var "SCENE='faction_select'" --var HELP=true
--          --var HOLD=60 --var KEEP=true --script tools/lua/textcover.lua --script tools/lua/helpall.lua --frames 6000
-- The popup draw (0x02011124..) reads topic [obj+5] and page [obj+4]: title = T[start[topic]],
-- body = T[start[topic] + page + 1], start/npages = u8 pairs at 0x0208F934. Once the popup has drawn, this
-- steps (topic, page) every STEP frames through all pairs and logs "help t p", then finishes.
local PAIRS = 0x0208F934
local NT = 36  -- pairs 36+ are (77,0), (0,0), then other data
local step = STEP or 20
local obj, t, p, k, last = nil, 0, 0, 0, -1
L.on_exec(0x02011124, function() obj = memory.getregister("arm9.r4") end)
L.on_frame(function(n)
  if not obj then return end
  k = k + 1
  if k % step ~= 1 then return end
  while t < NT and p >= memory.readbyte(PAIRS + 2 * t + 1) do t, p = t + 1, 0 end
  if t >= NT then L.log("help done"); L.shot("final.png"); L.finish(0); return end
  memory.writebyte(obj + 5, t)
  memory.writebyte(obj + 4, p)
  L.log(string.format("help %d %d", t, p))
  if t ~= last then L.shot(string.format("help_%02d_%d.png", t, p)); last = t end
  p = p + 1
end)
