"""Cover the `wisp` core plugin (ADR 018): its agents, skills, hooks and Codex counterpart.

The Stop hook (shared/hooks/stop-check.py) is exercised through its real stdin/stdout contract
against throwaway repositories, so the tests see what Claude Code sees.
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "wisp"
CODEX = ROOT / "harnesses" / "codex" / "plugins" / "wisp"
STOP_CHECK = ROOT / "shared" / "hooks" / "stop-check.py"
HANDBACK = ROOT / "shared" / "hooks" / "validate-handback.py"
DESCRIPTION_CAP = 450
AGENT_TIERS = {"verifier": ("opus", "high"), "adversary": ("opus", "high"), "recon": ("haiku", "low")}
MODES = ("explore", "spike", "fix", "build", "check", "ship")
REFERENCES = ("modes.md", "decision-cards.md", "verifier-brief.md", "specs-and-plans.md")


def frontmatter(path: Path) -> tuple[dict[str, str], str]:
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


def load(path: Path, name: str):
    specification = importlib.util.spec_from_file_location(name, path)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class WispStructureTests(unittest.TestCase):
    def test_manifest_names_the_plugin_and_lists_exactly_its_agents(self) -> None:
        manifest = json.loads((PLUGIN / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual((manifest["id"], manifest["name"]), ("wisp", "wisp"))
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertEqual(sorted(Path(item).stem for item in manifest["agents"]), sorted(AGENT_TIERS))
        self.assertEqual(sorted(path.stem for path in (PLUGIN / "agents").glob("*.md")), sorted(AGENT_TIERS))
        self.assertIn("verdict@3", manifest["produces"])

    def test_shared_is_a_link_to_the_repository_shared_tree(self) -> None:
        link = PLUGIN / "shared"
        self.assertTrue(link.is_symlink())
        self.assertEqual(os.readlink(link), "../../shared")
        self.assertTrue((link / "hooks" / "stop-check.py").is_file())

    def test_agents_have_their_tier_and_a_capped_description(self) -> None:
        for name, tier in AGENT_TIERS.items():
            with self.subTest(agent=name):
                meta, _ = frontmatter(PLUGIN / "agents" / f"{name}.md")
                self.assertEqual(meta["name"], name)
                self.assertEqual((meta["model"], meta["effort"]), tier)
                self.assertLessEqual(len(meta["description"]), DESCRIPTION_CAP)

    def test_work_and_its_six_aliases_exist_with_capped_descriptions(self) -> None:
        for name in ("work", *MODES):
            with self.subTest(skill=name):
                meta, body = frontmatter(PLUGIN / "skills" / name / "SKILL.md")
                self.assertEqual(meta["name"], name)
                self.assertLessEqual(len(meta["description"]), DESCRIPTION_CAP)
                if name != "work":
                    lines = [line for line in body.splitlines() if line.strip() and not line.startswith("#")]
                    self.assertEqual(lines, [f"Start the `wisp:work` skill in {name} mode with the user's request."])

    def test_work_references_exist_and_fit_the_cap(self) -> None:
        for reference in REFERENCES:
            with self.subTest(reference=reference):
                path = ROOT / "shared" / "references" / "work" / reference
                self.assertLessEqual(len(path.read_text(encoding="utf-8").splitlines()), 120)


class WispHookRegistrationTests(unittest.TestCase):
    def test_hooks_register_the_stop_check_and_the_handback_validator(self) -> None:
        hooks = json.loads((PLUGIN / "hooks" / "hooks.json").read_text(encoding="utf-8"))["hooks"]
        self.assertIn("shared/hooks/stop-check.py", hooks["Stop"][0]["hooks"][0]["command"])
        handback = [entry for entry in hooks["PreToolUse"] if entry["matcher"] == "SubagentHandback"]
        self.assertIn("shared/hooks/validate-handback.py", handback[0]["hooks"][0]["command"])

    def test_verifier_is_routed_to_verdict_3_and_retired_gates_are_not(self) -> None:
        routes = load(HANDBACK, "validate_handback_for_wisp").ROUTES
        self.assertEqual(routes.get("wisp:verifier"), ("verdict@3",))
        for retired in ("ranger", "scribe", "sentinel", "smith", "navigator", "weaver", "vanguard", "guide"):
            self.assertFalse(any(agent.startswith(f"{retired}:") for agent in routes), retired)


class StopCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.repository = Path(self.directory.name) / "repository"
        self.repository.mkdir()
        subprocess.run(["git", "init", "-q", str(self.repository)], check=True)

    def run_hook(self, payload: object, raw: str | None = None) -> subprocess.CompletedProcess[str]:
        environment = {key: value for key, value in os.environ.items() if key != "WISP_STOP_CHECK"}
        return subprocess.run(
            [sys.executable, str(STOP_CHECK)],
            input=raw if raw is not None else json.dumps(payload),
            capture_output=True,
            text=True,
            env=environment,
            check=False,
        )

    def event(self, message: str = "Done.", active: bool = False, **extra: object) -> dict:
        return {"hook_event_name": "Stop", "session_id": "s1", "cwd": str(self.repository), "stop_hook_active": active, "last_assistant_message": message, **extra}

    def dirty(self, name: str = "change.txt", text: str = "edit") -> None:
        (self.repository / name).write_text(text, encoding="utf-8")

    def assert_blocked(self, completed: subprocess.CompletedProcess[str]) -> None:
        self.assertEqual(completed.returncode, 0)
        decision = json.loads(completed.stdout)
        self.assertEqual(decision["decision"], "block")
        self.assertIn("Not verified:", decision["reason"])

    def assert_allowed(self, completed: subprocess.CompletedProcess[str]) -> None:
        self.assertEqual(completed.stdout, "")

    def test_a_clean_tree_stops_freely(self) -> None:
        self.assert_allowed(self.run_hook(self.event()))

    def test_uncommitted_changes_without_the_line_block_once_then_pass(self) -> None:
        self.dirty()
        self.assert_blocked(self.run_hook(self.event()))
        self.assert_allowed(self.run_hook(self.event(active=True)))

    def test_the_line_lets_the_stop_through_in_any_case(self) -> None:
        self.dirty()
        self.assert_allowed(self.run_hook(self.event("Tests pass.\n\nnot verified: Safari")))

    def test_the_final_message_falls_back_to_the_transcript(self) -> None:
        self.dirty()
        transcript = Path(self.directory.name) / "transcript.jsonl"
        lines = [
            {"type": "user", "message": {"content": "fix it"}},
            {"type": "assistant", "message": {"content": [{"type": "text", "text": "Fixed. Not verified: Windows."}]}},
        ]
        transcript.write_text("\n".join(json.dumps(line) for line in lines) + "\n", encoding="utf-8")
        payload = self.event(transcript_path=str(transcript))
        del payload["last_assistant_message"]
        self.assert_allowed(self.run_hook(payload))

    def test_outside_a_work_tree_it_does_nothing(self) -> None:
        outside = Path(self.directory.name) / "plain"
        outside.mkdir()
        (outside / "file.txt").write_text("x", encoding="utf-8")
        self.assert_allowed(self.run_hook({**self.event(), "cwd": str(outside)}))

    def test_it_fails_open_on_garbage_input(self) -> None:
        completed = self.run_hook(None, raw="not a hook payload")
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(completed.stdout, "")

    def test_it_can_be_switched_off(self) -> None:
        self.dirty()
        module = load(STOP_CHECK, "stop_check")
        os.environ["WISP_STOP_CHECK"] = "off"
        self.addCleanup(os.environ.pop, "WISP_STOP_CHECK", None)
        self.assertIsNone(module.decide(self.event()))


class WispCodexCounterpartTests(unittest.TestCase):
    def test_codex_has_the_same_skill_routes_identity_and_the_unverified_rule(self) -> None:
        source = {path.parent.name for path in (PLUGIN / "skills").glob("*/SKILL.md")}
        native = {path.parent.name for path in (CODEX / "skills").glob("*/SKILL.md")}
        self.assertEqual(native, source)
        manifest = json.loads((CODEX / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        shared = json.loads((PLUGIN / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual((manifest["name"], manifest["version"], manifest["author"]), (shared["id"], shared["version"], shared["author"]))


if __name__ == "__main__":
    unittest.main()
