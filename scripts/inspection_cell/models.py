"""Shared domain types and configuration."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class LineState(str, Enum):
    IDLE = "IDLE"
    CONVEYOR_RUNNING = "CONVEYOR_RUNNING"
    PART_DETECTED = "PART_DETECTED"
    CONVEYOR_STOPPED = "CONVEYOR_STOPPED"
    INSPECTING = "INSPECTING"
    PASS = "PASS"
    FAIL = "FAIL"
    ROBOT_PICK = "ROBOT_PICK"
    ROBOT_PLACE = "ROBOT_PLACE"
    JAM_DETECTED = "JAM_DETECTED"
    PICK_FAILED = "PICK_FAILED"
    ERROR = "ERROR"


class InspectionResult(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"


class FaultType(str, Enum):
    JAM = "JAM"
    PICK_FAILURE = "PICK_FAILURE"


@dataclass(frozen=True, slots=True)
class LineConfig:
    conveyor_speed_mps: float = 0.35
    sensor_to_inspection_distance_m: float = 1.2
    inspection_time_s: float = 1.0
    robot_cycle_time_s: float = 3.2
    defect_probability: float = 0.1
    jam_timeout_s: float = 8.0
    robot_pick_failure_probability: float = 0.0

    def __post_init__(self) -> None:
        if self.conveyor_speed_mps <= 0:
            raise ValueError("conveyor_speed_mps must be greater than zero")
        if self.sensor_to_inspection_distance_m < 0:
            raise ValueError("sensor_to_inspection_distance_m cannot be negative")
        if self.inspection_time_s < 0 or self.robot_cycle_time_s < 0:
            raise ValueError("cycle times cannot be negative")
        if self.jam_timeout_s <= 0:
            raise ValueError("jam_timeout_s must be greater than zero")
        for name, value in (
            ("defect_probability", self.defect_probability),
            ("robot_pick_failure_probability", self.robot_pick_failure_probability),
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0 and 1")

