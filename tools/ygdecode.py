"""ygdecode.py: decode a byte range with the game's text encoding (recon helper; controls shown as [XX]).

    python -X utf8 tools/ygdecode.py FILE [START_HEX [END_HEX]]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mkjptbl import glyph_chars  # noqa: E402

CH = glyph_chars()


def decode(b, i=0, end=None):
    end = len(b) if end is None else end
    out = []
    while i < end:
        c = b[i]
        if c < 0xF0:
            out.append(CH.get(c, f"{{{c:02X}}}"))
            i += 1
        elif 0xF1 <= c <= 0xF5 and i + 1 < end:
            g = 0xF0 + (c - 0xF1) * 0x100 + b[i + 1]
            out.append(CH.get(g, f"{{{g:03X}}}"))
            i += 2
        else:
            out.append(f"[{c:02X}]" + ("\n" if c == 0xFF else ""))
            i += 1
    return "".join(out)


if __name__ == "__main__":
    data = Path(sys.argv[1]).read_bytes()
    s = int(sys.argv[2], 16) if len(sys.argv) > 2 else 0
    e = int(sys.argv[3], 16) if len(sys.argv) > 3 else None
    print(decode(data, s, e))
