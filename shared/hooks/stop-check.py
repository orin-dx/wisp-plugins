#!/usr/bin/env python3
"""Claude Code Stop hook: ask once for a "Not verified" statement when work is left uncommitted.

Registered by plugins/wisp/hooks/hooks.json:

  {"hooks": {"Stop": [{"hooks": [
    {"type": "command", "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/shared/hooks/stop-check.py\""}]}]}}

Why: agents report success without saying what they did not check. A prompt asking for the list is
not enforced; a hook is. The owner reads the diff, the evidence and the `Not verified:` list, so a
turn that leaves changes in the tree must end with that list.

Behavior
  - Reads the Stop hook JSON from stdin (`cwd`, `session_id`, `stop_hook_active`,
    `last_assistant_message`, `transcript_path`).
  - Lets the stop through when `stop_hook_active` is set (the agent is already continuing because
    of a stop hook), when `cwd` is not a work tree or the tree is clean, when the final assistant
    message contains "not verified" (any case), or when the tree is unchanged since the last stop
    this hook let through for the session. The last rule keeps a question asked over an
    already-reported dirty tree from being blocked again.
  - Otherwise blocks once with {"decision": "block", "reason": ...}. The agent adds the line and
    stops; the next Stop carries `stop_hook_active` and passes.
  - The final message comes from `last_assistant_message`, or, when that is absent, from the last
    assistant text in the transcript file.
  - WISP_STOP_CHECK=off disables it. WISP_STOP_CHECK_STATE_DIR overrides where the per-session
    tree fingerprint is kept (default: the system temp directory).
  - Fails open: any internal error exits 1 with nothing on stdout, which does not block.
  - Standard library only.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
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


def fingerprint(cwd: str, status: str) -> str:
    """Hash of the status plus each changed path's size and modification time."""
    digest = hashlib.sha256(status.encode("utf-8"))
    tokens = status.split("\0")
    index = 0
    while index < len(tokens):
        entry = tokens[index]
        index += 1
        if len(entry) < 4:
            continue
        code, path = entry[:2], entry[3:]
        if "R" in code or "C" in code:
            index += 1  # the next token is the original path of a rename or copy
        try:
            stat = (Path(cwd) / path).stat()
            digest.update(f"{path}:{stat.st_size}:{stat.st_mtime_ns}".encode("utf-8"))
        except OSError:
            digest.update(f"{path}:missing".encode("utf-8"))
    return digest.hexdigest()


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


def state_file(state_directory: Path, session: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", session) or "unknown"
    return state_directory / f"{safe}.fingerprint"


def acknowledge(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def decide(event: dict[str, Any], state_directory: Path) -> dict[str, Any] | None:
    """Return a block decision, or None to let the stop through."""
    if os.environ.get("WISP_STOP_CHECK", "").lower() == "off":
        return None
    cwd = event.get("cwd") or os.getcwd()
    status = tree_status(str(cwd))
    if not status:
        return None
    current = fingerprint(str(cwd), status)
    record = state_file(state_directory, str(event.get("session_id", "unknown")))
    if event.get("stop_hook_active") or MARKER.search(final_message(event)):
        acknowledge(record, current)
        return None
    try:
        if record.read_text(encoding="utf-8") == current:
            return None
    except OSError:
        pass
    return {"decision": "block", "reason": REASON}


def main() -> int:
    try:
        event = json.load(sys.stdin)
        if not isinstance(event, dict):
            raise ValueError("hook input is not a JSON object")
        state_directory = Path(os.environ.get("WISP_STOP_CHECK_STATE_DIR", Path(tempfile.gettempdir()) / "wisp-stop-check"))
        decision = decide(event, state_directory)
    except Exception as error:  # fail open: only exit code 2 or a block decision stops the agent
        print(f"stop-check: internal error, not blocking: {error}", file=sys.stderr)
        return 1
    if decision is not None:
        print(json.dumps(decision))
    return 0


if __name__ == "__main__":
    sys.exit(main())
