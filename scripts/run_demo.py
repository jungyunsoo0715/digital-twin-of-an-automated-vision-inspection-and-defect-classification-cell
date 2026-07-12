#!/usr/bin/env python3
"""Run the local control-core demo without installing the package."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from inspection_cell.cli import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())

