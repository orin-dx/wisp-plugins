"""Enforce the agent authoring conventions on every plugin agent.

ADR 001 and ADR 006: every agent body has the five parts in order (constitution, backstory, goal,
judgment, output) with a byte-identical constitution, and no `<role>` section or `success_criteria`
checklist. Frontmatter names the agent, its role, and a model and effort tier.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
AGENTS = sorted(REPOSITORY_ROOT.glob("plugins/*/agents/*.md"))
PARTS = ["constitution", "backstory", "goal", "judgment", "output"]
TIERS = {("haiku", "low"), ("sonnet", "medium"), ("opus", "high")}


def split(path: Path) -> tuple[dict[str, str], str]:
    match = re.match(r"---\n(.*?)\n---\n(.*)", path.read_text(encoding="utf-8"), re.S)
    assert match, f"{path} has no frontmatter"
    meta: dict[str, str] = {}
    key = None
    for line in match.group(1).splitlines():
        found = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if found and not line.startswith(" "):
            key = found.group(1)
            meta[key] = "" if found.group(2).strip() in (">", ">-", "|") else found.group(2).strip()
        elif key and line.strip():
            meta[key] = (meta[key] + " " + line.strip()).strip()
    return meta, match.group(2)


class AgentStructureTests(unittest.TestCase):
    def test_there_are_agents_to_check(self) -> None:
        self.assertGreaterEqual(len(AGENTS), 40)

    def test_frontmatter_names_the_agent_and_its_tier(self) -> None:
        for path in AGENTS:
            with self.subTest(agent=path.relative_to(REPOSITORY_ROOT).as_posix()):
                meta, _ = split(path)
                self.assertEqual(meta.get("name"), path.stem)
                for key in ("role", "description", "model", "effort"):
                    self.assertTrue(meta.get(key), key)
                self.assertIn((meta["model"], meta["effort"]), TIERS)

    def test_the_five_parts_appear_once_and_in_order(self) -> None:
        for path in AGENTS:
            with self.subTest(agent=path.relative_to(REPOSITORY_ROOT).as_posix()):
                _, body = split(path)
                opened = re.findall(r"^<([a-z_]+)>$", body, re.M)
                self.assertEqual([part for part in opened if part in PARTS], PARTS)
                for part in PARTS:
                    self.assertEqual(len(re.findall(rf"^</{part}>$", body, re.M)), 1, part)
                    self.assertLess(body.index(f"<{part}>"), body.index(f"</{part}>"), part)
                self.assertNotIn("role", opened)
                self.assertNotIn("success_criteria", opened)

    def test_the_constitution_is_byte_identical_in_every_agent(self) -> None:
        blocks = {}
        for path in AGENTS:
            _, body = split(path)
            match = re.search(r"<constitution>.*?</constitution>", body, re.S)
            self.assertIsNotNone(match, path.name)
            blocks.setdefault(match.group(0), []).append(path.relative_to(REPOSITORY_ROOT).as_posix())
        self.assertEqual(len(blocks), 1, {key[:40]: value[:3] for key, value in blocks.items()})


if __name__ == "__main__":
    unittest.main()
