from __future__ import annotations

from marker_import_bridge import MarkerValidator


def test_validator_success() -> None:
    block = "id: A_x\nlevel: 1\ndescription: ok"
    data, errors = MarkerValidator().validate(block)
    assert not errors
    assert data["id"] == "A_x"


def test_validator_failure() -> None:
    block = "id: wrong\nlevel: 5"
    _, errors = MarkerValidator().validate(block)
    assert errors
