"""engine.py: arm9 code patches (VWF). docs/re/text.md "VWF".

Hook code + the 4x256 width table (tools/enfont.py) go after the ITCM autoload block's bss (0x01FFBDC0): the ITCM
section grows by bss + code, its bss becomes 0 (the zeros are now copied in). Each hook site is checked against its
original instruction before it is overwritten.
"""
import ndspy.code
from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks

ITCM = 0x01FF8000
DRAW = 0x0210E768  # system/centred text state: +0 glyph buffer, +4 u16 codes (code | font << 12), +0xA count

HOOKS = f"""
    b glyph_cell               @ entry +0 (sites BL to the entries; lr returns to the site)
    b hook_step                @ entry +4
    b pack_ctr                 @ entry +8 (function entries B here: lr is the caller's)
    b cells_count              @ entry +C
    b ov_adv                   @ entry +10
    b pack_run                 @ entry +14
    b hook_qw                  @ entry +18
    b count11                  @ entry +1C
    b lines_px                 @ entry +20
    b lines_px12               @ entry +24

ov_adv:                      @ ov9_15 0x0211DC8C add r4,r4,#0xB (ending epilogue, one glyph per 0x02012FFC call)
    push {{lr}}                   @ r7 = glyph code, fp = font id; r0-r3/ip are free here
    orr r0, r7, fp, lsl #12
    mov r1, #0xB
    bl width
    add r4, r4, r0
    pop {{pc}}

@ Dialogue text objects (0x020128B8, FONT_MES) get one 16x16 slot per glyph, and a scene's slot range is sized for
@ the Japanese (ending: 32). Instead each line is packed into 16 px cells: glyphs are blitted at their VWF pen x,
@ and a cell (slot + x/y/colour entry) is opened only when a glyph's visible pixels reach it.
@ state: +0 last cell (block) opened on this line, +4 y of that line, +8 last block of the current glyph.

cells_count:                 @ 0x02012904 bl 0x02013274: r0 = string, r1 = u8 per-line counts, r2 = lines -> cells
    push {{r4, r5, r6, r7, r8, r9, lr}}
    ldr r3, =state
    mvn ip, #0
    str ip, [r3]
    ldr ip, =0x7FFF
    str ip, [r3, #4]
    mov ip, #0
    cmp r0, #0
    beq cc_done
    mov r4, #0                 @ line
    mov r5, #0                 @ pen x
    mvn r6, #0                 @ last block opened
cc_loop:
    ldrb r3, [r0], #1
    cmp r3, #0xFF
    beq cc_done
    cmp r3, #0xFD
    addeq r4, r4, #1
    moveq r5, #0
    mvneq r6, #0
    beq cc_loop
    cmp r3, #0xFC
    addeq r0, r0, #1
    beq cc_loop
    mov r7, #11                @ advance
    mov r8, #16                @ visible width
    sub r9, r3, #0xF1
    cmp r9, #8
    addls r0, r0, #1           @ F1-F9 xx: a Japanese glyph, game metrics
    bls cc_have
    ldr r9, =wtab + 0x100
    ldrb r9, [r9, r3]
    cmp r9, #0
    beq cc_have
    mov r7, r9
    ldr r9, =vtab
    ldrb r8, [r9, r3]
cc_have:
    cmp r8, #0
    beq cc_adv
    add r8, r5, r8
    sub r8, r8, #1
    mov r8, r8, asr #4
    mov r9, r5, asr #4
cc_blk:
    cmp r9, r6
    ble cc_nb
    mov r6, r9
    add ip, ip, #1
    cmp r4, r2
    ldrblt r3, [r1, r4]
    addlt r3, r3, #1
    strblt r3, [r1, r4]
cc_nb:
    add r9, r9, #1
    cmp r9, r8
    ble cc_blk
cc_adv:
    add r5, r5, r7
    b cc_loop
cc_done:
    mov r0, ip
    pop {{r4, r5, r6, r7, r8, r9, pc}}

glyph_cell:                  @ 0x02012B0C (then b 0x02012A74): r1 = glyph, r8 = text object; sb/sl = slot ptr/bytes
    push {{r4, r5, r6, r7, lr}}
    mov r4, r1
    mov r5, #11
    mov r6, #16
    cmp r4, #0x100
    bhs gc_read
    ldr r3, =wtab + 0x100
    ldrb r0, [r3, r4]
    cmp r0, #0
    beq gc_read
    mov r5, r0
    ldr r3, =vtab
    ldrb r6, [r3, r4]
gc_read:
    ldr r0, [r8, #0x18]
    mov r1, r4, lsl #7
    mov r2, #0
    bl #0x1ffacdc              @ seek the font file to the glyph
    ldr r0, [r8, #0x18]
    ldr r1, =gbuf
    mov r2, #0x80
    bl #0x1ffaf1c              @ read it into gbuf
    ldr r7, =state
    ldrsh r0, [r8, #0x26]
    ldr r1, [r7, #4]
    cmp r0, r1
    strne r0, [r7, #4]
    mvnne r1, #0
    strne r1, [r7]
    ldrsh r4, [r8, #0x24]      @ pen x
    cmp r6, #0
    beq gc_adv
    mov r0, r4, asr #4
    add r1, r4, r6
    sub r1, r1, #1
    mov r1, r1, asr #4
    str r1, [r7, #8]
gc_blk:                        @ r0 = block
    ldr r2, [r7]
    cmp r0, r2
    ble gc_have
    str r0, [r7]
    mov r2, #0
    mov r3, #0x80
gc_zero:
    subs r3, r3, #4
    strge r2, [sb, r3]
    bgt gc_zero
    ldrb r3, [r8, #0x2c]
    mov ip, r3, lsl #1
    mov r1, r0, lsl #4
    ldr r2, [r8, #8]
    strh r1, [r2, ip]
    ldrsh r1, [r8, #0x26]
    ldr r2, [r8, #0xc]
    strh r1, [r2, ip]
    ldrh r1, [r8, #0x2a]
    ldr r2, [r8, #0x10]
    strh r1, [r2, ip]
    add r3, r3, #1
    strb r3, [r8, #0x2c]
    add sb, sb, #0x80
    add sl, sl, #0x80
gc_have:
    ldr r2, [r7]
    sub r2, r2, r0
    add r2, r2, #1
    sub r3, sb, r2, lsl #7     @ r3 = this block's cell
    rsb r2, r4, r0, lsl #4     @ glyph column = cell column + r2
    push {{r0, r4, r5, r6}}
    ldr r4, =gbuf
    mov r5, #0
gc_row:
    mov r6, #0
gc_col:
    adds r0, r6, r2
    bmi gc_next
    cmp r0, #16
    bge gc_next
    add r1, r4, r5, lsl #3
    ldrb r1, [r1, r0, lsr #1]
    tst r0, #1
    movne r1, r1, lsr #4
    ands r1, r1, #0xF
    beq gc_next
    add r0, r3, r5, lsl #3
    add r0, r0, r6, lsr #1
    ldrb ip, [r0]
    tst r6, #1
    biceq ip, ip, #0xF
    orreq ip, ip, r1
    bicne ip, ip, #0xF0
    orrne ip, ip, r1, lsl #4
    strb ip, [r0]
gc_next:
    add r6, r6, #1
    cmp r6, #16
    blt gc_col
    add r5, r5, #1
    cmp r5, #16
    blt gc_row
    pop {{r0, r4, r5, r6}}
    ldr r1, [r7, #8]
    add r0, r0, #1
    cmp r0, r1
    ble gc_blk
gc_adv:
    add r4, r4, r5
    strh r4, [r8, #0x24]
    ldr r0, [r8, #4]
    add r0, r0, #1
    str r0, [r8, #4]
    pop {{r4, r5, r6, r7, pc}}

hook_step:                   @ 0x02012D10 ldr r0,[sp,#0x18] (run draw 0x02012C10): r6 = slot << 7
    ldr r0, ={DRAW:#x}
    ldr r0, [r0, #4]
    mov r1, r6, lsr #7
    add r0, r0, r1, lsl #1
    ldrh r0, [r0]
    cmp r0, #0xC000            @ packed cell (pack_run): cells sit 16 px apart
    movhs r0, #16
    bxhs lr
    ldr r1, [sp, #0x18]
    b width

hook_qw:                     @ 0x02012D08 mov r3,#0xC in the run draw: quad width 16 for a packed cell, else 12
    push {{r0, r1, r2, lr}}
    ldr r0, ={DRAW:#x}
    ldr r0, [r0, #4]
    mov r1, r6, lsr #7
    add r0, r0, r1, lsl #1
    ldrh r0, [r0]
    cmp r0, #0xC000
    movhs r3, #16
    movlo r3, #12
    pop {{r0, r1, r2, pc}}

@ System text (run 0x02012DF4, centred 0x020130AC) is redrawn every frame, one slot per glyph, slot cached by
@ codes[slot] == glyph. Packed instead: each segment (text between FD / FC / FF) is blitted into 16 px cells at VWF
@ pen x (every block from 0 to the last one reached gets a cell). Cell cache: codes[slot] = 0xC000 | key & 0x1FFF
@ (no game code or glyph-search key reaches 0xC000) and slotkey[slot] = key (FNV over code, font, x in the cell).
@ Slots past the pool capacity are not drawn (one glyph per slot overran the pool and crashed).
@ ps: +0 x0 +4 y +8 z +C font +10 param +14 centred +18 segment x (run) +1C total px +20 segment start
@ +28 segment px +34/+38 miss mask +3C default advance +40 adv for 0x02012C10 +44 break +48 x +4C break ptr
@ +50 adv +54 code +58 glyph read
pack_run:                    @ 0x02012DF4: r0 x, r1 y, r2 z, r3 string, [sp] font (u8), [sp+4] param
    ldr ip, =ps
    stm ip, {{r0, r1, r2}}
    ldrb r0, [sp]
    str r0, [ip, #0xC]
    ldr r0, [sp, #4]
    str r0, [ip, #0x10]
    mov r0, #0
    str r0, [ip, #0x14]
    mov r0, r3
    b pack
pack_ctr:                    @ 0x020130AC: r0 y, r1 z, r2 string, r3 font, [sp] param; x = 0x80 - px / 2 per line
    ldr ip, =ps
    str r0, [ip, #4]
    str r1, [ip, #8]
    str r3, [ip, #0xC]
    ldr r0, [sp]
    str r0, [ip, #0x10]
    mov r0, #1
    str r0, [ip, #0x14]
    mov r0, #0
    str r0, [ip]
    mov r0, r2
pack:                          @ -> r0 = ceil(total px / 11) (a glyph count for callers sizing highlight bars)
    push {{r4, r5, r6, r7, r8, r9, r10, r11, lr}}
    ldr r11, =ps
    movs r4, r0
    beq pk_ret
    ldr r0, [r11, #0xC]
    and r0, r0, #3
    str r0, [r11, #0xC]
    ldr r1, [r11, #0x14]
    cmp r1, #0
    ldreq r2, =0x0208F9C0
    ldrbeq r2, [r2, r0]
    movne r2, #0xC
    str r2, [r11, #0x40]
    sub r2, r2, #1
    str r2, [r11, #0x3C]
    ldr r0, [r11]
    str r0, [r11, #0x18]
    mov r0, #0
    str r0, [r11, #0x1C]
pk_seg:                        @ pass 1: block keys, r5 pen, r6 blocks
    str r4, [r11, #0x20]
    mov r5, #0
    mov r6, #0
pk_p1:
    bl glyph_at
    cmp r0, #0x10000
    bhs pk_p1end
    cmp r2, #0
    beq pk_p1adv
    mov r7, r5, asr #4
    add r8, r5, r2
    sub r8, r8, #1
    mov r8, r8, asr #4
    cmp r8, #63
    movgt r8, #63
    ldr r9, =keys
pk_p1b:
    cmp r7, r8
    bgt pk_p1adv
pk_p1i:
    cmp r6, r7
    bgt pk_p1k
    ldr r10, =0x811C9DC5
    str r10, [r9, r6, lsl #2]
    add r6, r6, #1
    b pk_p1i
pk_p1k:
    ldr r10, [r11, #0xC]
    orr r10, r0, r10, lsl #12
    sub r3, r5, r7, lsl #4
    and r3, r3, #0xFF
    orr r10, r10, r3, lsl #16
    ldr r3, [r9, r7, lsl #2]
    eor r3, r3, r10
    ldr r10, =16777619
    mul r3, r10, r3
    str r3, [r9, r7, lsl #2]
    add r7, r7, #1
    b pk_p1b
pk_p1adv:
    add r5, r5, r1
    b pk_p1
pk_p1end:
    str r0, [r11, #0x44]
    str r5, [r11, #0x28]
    ldr r1, [r11, #0x1C]
    add r1, r1, r5
    str r1, [r11, #0x1C]
    ldr r1, [r11, #0x14]
    cmp r1, #0
    ldreq r7, [r11, #0x18]
    movne r7, #0x80
    subne r7, r7, r5, asr #1
    str r7, [r11, #0x48]
    ldr r9, ={DRAW:#x}             @ pass 2: r8 used, r6 = cells that fit, cache check
    ldrh r8, [r9, #0xA]
    ldrh r1, [r9, #8]
    sub r1, r1, r8
    cmp r6, r1
    movgt r6, r1
    cmp r6, #0
    movlt r6, #0
    mov r0, #0
    str r0, [r11, #0x34]
    str r0, [r11, #0x38]
    mov r5, #0
pk_p2:
    cmp r5, r6
    bge pk_p2end
    add r2, r8, r5
    ldr r3, =keys
    ldr r3, [r3, r5, lsl #2]
    mov r0, r3, lsl #19
    mov r0, r0, lsr #19
    orr r0, r0, #0xC000
    ldr r1, [r9, #4]
    add r1, r1, r2, lsl #1
    ldr r10, =slotkey
    ldrh ip, [r1]
    cmp ip, r0
    bne pk_miss
    cmp r2, #512
    bhs pk_miss
    ldr ip, [r10, r2, lsl #2]
    cmp ip, r3
    beq pk_p2n
pk_miss:
    strh r0, [r1]
    cmp r2, #512
    strlo r3, [r10, r2, lsl #2]
    ldr r0, [r9]
    add r0, r0, r2, lsl #7
    mov r1, #0
    mov ip, #0x80
pk_z:
    subs ip, ip, #4
    str r1, [r0, ip]
    bne pk_z
    and r0, r5, #31
    mov r1, #1
    mov r1, r1, lsl r0
    mov r0, r5, lsr #5
    add r0, r11, r0, lsl #2
    ldr ip, [r0, #0x34]
    orr ip, ip, r1
    str ip, [r0, #0x34]
pk_p2n:
    add r5, r5, #1
    b pk_p2
pk_p2end:                      @ pass 3: blit each glyph into its missed cells
    ldr r0, [r11, #0x34]
    ldr r1, [r11, #0x38]
    orrs r0, r0, r1
    beq pk_draw
    str r4, [r11, #0x4C]
    ldr r4, [r11, #0x20]
    mov r5, #0
pk_p3:
    bl glyph_at
    cmp r0, #0x10000
    bhs pk_p3end
    cmp r2, #0
    beq pk_p3adv
    str r1, [r11, #0x50]
    str r0, [r11, #0x54]
    mov r7, r5, asr #4
    add r10, r5, r2
    sub r10, r10, #1
    mov r10, r10, asr #4
    sub r3, r6, #1
    cmp r10, r3
    movgt r10, r3
    mov r0, #0
    str r0, [r11, #0x58]
pk_p3b:
    cmp r7, r10
    bgt pk_p3adv0
    mov r0, r7, lsr #5
    add r0, r11, r0, lsl #2
    ldr r0, [r0, #0x34]
    and r1, r7, #31
    mov r0, r0, lsr r1
    tst r0, #1
    beq pk_p3nb
    ldr r0, [r11, #0x58]
    cmp r0, #0
    bne pk_p3have
    mov r0, #1
    str r0, [r11, #0x58]
    ldr r0, [r11, #0xC]
    ldr r1, [r11, #0x54]
    ldr r2, =gbuf
    bl #0x2012130              @ glyph (font r0, code r1) -> gbuf
pk_p3have:
    ldr r0, [r9]
    add r1, r8, r7
    add r0, r0, r1, lsl #7
    rsb r1, r5, r7, lsl #4
    bl blit
pk_p3nb:
    add r7, r7, #1
    b pk_p3b
pk_p3adv0:
    ldr r1, [r11, #0x50]
pk_p3adv:
    add r5, r5, r1
    b pk_p3
pk_p3end:
    ldr r4, [r11, #0x4C]
pk_draw:
    cmp r6, #0
    beq pk_brk
    sub sp, sp, #0x10
    str r8, [sp]
    ldr r0, [r11, #0x10]
    str r0, [sp, #4]
    ldr r0, [r11, #0x40]
    str r0, [sp, #8]
    ldr r0, [r11, #0x48]
    ldr r1, [r11, #4]
    ldr r2, [r11, #8]
    mov r3, r6
    bl #0x2012c10              @ run draw: r6 quads from slot r8
    add sp, sp, #0x10
    add r8, r8, r6
    strh r8, [r9, #0xA]
pk_brk:
    ldr r0, [r11, #0x44]
    and r0, r0, #0xFF
    cmp r0, #0xFF
    beq pk_end
    add r4, r4, #1
    cmp r0, #0xFD
    bne pk_fc
    ldr r3, [r11, #4]
    add r3, r3, #0xF
    str r3, [r11, #4]
    ldr r3, [r11]
    str r3, [r11, #0x18]
    b pk_seg
pk_fc:                         @ FC xx: colour from 0x0209281C, the line goes on after this segment
    ldr r1, [r11, #0x48]
    ldr r2, [r11, #0x28]
    add r1, r1, r2
    str r1, [r11, #0x18]
    ldrb r0, [r4], #1
    ldr r1, =0x0209281C
    mov r0, r0, lsl #1
    ldrh r0, [r1, r0]
    ldr r1, =0x04000480
    str r0, [r1]
    b pk_seg
pk_end:
    ldr r0, [r11, #0x1C]
    add r0, r0, #10
    ldr r1, =5958
    mul r2, r0, r1
    mov r4, r2, lsr #16
pk_ret:
    mov r0, r4
    pop {{r4, r5, r6, r7, r8, r9, r10, r11, pc}}

count11:                     @ 0x02013224 glyph count: callers (ov9_06/07/10/15) lay out boxes / centring as 11 x n
    push {{r4, r5, r11, lr}}     @ -> ceil(px / 11), px from the font 0 advances
    ldr r11, =ps
    movs r4, r0
    beq c11_done
    mov r0, #0
    str r0, [r11, #0xC]
    mov r0, #11
    str r0, [r11, #0x3C]
    mov r5, #0
c11_loop:
    bl glyph_at
    cmp r0, #0x10000
    addlo r5, r5, r1
    blo c11_loop
    and r0, r0, #0xFF
    cmp r0, #0xFF
    beq c11_end
    add r4, r4, #1
    cmp r0, #0xFC
    addeq r4, r4, #1
    b c11_loop
c11_end:
    add r0, r5, #10
    ldr r1, =5958
    mul r2, r0, r1
    mov r0, r2, lsr #16
c11_done:
    pop {{r4, r5, r11, pc}}

@ 0x02013274 contract (r0 string, r1 u8 per-line counts, each += n, r2 lines -> r0 total) for callers that centre
@ a line at 128 - 11 n / 2 (HINT! tips, info band 0x0210E672, territory): n = round(line px / 11), not glyphs.
lines_px12:                  @ the same for a caller laying out 12 x n (ov9_10 medallion line)
    push {{r4, r5, r6, r7, r8, r9, r10, r11, lr}}
    mov r9, #12
    b lp_go
lines_px:
    push {{r4, r5, r6, r7, r8, r9, r10, r11, lr}}
    mov r9, #11
lp_go:
    ldr r11, =ps
    movs r4, r0
    beq lp_ret
    mov r6, r1
    mov r7, r2
    mov r0, #0
    str r0, [r11, #0xC]
    mov r0, #11
    str r0, [r11, #0x3C]
    mov r8, #0                 @ line
    mov r5, #0                 @ line px
    mov r10, #0                @ total
lp_loop:
    bl glyph_at
    cmp r0, #0x10000
    addlo r5, r5, r1
    blo lp_loop
    and r0, r0, #0xFF
    add r4, r4, #1
    cmp r0, #0xFC
    addeq r4, r4, #1
    cmpne r0, #0xFE
    beq lp_loop
    add r1, r5, r9, lsr #1     @ FD / FF ends a line: n = (px + d / 2) / d
    mov r2, #0
lp_div:
    cmp r1, r9
    subhs r1, r1, r9
    addhs r2, r2, #1
    bhs lp_div
    add r10, r10, r2
    cmp r8, r7
    ldrblt r1, [r6, r8]
    addlt r1, r1, r2
    strblt r1, [r6, r8]
    add r8, r8, #1
    mov r5, #0
    cmp r0, #0xFF
    bne lp_loop
    mov r0, r10
lp_ret:
    pop {{r4, r5, r6, r7, r8, r9, r10, r11, pc}}

glyph_at:                    @ r4 = string -> r0 code (0x100xx = break byte FC-FF, r4 stays), r1 advance, r2 visible
    ldrb r0, [r4]
    cmp r0, #0xFC
    orrhs r0, r0, #0x10000
    bxhs lr
    add r4, r4, #1
    sub r1, r0, #0xF1
    cmp r1, #8
    bhi ga_one
    ldrb r2, [r4], #1
    add r1, r1, #1
    mov r3, #0xF0
    mla r0, r1, r3, r2
ga_one:
    ldr r1, [r11, #0x3C]
    mov r2, #12                @ the game shows 12 columns of a glyph
    cmp r0, #0x100
    bxhs lr
    ldr r3, [r11, #0xC]
    ldr ip, =wtab
    add ip, ip, r3, lsl #8
    ldrb r3, [ip, r0]
    cmp r3, #0
    bxeq lr
    mov r1, r3
    ldr ip, =vtab
    ldrb r2, [ip, r0]
    bx lr

blit:                        @ gbuf glyph into cell r0: cell column c takes glyph column c + r1 (ink only)
    push {{r4, r5, r6, r7, lr}}
    ldr r4, =gbuf
    mov r5, #0
bl_row:
    mov r6, #0
bl_col:
    adds r2, r6, r1
    bmi bl_next
    cmp r2, #16
    bge bl_next
    add r3, r4, r5, lsl #3
    ldrb r3, [r3, r2, lsr #1]
    tst r2, #1
    movne r3, r3, lsr #4
    ands r3, r3, #0xF
    beq bl_next
    add r7, r0, r5, lsl #3
    add r7, r7, r6, lsr #1
    ldrb ip, [r7]
    tst r6, #1
    biceq ip, ip, #0xF
    orreq ip, ip, r3
    bicne ip, ip, #0xF0
    orrne ip, ip, r3, lsl #4
    strb ip, [r7]
bl_next:
    add r6, r6, #1
    cmp r6, #16
    blt bl_col
    add r5, r5, #1
    cmp r5, #16
    blt bl_row
    pop {{r4, r5, r6, r7, pc}}

width:                       @ r0 = code | font << 12, r1 = default -> r0 = advance
    mov r2, r0, lsr #12
    and r2, r2, #3
    bic r0, r0, #0xF000
    cmp r0, #0x100
    bhs width_def
    ldr r3, =wtab
    add r3, r3, r2, lsl #8
    ldrb r0, [r3, r0]
    cmp r0, #0
    bxne lr
width_def:
    mov r0, r1
    bx lr
.ltorg
wtab:                          @ filled from enfont.patched_fonts: 4x256 advances, then vtab
.space 0x400
vtab:
.space 0x100
state:
.space 0x10
gbuf:
.space 0x80
ps:
.space 0x60
keys:
.space 0x100
slotkey:
.space 0x800
"""
TAIL = 0x590 + 0x960  # wtab .. end of slotkey (zeros; wtab + vtab filled in)

