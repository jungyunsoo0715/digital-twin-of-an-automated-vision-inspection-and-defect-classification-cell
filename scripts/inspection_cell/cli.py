"""Command-line demo for the simulator-independent control core."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import line_config_from_mapping, load_json
from .line_controller import LineController


DEFAULT_CONFIG = Path(__file__).resolve().parents[2] / "configs" / "default.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the inspection-cell logic demo")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--parts", type=int, help="number of parts to process")
    parser.add_argument("--seed", type=int, help="random seed")
    parser.add_argument("--speed", type=float, help="override conveyor speed in m/s")
    return parser


def run(parts: int, seed: int, line_values: dict[str, object]) -> dict[str, object]:
    controller = LineController(line_config_from_mapping(line_values), seed=seed)
    controller.start()
    for index in range(1, parts + 1):
        outcome = controller.process_part(f"part-{index:04d}")
        if not outcome.completed:
            break
    return controller.kpi()


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    document = load_json(args.config)
    line_values = dict(document["line"])
    simulation = document.get("simulation", {})
    parts = args.parts if args.parts is not None else int(simulation.get("parts", 30))
    seed = args.seed if args.seed is not None else int(simulation.get("seed", 42))
    if parts < 0:
        raise SystemExit("--parts cannot be negative")
    if args.speed is not None:
        line_values["conveyor_speed_mps"] = args.speed
    print(json.dumps(run(parts, seed, line_values), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

