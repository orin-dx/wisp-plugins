#!/usr/bin/env python3
"""Claude Code Stop hook: ask once for a "Not verified" statement when work is left uncommitted.

Registered by plugins/wisp/hooks/hooks.json:

  {"hooks": {"Stop": [{"hooks": [
    {"type": "command", "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/shared/hooks/stop-check.py\""}]}]}}

Why: agents report success without saying what they did not check. A prompt asking for the list is
not enforced; a hook is. The owner reads the diff, the evidence and the `Not verified:` list, so a
turn that leaves changes in the tree must end with that list.

Behavior
  - Reads the Stop hook JSON from stdin (`cwd`, `stop_hook_active`, `last_assistant_message`,
    `transcript_path`).
  - Lets the stop through when `stop_hook_active` is set (the agent is already continuing because
    of a stop hook), when `cwd` is not a work tree or the tree is clean, or when the final
    assistant message contains "not verified" (any case).
  - Otherwise blocks once with {"decision": "block", "reason": ...}. The agent adds the line and
    stops; the next Stop carries `stop_hook_active` and passes.
  - The final message comes from `last_assistant_message`, or, when that is absent, from the last
    assistant text in the transcript file.
  - WISP_STOP_CHECK=off disables it.
  - Fails open: any internal error exits 1 with nothing on stdout, which does not block.
  - Standard library only.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from typing import Any

MARKER = re.compile(r"not\s+verified", re.IGNORECASE)
TIMEOUT_SECONDS = 5
REASON = (
    "There are uncommitted changes and your final message has no \"Not verified:\" line. "
    "Before stopping, add one listing what you did not check (checks not run, platforms or inputs "
    "not exercised, claims resting on another agent's summary), or \"Not verified: nothing beyond "
    "the evidence above\"."
)


def tree_status(cwd: str) -> str | None:
    """Porcelain status of the work tree at `cwd`, or None when it is not a work tree."""
    completed = subprocess.run(
        ["git", "-C", cwd, "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        capture_output=True,
        timeout=TIMEOUT_SECONDS,
        check=False,
    )
    if completed.returncode != 0:
        return None
    return completed.stdout.decode("utf-8", "replace")


def final_message(event: dict[str, Any]) -> str:
    message = event.get("last_assistant_message")
    if isinstance(message, str):
        return message
    transcript = event.get("transcript_path")
    if not isinstance(transcript, str) or not os.path.isfile(transcript):
        return ""
    last = ""
    with open(transcript, encoding="utf-8") as handle:
        for line in handle:
            try:
                record = json.loads(line)
            except ValueError:
                continue
            if not isinstance(record, dict) or record.get("type") != "assistant":
                continue
            content = (record.get("message") or {}).get("content")
            if isinstance(content, str):
                text = content
            elif isinstance(content, list):
                text = "\n".join(part.get("text", "") for part in content if isinstance(part, dict) and part.get("type") == "text")
            else:
                text = ""
            if text.strip():
                last = text
    return last


def decide(event: dict[str, Any]) -> dict[str, Any] | None:
    """Return a block decision, or None to let the stop through."""
    if os.environ.get("WISP_STOP_CHECK", "").lower() == "off" or event.get("stop_hook_active"):
        return None
    if not tree_status(str(event.get("cwd") or os.getcwd())):
        return None
    if MARKER.search(final_message(event)):
        return None
    return {"decision": "block", "reason": REASON}


def main() -> int:
    try:
        event = json.load(sys.stdin)
        if not isinstance(event, dict):
            raise ValueError("hook input is not a JSON object")
        decision = decide(event)
    except Exception as error:  # fail open: only exit code 2 or a block decision stops the agent
        print(f"stop-check: internal error, not blocking: {error}", file=sys.stderr)
        return 1
    if decision is not None:
        print(json.dumps(decision))
    return 0


if __name__ == "__main__":
    sys.exit(main())
