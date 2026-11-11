-- textcover.lua: log "TEXT <hash>" for every distinct string the game draws, for the skill's textcover.py.
--   regen.py --list tools/debug/tour.txt --qa work/qa/tour --rom build/yggdra_en.nds --script tools/lua/textcover.lua
--   python tools/cover.py writes build/strings.tsv (id -> the same hash of the string's built bytes).
-- Strings live in RAM buffers (script files) and the EXTRA block, so the key is the content, not the address:
-- hash = fold of (h * 31 + byte + 1) mod 4294967291 over the bytes before FF (tools/cover.py strhash, keep in step).
-- Hooks (docs/re/text.md "Draw routines"): dialogue object 0x020128B8 (r3), run 0x02012DF4 (r3), centred
-- 0x020130AC (r2), join 0x020132E0 (parts r1, r2, r3, [sp], [sp+4]; 0 = none).
local seen = {}
local function text(p)
  if p < 0x02000000 or p >= 0x02400000 then return end
  local h = 0
  for i = 0, 1023 do
    local b = memory.readbyte(p + i)
    if b == 0xFF then break end
    h = (h * 31 + b + 1) % 4294967291
  end
  if not seen[h] then seen[h] = true; L.log(string.format("TEXT %X", h)) end
end
local function r(n) return memory.getregister("arm9.r" .. n) end
L.on_exec(0x020128B8, function() text(r(3)) end)
L.on_exec(0x02012DF4, function() text(r(3)) end)
L.on_exec(0x020130AC, function() text(r(2)) end)
L.on_exec(0x020132E0, function()
  local sp = r(13)
  for _, p in ipairs({ r(1), r(2), r(3), memory.readdword(sp), memory.readdword(sp + 4) }) do text(p) end
end)