SITES = [  # (address, original instruction word, entry offset, or an instruction to put there)
    (0x02012904, 0xEB00025A, 0xC),       # bl 0x02013274 (glyph count) -> cells_count
    (0x02012B0C, 0xE5980018, 0),         # dialogue glyph: ldr r0,[r8,#0x18] -> bl glyph_cell
    (0x02012B10, 0xE1A02005, "b #0x2012a74"),  # mov r2,r5 -> back to the loop top
    (0x02012784, 0xE3A0300C, "mov r3, #0x10"),  # dialogue quad width 12 -> 16, so a whole cell shows
    (0x02012D10, 0xE59D0018, 4),         # run draw step: x += VWF advance (16 per packed cell)
    (0x02012D08, 0xE3A0300C, 0x18),      # run draw quad width: 16 for a packed cell
    (0x02012DF4, 0xE92D4FF0, ("b", 0x14)),  # system text run -> pack_run (whole function replaced)
    (0x020130AC, 0xE92D4FF8, ("b", 0x8)),   # centred system text -> pack_ctr
    (0x02013224, 0xE3500000, ("b", 0x1C)),  # glyph count (layout 11 x n) -> count11 = ceil(px / 11)
    (0x0200FDB4, 0xEB000D2E, 0x20),      # info band per-line counts (0x0210E672, centred 128 - 11 n / 2) -> lines_px
    (0x02010770, 0xEB000ABF, 0x20),      # the same, option menu band (0x0201038C: unlock message)
    (0x02080258, 0xEBFE4C05, 0x20),      # HINT! tip line 1 centring -> lines_px
    (0x020802E8, 0xEBFE4BE1, 0x20),      # HINT! tip line 2
]
OV_SITES = [  # (overlay image, address, original word, entry offset or instruction): overlays load at 0x0211B780
    ("ov9_15", 0x0211DC8C, 0xE284400B, 0x10),  # EDMES epilogue text: fixed 11 px advance -> VWF
    ("ov9_15", 0x0211E004, 0xE3A00066, "mov r0, #0x42"),  # EDMES epithet run x 102 -> 66, over the 称号： label
    ("ov9_10", 0x0211C004, 0xEBFBDC9A, 0x24),  # medallion line: 0x02013274 -> lines_px12 (centred 128 - 12 n / 2)
    ("ov9_14", 0x0211CF58, 0xEBFBD8C5, 0x20),  # territory captured line 2: -> lines_px
    ("ov9_14", 0x0211CFE0, 0xEBFBD8A3, 0x20),  # capital taken line 2: -> lines_px
    ("ov9_18", 0x0211EE38, 0xE3A000A2, "mov r0, #0xa1"),  # unlock-terms count digit x 162 -> 161: centred in the
    # English header's 5-space gap ("any 4of" touched at 162 / 4 spaces; ov9_18:3D58)
]
OV_BASE = 0x0211B780


