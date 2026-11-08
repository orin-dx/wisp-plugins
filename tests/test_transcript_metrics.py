"""Cover tools/transcript-metrics.py on synthetic transcripts and verdict files."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPOSITORY_ROOT / "tools" / "transcript-metrics.py"

specification = importlib.util.spec_from_file_location("transcript_metrics", TOOL)
assert specification is not None and specification.loader is not None
metrics = importlib.util.module_from_spec(specification)
specification.loader.exec_module(metrics)


def assistant(*blocks: dict) -> dict:
    return {"type": "assistant", "message": {"content": list(blocks)}}


def tool_use(identifier: str, name: str, **input_fields) -> dict:
    return {"type": "tool_use", "id": identifier, "name": name, "input": input_fields}


def tool_result(identifier: str, content, agent_id: str | None = None) -> dict:
    record = {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": identifier, "content": content}]}}
    if agent_id:
        record["toolUseResult"] = {"agentId": agent_id}
    return record


def notification(task: str, tokens: int, duration_ms: int) -> dict:
    text = (
        f"<task-notification><task-id>{task}</task-id><status>completed</status>"
        f"<usage><subagent_tokens>{tokens}</subagent_tokens><tool_uses>3</tool_uses>"
        f"<duration_ms>{duration_ms}</duration_ms></usage></task-notification>"
    )
    return {"type": "user", "message": {"content": text}}


class TranscriptMetricsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        project = self.root / "projects" / "-Users-x-Projects-site"
        project.mkdir(parents=True)
        lines = [
            assistant(tool_use("t1", "Agent", subagent_type="muse:exit-gate"), tool_use("t2", "Agent", subagent_type="fork")),
            tool_result("t1", "started", agent_id="a1"),
            tool_result("t2", "started", agent_id="a2"),
            notification("a1", 250_000, 120_000),
            notification("a1", 250_000, 120_000),  # repeated in the transcript, counted once
            notification("a2", 100_000, 60_000),
            assistant(tool_use("s1", "Skill", skill="muse:component"), tool_use("b1", "Bash", command="ls"), tool_use("r1", "Read", file_path="x")),
            tool_result("s1", "loaded"),
            tool_result("b1", "x" * 900),
            tool_result("r1", [{"type": "text", "text": "y" * 100}]),
            {"type": "user", "message": {"content": [{"type": "text", "text": "<command-name>/resume</command-name>"}]}},
        ]
        (project / "abcdef1234.jsonl").write_text("\n".join(json.dumps(line) for line in lines), encoding="utf-8")
        self.projects = self.root / "projects"
        self.files = metrics.session_files(self.projects, "site$")

    def test_agents_dedupes_notifications_and_splits_plugin_from_other(self) -> None:
        report = metrics.command_agents(self.files, cliff=200_000)
        gate = report["types"][("abcdef12", "muse:exit-gate")]
        self.assertEqual((gate["calls"], gate["tokens"], gate["minutes"]), (1, 250_000, 2.0))
        self.assertEqual((report["plugin_tokens"], report["other_tokens"]), (250_000, 100_000))
        self.assertEqual(report["over_cliff"], [("abcdef12", "muse:exit-gate", 250_000)])

    def test_skills_counts_skill_agent_and_command_invocations(self) -> None:
        report = metrics.command_skills(self.files)["abcdef12"]
        self.assertEqual(report["skills"], {"muse:component": 1})
        self.assertEqual(report["agents"], {"muse:exit-gate": 1, "fork": 1})
        self.assertEqual(report["commands"], {"resume": 1})

    def test_outputs_share_and_ceiling(self) -> None:
        report = metrics.command_outputs(self.files, "Bash", 0.5)
        self.assertEqual(report["by_tool"]["Bash"], 900)
        self.assertEqual(report["by_tool"]["Read"], 100)
        self.assertAlmostEqual(report["tool_share"], 900 / (900 + 100 + len("started") * 2 + len("loaded")), places=3)
        self.assertAlmostEqual(report["ceiling_of_tool_output"], report["tool_share"] * 0.5, places=3)

    def test_gates_report_rounds_retry_cap_long_summaries_and_escalation(self) -> None:
        directory = self.root / "specs"
        directory.mkdir()

        def verdict(name: str, **fields) -> None:
            (directory / name).write_text(json.dumps({"verdict": "fail", "blockers": [], **fields}), encoding="utf-8")

        verdict("SPEC-1-verdict.json", blockers=[{"criterion": "a", "finding": "b"}], retry_count=1)
        verdict("SPEC-1-verdict-2.json", retry_count=4, verdict_summary="x" * 301)
        verdict("SPEC-1-verdict-10.json", verdict="pass", retry_count=5)
        verdict("SPEC-2-verdict.json", blockers=[{"criterion": "escalation_required", "finding": "cap"}])
        report = metrics.command_gates(directory)
        first = report["SPEC-1"]
        self.assertEqual(first["rounds"], 3)
        self.assertEqual(first["verdicts"], ["fail", "fail", "pass"])  # rounds sort numerically, so 10 follows 2
        self.assertEqual(first["final"], "pass")
        self.assertEqual(first["blockers_per_round"], [1, 0, 0])
        self.assertEqual((first["max_retry_count"], first["over_retry_cap"], first["long_summaries"]), (5, 2, 1))
        self.assertEqual(report["SPEC-2"]["escalations"], 1)

    def test_command_line_runs_and_rejects_nothing_silently(self) -> None:
        self.assertEqual(metrics.main(["agents", "--projects-dir", str(self.projects), "--match", "site$"]), 0)
        self.assertEqual(metrics.main(["gates", str(self.root / "no-such-directory")]), 0)


class ContextCompositionTests(unittest.TestCase):
    def test_characters_are_attributed_to_their_origin(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "session.jsonl"
            records = [
                {"type": "user", "message": {"content": "hello there"}},
                assistant({"type": "text", "text": "ok"}, tool_use("t1", "Bash", command="ls"), tool_use("t2", "Agent", prompt="do the thing")),
                tool_result("t1", "x" * 900),
                tool_result("t2", [{"type": "text", "text": "y" * 100}]),
            ]
            path.write_text("\n".join(json.dumps(record) for record in records), encoding="utf-8")
            report = metrics.command_context([path], top=1)
            session = path.parent.name
        categories = report["by_category"]
        self.assertEqual(categories["user text"]["characters"], 11)
        self.assertEqual(categories["assistant text"]["characters"], 2)
        self.assertGreater(categories["delegation prompts"]["characters"], 0)
        self.assertEqual(categories["tool results"]["characters"], 1000)
        self.assertEqual(report["tool_results_by_tool"]["Bash"]["share"], 0.9)
        self.assertEqual(report["largest_results"], [{"characters": 900, "tool": "Bash", "session": session}])


if __name__ == "__main__":
    unittest.main()
