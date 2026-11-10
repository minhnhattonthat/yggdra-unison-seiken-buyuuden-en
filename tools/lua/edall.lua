-- edall.lua: show every EDMES ending record (38 files x 12 records of (epithet, paragraph), docs/re/text.md) for
-- text coverage; logs "TEXT <hash>" like textcover.lua (run with it).
--   emu.py build/yggdra_en.nds --state-in work/states/ending_f01.dst --script tools/lua/textcover.lua
--          --script tools/lua/edall.lua [--var FILES='0-37'] --frames 2000000 --timeout 7200
-- ov9_15 (scene 18) builds "EDMES%02d" with r2 = unit (sprintf BL 0x0211D254) and selects the record with
-- 0x02005654 r1 (BLs 0x0211D278 / 0x0211D288, the second after its +6). Every unit load of the ending gets the
-- next (file, record) not yet shown. Shown = the paragraph draw (0x0211DB44: sl = string, one glyph per call after
-- it) and the epithet draw on the bottom record page (0x0211E010, r3; only once the page timer
-- [obj+0x21C] - 0xF0 reaches 0x1F, ~300 frames after the load; a tap ends the page). When no record is shown for MAXIDLE
-- frames (the ending ran out, or a page broke) the start state is reloaded; a record missed twice is logged
-- "edall <file> <rec> MISS" and skipped. Logs "edall <file> <rec> ok".
local rb = memory.readbyte
local function r(n) return memory.getregister("arm9." .. n) end

local combos = {}
for part in (FILES or "0-37"):gmatch("[^,%s]+") do
  local a, b = part:match("^(%d+)-(%d+)$")
  a, b = tonumber(a or part), tonumber(b or part)
  for f = a, b do for k = 0, 11 do combos[#combos + 1] = { f, k } end end
end

local logged = {}
local function text(p)                       -- same key as textcover.lua / tools/cover.py strhash
  if p < 0x02000000 or p >= 0x02400000 then return end
  local h = 0
  for i = 0, 1023 do
    local c = rb(p + i)
    if c == 0xFF then break end
    h = (h * 31 + c + 1) % 4294967291
  end
  if not logged[h] then logged[h] = true; L.log(string.format("TEXT %X", h)) end
end

local ci, shown = 1, nil                     -- next combo to load; combo index on screen (set at its load)
local para, epi, tries, lastok, reload = false, false, 0, 0, false
local function finish()
  L.log("edall all done " .. L.frame); L.finish(0)
end
local function at(a, word, f)                -- other overlays load at these addresses: act only on ov9_15's code
  L.on_exec(a, function() if memory.readdword(a) == word then f() end end)
end
at(0x0211D254, 0xEBFB9801, function()        -- sprintf("EDMES%02d", r2): a new unit page
  if ci > #combos then return end
  shown, para, epi = ci, false, false
  memory.setregister("arm9.r2", combos[ci][1])
  if TRACE then L.log(string.format("load %d %d (game %d) f%d", combos[ci][1], combos[ci][2], r("r8"), L.frame)) end
end)
local function setrec(where)
  return function()
    if not shown then return end
    if TRACE then L.log(string.format("setrec %s r1 %d -> %d", where, r("r1"), combos[shown][2])) end
    memory.setregister("arm9.r1", combos[shown][2])
  end
end
at(0x0211D278, 0xEBFBA0F5, setrec("D278"))
-- page type 4 ([obj+0x221]) takes beq 0x0211D280 (r1 += 6, and 0xFF): exec hooks there never fire (JIT block of a
-- branch target), so r1 is set at the beq with the +6 taken off (mod 256)
at(0x0211D274, 0x0A000001, function()
  if shown and rb(r("r6") + 0x221) == 4 then
    if TRACE then L.log("setrec D274 type 4 -> " .. combos[shown][2]) end
    memory.setregister("arm9.r1", (combos[shown][2] - 6) % 256)
  end
end)
local function check()
  if shown == ci and para and epi then
    L.log(string.format("edall %d %d ok", combos[ci][1], combos[ci][2]))
    ci, tries, lastok = ci + 1, 0, L.frame
  end
end
at(0x0211DB44, 0xE3A0401E, function() if shown then para = true; text(r("r10")); check() end end)
at(0x0211E010, 0xEBFBD377, function() if shown then epi = true; text(r("r3")); check() end end)

L.on_frame(function(n)
  if ci > #combos then finish() end
  if reload then reload = false; savestate.load(STATE_IN); return end
  if n - lastok > (MAXIDLE or 4000) then
    tries = tries + 1
    if tries >= 2 then
      L.log(string.format("edall %d %d MISS%s%s", combos[ci][1], combos[ci][2], para and "" or " para",
        epi and "" or " epithet"))
      ci, tries = ci + 1, 0
    end
    shown, para, epi, lastok, reload = nil, false, false, n, true
  end
  -- next unit: tap once this page's epithet is up (a tap before ends the page), else every EVERY frames
  if lastok == n - 20 or n % (EVERY or 600) == 0 then L.press(TAP or "t128,100", 6) end
end)
