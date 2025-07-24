from __future__ import annotations

from marker_import_bridge import YAMLBlockSplitter


def test_splitter() -> None:
    raw = "a:1\n---\nb:2\n\n---\n\n"
    blocks = YAMLBlockSplitter.split(raw)
    assert blocks == ["a:1", "b:2"]
