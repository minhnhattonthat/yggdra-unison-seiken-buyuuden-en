-- warp.lua: cold boot -> any scene by name (tools/debug/scenes.txt), no save needed. docs/re/scenes.md has the RAM map.
--   emu.py ROM --out D --script tools/debug/warp.lua --var "SCENE='battle'" [--var FACTION=2] [--var HOLD=300]
--          [--var "STATE=[[abs/path.dst]]"] [--var MSG=12] [--var GOD=true] --frames 9000
-- Drives the game's own flow by touch, waiting on the scene manager (0x0210E010) rather than frame counts:
--   logos/attract -> title -> GAME START (help off unless HELP) -> faction FACTION -> prologue -> card select
--   -> sortie select (turn 1); then either stops there, attacks a territory (battle), or requests the target scene
--   through the scene manager (the game state is a real new game by then).
-- Logs "warp ok <scene> <frame>" when the target scene has run HOLD frames, saves STATE if given, shoots warp.png.
-- MSG=n: the next MESSAGE load after the target is reached opens MESSAGE<n> instead (dialogue viewer).

local M = 0x0210E010                         -- scene manager: +0x10 current, +0x18 next, +9 phase (1 = running)
local PLAYER = 0x02119138                    -- player faction byte
local UNLOCK = 0x0210E6E6                    -- u16 selectable-faction bits (new game: 0x0006 = factions 1, 2)
local function cur() return memory.readdword(M + 0x10) end
local function running() return memory.readbyte(M + 9) == 1 end
local function jump(id) memory.writedword(M + 0x18, id); memory.writebyte(M + 9, 2) end

-- name -> { stop = scene id to wait for, jump = scene to request from sortie select, attack = true for a battle }
local S = {
  title = { stop = 1 }, opening = { stop = 17 }, attract_op = { stop = 15, boot = true },
  faction_select = { stop = 2 }, prologue = { stop = 20 }, card_select = { stop = 3 }, sortie = { stop = 4 },
  battle = { stop = 5, attack = true },
  territory = { jump = 6 }, explore = { jump = 7 }, prize = { jump = 8 }, prisoner = { jump = 9 },
  medallion = { jump = 10 }, war_report = { jump = 11 }, turn_end = { jump = 12 }, save = { jump = 13 },
  load = { jump = 14 }, char_intro = { jump = 16 }, ending = { jump = 18 }, extras = { jump = 19 },
  epilogue = { jump = 18, file = "^EPI_MES" }, credits = { jump = 18, file = "^STAFFROLL" },
  tutorial = { jump = 21 },
}
local want = assert(S[SCENE], "unknown SCENE " .. tostring(SCENE))
local target = want.stop or want.jump
local fac = FACTION or 1
local hold = HOLD or 240

-- faction-select map taps (bottom screen) per faction id: one territory of each
-- (faction 5 has no start territory on the map: not selectable here)
local FAC_TAP = {
  [0] = "t20,20", [1] = "t132,85", [2] = "t160,150", [3] = "t210,130", [4] = "t225,100", [6] = "t170,85",
  [7] = "t82,128", [8] = "t37,132", [9] = "t59,129", [10] = "t167,52", [11] = "t60,60",
}

local taps = {                               -- scene id -> taps cycled while waiting in that scene
  [0] = { "t128,96" }, [15] = { "t128,96" }, [16] = { "t128,96" },
  [1] = { "t128,58", HELP and "t75,180" or "t187,180" },
  [17] = { "t128,96" },
  [2] = { FTAP or FAC_TAP[fac], "t218,182", "t75,180", "t200,150" },
  [20] = { "t128,100" },
  [3] = { "t128,100", "t75,180" },
  [4] = { ATTACK_TAP or "t155,65", "t218,182", "t75,180", "t128,150" },
  [18] = { "t128,100" },
}
local fileseen = false                       -- want.file: target = the scene that opens a file matching it
if want.file then
  L.on_exec(0x0200A540, function()           -- DATA.SFS open by name, r0 = name (docs/re/sfs.md)
    local p, s = memory.getregister("arm9.r0"), {}
    for i = 0, 31 do local b = memory.readbyte(p + i); if b == 0 then break end; s[#s + 1] = string.char(b) end
    if not fileseen and table.concat(s):match(want.file) then fileseen = true; L.log("file " .. table.concat(s)) end
  end)
end
local GAP = 45
local inscene, last, idx, reached, done = 0, -1, 0, nil, false

L.on_frame(function(n)
  local c = cur()
  if c ~= last then L.log(string.format("scene %d %d", n, c)); last = c; inscene = 0; idx = 0 end
  if not running() then return end
  inscene = inscene + 1
  if c == 1 and inscene == 2 and not NOUNLOCK then   -- system data: mark every faction cleared (opens them all)
    memory.writeword(UNLOCK, UNLOCK_BITS or 0x0FFF)        -- bit n = faction n (0..11)
  end
  if reached then
    if not done and n - reached >= hold then
      done = true
      L.shot("warp.png")
      if STATE then L.save_state(STATE) end
      L.log(string.format("warp ok %s scene %d frame %d", SCENE, c, n))
      if not KEEP then L.shot("final.png"); L.finish(0) end   -- KEEP=true: run on to --frames (routes, mash)
    end
    return
  end
  if c == target and (c ~= 15 or want.boot) and (c ~= 1 or SCENE == "title") and (not want.file or fileseen) then
    reached = n; L.log(string.format("reached %d frame %d player %d", c, n, memory.readbyte(PLAYER))); return
  end
  if c == 17 and target ~= 17 then jump(2); return end   -- skip the new-game scroll (it is its own scene)
  if want.jump and c == 4 and inscene == 60 then jump(want.jump); return end
  if c == 4 and not want.attack then return end
  local t = taps[c]
  if t and inscene > 30 and inscene % GAP == 0 then
    idx = idx % #t + 1
    L.press(t[idx], 6)
  end
end)

if MSG then                                  -- dialogue viewer: retarget the next MESSAGE load
  L.on_exec(0x02078760, function()
    L.log(string.format("msgload %d r0=%d r1=%d r2=%d r3=%d", L.frame or 0, memory.getregister("arm9.r0"),
      memory.getregister("arm9.r1"), memory.getregister("arm9.r2"), memory.getregister("arm9.r3")))
    if reached then memory.setregister("arm9.r0", MSG) end
  end)
end
