from __future__ import annotations

import subprocess
from pathlib import Path


def test_cli_e2e(tmp_path: Path) -> None:
    data_file = Path(__file__).parent / "data" / "valid_multi.yaml"
    cfg = tmp_path / "cfg.toml"
    (tmp_path / "markers").mkdir()
    (tmp_path / "markers_json").mkdir()
    cfg.write_text(
        """[paths]\nmarker_dir='"""
        + str(tmp_path / "markers")
        + "'\nmarker_json_dir='"
        + str(tmp_path / "markers_json")
        + "'\n"
        "",
        encoding="utf-8",
    )
    result = subprocess.run(
        [
            "python",
            "marker_import_bridge.py",
            "--input",
            str(data_file),
            "--config",
            str(cfg),
        ],
        cwd=Path.cwd(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "imported" in result.stdout
