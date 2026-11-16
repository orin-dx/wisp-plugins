"""An outcome against a baseline is asked for, recorded in `done_when` and left pending until the baseline is run."""

from __future__ import annotations

import importlib.util
import re
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
specification = importlib.util.spec_from_file_location("validate_handback", REPOSITORY_ROOT / "shared" / "hooks" / "validate-handback.py")
assert specification is not None and specification.loader is not None
validator = importlib.util.module_from_spec(specification)
specification.loader.exec_module(validator)

REQUIREMENT = validator.load_schema("requirement@1")

CONVENTION = "Outcome: <measure> at least <threshold> against <named baseline>, measured by <method>"
CONVENTION_PATTERN = re.compile(r"^Outcome: .+ at least .+ against .+, measured by .+$")

# v5 keeps no requirement clarifier or verification gate in the remaining plugins; list a prompt here when
# one that asks for or gates on a baseline is added, and these checks cover it.
CLARIFIERS: list[str] = []
GATE_SOURCES: list[str] = []
EVIDENCE = "shared/references/verification/evidence.md"


def read(relative: str) -> str:
    return (REPOSITORY_ROOT / relative).read_text(encoding="utf-8")


def requirement(done_when: list[str]) -> dict:
    return {
        "id": "REQ-042",
        "statement": "A code search tool that finds the file a developer needs.",
        "stakeholder": "Developer using an AI coding agent",
        "why": "Agents waste tokens when search misses the right file.",
        "done_when": done_when,
    }


class OutcomeBaselineTests(unittest.TestCase):
    def test_a_requirement_with_the_convention_validates_against_requirement_1(self) -> None:
        item = "Outcome: tasks found cleanly at least 34 of 36 against ripgrep, measured by the 36-task eval with both tools run the same way"
        self.assertRegex(item, CONVENTION_PATTERN)
        self.assertEqual(validator.validate(requirement([item, "Search returns in under one second"]), REQUIREMENT), [])

    def test_the_convention_needs_no_schema_change(self) -> None:
        self.assertTrue(validator.validate({**requirement(["x"]), "baseline": "ripgrep"}, REQUIREMENT))

    def test_clarifiers_ask_for_the_baseline_and_record_the_convention(self) -> None:
        for path in CLARIFIERS:
            with self.subTest(path=path):
                text = read(path)
                self.assertIn(CONVENTION, text)
                self.assertIn("baseline", text)
                self.assertIn('"replaces"', text)

    def test_the_gate_leaves_an_outcome_without_a_baseline_run_pending(self) -> None:
        for path in GATE_SOURCES:
            with self.subTest(path=path):
                text = read(path)
                self.assertIn("Outcome:", text)
                self.assertIn("pending", text)
                self.assertIn("verified scope", text)

    def test_the_evidence_reference_says_how_a_comparative_outcome_is_verified(self) -> None:
        text = read(EVIDENCE)
        bullet = next(line for line in text.splitlines() if line.startswith("- Comparative outcome"))
        for phrase in ("baseline and the product the same way", "what was not compared", "pending"):
            self.assertIn(phrase, bullet)
        self.assertLessEqual(len(text.splitlines()), 120)


if __name__ == "__main__":
    unittest.main()
