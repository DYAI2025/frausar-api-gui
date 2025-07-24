from __future__ import annotations

from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


@pytest.fixture()  # type: ignore[misc]
def temp_dirs(tmp_path: Path) -> tuple[Path, Path]:
    markers = tmp_path / "markers"
    json_dir = tmp_path / "markers_json"
    markers.mkdir()
    json_dir.mkdir()
    return markers, json_dir
