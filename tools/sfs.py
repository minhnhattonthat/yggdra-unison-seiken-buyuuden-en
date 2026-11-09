"""sfs.py: DATA.SFS archive (Sting, Yggdra Unison DS). See docs/re/sfs.md.

Directory lives in arm9.bin: 12-byte entries (hash u32, size u32, sector u32), sorted by hash, sector = 0x200 bytes.
hash = low 32 bits of h = h*0x89 + c over the 16-byte zero-padded file name (c signed).
Many files are compressed with the halfword LZ in decompress() (arm9 0x200A54C).
"""
import struct

DIR_OFF = 0x95C4C  # arm9.bin offset of the first entry (hash 0x13194, sector 0)
SECTOR = 0x200


def name_hash(name):
    b = name.encode("ascii")[:16].ljust(16, b"\0")
    h = 0
    for c in b:
        h = (h * 0x89 + (c - 256 if c >= 128 else c)) & 0xFFFFFFFFFFFFFFFF
    return h & 0xFFFFFFFF


def read_dir(arm9, data_len):
    """Entries from DIR_OFF while hashes rise and sectors stay inside the archive."""
    ents, o = [], DIR_OFF
    while o + 12 <= len(arm9):
        h, size, sec = struct.unpack_from("<3I", arm9, o)
        if ents and h <= ents[-1][0] or sec * SECTOR + size > data_len:
            break
        ents.append((h, size, sec))
        o += 12
    return ents


def unpack_pack(b):
    """.PACK graphics: u32 flags, u32 size[3], then the 3 parts back to back; flags bit i = part i is LZ-compressed.
    Returns [(raw_part, decompressed_or_None)]."""
    flags, *sizes = struct.unpack_from("<4I", b, 0)
    out, o = [], 0x10
    for i, n in enumerate(sizes):
        raw = b[o:o + n]
        out.append((raw, decompress(raw)[0] if flags >> i & 1 and n else None))
        o += n
    assert o == len(b), f"PACK sizes end at {o:#x}, file {len(b):#x}"
    return out


def decompress(src):
    """Halfword LZ: u32 out size, u16 n, n u16 control words, then literal halfwords.
    Control bit15 set: copy ((w>>10)&0x1F)+2 halfwords from (w&0x3FF) halfwords back; else w literal halfwords."""
    out_size, n = struct.unpack_from("<IH", src, 0)
    ctl = struct.unpack_from(f"<{n}H", src, 6)
    lit = 6 + 2 * n
    out = bytearray()
    for w in ctl:
        if w & 0x8000:
            ln = ((w >> 10) & 0x1F) + 2
            dist = (w & 0x3FF) * 2
            for _ in range(ln):  # forward copy, so overlapping runs repeat
                p = len(out) - dist
                out += out[p:p + 2]
        else:
            out += src[lit:lit + 2 * w]
            lit += 2 * w
    return bytes(out), out_size, lit
