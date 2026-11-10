-- msgall.lua: play every branch of bytecode script files (MESSAGE / SPMES / TUTO) one after another, for text
-- coverage (logs "TEXT <hash>" like textcover.lua).
--   emu.py build/yggdra_en.nds --state-in work/states/battle.dst --script tools/lua/textcover.lua
--          --script tools/lua/msgall.lua --var "FILES='0-220,SPMES001014,TUTO00_01'" --frames 400000 --timeout 3600
-- FILES: numbers / ranges = MESSAGE<n>; names = any other script file, loaded through the MESSAGE loader by
-- renaming MESSAGE001.BIN at the DATA.SFS open by name (0x0200A540, r0 = name buffer).
-- From the battle map: taps own castle (t16,152); the CAUTION draw call there (BL at 0x02010BA4) is patched into
-- BL 0x02078760 (MESSAGE loader: r0 file, r1 unit, r2 7 = own task, r3, [sp] 1; docs/re/scenes.md).
-- Traversal (interpreter loop 0x02005798, r1 = script pc, ctx 0x02101D64 +8 = script obj 0x0211B68C, obj+0 = file
-- base): every header entry and every target of switch op 19 (`19 var <u32 offs>`, docs/re/text.md) is queued. The
-- file is started once per queued block: the first interpreter step jumps to it, its end op 01 ends the event (blocks
-- chained inside one event pile up text objects and hang after ~38 strings). Strings are logged at op 30 / 51 (the
-- draw hooks of textcover.lua miss some calls under JIT). Logs "msgall <file> done|STUCK <frame> <blocks>".
-- SPMES: pass names (SPMES001014): see duelnop below. KIND='SPMES' (numbers aaabbb, run by the duel event task
-- 0x02077910 with its file-name sprintf 0x020772E8 r2 r3 swapped) freezes the game: kept only for probing.
local SP = KIND == "SPMES"
local SITE, OBJ = 0x02010BA4, 0x0211B68C
local LOADER = SP and 0x02077910 or 0x02078760
local curbase = 0
local function bl(at, to) return 0xEB000000 + ((to - at - 8) / 4) % 0x1000000 end  -- Lua 5.1: no bit ops
local rd, rb = memory.readdword, memory.readbyte
local function r(n) return memory.getregister("arm9.r" .. n) end
local function u32(a) return rb(a) + rb(a + 1) * 0x100 + rb(a + 2) * 0x10000 + rb(a + 3) * 0x1000000 end

