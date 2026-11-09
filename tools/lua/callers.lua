-- callers.lua: log each distinct caller (lr) of the functions in ADDRS, with the first frame it was seen.
--   emu.py ... --script tools/lua/callers.lua --var "ADDRS={0x01FFAF1C,0x02012C10}"
-- Used to find which draw routine renders a text (docs/re/text.md "Draw routines").
local frame = 0
L.on_frame(function(n) frame = n end)
local seen = {}
for _, a in ipairs(ADDRS or {}) do
  L.on_exec(a, function()
    local lr = memory.getregister("arm9.r14")
    local k = string.format("%08X<-%08X", a, lr)
    if not seen[k] then
      seen[k] = true
      L.log(string.format("call %d %s r0=%08X r1=%08X r2=%08X", frame, k, memory.getregister("arm9.r0"),
        memory.getregister("arm9.r1"), memory.getregister("arm9.r2")))
    end
  end)
end
