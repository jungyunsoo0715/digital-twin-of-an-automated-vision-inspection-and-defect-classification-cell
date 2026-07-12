from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from inspection_cell.line_controller import LineController
from inspection_cell.models import FaultType, InspectionResult, LineConfig, LineState


class LineControllerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.controller = LineController(LineConfig(), seed=42)
        self.controller.start()

    def test_pass_cycle_updates_kpi(self) -> None:
        outcome = self.controller.process_part(
            "part-0001", forced_result=InspectionResult.PASS
        )
        self.assertTrue(outcome.completed)
        self.assertEqual(self.controller.state, LineState.CONVEYOR_RUNNING)
        self.assertEqual(self.controller.kpi()["totalCount"], 1)
        self.assertEqual(self.controller.kpi()["passCount"], 1)

    def test_fail_cycle_invokes_robot_metric(self) -> None:
        outcome = self.controller.process_part(
            "part-0001", forced_result=InspectionResult.FAIL
        )
        self.assertTrue(outcome.completed)
        self.assertEqual(self.controller.kpi()["failCount"], 1)
        self.assertEqual(self.controller.kpi()["robotPickCount"], 1)

    def test_jam_stops_line_and_reset_returns_to_idle(self) -> None:
        outcome = self.controller.process_part("part-0001", forced_fault=FaultType.JAM)
        self.assertFalse(outcome.completed)
        self.assertEqual(self.controller.state, LineState.ERROR)
        self.assertEqual(self.controller.kpi()["totalCount"], 0)
        self.assertEqual(self.controller.kpi()["lastFault"], "JAM")
        self.controller.reset()
        self.assertEqual(self.controller.state, LineState.IDLE)

    def test_pick_failure_does_not_count_incomplete_part(self) -> None:
        outcome = self.controller.process_part(
            "part-0001",
            forced_result=InspectionResult.FAIL,
            forced_fault=FaultType.PICK_FAILURE,
        )
        self.assertFalse(outcome.completed)
        self.assertEqual(self.controller.state, LineState.ERROR)
        self.assertEqual(self.controller.kpi()["totalCount"], 0)
        self.assertEqual(self.controller.kpi()["lastFault"], "PICK_FAILURE")

    def test_seed_reproduces_results(self) -> None:
        first = LineController(LineConfig(defect_probability=0.4), seed=7)
        second = LineController(LineConfig(defect_probability=0.4), seed=7)
        first.start()
        second.start()
        first_results = [first.process_part(str(i)).result for i in range(20)]
        second_results = [second.process_part(str(i)).result for i in range(20)]
        self.assertEqual(first_results, second_results)
        self.assertEqual(first.kpi(), second.kpi())


if __name__ == "__main__":
    unittest.main()

