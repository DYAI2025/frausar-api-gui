"""Utilities to repair marker data before validation."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Tuple
from dateutil import parser

COMMON_FIELD_FIXES = {
    "beschreibg": "description",
    "descr": "description",
}

LEVEL_PREFIX = {1: "A", 2: "S", 3: "C", 4: "MM"}


def _iso_or_none(value: Any) -> str | None:
    try:
        return datetime.fromisoformat(str(value)).isoformat()
    except Exception:
        try:
            return parser.parse(str(value)).isoformat()
        except Exception:
            return None


class MarkerRepairEngine:
    """Apply automatic fixes to marker dictionaries."""

    def __init__(self, config: Dict[str, Any] | None = None) -> None:
        self.auto_fix_typo = True
        self.auto_fix_dates = True
        self.fallback_author = "auto_import"
        if config:
            self.auto_fix_typo = config.get("auto_fix_typo", True)
            self.auto_fix_dates = config.get("auto_fix_dates", True)
            self.fallback_author = config.get("fallback_author", "auto_import")

    def repair(self, data: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
        modified = False
        if self.auto_fix_typo:
            for wrong, correct in COMMON_FIELD_FIXES.items():
                if wrong in data:
                    data[correct] = data.pop(wrong)
                    modified = True
        defaults = {"version": "1.0.0", "status": "draft"}
        for k, v in defaults.items():
            if k not in data:
                data[k] = v
                modified = True
        if "author" not in data:
            data["author"] = self.fallback_author
            modified = True
        if self.auto_fix_dates:
            for key in ("created", "last_modified"):
                if key in data:
                    iso = _iso_or_none(data[key])
                    if iso:
                        data[key] = iso
                        modified = True
        if "level" in data and "id" in data:
            try:
                lvl = int(data["level"])
                expected = LEVEL_PREFIX.get(lvl)
                if expected:
                    if not str(data["id"]).startswith(f"{expected}_"):
                        suffix = str(data["id"]).split("_", 1)[-1]
                        data["id"] = f"{expected}_{suffix}"
                        modified = True
            except Exception:
                pass
        return data, modified
