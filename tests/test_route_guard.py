"""Cover the routing guard: direct calls to pipeline agents go through a skill first, once per agent."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPOSITORY_ROOT / "shared" / "hooks" / "route-guard.py"
specification = importlib.util.spec_from_file_location("route_guard", TOOL)
assert specification is not None and specification.loader is not None
guard = importlib.util.module_from_spec(specification)
specification.loader.exec_module(guard)

GUARDED = ("muse", "navigator", "ranger", "scribe", "sentinel", "smith")


def agent(subagent_type: str, session: str = "s1", **extra) -> dict:
    return {"hook_event_name": "PreToolUse", "session_id": session, "tool_name": "Agent", "tool_input": {"subagent_type": subagent_type, "prompt": "x"}, **extra}


def skill(name: str, session: str = "s1") -> dict:
    return {"hook_event_name": "PreToolUse", "session_id": session, "tool_name": "Skill", "tool_input": {"skill": name}}


def prompt(text: str, session: str = "s1") -> dict:
    return {"hook_event_name": "UserPromptSubmit", "session_id": session, "prompt": text}


class RouteGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.state = Path(directory.name)

    def decide(self, event: dict, plugin: str = "smith"):
        return guard.decide(event, plugin, self.state)

    def test_a_direct_call_is_redirected_once_and_names_the_skill(self) -> None:
        denied = self.decide(agent("smith:reviewer"))
        self.assertEqual(denied["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertIn("smith:implement", denied["hookSpecificOutput"]["permissionDecisionReason"])
        self.assertIsNone(self.decide(agent("smith:reviewer")))
        self.assertIsNotNone(self.decide(agent("smith:exit-gate")))

    def test_a_skill_started_by_the_model_or_by_a_slash_command_allows_its_agents(self) -> None:
        self.assertIsNone(self.decide(skill("smith:implement")))
        self.assertIsNone(self.decide(agent("smith:reviewer")))
        self.assertIsNone(self.decide(prompt("/smith:spike does this work?", session="s2")))
        self.assertIsNone(self.decide(agent("smith:implementer", session="s2")))

    def test_other_plugins_sessions_and_subagent_calls_are_left_alone(self) -> None:
        self.assertIsNone(self.decide(skill("scribe:gate-spec")))
        self.assertIsNotNone(self.decide(agent("smith:reviewer")))
        self.assertIsNone(self.decide(agent("general-purpose")))
        self.assertIsNone(self.decide(agent("scribe:auditor")))
        self.assertIsNone(self.decide(agent("smith:mutator", agent_id="inner")))
        self.assertIsNotNone(self.decide(agent("smith:reviewer", session="other")))

    def test_the_guard_can_be_turned_off(self) -> None:
        os.environ["WISP_ROUTE_GUARD"] = "off"
        self.addCleanup(os.environ.pop, "WISP_ROUTE_GUARD", None)
        self.assertIsNone(self.decide(agent("smith:reviewer")))

    def test_parallel_calls_keep_every_record(self) -> None:
        from concurrent.futures import ThreadPoolExecutor

        environment = {**os.environ, "WISP_ROUTE_STATE_DIR": str(self.state)}

        def call(payload: dict, plugin: str) -> str:
            done = subprocess.run([sys.executable, str(TOOL), plugin], input=json.dumps(payload), capture_output=True, text=True, env=environment, check=False)
            return done.stdout

        starts = [(skill("smith:implement", session="par"), "smith"), (skill("ranger:audit", session="par"), "ranger")] * 4
        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(lambda args: call(*args), starts))
        for plugin, agent_type in (("smith", "smith:reviewer"), ("ranger", "ranger:adversary")):
            self.assertEqual(call(agent(agent_type, session="par"), plugin), "", f"{agent_type} was denied although its skill had started")
        denials = list(ThreadPoolExecutor(max_workers=8).map(lambda _: call(agent("scribe:auditor", session="par2"), "scribe"), range(8)))
        self.assertEqual(sum(1 for out in denials if out), 1, "exactly one parallel direct call is redirected")

    def test_command_contract_and_fail_open(self) -> None:
        environment = {**os.environ, "WISP_ROUTE_STATE_DIR": str(self.state)}
        denied = subprocess.run([sys.executable, str(TOOL), "ranger"], input=json.dumps(agent("ranger:adversary", session="cli")), capture_output=True, text=True, env=environment, check=False)
        self.assertEqual(denied.returncode, 0)
        self.assertEqual(json.loads(denied.stdout)["hookSpecificOutput"]["permissionDecision"], "deny")
        broken = subprocess.run([sys.executable, str(TOOL), "ranger"], input="not json", capture_output=True, text=True, env=environment, check=False)
        self.assertEqual((broken.returncode, broken.stdout), (1, ""))

    def test_every_pipeline_plugin_registers_the_guard_for_itself(self) -> None:
        for plugin in GUARDED:
            with self.subTest(plugin=plugin):
                hooks = json.loads((REPOSITORY_ROOT / "plugins" / plugin / "hooks" / "hooks.json").read_text(encoding="utf-8"))["hooks"]
                commands = [h["command"] for entry in hooks["PreToolUse"] for h in entry["hooks"]]
                self.assertTrue(any(c.endswith(f'route-guard.py" {plugin}') for c in commands), commands)
                prompt_commands = [h["command"] for entry in hooks["UserPromptSubmit"] for h in entry["hooks"]]
                self.assertTrue(any(c.endswith(f'route-guard.py" {plugin}') for c in prompt_commands))
                self.assertIn(plugin, guard.SUGGEST)


if __name__ == "__main__":
    unittest.main()
