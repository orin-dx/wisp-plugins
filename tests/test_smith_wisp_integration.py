"""Guard Smith's optional Wisp handoff across native harnesses."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CLAUDE_SKILL = ROOT / "plugins/smith/skills/implement/SKILL.md"
CODEX_SKILL = ROOT / "harnesses/codex/plugins/smith/skills/implement/SKILL.md"
SCHEMA = "shared/schemas/implementation-context@1.json"


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path} must contain a JSON object")
    return value


class SmithWispIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.claude = CLAUDE_SKILL.read_text(encoding="utf-8").lower()
        cls.codex = CODEX_SKILL.read_text(encoding="utf-8").lower()

    def test_both_harnesses_require_success_and_exact_selection(self) -> None:
        for harness, source in (("Claude/AGY", self.claude), ("Codex", self.codex)):
            with self.subTest(harness=harness):
                self.assertIn("implementation-context@1", source)
                self.assertIn("status: ok", source)
                self.assertIn("selection", source)
                self.assertIn("exact", source)
                self.assertIn("untrusted workspace data", source)
                self.assertIn("higher-priority instructions", source)

    def test_fallback_preserves_each_native_drift_policy(self) -> None:
        self.assertIn("unavailable", self.claude)
        self.assertIn("error", self.claude)
        self.assertIn("unsupported", self.claude)
        self.assertIn("malformed", self.claude)
        self.assertIn("spec-drift warning", self.claude)
        self.assertIn("unavailable", self.codex)
        self.assertIn("error", self.codex)
        self.assertIn("unsupported", self.codex)
        self.assertIn("malformed", self.codex)
        self.assertIn("stop-on-spec-drift", self.codex)

    def test_codex_runtime_packages_the_shared_result_schema(self) -> None:
        catalog = read_json(ROOT / "harnesses/codex/catalog.json")
        smith = next(plugin for plugin in catalog["plugins"] if plugin["id"] == "smith")
        self.assertIn(SCHEMA, smith["runtime_files"])
        self.assertTrue((ROOT / SCHEMA).is_file())

    def test_smith_declares_the_optional_contract(self) -> None:
        manifest = read_json(ROOT / "plugins/smith/plugin.json")
        self.assertIn("implementation-context@1", manifest["consumes"])


if __name__ == "__main__":
    unittest.main()
