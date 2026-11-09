"""kanji_guess.py: first-guess char for each FONT_MES glyph by template matching against MS Gothic (JIS X 0208).

Writes work/kanji_guess.tsv: glyph hex, best char, score, 2nd, 3rd. A guess only: tbl/jp.tbl gets reviewed readings.
    python -X utf8 tools/kanji_guess.py [--first 0xEC] [--font C:/Windows/Fonts/msgothic.ttc]
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
N = 20  # comparison grid


def norm(mask):
    ys, xs = np.nonzero(mask)
    if len(ys) == 0:
        return None
    crop = mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1].astype(np.uint8) * 255
    h, w = crop.shape
    s = max(h, w)
    sq = np.zeros((s, s), np.uint8)
    sq[(s - h) // 2:(s - h) // 2 + h, (s - w) // 2:(s - w) // 2 + w] = crop
    v = np.asarray(Image.fromarray(sq).resize((N, N), Image.BILINEAR), np.float32).ravel()
    v -= v.mean()
    n = np.linalg.norm(v)
    return v / n if n else None


def glyph_masks(path, ink_max):
    d = Path(path).read_bytes()
    out = []
    for g in range(len(d) // 128):
        a = np.frombuffer(d[g * 128:(g + 1) * 128], np.uint8)
        px = np.empty(256, np.uint8)
        px[0::2], px[1::2] = a & 15, a >> 4
        px = px.reshape(16, 16)
        out.append((px > 0) & (px <= ink_max))
    return out


def jis_kanji():
    for lead in range(0x88, 0xEB):
        for trail in list(range(0x40, 0x7F)) + list(range(0x80, 0xFD)):
            try:
                c = bytes([lead, trail]).decode("cp932")
            except UnicodeDecodeError:
                continue
            if "\u4e00" <= c <= "\u9fff" or c == "々":
                yield c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--first", type=lambda s: int(s, 0), default=0xEC)
    ap.add_argument("--font", default="C:/Windows/Fonts/msgothic.ttc")
    ap.add_argument("--ink", type=int, default=8)
    a = ap.parse_args()
    cands = list(jis_kanji())
    vecs, chars = [], []
    for size in (12, 13):
        font = ImageFont.truetype(a.font, size)
        for c in cands:
            im = Image.new("L", (24, 24))
            ImageDraw.Draw(im).text((2, 2), c, fill=255, font=font)
            v = norm(np.asarray(im) > 100)
            if v is not None:
                vecs.append(v)
                chars.append(c)
    M = np.stack(vecs)
    rows = []
    masks = glyph_masks(ROOT / "work/sfs/FONT_MES.NTFT", a.ink)
    for g in range(a.first, len(masks)):
        v = norm(masks[g])
        if v is None:
            rows.append(f"{g:x}\t\t0\n")
            continue
        sc = M @ v
        best, seen = [], set()
        for i in np.argsort(-sc):
            if chars[i] not in seen:
                seen.add(chars[i])
                best.append((chars[i], sc[i]))
            if len(best) == 3:
                break
        rows.append(f"{g:x}\t{best[0][0]}\t{best[0][1]:.3f}\t{best[1][0]}\t{best[2][0]}\n")
    (ROOT / "work/kanji_guess.tsv").write_text("".join(rows), encoding="utf-8")
    print(len(rows), "glyphs ->", ROOT / "work/kanji_guess.tsv")


if __name__ == "__main__":
    main()
