"""Deterministic inspection-result simulation."""

from __future__ import annotations

import random

from .models import InspectionResult


class InspectionController:
    def __init__(self, defect_probability: float, seed: int | None = None) -> None:
        if not 0.0 <= defect_probability <= 1.0:
            raise ValueError("defect_probability must be between 0 and 1")
        self.defect_probability = defect_probability
        self._random = random.Random(seed)

    def inspect(self) -> InspectionResult:
        if self._random.random() < self.defect_probability:
            return InspectionResult.FAIL
        return InspectionResult.PASS

