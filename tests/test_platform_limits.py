"""Cover scripts/check-platform-limits.py on synthetic trees and on the real repository."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPOSITORY_ROOT / "scripts" / "check-platform-limits.py"

specification = importlib.util.spec_from_file_location("check_platform_limits", SCRIPT)
assert specification is not None and specification.loader is not None
limits = importlib.util.module_from_spec(specification)
specification.loader.exec_module(limits)


def write(root: Path, relative: str, text: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def agent(name: str, description: str) -> str:
    return f"---\nname: {name}\nrole: Example\nmodel: sonnet\neffort: medium\ndescription: >-\n  {description}\n---\n\nBody.\n"


def skill(name: str, description: str, version: str = "1.0.0") -> str:
    return f"---\nname: {name}\ndescription: {description}\nversion: {version}\n---\n\nBody.\n"


class PlatformLimitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        write(self.root, "plugins/alpha/agents/worker.md", agent("worker", "Does the work."))
        write(self.root, "plugins/alpha/skills/run/SKILL.md", skill("run", "Runs the pipeline."))
        write(self.root, "plugins/beta/agents/judge.md", agent("judge", "Judges the result."))
        write(self.root, "plugins/beta/skills/check/SKILL.md", skill("check", "Checks the result."))

    def test_folded_frontmatter_values_are_joined(self) -> None:
        meta = limits.parse_frontmatter(agent("worker", "First part second part."))
        self.assertEqual(meta["description"], "First part second part.")
        self.assertEqual(meta["name"], "worker")

    def test_existing_references_resolve(self) -> None:
        write(self.root, "plugins/alpha/README.md", "Hand off to `beta:judge`, then run beta/check and alpha:run.\n")
        self.assertEqual(limits.check_cross_references(self.root), [])

    def test_missing_references_are_reported_with_file_and_line(self) -> None:
        write(self.root, "plugins/alpha/README.md", "Intro.\nSee `beta:referee` for judgment.\nOr beta/verify.\n")
        failures = limits.check_cross_references(self.root)
        self.assertEqual(len(failures), 2)
        self.assertIn("plugins/alpha/README.md:2", failures[0])
        self.assertIn("beta:referee", failures[0])
        self.assertIn("beta/verify", failures[1])

    def test_negative_statements_and_paths_are_not_references(self) -> None:
        write(
            self.root,
            "plugins/alpha/README.md",
            "There is no separate beta/verify skill to invoke.\nSee ../beta/ and plugins/beta/agents and https://example.com/beta/page.\n",
        )
        self.assertEqual(limits.check_cross_references(self.root), [])

    def test_description_budget_fails_only_above_the_threshold(self) -> None:
        failures, summary = limits.check_description_budget(self.root)
        self.assertEqual(failures, [])
        self.assertIn("2 agent descriptions", summary)
        write(self.root, "plugins/alpha/agents/huge.md", agent("huge", "x" * (12_000 * 4)))
        failures, _ = limits.check_description_budget(self.root)
        self.assertEqual(len(failures), 1)

    def test_skill_name_and_length_are_checked(self) -> None:
        write(self.root, "plugins/alpha/skills/wrong/SKILL.md", skill("other-name", "Fine."))
        write(self.root, "plugins/alpha/skills/long/SKILL.md", skill("long", "x" * 1_025))
        failures = limits.check_skill_metadata(self.root)
        self.assertEqual(len(failures), 2)
        self.assertTrue(any("must equal its directory name" in failure for failure in failures))
        self.assertTrue(any("1025 characters" in failure for failure in failures))

    def test_codex_budget(self) -> None:
        write(self.root, "harnesses/codex/plugins/alpha/skills/run/SKILL.md", skill("run", "x" * 8_001))
        failures, _ = limits.check_codex_budget(self.root)
        self.assertEqual(len(failures), 1)

    def test_the_repository_passes_its_own_checks(self) -> None:
        self.assertEqual(limits.check_cross_references(REPOSITORY_ROOT), [])
        self.assertEqual(limits.check_skill_metadata(REPOSITORY_ROOT), [])
        self.assertEqual(limits.check_description_budget(REPOSITORY_ROOT)[0], [])
        self.assertEqual(limits.check_codex_budget(REPOSITORY_ROOT)[0], [])


if __name__ == "__main__":
    unittest.main()
