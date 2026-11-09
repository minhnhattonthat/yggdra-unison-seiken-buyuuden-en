-- extras_all.lua: open every Extra Contents entry (card dictionary, sound mode, item encyclopedia) for QA tours.
--   play.py SESSION --rom ROM --state work/states/extras.dst --script tools/lua/extras_all.lua
-- Bit arrays read by ov9_06 (ldrb [base, n asr 3] & 1 << (n & 7)): cards 0x0210E6F8, sounds 0x0210E6FE,
-- items 0x0210E703 (up to 0x0210E71F covers 232 items). Rewritten every frame, so the save data shows them too.
L.on_frame(function()
  for a = 0x0210E6F8, 0x0210E71F do memory.writebyte(a, 0xFF) end
end)
