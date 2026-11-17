"""Spec unknowns are stated in `scope` as assumptions or open owner decisions, not banned (ADR 016)."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
specification = importlib.util.spec_from_file_location("validate_handback", REPOSITORY_ROOT / "shared" / "hooks" / "validate-handback.py")
assert specification is not None and specification.loader is not None
validator = importlib.util.module_from_spec(specification)
specification.loader.exec_module(validator)

SPEC = validator.load_schema("spec@1")

# v5 keeps the spec rules in the shared reference and the constitution; the plugins that drafted and gated
# specs are gone. List a spec drafter, gate or skill here when one is added, and these checks cover it.
DRAFTERS: list[str] = []
GATES: list[str] = []
SKILLS: list[str] = []
REFERENCE = "shared/references/verification/gate-readiness.md"
CONSTITUTION = "shared/constitution.md"

# Wording of the retired blanket ban. Any of these back in a spec prompt means a TBD fails a spec again.
RETIRED = [
    "regardless of how minor",
    "rather than emit a TBD",
    "No TBDs",
    "no TBDs remain",
    "never in TBD language",
    "Do not leave TBD markers",
    "An unknown goes in `non_goals` or `reasoning`",
]


def read(relative: str) -> str:
    return (REPOSITORY_ROOT / relative).read_text(encoding="utf-8")


def spec(scope: str) -> dict:
    return {
        "id": "SPEC-016",
        "purpose": "Let a visitor export the report table.",
        "scope": scope,
        "non_goals": ["Scheduled exports"],
        "acceptance_criteria": [
            {"id": "AC-001", "criterion": "Clicking Export downloads a CSV whose rows equal the table rows.", "is_error_case": False},
            {"id": "AC-002", "criterion": "With zero rows, Export is disabled and has the accessible name 'Export (no rows)'.", "is_error_case": True},
        ],
    }


def unknown_lines(document: dict) -> dict[str, list[str]]:
    lines = [line.strip() for line in document["scope"].splitlines()]
    return {label: [line for line in lines if line.startswith(f"{label}:")] for label in ("Assumption", "Open decision")}


class SpecUnknownTests(unittest.TestCase):
    def test_spec_1_carries_both_lines_in_scope_without_a_schema_change(self) -> None:
        document = spec(
            "Export button on the reports page.\n"
            "Assumption: the table holds at most 10,000 rows.\n"
            "Open decision: include hidden columns?; options: yes | no; affects: AC-001"
        )
        self.assertEqual(validator.validate(document, SPEC), [])
        found = unknown_lines(document)
        self.assertEqual(len(found["Assumption"]), 1)
        self.assertEqual(len(found["Open decision"]), 1)

    def test_a_separate_unknowns_field_would_need_a_new_schema_version(self) -> None:
        for field in ("assumptions", "open_decisions"):
            with self.subTest(field=field):
                self.assertTrue(validator.validate({**spec("Export button."), field: ["x"]}, SPEC))

    def test_scope_is_forwarded_and_reasoning_is_not(self) -> None:
        self.assertIn("scope", SPEC["required"])
        self.assertIn("not consumed downstream", SPEC["properties"]["reasoning"]["description"])

    def test_every_spec_prompt_uses_both_labels(self) -> None:
        for relative in [*DRAFTERS, *GATES, *SKILLS, REFERENCE, CONSTITUTION]:
            with self.subTest(file=relative):
                text = read(relative)
                self.assertIn("`Assumption:`", text)
                self.assertIn("`Open decision:`", text)

    def test_no_spec_prompt_bans_every_tbd(self) -> None:
        for relative in [*DRAFTERS, *GATES, *SKILLS, REFERENCE, CONSTITUTION]:
            text = read(relative)
            for phrase in RETIRED:
                with self.subTest(file=relative, phrase=phrase):
                    self.assertNotIn(phrase, text)

    def test_gates_block_undecided_and_untestable_unknowns_but_not_a_stated_assumption(self) -> None:
        for relative in [*GATES, REFERENCE]:
            with self.subTest(file=relative):
                text = read(relative)
                self.assertIn("owner_decision", text)
                self.assertIn("leaves a criterion untestable", text)
                self.assertRegex(text, r"(?i)(stated `?Assumption:?`? (SHALL NOT be|is not|is never) a blocker|never a stated assumption)")

    def test_open_decisions_go_to_the_user_not_the_drafter(self) -> None:
        for relative in SKILLS:
            if "gate-spec" in relative and "codex" in relative:
                continue
            with self.subTest(file=relative):
                self.assertRegex(read(relative), r"(?i)(open decision|owner_decision)[^.]*(to the user|for the user)")


if __name__ == "__main__":
    unittest.main()
