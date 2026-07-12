"""Production-cycle orchestration independent of simulator APIs."""

from __future__ import annotations

from dataclasses import dataclass

from .fault_manager import FaultManager
from .inspection_controller import InspectionController
from .metrics_collector import MetricsCollector
from .models import FaultType, InspectionResult, LineConfig, LineState
from .state_machine import LineStateMachine


@dataclass(frozen=True, slots=True)
class CycleOutcome:
    part_id: str
    result: InspectionResult | None
    completed: bool
    fault: FaultType | None
    cycle_time_s: float


class LineController:
    """Coordinates one logical part cycle and preserves safety invariants."""

    def __init__(self, config: LineConfig | None = None, seed: int | None = None) -> None:
        self.config = config or LineConfig()
        self.state_machine = LineStateMachine()
        self.inspection = InspectionController(self.config.defect_probability, seed=seed)
        fault_seed = None if seed is None else seed + 1
        self.faults = FaultManager(
            self.config.robot_pick_failure_probability,
            seed=fault_seed,
        )
        self.metrics = MetricsCollector()

    @property
    def state(self) -> LineState:
        return self.state_machine.state

    def start(self) -> None:
        self.state_machine.transition(LineState.CONVEYOR_RUNNING)

    def reset(self) -> None:
        if self.state is not LineState.ERROR:
            raise RuntimeError("reset is only allowed from ERROR")
        self.state_machine.transition(LineState.IDLE)

    def process_part(
        self,
        part_id: str,
        *,
        forced_result: InspectionResult | None = None,
        forced_fault: FaultType | None = None,
    ) -> CycleOutcome:
        if self.state is not LineState.CONVEYOR_RUNNING:
            raise RuntimeError(f"cannot process a part while line is {self.state.value}")

        travel_time_s = (
            self.config.sensor_to_inspection_distance_m / self.config.conveyor_speed_mps
        )
        jammed = forced_fault is FaultType.JAM or self.faults.is_jammed(
            travel_time_s, self.config.jam_timeout_s
        )
        if jammed:
            self.state_machine.transition(LineState.JAM_DETECTED)
            self.state_machine.transition(LineState.ERROR)
            self.metrics.record_fault(FaultType.JAM)
            return CycleOutcome(part_id, None, False, FaultType.JAM, travel_time_s)

        self.state_machine.transition(LineState.PART_DETECTED)
        self.state_machine.transition(LineState.CONVEYOR_STOPPED)
        self.state_machine.transition(LineState.INSPECTING)

        result = forced_result or self.inspection.inspect()
        cycle_time_s = travel_time_s + self.config.inspection_time_s

        if result is InspectionResult.PASS:
            self.state_machine.transition(LineState.PASS)
            self.state_machine.transition(LineState.CONVEYOR_RUNNING)
            self.metrics.record_completed(result, cycle_time_s)
            return CycleOutcome(part_id, result, True, None, cycle_time_s)

        self.state_machine.transition(LineState.FAIL)
        self.state_machine.transition(LineState.ROBOT_PICK)
        pick_failed = forced_fault is FaultType.PICK_FAILURE or self.faults.pick_fails()
        if pick_failed:
            self.state_machine.transition(LineState.PICK_FAILED)
            self.state_machine.transition(LineState.ERROR)
            self.metrics.record_fault(FaultType.PICK_FAILURE)
            return CycleOutcome(part_id, result, False, FaultType.PICK_FAILURE, cycle_time_s)

        cycle_time_s += self.config.robot_cycle_time_s
        self.state_machine.transition(LineState.ROBOT_PLACE)
        self.state_machine.transition(LineState.CONVEYOR_RUNNING)
        self.metrics.record_completed(result, cycle_time_s)
        return CycleOutcome(part_id, result, True, None, cycle_time_s)

    def kpi(self) -> dict[str, object]:
        return self.metrics.snapshot(self.state, self.config.conveyor_speed_mps)

