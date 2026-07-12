from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from inspection_cell.models import LineState
from inspection_cell.state_machine import InvalidTransition, LineStateMachine


class LineStateMachineTests(unittest.TestCase):
    def test_happy_path_pass(self) -> None:
        machine = LineStateMachine()
        for state in (
            LineState.CONVEYOR_RUNNING,
            LineState.PART_DETECTED,
            LineState.CONVEYOR_STOPPED,
            LineState.INSPECTING,
            LineState.PASS,
            LineState.CONVEYOR_RUNNING,
        ):
            machine.transition(state)
        self.assertEqual(machine.state, LineState.CONVEYOR_RUNNING)

    def test_invalid_transition_is_rejected_without_state_change(self) -> None:
        machine = LineStateMachine()
        with self.assertRaises(InvalidTransition):
            machine.transition(LineState.ROBOT_PICK)
        self.assertEqual(machine.state, LineState.IDLE)


if __name__ == "__main__":
    unittest.main()

