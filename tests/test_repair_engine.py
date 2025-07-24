from __future__ import annotations

from marker_repair_engine import MarkerRepairEngine


def test_repair_typo_and_defaults() -> None:
    data = {"id": "A_t", "level": 1, "beschreibg": "test"}
    repaired, modified = MarkerRepairEngine().repair(data)
    assert modified
    assert repaired["description"] == "test"
    assert repaired["version"] == "1.0.0"
