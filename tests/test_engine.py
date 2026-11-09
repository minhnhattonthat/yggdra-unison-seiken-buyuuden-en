import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build  # noqa: E402

needs_rom = pytest.mark.skipif(not build.ORIG.is_file(), reason="no ROM dump")


@needs_rom
def test_engine_patch():
    import ndspy.code
    import enfont
    import engine
    import text
    fonts, wtab = enfont.patched_fonts(text.sfs_files(set(enfont.FONTS)))
    arm9 = text.code_images()["arm9"]
    new = ndspy.code.MainCodeFile(engine.patch_arm9(arm9, wtab), 0x02000000)
    old = ndspy.code.MainCodeFile(arm9, 0x02000000)
    oi = next(s for s in old.sections if s.ramAddress == engine.ITCM)
    ni = next(s for s in new.sections if s.ramAddress == engine.ITCM)
    at = len(oi.data) + oi.bssSize
    assert ni.bssSize == 0 and ni.data[:len(oi.data)] == oi.data and not any(ni.data[len(oi.data):at])
    assert wtab in ni.data[at:]
    changed = [i for i in range(0, len(old.sections[0].data), 4) if old.sections[0].data[i:i + 4] != new.sections[0].data[i:i + 4]]
    # besides the hook sites only the module params change (autoload list pointers move with the ITCM size)
    extra = sorted(set(0x02000000 + i for i in changed) - {s for s, _, _ in engine.SITES})
    assert len(changed) == len(engine.SITES) + len(extra) and all(a < 0x02000C00 for a in extra), [hex(a) for a in extra]


@needs_rom
def test_english_glyphs():
    import enfont
    import text
    fonts, wtab = enfont.patched_fonts(text.sfs_files(set(enfont.FONTS)))
    gl = enfont.glyphs(text.sfs_files({"FONT_MES.NTFT"})["FONT_MES.NTFT"])
    codes = [c for c, _, _ in gl.values()]
    assert len(codes) == len(set(codes)) and all(c < 0xF0 for c in codes)
    for ch, (code, px, adv) in gl.items():
        assert 0 < adv <= 15 and wtab[0x100 + code] == adv  # VWF cells assume advance < 16
        if ch != " ":
            assert any(px[y][0] for y in range(16)), ch  # shifted to column 0
            assert wtab[0x400 + code] == adv + 1
    t = text.Table.load(ROOT / "tbl/en.tbl")
    assert t.encode("Hello, world! 1-2: \"A/B\" 50% & *") is not None
