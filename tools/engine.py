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
    b hook_center              @ entry +8
    b cells_count              @ entry +C
    b ov_adv                   @ entry +10

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
    ldr r1, [sp, #0x18]
    b width

hook_center:                 @ 0x02013114 / 0x020131C8 mul r0,r5,r0 (r0 = 0xB): r0 = px of the r5 glyphs queued
    push {{r4, r5, r6, lr}}
    ldr r1, ={DRAW:#x}
    ldrh r4, [r1, #0xA]
    ldr r6, [r1, #4]
    add r6, r6, r4, lsl #1
    mov r4, #0
center_loop:
    subs r5, r5, #1
    blt center_done
    ldrh r0, [r6], #2
    mov r1, #0xB
    bl width
    add r4, r4, r0
    b center_loop
center_done:
    mov r0, r4
    pop {{r4, r5, r6, pc}}

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
"""
TAIL = 0x590  # wtab .. end of gbuf

SITES = [  # (address, original instruction word, entry offset, or an instruction to put there)
    (0x02012904, 0xEB00025A, 0xC),       # bl 0x02013274 (glyph count) -> cells_count
    (0x02012B0C, 0xE5980018, 0),         # dialogue glyph: ldr r0,[r8,#0x18] -> bl glyph_cell
    (0x02012B10, 0xE1A02005, "b #0x2012a74"),  # mov r2,r5 -> back to the loop top
    (0x02012784, 0xE3A0300C, "mov r3, #0x10"),  # dialogue quad width 12 -> 16, so a whole cell shows
    (0x02012D10, 0xE59D0018, 4),
    (0x02013114, 0xE0000095, 8),
    (0x020131C8, 0xE0000095, 8),
]
OV_SITES = [  # (overlay image, address, original word, entry offset): overlays load at 0x0211B780
    ("ov9_15", 0x0211DC8C, 0xE284400B, 0x10),  # EDMES epilogue text: fixed 11 px advance -> VWF
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
        data[off:off + 4] = asm(f"bl #{at + entry:#x}", site)
        out[img] = bytes(data)
    return out


def asm(src, addr):
    enc, _ = Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(src, addr)
    return bytes(enc)


def patch_arm9(arm9, wtab):
    code = ndspy.code.MainCodeFile(arm9, 0x02000000)
    main, itcm = code.sections[0], next(s for s in code.sections if s.ramAddress == ITCM)
    at = ITCM + len(itcm.data) + itcm.bssSize
    blob = asm(HOOKS, at)
    assert len(wtab) == 0x500 and not any(blob[-TAIL:])
    blob = blob[:-TAIL] + wtab + blob[-TAIL + len(wtab):]
    itcm.data = bytes(itcm.data) + bytes(itcm.bssSize) + blob
    itcm.bssSize = 0
    assert at + len(blob) <= 0x02000000 - 0x1000, "ITCM full"  # top 4 KB kept clear (unchecked)
    data = bytearray(main.data)
    for site, orig, entry in SITES:
        off = site - 0x02000000
        assert int.from_bytes(data[off:off + 4], "little") == orig, f"{site:#x}: unexpected original instruction"
        data[off:off + 4] = asm(entry if isinstance(entry, str) else f"bl #{at + entry:#x}", site)
    main.data = bytes(data)
    return code.save()
