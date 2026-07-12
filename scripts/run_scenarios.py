#!/usr/bin/env python3
"""Compare configured conveyor-speed scenarios under controlled conditions."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from inspection_cell.cli import run  # noqa: E402
from inspection_cell.config import load_json  # noqa: E402


def main() -> int:
    defaults = load_json(ROOT / "configs" / "default.json")
    scenarios = load_json(ROOT / "configs" / "scenarios.json")
    results: dict[str, object] = {}
    for name, scenario in scenarios.items():
        line_values = dict(defaults["line"])
        line_values["conveyor_speed_mps"] = scenario["conveyor_speed_mps"]
        results[name] = run(int(scenario["parts"]), 42, line_values)
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

