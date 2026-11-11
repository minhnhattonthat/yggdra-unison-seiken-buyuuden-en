-- fumfac.lua: force the faction of the rumor screen 風聞 (task 0x0208ED54(n): FUM_TI<faction %02d><'A'+n>.PACK title,
-- FUM<faction><letter> paragraph; game calls it after a story battle, 0x02080908). With spmes.lua CALL=0x0208ED54 R0=n:
--   emu.py build/yggdra_en.nds --state-in work/states/battle.dst --script tools/lua/spmes.lua --var CALL=0x0208ED54
--     --var R0=0 --script tools/lua/fumfac.lua --var FAC=1 --route-str "100 -;10 t16,152;600 -" --shot-every 60
-- Both sprintf calls take the faction from 0x02043464; r0 is overwritten at the `mov r2, r0` after each.
-- LETTER='B' also swaps the letter (r5 = 'A'+n, the sprintf's r3): shows the B/D/E textures in the mode-A layout
-- (modes 1/3/4 draw behind the battle BG in this forced view; their quads match mode A: docs/re/scenes.md).
for _, at in ipairs({0x0208EF94, 0x0208EFEC}) do
  L.on_exec(at, function()
    memory.setregister("arm9.r0", FAC or 0)
    if LETTER then memory.setregister("arm9.r5", string.byte(LETTER)) end
    L.log(string.format("fum %08X fac %d %s", at, FAC or 0, LETTER or ""))
  end)
end
