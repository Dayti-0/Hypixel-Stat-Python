import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


@pytest.fixture
def raw_player():
    return json.loads((ROOT / "tests" / "fixtures" / "player.json").read_text(encoding="utf-8"))
