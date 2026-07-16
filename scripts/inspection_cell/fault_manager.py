"""Fault decisions kept separate from production sequencing."""

from __future__ import annotations

import random


class FaultManager:
    def __init__(self, pick_failure_probability: float = 0.0, seed: int | None = None) -> None:
        if not 0.0 <= pick_failure_probability <= 1.0:
            raise ValueError("pick_failure_probability must be between 0 and 1")
        self.pick_failure_probability = pick_failure_probability
        self._random = random.Random(seed)

    def pick_fails(self) -> bool:
        return self._random.random() < self.pick_failure_probability

    @staticmethod
    def is_jammed(travel_time_s: float, timeout_s: float) -> bool:
        return travel_time_s > timeout_s

