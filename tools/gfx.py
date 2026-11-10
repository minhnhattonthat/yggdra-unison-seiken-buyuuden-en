"""gfx.py: English textures. gfx/<NAME>.png (an edited decode of DATA.SFS NAME.PACK) -> a new PACK for the build.

The palette is kept byte for byte (the code uploads it by the PACK's size); only texels (+ 4x4 index data) are
re-encoded, every part stored raw (flags 0x100, as the raw PACKs the game already loads).
  4x4: each block takes the (palette offset, mode) that reproduces it best from the *original* palette, so the
       English may only use colours the texture already had (ink, outline, gradient steps, transparent).
  2/4/8 bpp: nearest palette colour per pixel.
An unedited decode re-encodes to the same pixels (tests/test_gfx.py).

    python -X utf8 tools/gfx.py dump NAME.. [--out work/gfx/orig]   decode PACKs to PNG (start of an edit)
    python -X utf8 tools/gfx.py check [NAME..]                     every (or each named) gfx/*.png encodes; prints changed px,
                                                                   writes the re-decoded result to work/gfx/enc/
"""
import struct
import sys
from functools import cache
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import sfs  # noqa: E402
import tex  # noqa: E402

GFX = ROOT / "gfx"


@cache
def originals():
    import text
    return text.sfs_files()


def pack_of(name):
    return originals()[name]


WIDTH = {"CNAMEC": 64}  # tex.guess reads 21 of the 72 CNAMEC name tags as 128 x 8; all are 64 x 16


def load(name):
    """Decode original NAME.PACK, with the WIDTH override."""
    return decode(pack_of(name), next((w for p, w in WIDTH.items() if name.startswith(p)), None))


def decode(b, w=None):
    """PACK bytes -> (RGBA image, (tex, pal, idx, kind, w)). w: width (default: tex.guess)."""
    t, p, i = tex.parts(b)
    w = w or tex.guess(t, p, i)
    k = tex.kind(t, p, i)
    img = tex.render(t, p, i, w)
    if k != "4x4" and p:  # paletted: colour 0 is the transparent key (magenta in these PACKs)
        a = np.array(img)
        a[(a[..., :3] == tex.colours(p)[0][:3]).all(-1)] = 0
        img = Image.fromarray(a)
    return img, (t, p, i, k, w)


def _rgba(pal):
    return np.array(tex.colours(pal), dtype=np.int32)


