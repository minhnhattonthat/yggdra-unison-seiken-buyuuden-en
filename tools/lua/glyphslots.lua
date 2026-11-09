-- glyphslots.lua: log the text glyph-slot pools every 30 frames when they change (docs/re/text.md "Glyph slots").
-- 0x0210E768: +8 capacity, +0xA used (system/centred text), +0xC/+0xE saved marks; +0x18.. second pool.
-- 0x0210E7B8 +2: next slot for dialogue text objects (arg to 0x020128B8).
local last = ""
L.on_frame(function(n)
  if n % 30 ~= 0 then return end
  local b = 0x0210E768
  local s = string.format("sys cap %d used %d marks %d %d | p2 %d %d %d %d | dlg %d",
    memory.readword(b + 8), memory.readword(b + 0xA), memory.readword(b + 0xC), memory.readword(b + 0xE),
    memory.readword(b + 0x18), memory.readword(b + 0x1A), memory.readword(b + 0x1C), memory.readword(b + 0x1E),
    memory.readword(0x0210E7BA))
  if s ~= last then L.log(n .. " " .. s); last = s end
end)
