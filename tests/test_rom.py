import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import check_rom  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.skipif(not (ROOT / "rom/yggdra.nds").is_file(), reason="no ROM dump")
def test_rom_hash():
    check_rom.check()  # sys.exit on mismatch fails the test
