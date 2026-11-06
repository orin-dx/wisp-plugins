import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = sorted(ROOT.glob("plugins/*/agents/*.md"))
SKILLS = sorted(ROOT.glob("plugins/*/skills/*/SKILL.md"))

# Descriptions are routing text loaded into every session; keep them short.
AGENT_DESCRIPTION_CAP = 450
SKILL_DESCRIPTION_CAP = 600


def frontmatter(path):
    match = re.match(r"---\n(.*?)\n---\n", path.read_text(), re.S)
    return match.group(1) if match else ""


def field(path, key):
    match = re.search(rf"^{key}:\s*(.+)$", frontmatter(path), re.M)
    return match.group(1).strip() if match else None


def description(path):
    match = re.search(
        r"^description:\s*(?:>-?|\|-?)?\s*\n?(.*?)(?=^[a-zA-Z_-]+:|\Z)",
        frontmatter(path),
        re.S | re.M,
    )
    return re.sub(r"\s+", " ", match.group(1)).strip() if match else ""


class PromptAlignmentTests(unittest.TestCase):
    def test_constitution_block_is_identical_in_every_agent(self):
        blocks = {}
        for path in AGENTS:
            match = re.search(r"<constitution>(.*?)</constitution>", path.read_text(), re.S)
            self.assertIsNotNone(match, path)
            blocks.setdefault(match.group(1), []).append(path.name)
        self.assertEqual(1, len(blocks), {k[:40]: v for k, v in blocks.items()})

    def test_descriptions_stay_routing_text(self):
        for paths, cap in ((AGENTS, AGENT_DESCRIPTION_CAP), (SKILLS, SKILL_DESCRIPTION_CAP)):
            for path in paths:
                with self.subTest(path=str(path.relative_to(ROOT))):
                    self.assertLessEqual(len(description(path)), cap)

    def test_exit_gates_run_at_the_tier_the_constitution_names(self):
        constitution = (ROOT / "shared/constitution.md").read_text()
        opus_line = next(line for line in constitution.splitlines() if line.startswith("- `opus / high`"))
        self.assertIn("exit gates", opus_line)
        gates = sorted(ROOT.glob("plugins/*/agents/exit-gate.md"))
        self.assertGreaterEqual(len(gates), 5)
        for path in gates:
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertEqual("opus", field(path, "model"))
                self.assertEqual("high", field(path, "effort"))

    def test_no_prompt_or_manifest_references_a_retired_verdict_version(self):
        sources = AGENTS + SKILLS + sorted(ROOT.glob("plugins/*/plugin.json")) + sorted(ROOT.glob("plugins/*/README.md"))
        for path in sources:
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertNotIn("verdict@1", path.read_text())


if __name__ == "__main__":
    unittest.main()
