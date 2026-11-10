"""An unedited texture decode re-encodes (original palette) to the same pixels: 4x4 and paletted."""
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import gfx  # noqa: E402


@pytest.mark.parametrize("name", ["SHOOTNAME00.PACK", "CNAMEA00.PACK", "EVSFONT00.PACK", "IT_EF001.PACK"])
def test_roundtrip(name):
    if not (ROOT / "rom/yggdra.nds").exists():
        pytest.skip("no ROM")
    orig = gfx.pack_of(name)
    img, _ = gfx.decode(orig)
    new = gfx.encode(orig, img)
    assert np.array_equal(np.array(gfx.decode(new)[0]), np.array(img))


def test_gen_gfx_clears():
    """clear=panel paints the commonest border colour, so a leader line crossing the box doesn't streak (clear=row
    did); clear=fill works on a box touching the texture edge (used to raise)."""
    import gen_gfx
    a = np.zeros((40, 80, 4), np.uint8)
    a[...] = (0, 0, 128, 255)
    a[10, :] = (255, 0, 0, 255)  # red leader line through the box
    gen_gfx.draw(a, "Ab", {"box": "10,5,40,20", "clear": "panel", "fill": "255,255,255"})
    box = a[5:25, 10:50]
    assert not ((box[..., 0] == 255) & (box[..., 1] == 0) & (box[..., 2] == 0)).any()
    gen_gfx.draw(a, "Ab", {"box": "0,0,30,10", "clear": "fill"})
