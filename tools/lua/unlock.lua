-- unlock.lua: mark factions as "newly unlocked" (u16 0x0210E6E8, docs/re/scenes.md) on the first frame, so the next
-- entry to faction select (ov9_18) shows its unlock message. Width gate tour helper.
--   --var NEW=0x0FF8  (bits = faction ids; default factions 3..11)
local done = false
L.on_frame(function(n)
  -- on the title (scene 1), after boot has loaded the system data over these words
  if not done and memory.readdword(0x0210E020) == 1 then
    done = true
    memory.writeword(0x0210E6E6, 0x0FFF)
    memory.writeword(0x0210E6E8, NEW or 0x0FF8)
    -- CLEAR=0x0FFF: cleared-faction bits (u16 0x0210E6E4): the faction panel shows "☆ CLEAR" (ov9_18 0x0211D5F4)
    if CLEAR then memory.writeword(0x0210E6E4, CLEAR) end
    L.log("unlock " .. string.format("%04X", NEW or 0x0FF8))
  end
end)
