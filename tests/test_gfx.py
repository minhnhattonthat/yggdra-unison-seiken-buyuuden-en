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
