"""Isaac Sim integration boundary.

The module is intentionally importable without Isaac Sim. Implement SDK-specific
calls only inside ``IsaacSimAdapter`` after the target Isaac Sim version and Stage
prim paths are confirmed.
"""

from __future__ import annotations

from typing import Protocol


class CellHardwarePort(Protocol):
    def set_conveyor_speed(self, speed_mps: float) -> None: ...

    def stop_conveyor(self) -> None: ...

    def read_part_sensor(self) -> bool: ...

    def command_robot_pick(self, part_id: str) -> None: ...

    def command_robot_place(self, target: str) -> None: ...


class IsaacSimAdapter:
    """Placeholder that makes unimplemented simulator behavior explicit."""

    def __init__(self, stage: object) -> None:
        self.stage = stage

    def set_conveyor_speed(self, speed_mps: float) -> None:
        raise NotImplementedError("connect to the selected Isaac Sim conveyor API")

    def stop_conveyor(self) -> None:
        raise NotImplementedError("connect to the selected Isaac Sim conveyor API")

    def read_part_sensor(self) -> bool:
        raise NotImplementedError("connect to the Stage sensor prim")

    def command_robot_pick(self, part_id: str) -> None:
        raise NotImplementedError("connect to the selected robot controller")

    def command_robot_place(self, target: str) -> None:
        raise NotImplementedError("connect to the selected robot controller")

