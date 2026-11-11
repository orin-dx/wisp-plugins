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

  context  Where characters entering the conversation come from, per category: user text,
           assistant text, tool calls (agent delegation prompts counted apart), tool results by tool
           (agent results are the handoffs), plus the single largest results. Characters, not
           tokens: divide by about 4 for a rough token count. Use it to decide what to keep out of
           context before cutting anything.

  turns    Per session: human prompts, assistant turns, tool calls, subagent spawns, retries and
           subagent tokens, for "turns to acceptance" and "rework" in a paired evaluation. Select
           sessions with --file PATH (repeatable) or --projects-dir/--match; --json prints rows;
           --trial task=t1,arm=control,run=1[,score=0.8] prints one paired-analysis trial line per
           session, adding the measured turns, prompts, tool_calls, retries, subagents and tokens.
           Definitions, all approximate:
             human prompt   a user record that is not a tool result, task notification, system
                            reminder, local-command echo, meta record or sidechain record, and has
                            non-empty text. Slash commands count; interrupts do not.
             assistant turn distinct assistant message ids (one id can span several records),
                            counting records without an id once each. Sidechain records are skipped.
             tool call      tool_use blocks. Subagent spawns are the Agent or Task calls among them.
             retry          a tool call that comes next after a failed result (is_error true, or a
                            permission denial or user rejection message), uses the same tool name and
                            has different input. Same-input reruns, a different tool, or a human
                            prompt in between do not count. One failure yields at most one retry.
           Limits: a retry with a changed command can be legitimate progress; a failed call retried
           through another tool is missed; subagent internals live in separate files and are not
           counted; the tokens are what subagents reported. Use it to compare arms, not to grade one.

Examples:
  python3 tools/transcript-metrics.py turns --file session-a.jsonl --trial task=t1,arm=control,run=1
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


def command_context(files: list[Path], top: int) -> dict[str, Any]:
    """Characters by origin across sessions. A tool result is counted once, under the tool that produced it."""
    categories: collections.Counter[str] = collections.Counter()
    results: collections.Counter[str] = collections.Counter()
    calls: collections.Counter[str] = collections.Counter()
    largest: list[tuple[int, str, str]] = []
    for path in files:
        names: dict[str, str] = {}
        counted: set[str] = set()
        for record in records(path):
            kind = record.get("type")
            for block in content_blocks(record):
                block_type = block.get("type")
                if block_type == "text":
                    categories["assistant text" if kind == "assistant" else "user text"] += len(block.get("text", ""))
                elif block_type == "tool_use":
                    names[block["id"]] = str(block.get("name"))
                    size = len(json.dumps(block.get("input", {})))
                    calls[str(block.get("name"))] += size
                    categories["delegation prompts" if block.get("name") in ("Agent", "Task") else "tool calls"] += size
                elif block_type == "tool_result" and block.get("tool_use_id") in names and block["tool_use_id"] not in counted:
                    counted.add(block["tool_use_id"])
                    size = result_characters(block)
                    name = names[block["tool_use_id"]]
                    results[name] += size
                    largest.append((size, name, path.parent.name))
            message = record.get("message")
            if isinstance(message, dict) and isinstance(message.get("content"), str):
                categories["assistant text" if kind == "assistant" else "user text"] += len(message["content"])
    categories["tool results"] = sum(results.values())
    total = sum(categories.values())
    largest.sort(reverse=True)
    return {
        "total_characters": total,
        "by_category": {name: {"characters": count, "share": round(count / total, 4) if total else 0.0} for name, count in categories.most_common()},
        "tool_results_by_tool": {name: {"characters": count, "share": round(count / categories["tool results"], 4) if categories["tool results"] else 0.0} for name, count in results.most_common()},
        "tool_call_inputs_by_tool": dict(calls.most_common(8)),
        "largest_results": [{"characters": size, "tool": name, "session": session} for size, name, session in largest[:top]],
    }


NON_PROMPT_PREFIXES = ("<task-notification", "<system-reminder", "<local-command", "[Request interrupted")
DENIAL_MARKERS = ("doesn't want to proceed", "has been denied", "was denied", "permission denied by", "user rejected")


