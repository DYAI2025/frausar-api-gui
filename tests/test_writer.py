from __future__ import annotations

from pathlib import Path

from marker_import_bridge import MarkerWriter


def test_writer(temp_dirs: tuple[Path, Path]) -> None:
    markers, json_dir = temp_dirs
    writer = MarkerWriter(markers, json_dir)
    data = {"id": "A_w", "level": 1, "description": "d"}
    path, json_path = writer.write(data)
    assert path.exists()
    assert json_path.exists()
    assert Path(json_path).read_text().startswith("{")
