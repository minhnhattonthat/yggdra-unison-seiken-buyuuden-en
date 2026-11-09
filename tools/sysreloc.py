"""sysreloc.py: put system strings (script/system/*.json rows) into the arm9 / overlay images, moving any that
outgrow their slot into the EXTRA block (docs/re/text.md "System text relocation").

A string that fits its slot (`max` bytes incl. FF) is written in place, zero-padded. A longer one goes into the
EXTRA block, a new arm9 autoload section at main RAM 0x02123460 (the overlay slot's end = the original main arena
lo), deduplicated; every pointer in its row's `ptrs` is rewritten (each must still hold the old address) and
engine.patch_arm9 raises the arena lo past the block. Every pointer target is a pointer-scan hit at a string start.

    images, extra = relocate(images, [(row, raw_bytes_without_ff), ...])
"""
import struct

ARM9_BASE, OVL_BASE = 0x02000000, 0x0211B780
EXTRA = 0x02123460  # OS_GetInitArenaLo main (literal at arm9 0x02025088); overlays end <= here (ov9_13)


def base(img):
    return ARM9_BASE if img == "arm9" else OVL_BASE


def relocate(images, rows):
    """images {img: bytes}; rows [(row, raw)] -> (new images, extra block bytes)."""
    out = {k: bytearray(v) for k, v in images.items()}
    extra, at = bytearray(), {}
    for row, raw in rows:
        img, off = row["id"].split(":")
        off = int(off, 16)
        data = raw + b"\xff"
        if len(data) <= row["max"]:
            out[img][off:off + row["max"]] = data.ljust(row["max"], b"\0")
            continue
        if data not in at:
            at[data] = EXTRA + len(extra)
            extra += data
            extra += bytes(-len(extra) % 4)
        old = base(img) + off
        out[img][off:off + row["max"]] = b"\xff".ljust(row["max"], b"\0")  # stale slot: empty string
        for p in row["ptrs"]:
            pimg, poff = p.split(":")
            poff = int(poff, 16)
            cur = struct.unpack_from("<I", out[pimg], poff)[0]
            assert cur == old, f"{row['id']}: pointer {p} holds {cur:#x}, not {old:#x}"
            struct.pack_into("<I", out[pimg], poff, at[data])
    return {k: bytes(v) for k, v in out.items()}, bytes(extra)


def selftest():
    img = {"arm9": bytes(16) + b"\x0c\x00\x00\x02" + b"\x01\x02\xff\x00", "ov9_01": bytes(4)}
    row = {"id": "arm9:14", "max": 4, "ptrs": ["arm9:10"]}
    a, x = relocate(img, [(row, b"\x05\x06\x07")])
    assert a["arm9"][0x14:0x18] == b"\x05\x06\x07\xff" and not x
    row = {"id": "arm9:14", "max": 4, "ptrs": ["arm9:10"]}
    img2 = {"arm9": bytes(16) + struct.pack("<I", 0x02000014) + b"\x01\x02\xff\x00"}
    a, x = relocate(img2, [(row, b"\x05\x06\x07\x08\x09")])
    assert x == b"\x05\x06\x07\x08\x09\xff\0\0" and struct.unpack_from("<I", a["arm9"], 0x10)[0] == EXTRA
    assert a["arm9"][0x14] == 0xFF


if __name__ == "__main__":
    selftest()
    print("ok")
