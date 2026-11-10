"""Check ADR-014: plans state outcomes and contracts, code only where it earns its cost, with no schema change."""

from __future__ import annotations

import copy
import importlib.util
import json
import re
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
specification = importlib.util.spec_from_file_location("validate_handback", REPOSITORY_ROOT / "shared" / "hooks" / "validate-handback.py")
assert specification is not None and specification.loader is not None
validator = importlib.util.module_from_spec(specification)
specification.loader.exec_module(validator)

PLAN_SCHEMA = validator.load_schema("plan@1")
NAVIGATOR = REPOSITORY_ROOT / "plugins/navigator"


def read(relative: str) -> str:
    return (REPOSITORY_ROOT / relative).read_text(encoding="utf-8")


def outcome_level_plan() -> dict:
    return {
        "goal": "Add a capped exponential backoff retry helper to textkit.",
        "architecture": "A new retry module wraps a callable; the CLI count subcommand calls it.",
        "tech_stack": ["python"],
        "linked_spec": "SPEC-100",
        "spec_file_path": "docs/specs/SPEC-100.json",
        "spec_hash": "sha256:00",
        "tasks": [
            {
                "id": "T1",
                "title": "Add retry module",
                "files": {"create": ["textkit/retry.py"], "test": ["tests/test_retry.py"]},
                "steps": [
                    "Outcome: textkit/retry.py exists and retry_call retries with capped exponential backoff.",
                    "Signature: def retry_call(fn, attempts=3, base_delay=0.1, max_delay=1.0, sleep=time.sleep) -> T; ValueError when attempts < 1.",
                    "Test AC-002: fn fails twice then returns; assert sleeps == [0.1, 0.2].",
                    "Verify: python3 -m unittest discover -s tests, exit code 0.",
                ],
                "commit_message": "feat(retry): add retry_call",
                "depends_on": [],
                "covers_criteria": ["AC-001", "AC-002"],
            },
            {
                "id": "T2",
                "title": "Wire --retries into the count command",
                "files": {"modify": ["textkit/cli.py"], "test": ["tests/test_cli.py"]},
                "steps": [
                    "Outcome: textkit count accepts --retries N and exits 2 for N < 1.",
                    "Verify: python3 -m unittest discover -s tests, exit code 0.",
                ],
                "commit_message": "feat(cli): add --retries to count",
                "depends_on": ["T1"],
                "covers_criteria": ["AC-006"],
            },
        ],
    }


class PlanSchemaDecisionTest(unittest.TestCase):
    def test_no_new_plan_version_was_added(self) -> None:
        self.assertEqual(sorted(path.name for path in (REPOSITORY_ROOT / "shared/schemas").glob("plan@*.json")), ["plan@1.json"])

    def test_code_is_not_a_required_task_field(self) -> None:
        task = PLAN_SCHEMA["properties"]["tasks"]["items"]
        self.assertEqual(sorted(task["required"]), ["commit_message", "files", "id", "steps", "title"])
        self.assertFalse(task["additionalProperties"])
        self.assertNotIn("code", task["properties"])

    def test_outcome_level_plan_validates(self) -> None:
        self.assertEqual(validator.validate(outcome_level_plan(), PLAN_SCHEMA), [])

    def test_extra_task_keys_are_rejected(self) -> None:
        plan = outcome_level_plan()
        plan["tasks"][0]["outcome"] = "not a schema field"
        self.assertNotEqual(validator.validate(plan, PLAN_SCHEMA), [])

    def test_plan_without_code_still_covers_every_criterion(self) -> None:
        plan = outcome_level_plan()
        covered = {criterion for task in plan["tasks"] for criterion in task["covers_criteria"]}
        self.assertEqual(covered, {"AC-001", "AC-002", "AC-006"})
        self.assertFalse(any("```" in step for task in plan["tasks"] for step in task["steps"]))


class PlannerRulesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.planner = read("plugins/navigator/agents/planner.md")

    def test_planner_names_the_required_task_content(self) -> None:
        for phrase in ("The outcome", "signatures", "verification command", "covers_criteria", "commit message"):
            self.assertIn(phrase, self.planner)

    def test_planner_limits_code_to_non_obvious_logic(self) -> None:
        self.assertIn("non-obvious or a wrong shape would be costly", self.planner)
        self.assertNotIn("The exact implementation code\n", self.planner)

    def test_planner_keeps_steps_inside_the_schema(self) -> None:
        self.assertIn("add no other keys", self.planner)
        self.assertIn("`steps` strings", self.planner)

    def test_planner_still_forbids_placeholders(self) -> None:
        self.assertIn("NEVER use placeholders", self.planner)

    def test_planner_description_fits_the_limit(self) -> None:
        description = re.search(r"description: >-\n((?:  .*\n)+)", self.planner)
        assert description is not None
        self.assertLessEqual(len(" ".join(description.group(1).split())), 450)


class ChallengerRulesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.challenger = read("plugins/navigator/agents/challenger.md")

    def test_challenger_flags_bodies_for_routine_logic(self) -> None:
        self.assertIn("full function body for routine logic", self.challenger)

    def test_challenger_does_not_require_code(self) -> None:
        self.assertIn("Absence of implementation code is not under-specification", self.challenger)

    def test_challenger_keeps_its_structural_checks(self) -> None:
        for kind in ("wrong-order", "orphaned-criteria", "interface-incompleteness", "missing-error-handling", "poor-batching"):
            self.assertIn(kind, self.challenger)


class ConsumerAndCounterpartTest(unittest.TestCase):
    def test_implementer_may_still_reshape_plan_code(self) -> None:
        self.assertIn("Copying the plan's code when a better shape meets the same files, criteria, and tests", read("plugins/smith/agents/implementer.md"))

    def test_estimator_does_not_depend_on_plan_code(self) -> None:
        self.assertNotRegex(read("plugins/navigator/agents/estimator.md").lower(), r"exact (implementation )?code")

    def test_codex_skill_matches_the_rule(self) -> None:
        codex = read("harnesses/codex/plugins/navigator/skills/plan/SKILL.md")
        self.assertIn("non-obvious or a wrong shape would be costly", codex)
        self.assertNotIn("concrete code baseline", codex)

    def test_claude_skill_points_to_the_record(self) -> None:
        self.assertIn("014-outcome-level-plans.md", read("plugins/navigator/skills/plan/SKILL.md"))

    def test_record_supersedes_only_the_code_requirement(self) -> None:
        record = read("docs/adr/014-outcome-level-plans.md")
        self.assertIn("**Supersedes:**", record)
        self.assertIn("ADR-009", record)
        self.assertIn("superseded by ADR-014", read("docs/adr/009-implementer-shape-latitude.md").split("\n")[2])


if __name__ == "__main__":
    unittest.main()
