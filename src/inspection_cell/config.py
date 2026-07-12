"""JSON configuration loading helpers."""

from __future__ import annotations

import json
from dataclasses import fields
from pathlib import Path
from typing import Any

from .models import LineConfig


def load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as file:
        return json.load(file)


def line_config_from_mapping(values: dict[str, Any]) -> LineConfig:
    allowed = {field.name for field in fields(LineConfig)}
    unknown = set(values) - allowed
    if unknown:
        names = ", ".join(sorted(unknown))
        raise ValueError(f"unknown line configuration field(s): {names}")
    return LineConfig(**values)

