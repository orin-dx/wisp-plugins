#!/usr/bin/env python3
"""Measure plugin and agent use from Claude Code session transcripts and persisted gate verdicts.

Subcommands (all read-only, standard library only):

  agents   Subagent calls, reported tokens and minutes per agent type per session, with the share
           spent by plugin agents (types containing ":") against everything else, and flags for
           tasks whose reported tokens pass --cliff (default 200000). Tokens are what each subagent
           reported, not a bill; the flag approximates the long-context pricing tier and cannot see
           per-request context size.
  skills   Skill and slash-command invocations against agent invocations per session. A plugin
           whose skills are never invoked never runs the agents that only its skills start.
  gates    Rounds per spec, final verdict, blockers per round, retry counts above 3, summaries over
           300 characters and escalations, from verdict files named <spec>-verdict[-<n>].json.
  outputs  Share of tool-result characters by tool, and the ceiling a compressor that only sees one
           tool (default Bash) could reach: share of that tool times the assumed reduction.

Examples:
  python3 tools/transcript-metrics.py agents --match 'orin-dx$|Projects-pages$'
  python3 tools/transcript-metrics.py gates ~/projects/pages/docs/specs
  python3 tools/transcript-metrics.py outputs --match 'Projects-pages$' --tool Bash --reduction 0.7
"""

from __future__ import annotations

import argparse
import collections
import glob
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Iterator

NOTIFICATION = re.compile(
    r"<task-id>([^<]+)</task-id>.*?<subagent_tokens>(\d+)</subagent_tokens>"
    r"<tool_uses>(\d+)</tool_uses><duration_ms>(\d+)</duration_ms>",
    re.S,
)
COMMAND = re.compile(r"<command-name>/?([^<]+)</command-name>")
VERDICT_NAME = re.compile(r"^(?P<spec>.+?)-verdict(?:-(?P<round>\d+))?\.json$")


def session_files(projects_dir: Path, match: str) -> list[Path]:
    pattern = re.compile(match)
    found: list[Path] = []
    for directory in sorted(projects_dir.iterdir()) if projects_dir.is_dir() else []:
        if directory.is_dir() and pattern.search(directory.name):
            found.extend(sorted(directory.glob("*.jsonl")))
    return found


def records(path: Path) -> Iterator[dict[str, Any]]:
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            record = json.loads(line)
        except ValueError:
            continue
        if isinstance(record, dict):
            yield record


def content_blocks(record: dict[str, Any]) -> list[dict[str, Any]]:
    message = record.get("message")
    if isinstance(message, dict) and isinstance(message.get("content"), list):
        return [block for block in message["content"] if isinstance(block, dict)]
    return []


def agent_tasks(path: Path) -> dict[str, tuple[str, int, int, int]]:
    """Map task id -> (agent type, reported tokens, tool uses, duration ms), deduplicated."""
    started: dict[str, str] = {}
    by_agent: dict[str, str] = {}
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    for line in lines:
        try:
            record = json.loads(line)
        except ValueError:
            continue
        for block in content_blocks(record) if isinstance(record, dict) else []:
            if block.get("type") == "tool_use" and block.get("name") in ("Agent", "Task"):
                started[block["id"]] = (block.get("input") or {}).get("subagent_type") or "none"
            if block.get("type") == "tool_result" and block.get("tool_use_id") in started:
                result = record.get("toolUseResult")
                if isinstance(result, dict) and result.get("agentId"):
                    by_agent[result["agentId"]] = started[block["tool_use_id"]]
    tasks: dict[str, tuple[str, int, int, int]] = {}
    for line in lines:
        if "<subagent_tokens>" in line:
            for task, tokens, tools, duration in NOTIFICATION.findall(line.replace("\\n", " ")):
                if task in by_agent:
                    tasks[task] = (by_agent[task], int(tokens), int(tools), int(duration))
    return tasks


def command_agents(files: list[Path], cliff: int) -> dict[str, Any]:
    per_type: dict[tuple[str, str], list[int]] = collections.defaultdict(lambda: [0, 0, 0])
    plugin_tokens = other_tokens = 0
    flagged: list[tuple[str, str, int]] = []
    for path in files:
        session = path.stem[:8]
        for task, (kind, tokens, _tools, duration) in agent_tasks(path).items():
            entry = per_type[(session, kind)]
            entry[0] += 1
            entry[1] += tokens
            entry[2] += duration
            if ":" in kind:
                plugin_tokens += tokens
            else:
                other_tokens += tokens
            if tokens > cliff:
                flagged.append((session, kind, tokens))
    return {
        "types": {key: {"calls": v[0], "tokens": v[1], "minutes": round(v[2] / 60000, 1)} for key, v in per_type.items()},
        "plugin_tokens": plugin_tokens,
        "other_tokens": other_tokens,
        "over_cliff": flagged,
    }


