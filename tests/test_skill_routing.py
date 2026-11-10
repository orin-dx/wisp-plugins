import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGINS = ("ranger", "sentinel", "muse", "scribe")
SKILLS = sorted(p for plugin in PLUGINS for p in ROOT.glob(f"plugins/{plugin}/skills/*/SKILL.md"))
DESCRIPTION_CAP = 450
CONTEXT = "shared/references/tooling/context.md"

# Skills that run commands, builds or renders, or read the workspace broadly.
RUNS_COMMANDS = {
    "ranger/skills/audit",
    "sentinel/skills/gate",
    "muse/skills/sketch",
    "scribe/skills/audit-architecture",
    "scribe/skills/spec-drift",
}
# Read-only analysis or exploration: no freehand alternative to replace.
NO_FREEHAND_CLAIM = {
    "scribe/skills/spec-drift",
    "scribe/skills/audit-architecture",
    "scribe/skills/verify-spec",
    "scribe/skills/architect",
    "muse/skills/promote",
}


def key(path):
    return str(path.parent.relative_to(ROOT / "plugins"))


def description(path):
    text = path.read_text()
    match = re.search(r"^description:\s*(?:>-?)?\s*\n?(.*?)(?=^[a-zA-Z_-]+:)", text.split("---")[1], re.S | re.M)
    return re.sub(r"\s+", " ", match.group(1)).strip()


def codex_path(path):
    plugin, _, skill = key(path).split("/")
    return ROOT / "harnesses/codex/plugins" / plugin / "skills" / skill / "SKILL.md"


class SkillRoutingTests(unittest.TestCase):
    def test_all_skills_found(self):
        self.assertGreaterEqual(len(SKILLS), 13)

    def test_descriptions_fit_the_routing_cap(self):
        for path in SKILLS:
            with self.subTest(skill=key(path)):
                self.assertLessEqual(len(description(path)), DESCRIPTION_CAP)

    def test_command_running_skills_route_the_context_reference(self):
        for path in SKILLS:
            if key(path) in RUNS_COMMANDS:
                with self.subTest(skill=key(path)):
                    self.assertIn(CONTEXT, path.read_text())
                    self.assertIn(CONTEXT, codex_path(path).read_text())

    def test_codex_catalog_lists_the_reference_for_each_plugin_that_loads_it(self):
        catalog = (ROOT / "harnesses/codex/catalog.json").read_text()
        for plugin in {k.split("/")[0] for k in RUNS_COMMANDS}:
            with self.subTest(plugin=plugin):
                entry = re.search(rf'"id": "{plugin}",\s*"runtime_files": \[(.*?)\]', catalog, re.S)
                self.assertIsNotNone(entry)
                self.assertIn(CONTEXT, entry.group(1))

    def test_read_only_analysis_skills_do_not_claim_to_replace_freehand_work(self):
        for path in SKILLS:
            if key(path) in NO_FREEHAND_CLAIM:
                with self.subTest(skill=key(path)):
                    self.assertNotIn("freehand", description(path).lower())
                    self.assertNotIn("freehand", codex_path(path).read_text().split("\n")[2].lower())

    def test_skills_that_replace_freehand_work_say_so_in_both_harnesses(self):
        for name in ("ranger/skills/audit", "sentinel/skills/gate", "muse/skills/component", "scribe/skills/draft-spec"):
            path = ROOT / "plugins" / name / "SKILL.md"
            with self.subTest(skill=name):
                self.assertTrue(description(path).startswith("Use this, not"))
                self.assertIn("freehand", codex_path(path).read_text().split("\n")[2].lower())


if __name__ == "__main__":
    unittest.main()
