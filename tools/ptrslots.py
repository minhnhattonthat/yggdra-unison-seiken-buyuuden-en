"""ptrslots.py: jp_left.py --slots file for an NDS code image: every aligned u32 in arm9 and the overlays that points
into the image's data (arm9: 0x0208F000.. end, overlays: whole image), as "SLOT TARGET" file offsets of IMAGE.

    python tools/ptrslots.py arm9|ov9_NN BUILT_IMAGE.bin > work/slots_<img>.txt
    python -X utf8 "$SKILL/scripts/jp_left.py" BUILT_IMAGE.bin --tbl tbl/jp_sys.tbl --slots work/slots_<img>.txt

Pointers from code into code also land here; jp_left only reports targets that decode as Japanese.
"""
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import text  # noqa: E402

DATA_LO = {"arm9": 0x8F000}


def main():
    img, built = sys.argv[1], Path(sys.argv[2]).read_bytes()
    base, lo = text.base_of(img), DATA_LO.get(img, 0)
    srcs = text.code_images()
    for name, b in srcs.items():
        if img != "arm9" and name != img:
            continue  # overlay strings are only pointed at from the same overlay (text.md)
        for i in range(0, len(b) - 3, 4):
            t = struct.unpack_from("<I", b, i)[0] - base
            if lo <= t < len(built) and not (name == img and i == t):
                if name == img:
                    print(f"{i:X} {t:X}")
                else:
                    print(f"{t:X} {t:X}")  # pointer lives in another image: give the target as its own slot


if __name__ == "__main__":
    main()
