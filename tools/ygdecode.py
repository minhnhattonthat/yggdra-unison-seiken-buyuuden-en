"""ygdecode.py: decode a byte range with the game's text encoding (recon helper; unknown bytes shown as [XX]).

    python -X utf8 tools/ygdecode.py FILE [START_HEX [END_HEX]] [--font mes|sys|end]
Glyph codes: byte < F0, or F1..F9 + xx = (b - 0xF0) * 0xF0 + xx (docs/re/text.md). FD = new line, FF = end.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mkjptbl import chars  # noqa: E402

CH = chars("mes")


def decode(b, i=0, end=None):
    end = len(b) if end is None else end
    out = []
    while i < end:
        c = b[i]
        if c < 0xF0:
            out.append(CH.get(c, f"{{{c:02X}}}"))
            i += 1
        elif 0xF1 <= c <= 0xF9 and i + 1 < end:
            g = (c - 0xF0) * 0xF0 + b[i + 1]
            out.append(CH.get(g, f"{{{g:03X}}}"))
            i += 2
        elif c == 0xFD:
            out.append("\n")
            i += 1
        else:
            out.append(f"[{c:02X}]" + ("\n" if c == 0xFF else ""))
            i += 1
    return "".join(out)


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--font" in args:
        k = args.index("--font")
        CH = chars(args[k + 1])
        del args[k:k + 2]
    data = Path(args[0]).read_bytes()
    s = int(args[1], 16) if len(args) > 1 else 0
    e = int(args[2], 16) if len(args) > 2 else None
    print(decode(data, s, e))
