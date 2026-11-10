"""Cover the SubagentHandback validator spike (shared/hooks/validate-handback.py).

The hook denies a gate agent's handback when it does not conform to its verdict schema, caps
denials per agent, ignores other agents, and fails open on internal errors. These tests exercise
the decision function directly and the command through its real stdin/stdout contract.
"""

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
TOOL = REPOSITORY_ROOT / "shared" / "hooks" / "validate-handback.py"

specification = importlib.util.spec_from_file_location("validate_handback", TOOL)
assert specification is not None and specification.loader is not None
validate_handback = importlib.util.module_from_spec(specification)
specification.loader.exec_module(validate_handback)

VALID_PASS_V3 = {
    "verdict": "pass",
    "confidence": "high",
    "verified_scope": ["every acceptance criterion read against the live code"],
    "blockers": [],
    "coverage_gaps": [],
    "pending_checks": [],
    "verdict_summary": "All criteria hold.",
}
VALID_FAIL_V3 = {
    **VALID_PASS_V3,
    "verdict": "fail",
    "blockers": [{"criterion": "AC-3", "finding": "The disabled state still takes focus."}],
    "verdict_summary": "One blocker.",
}
VALID_V1 = {"verdict": "pass", "confidence": "high", "verdict_summary": "Complete."}


def event(message: str, agent_type: str = "smith:exit-gate", agent_id: str = "agent-1") -> dict:
    return {
        "hook_event_name": "PreToolUse",
        "tool_name": "SubagentHandback",
        "tool_input": {"message": message},
        "agent_type": agent_type,
        "agent_id": agent_id,
    }


class HandbackValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.state = Path(self.directory.name)

    def decide(self, payload: dict, max_denials: int = 3):
        return validate_handback.decide(payload, self.state, max_denials)

    def test_valid_handbacks_pass_in_every_shape(self) -> None:
        shapes = [
            json.dumps(VALID_PASS_V3),
            "```json\n" + json.dumps(VALID_FAIL_V3) + "\n```",
            "Here is my verdict.\n\n" + json.dumps(VALID_PASS_V3) + "\n\nLet me know.",
        ]
        for message in shapes:
            with self.subTest(message=message[:40]):
                self.assertIsNone(self.decide(event(message)))

    def test_muse_gate_is_checked_against_verdict_3_like_the_others(self) -> None:
        self.assertIsNone(self.decide(event(json.dumps(VALID_PASS_V3), "muse:exit-gate")))
        denied = self.decide(event(json.dumps(VALID_V1), "muse:exit-gate"))
        reason = denied["hookSpecificOutput"]["permissionDecisionReason"]
        self.assertIn("verdict@3", reason)
        self.assertIn("verified_scope", reason)

    def test_escalation_is_a_blocker_not_a_verdict_value(self) -> None:
        escalate = {**VALID_PASS_V3, "verdict": "escalate"}
        denied = self.decide(event(json.dumps(escalate), "muse:exit-gate"))
        self.assertIn("expected one of", denied["hookSpecificOutput"]["permissionDecisionReason"])
        escalation_blocker = {
            **VALID_FAIL_V3,
            "blockers": [{"criterion": "escalation_required", "finding": "Retry cap reached; human review needed."}],
        }
        self.assertIsNone(self.decide(event(json.dumps(escalation_blocker), "muse:exit-gate", agent_id="esc")))

    def test_summary_over_300_characters_is_the_recorded_real_world_violation(self) -> None:
        too_long = {**VALID_PASS_V3, "verdict_summary": "x" * 301}
        denied = self.decide(event(json.dumps(too_long)))
        self.assertIn("at most 300 characters", denied["hookSpecificOutput"]["permissionDecisionReason"])
        self.assertIsNone(self.decide(event(json.dumps({**VALID_PASS_V3, "verdict_summary": "x" * 300}), agent_id="b")))

    def test_conditional_rules_are_enforced(self) -> None:
        fail_without_blockers = {**VALID_PASS_V3, "verdict": "fail"}
        pass_with_blockers = {**VALID_PASS_V3, "blockers": VALID_FAIL_V3["blockers"]}
        for report, expected in [(fail_without_blockers, "blockers"), (pass_with_blockers, "blockers")]:
            with self.subTest(expected=expected):
                denied = self.decide(event(json.dumps(report), agent_id=f"agent-{expected}-{len(report['blockers'])}"))
                self.assertEqual(denied["hookSpecificOutput"]["permissionDecision"], "deny")
                self.assertIn(expected, denied["hookSpecificOutput"]["permissionDecisionReason"])

    def test_type_lists_are_supported(self) -> None:
        schema = {"type": "object", "properties": {"value": {"type": ["string", "null"]}}}
        self.assertEqual(validate_handback.validate({"value": None}, schema), [])
        self.assertEqual(validate_handback.validate({"value": "text"}, schema), [])
        self.assertEqual(validate_handback.validate({"value": 3}, schema), ["$.value: expected string or null"])

    def test_a_retry_past_the_cap_must_escalate_instead_of_passing(self) -> None:
        late_pass = {**VALID_PASS_V3, "retry_count": 4}
        denied = self.decide(event(json.dumps(late_pass), agent_id="late"))
        self.assertIn("escalation_required", denied["hookSpecificOutput"]["permissionDecisionReason"])
        escalated = {**VALID_FAIL_V3, "retry_count": 4, "blockers": [{"criterion": "escalation_required", "finding": "Cap reached."}]}
        self.assertIsNone(self.decide(event(json.dumps(escalated), agent_id="late2")))
        self.assertIsNone(self.decide(event(json.dumps({**VALID_PASS_V3, "retry_count": 3}), agent_id="late3")))

    def test_blank_blocker_text_is_denied_but_terse_real_text_is_not(self) -> None:
        blank = {**VALID_FAIL_V3, "blockers": [{"criterion": "AC-3", "finding": "   ", "location": "AC-3"}]}
        denied = self.decide(event(json.dumps(blank), agent_id="blank"))
        self.assertIn("$.blockers[0].finding", denied["hookSpecificOutput"]["permissionDecisionReason"])
        blank_gap = {**VALID_FAIL_V3, "coverage_gaps": [{"kind": "x", "finding": "\n", "blocking": False}]}
        denied = self.decide(event(json.dumps(blank_gap), agent_id="blank2"))
        self.assertIn("$.coverage_gaps[0].finding", denied["hookSpecificOutput"]["permissionDecisionReason"])
        terse = {**VALID_FAIL_V3, "blockers": [{"criterion": "escalation_required", "finding": "Cap reached."}]}
        self.assertIsNone(self.decide(event(json.dumps(terse), agent_id="terse")))
        located = {**VALID_FAIL_V3, "blockers": [{"criterion": "AC-3", "finding": "Quote: 'handles errors'. Replace with the observable result.", "location": "AC-3"}]}
        self.assertIsNone(self.decide(event(json.dumps(located), agent_id="located")))

    def test_trace_records_each_inspected_event(self) -> None:
        trace_file = self.state / "trace.jsonl"
        os.environ["WISP_HANDBACK_TRACE"] = str(trace_file)
        self.addCleanup(os.environ.pop, "WISP_HANDBACK_TRACE", None)
        self.decide(event(json.dumps(VALID_PASS_V3)))
        self.decide(event("not json", agent_id="t2"))
        outcomes = [json.loads(line)["outcome"] for line in trace_file.read_text().splitlines()]
        self.assertEqual(outcomes, ["accepted", "denied"])

    def test_missing_json_is_denied(self) -> None:
        denied = self.decide(event("I reviewed it and it looks fine."))
        self.assertIn("no JSON object", denied["hookSpecificOutput"]["permissionDecisionReason"])

    def test_other_agents_and_tools_are_ignored(self) -> None:
        self.assertIsNone(self.decide(event("not json", agent_type="smith:implementer")))
        other_tool = event("not json")
        other_tool["tool_name"] = "Read"
        self.assertIsNone(self.decide(other_tool))

    def test_denials_stop_at_the_cap_per_agent(self) -> None:
        bad = event("not json", agent_id="agent-cap")
        results = [self.decide(bad, max_denials=3) for _ in range(5)]
        self.assertEqual([result is not None for result in results], [True, True, True, False, False])
        self.assertIsNotNone(self.decide(event("not json", agent_id="a-different-agent"), max_denials=3))

    def test_command_denies_through_stdout_with_exit_zero(self) -> None:
        environment = {**os.environ, "WISP_HANDBACK_STATE_DIR": str(self.state)}
        completed = subprocess.run(
            [sys.executable, str(TOOL)],
            input=json.dumps(event("not json", agent_id="agent-cli")),
            capture_output=True,
            text=True,
            env=environment,
            check=False,
        )
        self.assertEqual(completed.returncode, 0)
        output = json.loads(completed.stdout)["hookSpecificOutput"]
        self.assertEqual(output["hookEventName"], "PreToolUse")
        self.assertEqual(output["permissionDecision"], "deny")

    def test_command_fails_open_on_garbage_input(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(TOOL)], input="not a hook payload", capture_output=True, text=True, check=False
        )
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(completed.stdout, "")

    def test_every_route_names_an_existing_schema(self) -> None:
        for agent_type, schemas in validate_handback.ROUTES.items():
            with self.subTest(agent_type=agent_type):
                for schema in schemas:
                    self.assertTrue((REPOSITORY_ROOT / "shared" / "schemas" / f"{schema}.json").is_file())
                plugin, _, agent = agent_type.partition(":")
                self.assertTrue((REPOSITORY_ROOT / "plugins" / plugin / "agents" / f"{agent}.md").is_file())

    def test_every_exit_gate_agent_is_routed_and_its_plugin_registers_the_hook(self) -> None:
        for gate in sorted((REPOSITORY_ROOT / "plugins").glob("*/agents/exit-gate.md")):
            plugin = gate.parents[1].name
            with self.subTest(plugin=plugin):
                self.assertIn(f"{plugin}:exit-gate", validate_handback.ROUTES)
                registration = json.loads((gate.parents[1] / "hooks" / "hooks.json").read_text(encoding="utf-8"))
                entry = registration["hooks"]["PreToolUse"][0]
                self.assertEqual(entry["matcher"], "SubagentHandback")
                self.assertIn("shared/hooks/validate-handback.py", entry["hooks"][0]["command"])


if __name__ == "__main__":
    unittest.main()
