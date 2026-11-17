"""Aggregate subagent token use and duration per agent type from Claude Code transcripts.

Usage: python3 -I gate-cost.py <projects-dir> <dir-name-regex>
Example: python3 -I gate-cost.py ~/.claude/projects 'orin-dx$|Projects-pages$'

Background subagent results arrive as <task-notification> blocks carrying
<subagent_tokens>, <tool_uses> and <duration_ms>. The same notification can be
repeated several times in a transcript, so results are deduplicated by task id.
The agent type comes from the Agent tool_use that started the task.
Only top-level session files are read (not subagent transcripts).
Tokens are the usage each subagent reported, not a bill.
"""

import collections
import glob
import json
import os
import re
import sys

root, pattern = os.path.expanduser(sys.argv[1]), re.compile(sys.argv[2])
NOTIFICATION = re.compile(
    r"<task-id>([^<]+)</task-id>.*?<subagent_tokens>(\d+)</subagent_tokens>"
    r"<tool_uses>(\d+)</tool_uses><duration_ms>(\d+)</duration_ms>",
    re.S,
)
per_session = collections.defaultdict(dict)
for directory in sorted(os.listdir(root)):
    if not pattern.search(directory):
        continue
    for path in glob.glob(f"{root}/{directory}/*.jsonl"):
        session = os.path.basename(path)[:8]
        started, by_agent = {}, {}
        lines = open(path, errors="ignore").read().splitlines()
        for line in lines:
            try:
                record = json.loads(line)
            except ValueError:
                continue
            message = record.get("message")
            if not (isinstance(message, dict) and isinstance(message.get("content"), list)):
                continue
            for block in message["content"]:
                if block.get("type") == "tool_use" and block.get("name") in ("Agent", "Task"):
                    started[block["id"]] = block.get("input", {}).get("subagent_type") or "none"
                if block.get("type") == "tool_result" and block.get("tool_use_id") in started:
                    result = record.get("toolUseResult")
                    if isinstance(result, dict) and result.get("agentId"):
                        by_agent[result["agentId"]] = started[block["tool_use_id"]]
        for line in lines:
            if "<subagent_tokens>" in line:
                for task, tokens, tools, duration in NOTIFICATION.findall(line.replace("\\n", " ")):
                    if task in by_agent:
                        per_session[session][task] = (by_agent[task], int(tokens), int(tools), int(duration))
totals = collections.defaultdict(lambda: [0, 0, 0, 0])
for session, tasks in per_session.items():
    for agent_type, tokens, tools, duration in tasks.values():
        entry = totals[(session, agent_type)]
        entry[0] += 1
        entry[1] += tokens
        entry[2] += tools
        entry[3] += duration
print("session agent_type calls total_tokens avg_tokens avg_minutes")
for (session, agent_type), entry in sorted(totals.items(), key=lambda item: -item[1][1]):
    print(session, agent_type, entry[0], entry[1], entry[1] // entry[0], round(entry[3] / 60000 / entry[0], 1))
for session in per_session:
    plugin = [e for (s, t), e in totals.items() if s == session and ":" in t]
    other = [e for (s, t), e in totals.items() if s == session and ":" not in t]
    print(session, "plugin-agent tokens", sum(e[1] for e in plugin), "calls", sum(e[0] for e in plugin))
    print(session, "other subagent tokens", sum(e[1] for e in other), "calls", sum(e[0] for e in other))