local files = {}
for part in FILES:gmatch("[^,%s]+") do
  local a, b = part:match("^(%d+)-(%d+)$")
  if a then for i = tonumber(a), tonumber(b) do files[#files + 1] = i end
  else files[#files + 1] = tonumber(part) or part end
end
L.log(string.format("msgall %d files", #files))
local EVENT = 0x0211A874                    -- bit 0x200 = MESSAGE task running (set by the loader, cleared on exit)

local logged = {}
local function text(p)                       -- same key as textcover.lua / tools/cover.py strhash
  local h = 0
  for i = 0, 1023 do
    local c = rb(p + i)
    if c == 0xFF then break end
    h = (h * 31 + c + 1) % 4294967291
  end
  if not logged[h] then logged[h] = true; L.log(string.format("TEXT %X", h)) end
end
local function strop(b, pc)                  -- 30 xx <u32 off>: show message; 51 <u32 off>: string argument
  local op = rb(pc)
  if op == 0x30 then text(b + u32(pc + 2)) elseif op == 0x51 then text(b + u32(pc + 1)) end
end

-- per file: queue / seen hold file offsets (the buffer can move between starts)
local fi, ORIG, armed, running, ended, fresh, lastop, lastpc, swap, blocks = 0, nil, false, false, false, false, 0, nil, nil, 0
local duel = false                           -- the running file is an SPMES duel event (see duelnop)
local queue, seen, inited, target
local function push(o, b)                    -- skip bare end ops (empty switch cases); the file is freed on exit
  if o ~= 0 and not seen[o] then seen[o] = true; if rb(b + o) ~= 0x01 then queue[#queue + 1] = o end end
end
-- SPMES duel-event files run in the MESSAGE task (renamed in like TUTO). Their portrait / unit / wait ops need a
-- real duel (under the duel task 0x02077910 the game freezes at the second speaker), so every op but 30 (line) /
-- 39 / 01 becomes the 1-byte no-op 1D (handler 0x020057EC). 39 (wait for text out + page tap, 0x020066B8) becomes
-- end op 01, and each line is queued as its own start: in the MESSAGE task a passed 39 swaps in MESSAGE001.
-- All 402 SPMES%06d files use only these ops (lengths from SPMES001014); TUTO / SPMES_APP / SPMES_TRE add 54 (4
-- bytes), TUTO 56 (6, arrow), SPMES_WR 52 (2), 53 (1), 14 (8, `14 a b c <u32 off>` branch), 06 (5, goto), 51 (5,
-- string arg: kept and queued, so every branch's fragment runs). Lengths cover all 435 SPMES* / TUTO* files; an entry
-- with any other op is left as it is.
local LEN = { [0x44] = 3, [0x50] = 2, [0x05] = 3, [0x33] = 9, [0x35] = 3, [0x36] = 7, [0x30] = 6, [0x39] = 1,
  [0x55] = 2, [0x54] = 4, [0x56] = 6, [0x52] = 2, [0x53] = 1, [0x14] = 8, [0x06] = 5, [0x51] = 5, [0x01] = 1 }
local function duelnop(b)
  for i = 0, rd(b + 4) - 1 do
    local e, pc = rd(b + 0xC + 4 * i), nil
    pc = e
    while LEN[rb(pc)] and rb(pc) ~= 0x01 do pc = pc + LEN[rb(pc)] end
    if rb(pc) ~= 0x01 then
      if not inited then L.log(string.format("duelnop: op %02X at +%X, entry %d left as is", rb(pc), pc - b, i)) end
    else
      pc = e
      while rb(pc) ~= 0x01 do
        local op, n = rb(pc), LEN[rb(pc)]
        if op == 0x30 or op == 0x51 then push(pc - b, b)    -- one start per line, like a MESSAGE block
        elseif op == 0x39 then memory.writebyte(pc, 0x01)
        else for k = 0, n - 1 do memory.writebyte(pc + k, 0x1D) end end
        pc = pc + n
      end
    end
  end
end
L.on_exec(0x02005798, function()
  -- the MESSAGE loader's script obj only; after its end op the task re-runs the script until a tap closes it
  -- SPMES: the duel event task's obj is on the heap: any obj but the MESSAGE one
  if not running or ended then return end
  local obj = rd(0x02101D64 + 8)
  if (obj == OBJ) == SP then return end
  local pc = r(1)
  if pc ~= lastpc then lastpc, lastop = pc, L.frame end   -- a waiting op re-runs at the same pc every frame
  local b = rd(obj)
  -- a loaded script file: header table relocated to file+0xC (any other obj here is not ours / not a file yet)
  if b < 0x02000000 or b >= 0x02400000 or rd(b + 8) ~= b + 0xC or rd(b + 4) > 16 then return end
  curbase = b
  if fresh then                              -- first step of this start
    fresh = false
    duel = type(files[fi]) == "string" and (files[fi]:match("^SPMES") or files[fi]:match("^TUTO")) ~= nil
    if duel then duelnop(b) end
    if not inited then
      inited = true
      local n, t = rd(b + 4), rd(b + 8)
      for i = 0, n - 1 do push(rd(t + 4 * i) - b, b) end
      seen[pc - b] = true
    elseif target then
      pc = b + target
      memory.setregister("arm9.r1", pc)
    end
    if TRACE then L.log(string.format("start %s queue %d target %s", tostring(files[fi]), #queue, tostring(target))) end
  end
  local op = rb(pc)
  if TRACE then L.log(string.format("op %02X at +%X", op, pc - b)) end
  strop(b, pc)
  if op == 0x19 then                         -- switch: table of u32 offsets (unaligned) up to the lowest target
    local tab, lo, k = pc + 2, 0x7FFFFFFF, 0
    while tab + 4 * k < lo and k < 256 do
      local o = u32(tab + 4 * k)
      if o ~= 0 then lo = math.min(lo, b + o); push(o, b) end
      k = k + 1
    end
  elseif op == 0x01 then ended = L.frame end
end)

L.on_exec(0x0200A540, function()             -- rename MESSAGE001.BIN to the wanted script file
  if not swap then return end
  local p, s = r(0), {}
  for i = 0, 15 do local c = rb(p + i); if c == 0 then break end; s[#s + 1] = string.char(c) end
  if table.concat(s) ~= "MESSAGE001.BIN" then return end
  local name = swap .. ".BIN"
  for i = 1, #name do memory.writebyte(p + i - 1, name:byte(i)) end
  memory.writebyte(p + #name, 0)   -- swap stays on: the loader opens the file more than once
end)

local function arm(next_file)
  if next_file then
    fi = fi + 1
    if fi > #files then L.log("msgall all done " .. L.frame); L.finish(0) end
    queue, seen, inited, blocks, swap = {}, {}, false, 0, nil
  end
  ORIG = ORIG or rd(SITE)
  memory.writedword(SITE, bl(SITE, LOADER))
  armed = true
end
L.on_exec(SITE, function()
  if not armed then return end
  armed = false
  local f = files[fi]
  ended, fresh, lastop, lastpc, running = false, true, L.frame, nil, true
  blocks = blocks + 1
  if SP then memory.setregister("arm9.r0", 0); memory.setregister("arm9.r1", 0); return end
  if type(f) == "string" then swap = f; f = 1 end
  memory.setregister("arm9.r0", f); memory.setregister("arm9.r1", 0); memory.setregister("arm9.r2", 7)
  memory.setregister("arm9.r3", 0); memory.writedword(r(13), 1)
end)
L.on_exec(SITE + 4, function() if ORIG then memory.writedword(SITE, ORIG) end end)
L.on_exec(0x020772E8, function()             -- SPMES%03d%03d sprintf
  if SP and running then
    local f = files[fi]
    memory.setregister("arm9.r2", math.floor(f / 1000)); memory.setregister("arm9.r3", f % 1000)
  end
end)

local TAP, GAP = TAP or "t16,152", GAP or 20
L.on_frame(function(n)
  if n == 1 then arm(true) end
  if running then
    local busy = SP and ended and n - ended < 120 or not SP and math.floor(rd(EVENT) / 0x200) % 2 == 1
    local stuck = not ended and n - lastop > (MAXIDLE or 600) or ended and n - ended > (MAXIDLE or 600)
    if (ended and not busy) or stuck then
      running = false
      if stuck then   -- the scene is often broken after this: exit, tools/msgcover.py restarts after this file
        L.log(string.format("msgall %s STUCK %d at +%X", files[fi], n, (lastpc or 0) - curbase)); L.finish(3)
      end
      target = table.remove(queue, 1)
      if target then arm(false) else
        L.log(string.format("msgall %s done %d %d", files[fi], n, blocks)); arm(true)
      end
    end
  end
  local quiet = running and not ended and (duel or n - lastop < (SP and 250 or 0) and lastpc == nil)
  if n % GAP == 0 and not quiet then L.press(TAP, HOLD or 8) end
end)
