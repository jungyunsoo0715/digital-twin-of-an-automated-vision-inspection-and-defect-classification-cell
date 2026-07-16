"""Production KPI aggregation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .models import FaultType, InspectionResult, LineState


@dataclass(slots=True)
class MetricsCollector:
    total_count: int = 0
    pass_count: int = 0
    fail_count: int = 0
    robot_pick_count: int = 0
    cycle_times_s: list[float] = field(default_factory=list)
    last_fault: FaultType | None = None

    def record_completed(self, result: InspectionResult, cycle_time_s: float) -> None:
        if cycle_time_s < 0:
            raise ValueError("cycle_time_s cannot be negative")
        self.total_count += 1
        if result is InspectionResult.PASS:
            self.pass_count += 1
        else:
            self.fail_count += 1
            self.robot_pick_count += 1
        self.cycle_times_s.append(cycle_time_s)
        self._validate()

    def record_fault(self, fault: FaultType) -> None:
        self.last_fault = fault

    def snapshot(self, state: LineState, conveyor_speed_mps: float) -> dict[str, Any]:
        defect_rate = (self.fail_count / self.total_count * 100.0) if self.total_count else 0.0
        average_cycle = (
            sum(self.cycle_times_s) / len(self.cycle_times_s) if self.cycle_times_s else 0.0
        )
        return {
            "lineStatus": state.value,
            "totalCount": self.total_count,
            "passCount": self.pass_count,
            "failCount": self.fail_count,
            "defectRate": round(defect_rate, 2),
            "averageCycleTime": round(average_cycle, 3),
            "conveyorSpeed": conveyor_speed_mps,
            "robotPickCount": self.robot_pick_count,
            "lastFault": self.last_fault.value if self.last_fault else None,
        }

    def _validate(self) -> None:
        if self.total_count != self.pass_count + self.fail_count:
            raise RuntimeError("KPI invariant violated: total must equal pass + fail")

