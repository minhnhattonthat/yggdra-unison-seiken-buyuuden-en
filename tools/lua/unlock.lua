-- unlock.lua: mark factions as "newly unlocked" (u16 0x0210E6E8, docs/re/scenes.md) on the first frame, so the next
-- entry to faction select (ov9_18) shows its unlock message. Width gate tour helper.
--   --var NEW=0x0FF8  (bits = faction ids; default factions 3..11)
L.on_frame(function(n)
  if n == 1 then
    memory.writeword(0x0210E6E6, 0x0FFF)
    memory.writeword(0x0210E6E8, NEW or 0x0FF8)
    L.log("unlock " .. string.format("%04X", NEW or 0x0FF8))
  end
end)