def candidates(pal):
    """[(index word, 4 RGBA colours)] for every palette offset x mode the hardware allows within pal."""
    c = _rgba(pal)
    n = len(c)
    clear = np.array([0, 0, 0, 0])
    out = []
    for base in range(0, n - 1, 2):
        a, b = c[base], c[base + 1]
        out.append((base // 2 | 1 << 14, [a, b, (a + b) // 2, clear]))
        out.append((base // 2 | 3 << 14, [a, b, (5 * a + 3 * b) // 8, (3 * a + 5 * b) // 8]))
        if base + 2 < n:
            out.append((base // 2, [a, b, c[base + 2], clear]))
        if base + 3 < n:
            out.append((base // 2 | 2 << 14, [a, b, c[base + 2], c[base + 3]]))
    return [w for w, _ in out], np.array([cs for _, cs in out], dtype=np.int32)  # (C,), (C, 4, 4)


def _dist(px, cols):
    """px (..., 4) vs cols (C, 4, 4) -> (..., C, 4): squared RGB distance; alpha mismatch = huge."""
    d = ((px[..., None, None, :3] - cols[..., :3]) ** 2).sum(-1)
    clear_px = px[..., None, None, 3] < 128
    clear_c = cols[..., 3] < 128
    return np.where(clear_px != clear_c, 10 ** 7, np.where(clear_px, 0, d))


def encode_4x4(img, pal, nblocks):
    a = np.array(img.convert("RGBA"), dtype=np.int32)
    h, w = a.shape[:2]
    bw = w // 4
    blocks = a.reshape(h // 4, 4, bw, 4, 4).transpose(0, 2, 1, 3, 4).reshape(-1, 16, 4)[:nblocks]
    words, cols = candidates(pal)
    uniq, inv = np.unique(blocks.reshape(len(blocks), -1), axis=0, return_inverse=True)
    uniq = uniq.reshape(-1, 16, 4)
    best_c = np.empty(len(uniq), dtype=np.int64)
    best_k = np.empty((len(uniq), 16), dtype=np.int64)
    step = max(1, 2_000_000 // (16 * len(cols) * 4))
    for s in range(0, len(uniq), step):
        d = _dist(uniq[s:s + step], cols)  # (b, 16, C, 4)
        k = d.argmin(-1)  # (b, 16, C)
        err = np.take_along_axis(d, k[..., None], -1)[..., 0].sum(1)  # (b, C)
        c = err.argmin(1)
        best_c[s:s + step] = c
        best_k[s:s + step] = k[np.arange(len(c)), :, c]
    texb, idxb = bytearray(), bytearray()
    for u in inv.reshape(-1):
        k = best_k[u]
        texb += bytes(int(sum(int(k[r * 4 + x]) << (2 * x) for x in range(4))) for r in range(4))
        idxb += struct.pack("<H", words[best_c[u]])
    return bytes(texb), bytes(idxb)


def encode_pal(img, pal, bpp, n):
    a = np.array(img.convert("RGBA"), dtype=np.int32).reshape(-1, 4)[:n]
    c = _rgba(pal)
    k = ((a[:, None, :3] - c[None, 1:, :3]) ** 2).sum(-1).argmin(1) + 1
    k[a[:, 3] < 128] = 0
    per = 8 // bpp
    k = np.concatenate([k, np.zeros(-len(k) % per, dtype=k.dtype)]).reshape(-1, per)
    return bytes(int(sum(int(v) << (bpp * j) for j, v in enumerate(row))) for row in k)


def encode(orig_pack, img):
    """New PACK bytes for img (same size as the original decode)."""
    _, (t, p, i, k, w) = decode(orig_pack, img.size[0])
    ref = tex.render(t, p, i, w)
    assert img.size == ref.size, f"image {img.size} != texture {ref.size}"
    if k == "4x4":
        t2, i2 = encode_4x4(img, p, len(t) // 4)
    else:
        bpp = {"2bpp": 2, "4bpp": 4, "8bpp": 8}[k]
        t2, i2 = encode_pal(img, p, bpp, len(t) * 8 // bpp), i
    assert len(t2) == len(t) and len(i2) == len(i)
    return struct.pack("<4I", 0x100, len(t2), len(p), len(i2)) + t2 + p + i2


def files(only=None):
    """{NAME.PACK: bytes} for every gfx/NAME.png (or those NAMEs)."""
    out = {}
    for png in sorted(GFX.glob("*.png")):
        if only and png.stem not in only:
            continue
        name = png.stem + ".PACK"
        out[name] = encode(pack_of(name), Image.open(png))
    return out


def main(argv):
    if argv[:1] == ["dump"]:
        out = Path(argv[argv.index("--out") + 1]) if "--out" in argv else ROOT / "work/gfx/orig"
        out.mkdir(parents=True, exist_ok=True)
        for n in [a for a in argv[1:] if not a.startswith("--") and Path(a) != out]:
            img, (_, p, _, k, w) = load(n + ".PACK")
            img.save(out / f"{n}.png")
            print(f"{out / n}.png {k} {img.size} pal {len(p) // 2}")
        return 0
    if argv[:1] == ["check"]:
        prev = ROOT / "work/gfx/enc"  # what the game will show: the encoded texture decoded again
        prev.mkdir(parents=True, exist_ok=True)
        for name, b in files(argv[1:]).items():
            old, (*_, w) = load(name)
            new, _ = decode(b, w)  # the edit can change tex.guess's pick; the game's width is fixed in code
            new.save(prev / (name[:-5] + ".png"))
            want = np.array(Image.open(GFX / (name[:-5] + ".png")).convert("RGBA"), dtype=np.int32)
            got = np.array(new, dtype=np.int32)
            off = int((np.abs(got - want).max(-1) > 24).sum())
            diff = int((np.array(old) != np.array(new)).any(-1).sum())
            print(f"{name}: {diff} px changed from the original, {off} px off the edited PNG by > 24")
        return 0
    sys.exit(__doc__)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
