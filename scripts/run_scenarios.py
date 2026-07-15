#!/usr/bin/env python3
"""Compare configured conveyor-speed scenarios under controlled conditions."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from inspection_cell.cli import run  # noqa: E402
from inspection_cell.config import load_json  # noqa: E402


def default_output_path() -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return ROOT / "data" / "results" / f"scenario_results_{timestamp}.json"


def parse_args() -> Path:
    parser = ArgumentParser(
        description="Run configured scenario comparisons and save the results as JSON."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=default_output_path(),
        help="Path for the generated JSON result file.",
    )
    return parser.parse_args().output


def main() -> int:
    output_path = parse_args()
    defaults = load_json(ROOT / "configs" / "default.json")
    scenarios = load_json(ROOT / "configs" / "scenarios.json")
    results: dict[str, object] = {}
    for name, scenario in scenarios.items():
        line_values = dict(defaults["line"])
        line_values["conveyor_speed_mps"] = scenario["conveyor_speed_mps"]
        results[name] = run(int(scenario["parts"]), 42, line_values)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_text = json.dumps(results, ensure_ascii=False, indent=2)
    output_path.write_text(output_text + "\n", encoding="utf-8")
    print(output_text)
    print(f"\nSaved scenario results to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
