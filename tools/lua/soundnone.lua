-- soundnone.lua: sound mode with no track selected, so the top screen shows "Touch a sound." (ov9_06:3FD4).
--   emu.py build/yggdra_en.nds --out work/qa/cover2/sound_none --state-in work/states/extras.dst
--          --script tools/lua/textcover.lua --script tools/lua/soundnone.lua --route-str "30 -;6 t128,98;400 -" --frames 420
-- Sound mode always starts on a track; ov9_06 0x0211DA64 draws the prompt when the index [0x0211FE10] is -1.
L.on_frame(function(n)
  if n >= 200 and n < 400 then memory.writeword(0x0211FE10, 0xFFFF) end
  if n == 300 then L.shot("touch_a_sound.png") end
end)