def command_skills(files: list[Path]) -> dict[str, Any]:
    result: dict[str, dict[str, Any]] = {}
    for path in files:
        skills: collections.Counter[str] = collections.Counter()
        agents: collections.Counter[str] = collections.Counter()
        commands: collections.Counter[str] = collections.Counter()
        for record in records(path):
            for block in content_blocks(record):
                if block.get("type") == "tool_use":
                    name = block.get("name")
                    if name == "Skill":
                        skills[str((block.get("input") or {}).get("skill"))] += 1
                    elif name in ("Agent", "Task"):
                        agents[str((block.get("input") or {}).get("subagent_type") or "none")] += 1
                elif block.get("type") == "text" and isinstance(block.get("text"), str):
                    commands.update(match.strip() for match in COMMAND.findall(block["text"]))
        result[path.stem[:8]] = {"skills": dict(skills), "commands": dict(commands), "agents": dict(agents)}
    return result


def command_gates(directory: Path) -> dict[str, Any]:
    specs: dict[str, list[tuple[int, dict[str, Any]]]] = collections.defaultdict(list)
    for path in sorted(directory.glob("*verdict*.json")):
        match = VERDICT_NAME.match(path.name)
        if not match:
            continue
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if isinstance(report, dict):
            specs[match.group("spec")].append((int(match.group("round") or 1), report))
    summary: dict[str, Any] = {}
    for spec, rounds in sorted(specs.items()):
        rounds.sort(key=lambda item: item[0])
        verdicts = [str(report.get("verdict")) for _, report in rounds]
        blockers = [len(report.get("blockers") or []) for _, report in rounds]
        retry_counts = [report.get("retry_count") for _, report in rounds if isinstance(report.get("retry_count"), int)]
        escalations = sum(
            1
            for _, report in rounds
            if report.get("verdict") == "escalate"
            or any(isinstance(b, dict) and b.get("criterion") == "escalation_required" for b in report.get("blockers") or [])
        )
        summary[spec] = {
            "rounds": len(rounds),
            "verdicts": verdicts,
            "final": verdicts[-1],
            "blockers_per_round": blockers,
            "max_retry_count": max(retry_counts) if retry_counts else None,
            "over_retry_cap": sum(1 for count in retry_counts if count > 3),
            "long_summaries": sum(1 for _, r in rounds if len(str(r.get("verdict_summary", ""))) > 300),
            "escalations": escalations,
        }
    return summary


def result_characters(block: dict[str, Any]) -> int:
    content = block.get("content")
    if isinstance(content, str):
        return len(content)
    if isinstance(content, list):
        return sum(len(part.get("text", "")) for part in content if isinstance(part, dict))
    return 0


def command_outputs(files: list[Path], tool: str, reduction: float) -> dict[str, Any]:
    by_tool: collections.Counter[str] = collections.Counter()
    for path in files:
        names: dict[str, str] = {}
        counted: set[str] = set()
        for record in records(path):
            for block in content_blocks(record):
                if block.get("type") == "tool_use":
                    names[block["id"]] = str(block.get("name"))
                elif block.get("type") == "tool_result" and block.get("tool_use_id") in names and block["tool_use_id"] not in counted:
                    counted.add(block["tool_use_id"])
                    by_tool[names[block["tool_use_id"]]] += result_characters(block)
    total = sum(by_tool.values())
    share = by_tool[tool] / total if total else 0.0
    return {
        "total_characters": total,
        "by_tool": dict(by_tool.most_common()),
        "tool": tool,
        "tool_share": round(share, 4),
        "ceiling_of_tool_output": round(share * reduction, 4),
        "reduction": reduction,
    }


def print_agents(report: dict[str, Any]) -> None:
    print("session agent_type calls total_tokens avg_tokens minutes")
    for (session, kind), v in sorted(report["types"].items(), key=lambda item: -item[1]["tokens"]):
        print(session, kind, v["calls"], v["tokens"], v["tokens"] // v["calls"], v["minutes"])
    total = report["plugin_tokens"] + report["other_tokens"]
    if total:
        print(f"plugin agents {report['plugin_tokens']} tokens ({report['plugin_tokens'] / total:.0%}); other subagents {report['other_tokens']}")
    for session, kind, tokens in report["over_cliff"]:
        print(f"over cliff: {session} {kind} {tokens} tokens")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("agents", "skills", "outputs"):
        p = sub.add_parser(name)
        p.add_argument("--projects-dir", default="~/.claude/projects")
        p.add_argument("--match", default=".")
        if name == "agents":
            p.add_argument("--cliff", type=int, default=200_000)
        if name == "outputs":
            p.add_argument("--tool", default="Bash")
            p.add_argument("--reduction", type=float, default=0.7)
    gates = sub.add_parser("gates")
    gates.add_argument("directory")
    args = parser.parse_args(argv)

    if args.command == "gates":
        report = command_gates(Path(args.directory).expanduser())
        print("spec rounds final blockers_per_round max_retry over_cap long_summaries escalations")
        for spec, v in report.items():
            print(spec, v["rounds"], v["final"], v["blockers_per_round"], v["max_retry_count"], v["over_retry_cap"], v["long_summaries"], v["escalations"])
        return 0
    files = session_files(Path(os.path.expanduser(args.projects_dir)), args.match)
    if args.command == "agents":
        print_agents(command_agents(files, args.cliff))
    elif args.command == "skills":
        for session, v in command_skills(files).items():
            print(session, "skills", v["skills"], "commands", v["commands"], "agents", v["agents"])
    else:
        print(json.dumps(command_outputs(files, args.tool, args.reduction), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
