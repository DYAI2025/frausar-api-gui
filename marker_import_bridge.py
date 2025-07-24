"""CLI and utilities to import marker YAML blocks."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple
from uuid import uuid4

import tomllib
from pydantic import BaseModel, ValidationError, field_validator
from ruamel.yaml import YAML

from marker_repair_engine import MarkerRepairEngine


def load_config(path: Path) -> Dict[str, Any]:
    if path.exists():
        with open(path, "rb") as f:
            return tomllib.load(f)
    return {}


class YAMLBlockSplitter:
    """Split raw text into YAML blocks."""

    @staticmethod
    def split(raw: str) -> List[str]:
        blocks = re.split(r"^\s*---\s*$", raw, flags=re.M)
        return [b.strip() for b in blocks if b.strip()]


class MarkerBase(BaseModel):  # type: ignore[misc]
    id: str
    level: int
    description: str
    version: str = "1.0.0"
    status: str = "draft"
    author: str = "auto_import"

    @field_validator("level")  # type: ignore[misc]
    @classmethod
    def _validate_level(cls, v: int) -> int:
        if v not in {1, 2, 3, 4}:
            raise ValueError("level must be between 1 and 4")
        return v

    @field_validator("id")  # type: ignore[misc]
    @classmethod
    def _validate_id(cls, v: str) -> str:
        if not re.match(r"^[A-Z]{1,3}_.+", v):
            raise ValueError("invalid id format")
        return v


class MarkerValidator:
    """Validate YAML blocks against the Marker schema."""

    def __init__(self) -> None:
        self.yaml = YAML(typ="safe", pure=True)

    def validate(self, text: str) -> Tuple[Dict[str, Any], List[str]]:
        data = self.yaml.load(text)
        try:
            valid = MarkerBase(**data)
            return valid.model_dump(), []
        except ValidationError as err:
            return data, [e["msg"] for e in err.errors()]


class MarkerWriter:
    """Write marker files in YAML and JSON form."""

    def __init__(self, marker_dir: Path, json_dir: Path) -> None:
        self.marker_dir = marker_dir
        self.json_dir = json_dir
        self.yaml = YAML(typ="rt")
        self.marker_dir.mkdir(parents=True, exist_ok=True)
        self.json_dir.mkdir(parents=True, exist_ok=True)

    def write(self, data: Dict[str, Any]) -> Tuple[Path, Path]:
        path = self.marker_dir / f"{data['id']}.yaml"
        if path.exists():
            path = self.marker_dir / f"{data['id']}_{uuid4().hex[:6]}.yaml"
        with open(path, "w", encoding="utf-8") as f:
            self.yaml.dump(data, f)
        json_path = self.json_dir / (path.stem + ".json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return path, json_path


class HistoryLogger:
    def __init__(self, path: Path) -> None:
        self.path = path
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def append(self, entry: Dict[str, Any]) -> None:
        history = json.loads(self.path.read_text(encoding="utf-8"))
        history.append(entry)
        self.path.write_text(json.dumps(history, indent=2), encoding="utf-8")


def process_blocks(blocks: List[str], cfg: Dict[str, Any]) -> int:
    paths = cfg.get("paths", {})
    marker_dir = Path(paths.get("marker_dir", "./markers"))
    json_dir = Path(paths.get("marker_json_dir", "./markers_json"))
    logger = HistoryLogger(Path("import_history.json"))

    validator = MarkerValidator()
    repairer = MarkerRepairEngine(cfg.get("repair", {}))
    writer = MarkerWriter(marker_dir, json_dir)

    ok = 0
    failed = 0
    for block in blocks:
        data, errors = validator.validate(block)
        status = "imported"
        if errors:
            data, _ = repairer.repair(data)
            data, errors = validator.validate(YAML().dump(data))
            status = "fixed"
        if errors:
            logger.append({"status": "failed", "errors": errors, "snippet": block})
            failed += 1
            continue
        writer.write(data)
        logger.append({"status": status, "id": data["id"]})
        ok += 1
    print(f"{ok} imported, {failed} failed")
    return 0 if failed == 0 else 1


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--input", type=Path)
    parser.add_argument(
        "--config", type=Path, default=Path("~/.frausar_import.toml").expanduser()
    )
    args = parser.parse_args(argv)

    if args.stdin:
        raw = sys.stdin.read()
    elif args.input:
        raw = args.input.read_text(encoding="utf-8")
    else:
        parser.error("--stdin or --input required")

    cfg = load_config(args.config)
    blocks = YAMLBlockSplitter.split(raw)
    return process_blocks(blocks, cfg)


if __name__ == "__main__":
    raise SystemExit(main())
