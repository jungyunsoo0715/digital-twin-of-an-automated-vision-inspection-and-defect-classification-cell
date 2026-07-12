"""Strict state transitions for the production cell."""

from __future__ import annotations

from dataclasses import dataclass, field

from .models import LineState


class InvalidTransition(RuntimeError):
    """Raised when a command attempts an undefined state transition."""


ALLOWED_TRANSITIONS: dict[LineState, frozenset[LineState]] = {
    LineState.IDLE: frozenset({LineState.CONVEYOR_RUNNING}),
    LineState.CONVEYOR_RUNNING: frozenset(
        {LineState.PART_DETECTED, LineState.JAM_DETECTED}
    ),
    LineState.PART_DETECTED: frozenset({LineState.CONVEYOR_STOPPED}),
    LineState.CONVEYOR_STOPPED: frozenset({LineState.INSPECTING}),
    LineState.INSPECTING: frozenset({LineState.PASS, LineState.FAIL}),
    LineState.PASS: frozenset({LineState.CONVEYOR_RUNNING}),
    LineState.FAIL: frozenset({LineState.ROBOT_PICK}),
    LineState.ROBOT_PICK: frozenset({LineState.ROBOT_PLACE, LineState.PICK_FAILED}),
    LineState.ROBOT_PLACE: frozenset({LineState.CONVEYOR_RUNNING}),
    LineState.JAM_DETECTED: frozenset({LineState.ERROR}),
    LineState.PICK_FAILED: frozenset({LineState.ERROR}),
    LineState.ERROR: frozenset({LineState.IDLE}),
}


@dataclass(slots=True)
class LineStateMachine:
    state: LineState = LineState.IDLE
    history: list[LineState] = field(default_factory=lambda: [LineState.IDLE])

    def transition(self, target: LineState) -> None:
        if target not in ALLOWED_TRANSITIONS[self.state]:
            raise InvalidTransition(f"invalid transition: {self.state.value} -> {target.value}")
        self.state = target
        self.history.append(target)

