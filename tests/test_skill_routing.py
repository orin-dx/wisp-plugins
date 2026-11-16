import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = sorted(ROOT.glob("plugins/*/skills/*/SKILL.md"))
DESCRIPTION_CAP = 450
# Codex gate skills carry the gate round rule themselves: no role card is read on the single-agent path.
# The remaining plugins have no gate skill; list one here when it is added.
CODEX_GATES: tuple[str, ...] = ()
# Codex skills that verify against evidence name the behavior-evidence reference and ship it.
CODEX_EVIDENCE: tuple[str, ...] = ()
EVIDENCE = "shared/references/verification/evidence.md"
CONTEXT = "shared/references/tooling/context.md"

# Skills that run commands, builds or renders, or read the workspace broadly.
RUNS_COMMANDS = {
    "muse/skills/sketch",
}
# Read-only analysis or exploration: no freehand alternative to replace.
NO_FREEHAND_CLAIM = {
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
        for name in ("courier/skills/changeset",):
            path = ROOT / "plugins" / name / "SKILL.md"
            with self.subTest(skill=name):
                self.assertTrue(description(path).startswith("Use this, not"))
                self.assertIn("freehand", codex_path(path).read_text().split("\n")[2].lower())

    def test_codex_gate_skills_state_the_round_rule(self):
        for name in CODEX_GATES:
            text = (ROOT / "harnesses/codex/plugins" / name / "SKILL.md").read_text()
            with self.subTest(skill=name):
                self.assertIn("escalation_required", text)
                self.assertIn("complete blocker set", text)
                self.assertNotIn("round rules", text)

    def test_codex_verifying_skills_name_and_ship_the_behavior_evidence_reference(self):
        catalog = (ROOT / "harnesses/codex/catalog.json").read_text()
        for name in CODEX_EVIDENCE:
            plugin = name.split("/")[0]
            with self.subTest(skill=name):
                self.assertIn(EVIDENCE, (ROOT / "harnesses/codex/plugins" / name / "SKILL.md").read_text())
                entry = re.search(rf'"id": "{plugin}",\s*"runtime_files": \[(.*?)\]', catalog, re.S)
                self.assertIsNotNone(entry)
                self.assertIn(EVIDENCE, entry.group(1))


if __name__ == "__main__":
    unittest.main()