def human_text(record: dict[str, Any]) -> str:
    """Return the prompt text of a human user record, or an empty string for anything else."""
    if record.get("type") != "user" or record.get("isMeta") or record.get("isSidechain"):
        return ""
    message = record.get("message")
    content = message.get("content") if isinstance(message, dict) else None
    if isinstance(content, str):
        text = content
    elif isinstance(content, list) and not any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
        text = "".join(str(b.get("text", "")) for b in content if isinstance(b, dict) and b.get("type") == "text")
    else:
        return ""
    text = text.strip()
    return "" if not text or text.startswith(NON_PROMPT_PREFIXES) else text


def failed_result(block: dict[str, Any]) -> bool:
    if block.get("is_error"):
        return True
    content = block.get("content")
    text = content if isinstance(content, str) else " ".join(str(p.get("text", "")) for p in content if isinstance(p, dict)) if isinstance(content, list) else ""
    return any(marker in text[:400] for marker in DENIAL_MARKERS)


def session_turns(path: Path) -> dict[str, int]:
    prompts = tool_calls = spawns = retries = 0
    message_ids: set[str] = set()
    anonymous = 0
    calls: dict[str, tuple[str, Any]] = {}
    failed: tuple[str, Any] | None = None
    for record in records(path):
        if human_text(record):
            prompts += 1
            failed = None
            continue
        if record.get("isSidechain"):
            continue
        message = record.get("message")
        if record.get("type") == "assistant" and isinstance(message, dict) and message.get("content"):
            if message.get("id"):
                message_ids.add(str(message["id"]))
            else:
                anonymous += 1
        for block in content_blocks(record):
            if block.get("type") == "tool_use":
                tool_calls += 1
                spawns += block.get("name") in ("Agent", "Task")
                if failed and failed[0] == block.get("name") and failed[1] != block.get("input"):
                    retries += 1
                failed = None
                calls[str(block.get("id"))] = (str(block.get("name")), block.get("input"))
            elif block.get("type") == "tool_result" and str(block.get("tool_use_id")) in calls and failed_result(block):
                failed = calls[str(block["tool_use_id"])]
    tokens = sum(task[1] for task in agent_tasks(path).values())
    return {"prompts": prompts, "turns": len(message_ids) + anonymous, "tool_calls": tool_calls, "subagents": spawns, "retries": retries, "subagent_tokens": tokens}


def command_turns(files: list[Path]) -> dict[str, dict[str, int]]:
    return {path.stem[:8]: session_turns(path) for path in files}


def parse_trial(spec: str) -> dict[str, Any]:
    trial: dict[str, Any] = {}
    for pair in filter(None, spec.split(",")):
        key, _, value = pair.partition("=")
        try:
            trial[key] = int(value)
        except ValueError:
            try:
                trial[key] = float(value)
            except ValueError:
                trial[key] = value
    return trial


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
    for name in ("agents", "skills", "outputs", "context"):
        p = sub.add_parser(name)
        p.add_argument("--projects-dir", default="~/.claude/projects")
        p.add_argument("--match", default=".")
        if name == "agents":
            p.add_argument("--cliff", type=int, default=200_000)
        if name == "context":
            p.add_argument("--top", type=int, default=10)
        if name == "outputs":
            p.add_argument("--tool", default="Bash")
            p.add_argument("--reduction", type=float, default=0.7)
    turns = sub.add_parser("turns")
    turns.add_argument("--projects-dir", default="~/.claude/projects")
    turns.add_argument("--match", default=".")
    turns.add_argument("--file", action="append", default=[])
    turns.add_argument("--json", action="store_true")
    turns.add_argument("--trial", help="key=value pairs for a paired-analysis trial line, for example task=t1,arm=control,run=1,score=0.8")
    gates = sub.add_parser("gates")
    gates.add_argument("directory")
    args = parser.parse_args(argv)

    if args.command == "turns":
        files = [Path(f).expanduser() for f in args.file] or session_files(Path(os.path.expanduser(args.projects_dir)), args.match)
        report = command_turns(files)
        if args.trial:
            for row in report.values():
                print(json.dumps({**parse_trial(args.trial), **{k: v for k, v in row.items()}}))
        elif args.json:
            print(json.dumps(report, indent=2))
        else:
            print("session prompts turns tool_calls subagents retries subagent_tokens")
            for session, row in report.items():
                print(session, row["prompts"], row["turns"], row["tool_calls"], row["subagents"], row["retries"], row["subagent_tokens"])
        return 0

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
    elif args.command == "context":
        print(json.dumps(command_context(files, args.top), indent=2))
    else:
        print(json.dumps(command_outputs(files, args.tool, args.reduction), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
