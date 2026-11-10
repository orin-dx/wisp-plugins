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


def human(text: str) -> dict:
    return {"type": "user", "message": {"content": text}}


def assistant_message(message_id: str, *blocks: dict) -> dict:
    return {"type": "assistant", "message": {"id": message_id, "content": list(blocks)}}


def error_result(identifier: str, content: str = "boom") -> dict:
    record = tool_result(identifier, content)
    record["message"]["content"][0]["is_error"] = True
    return record


def synthetic_session(path: Path, extra_failures: int) -> None:
    """One session: 2 prompts, a denial then a changed retry, then `extra_failures` more failed-and-changed pairs."""
    lines = [
        human("draft the spec"),
        assistant_message("m1", tool_use("a", "Bash", command="make test")),
        assistant_message("m1", tool_use("b", "Agent", subagent_type="muse:exit-gate")),  # same message id, counted once
        error_result("a"),
        tool_result("b", "started", agent_id="g1"),
        notification("g1", 1000, 1000),
        assistant_message("m2", tool_use("c", "Bash", command="make test V=1")),
        tool_result("c", "ok"),
        human("<system-reminder>ignored</system-reminder>"),
        {"type": "user", "isMeta": True, "message": {"content": "meta"}},
        human("looks good"),
    ]
    for index in range(extra_failures):
        lines += [
            assistant_message(f"x{index}", tool_use(f"f{index}", "Read", file_path=f"a{index}")),
            tool_result(f"f{index}", "Permission denied by user: The user doesn't want to proceed with this tool use."),
            assistant_message(f"y{index}", tool_use(f"r{index}", "Read", file_path=f"b{index}")),
            tool_result(f"r{index}", "ok"),
        ]
    path.write_text("\n".join(json.dumps(line) for line in lines), encoding="utf-8")


class TurnsTests(unittest.TestCase):
    def test_counts_prompts_turns_calls_spawns_and_narrow_retries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "abcdef1234.jsonl"
            synthetic_session(path, extra_failures=0)
            row = metrics.session_turns(path)
        self.assertEqual(row, {"prompts": 2, "turns": 2, "tool_calls": 3, "subagents": 1, "retries": 1, "subagent_tokens": 1000})

    def test_same_input_rerun_and_other_tool_are_not_retries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "s.jsonl"
            lines = [
                assistant_message("m1", tool_use("a", "Bash", command="ls")),
                error_result("a"),
                assistant_message("m2", tool_use("b", "Bash", command="ls")),  # same input
                error_result("b"),
                assistant_message("m3", tool_use("c", "Read", file_path="x")),  # other tool
                error_result("c"),
                human("try again"),
                assistant_message("m4", tool_use("d", "Read", file_path="y")),  # after a human prompt
            ]
            path.write_text("\n".join(json.dumps(line) for line in lines), encoding="utf-8")
            self.assertEqual(metrics.session_turns(path)["retries"], 0)


class DryRunTests(unittest.TestCase):
    """The runbook's commands on synthetic sessions: turns -> trials file -> paired compare."""

    def test_runbook_pipeline_produces_expected_tables(self) -> None:
        import contextlib
        import io

        paired = importlib.util.spec_from_file_location("paired_analysis", REPOSITORY_ROOT / "tools" / "paired-analysis.py")
        assert paired is not None and paired.loader is not None
        analysis = importlib.util.module_from_spec(paired)
        paired.loader.exec_module(analysis)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            lines = []
            for task, (control_failures, treatment_failures) in {"t1": (4, 1), "t2": (3, 0), "t3": (5, 1), "t4": (2, 0)}.items():
                for arm, failures, score in (("control", control_failures, 0.5), ("treatment", treatment_failures, 0.8)):
                    session = root / f"{task}-{arm}.jsonl"
                    synthetic_session(session, failures)
                    out = io.StringIO()
                    with contextlib.redirect_stdout(out):
                        self.assertEqual(metrics.main(["turns", "--file", str(session), "--trial", f"task={task},arm={arm},run=1,score={score}"]), 0)
                    lines.append(out.getvalue().strip())
            trials = root / "trials.jsonl"
            trials.write_text("\n".join(lines), encoding="utf-8")
            first = json.loads(lines[0])
            self.assertEqual((first["task"], first["arm"], first["retries"], first["prompts"]), ("t1", "control", 5, 2))
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                analysis.main(["compare", str(trials), "--baseline", "control", "--metrics", "score,turns,retries"])
            table = out.getvalue()
            labels = root / "labels.json"
            labels.write_text(json.dumps([{"a": "pass", "b": "pass"}, {"a": "fail", "b": "fail"}, {"a": "pass", "b": "fail"}, {"a": "fail", "b": "fail"}]), encoding="utf-8")
            agreement = io.StringIO()
            with contextlib.redirect_stdout(agreement):
                analysis.main(["agreement", str(labels)])
        self.assertIn("4 tasks, 4 paired, 0 excluded", table)
        self.assertIn("treatment versus control", table)
        self.assertIn("turns: median delta -6 ", table)
        self.assertIn("retries: median delta -3 ", table)
        self.assertIn("better 4, worse 0, tied 0", table)
        self.assertIn("4 items, raw agreement 75.0%, Cohen's kappa 0.50", agreement.getvalue())


if __name__ == "__main__":
    unittest.main()