def entries(arm9):
    """Address of the hook entry table (start of the HOOKS blob) for this original arm9."""
    code = ndspy.code.MainCodeFile(arm9, 0x02000000)
    itcm = next(s for s in code.sections if s.ramAddress == ITCM)
    return ITCM + len(itcm.data) + itcm.bssSize


def patch_overlays(images, at):
    """{image: bytes} -> the OV_SITES overlays with their hooks; at = entries(original arm9)."""
    out = {}
    for img, site, orig, entry in OV_SITES:
        data = bytearray(out.get(img, images[img]))
        off = site - OV_BASE
        assert int.from_bytes(data[off:off + 4], "little") == orig, f"{img} {site:#x}: unexpected original instruction"
        data[off:off + 4] = asm(entry if isinstance(entry, str) else f"bl #{at + entry:#x}", site)
        out[img] = bytes(data)
    return out


def asm(src, addr):
    enc, _ = Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(src, addr)
    return bytes(enc)


ARENA_LO = {0x02025088: 0x02123460, 0x02025094: 0x01FFBDC0}  # OS_GetInitArenaLo literals: main, ITCM


def patch_arm9(arm9, wtab, extra=b""):
    """VWF hooks into ITCM; extra = relocated system strings (tools/sysreloc.py), a new autoload section at
    sysreloc.EXTRA. Both arena lo literals move past what we add, so no heap is ever placed over it."""
    import sysreloc
    code = ndspy.code.MainCodeFile(arm9, 0x02000000)
    main, itcm = code.sections[0], next(s for s in code.sections if s.ramAddress == ITCM)
    at = ITCM + len(itcm.data) + itcm.bssSize
    blob = asm(HOOKS, at)
    assert len(wtab) == 0x500 and not any(blob[-TAIL:])
    blob = blob[:-TAIL] + wtab + blob[-TAIL + len(wtab):]
    itcm.data = bytes(itcm.data) + bytes(itcm.bssSize) + blob
    itcm.bssSize = 0
    assert at + len(blob) <= 0x02000000 - 0x1000, "ITCM full"  # top 4 KB kept clear (unchecked)
    lo = {0x02025094: (at + len(blob) + 31) & ~31}
    if extra:
        code.sections.append(ndspy.code.MainCodeFile.Section(bytes(extra), sysreloc.EXTRA, 0, implicit=False))
        lo[0x02025088] = (sysreloc.EXTRA + len(extra) + 31) & ~31
        assert lo[0x02025088] <= 0x02140000, "EXTRA block over 120 KB: check the heap still fits"
    data = bytearray(main.data)
    for a, v in lo.items():
        assert int.from_bytes(data[a - 0x02000000:a - 0x02000000 + 4], "little") == ARENA_LO[a]
        data[a - 0x02000000:a - 0x02000000 + 4] = v.to_bytes(4, "little")
    for site, orig, entry in SITES:
        off = site - 0x02000000
        assert int.from_bytes(data[off:off + 4], "little") == orig, f"{site:#x}: unexpected original instruction"
        src = entry if isinstance(entry, str) else f"{entry[0]} #{at + entry[1]:#x}" if isinstance(entry, tuple) \
            else f"bl #{at + entry:#x}"
        data[off:off + 4] = asm(src, site)
    main.data = bytes(data)
    return code.save()
