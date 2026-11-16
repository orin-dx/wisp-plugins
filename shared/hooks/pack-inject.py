#!/usr/bin/env python3
"""Claude Code SessionStart hook that injects the packs a repository declares.

Usage (in a plugin's hooks/hooks.json): pack-inject.py, registered for SessionStart. The packs
directory is `$CLAUDE_PLUGIN_ROOT/packs`, or the first argument.

A repository declares packs with a line in AGENTS.md:

    Packs: rust-house, ts-house

Behavior
  - Reads `Packs:` lines from the AGENTS.md files at the working directory, in the directories
    above it up to the repository root, and in the directories below it (monorepo packages).
  - Injects each declared pack once, as `hookSpecificOutput.additionalContext`, however many
    AGENTS.md files name it. A name with no pack file is ignored.
  - Ignores `Packs:` lines inside fenced code blocks, so documentation examples do not load packs.
  - Fails open: any error prints nothing and exits 0, so a session always starts.
  - Standard library only.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

PACKS_LINE = re.compile(r"^\s*(?:[-*]\s+)?\**Packs:\**\s*(.+?)\s*$")
PACK_NAME = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
SKIPPED_DIRECTORIES = {"node_modules", "target", "dist", "build", "vendor", "venv"}
MAX_DEPTH_BELOW = 4
MAX_FILES = 64
MAX_FILE_BYTES = 256_000
MAX_CONTEXT_CHARACTERS = 60_000


def declared_in(text: str) -> list[str]:
    """Pack names from the `Packs:` lines of one AGENTS.md, in order, skipping fenced code blocks."""
    names: list[str] = []
    opening: str | None = None
    for line in text.splitlines():
        fence = FENCE.match(line)
        if fence is not None:
            marker = fence.group(1)
            if opening is None:
                opening = marker
                continue
            if marker[0] == opening[0] and len(marker) >= len(opening) and not fence.group(2).strip():
                opening = None
                continue
        if opening is not None:
            continue
        match = PACKS_LINE.match(line)
        if match is None:
            continue
        for token in re.split(r"[,\s]+", match.group(1)):
            name = token.strip("`*_.;")
            if PACK_NAME.fullmatch(name):
                names.append(name)
    return names


def agent_files(start: Path) -> list[Path]:
    """AGENTS.md files: from the repository root (or the filesystem root) down to `start`, then below `start`."""
    above: list[Path] = []
    for directory in [start, *start.parents]:
        candidate = directory / "AGENTS.md"
        if candidate.is_file():
            above.append(candidate)
        if (directory / ".git").exists():
            break
    found = list(reversed(above))
    below: list[Path] = []
    for root, directories, files in os.walk(start):
        depth = len(Path(root).relative_to(start).parts)
        directories[:] = sorted(
            name for name in directories if not name.startswith(".") and name not in SKIPPED_DIRECTORIES
        )
        if depth >= MAX_DEPTH_BELOW:
            directories[:] = []
        if depth > 0 and "AGENTS.md" in files:
            below.append(Path(root) / "AGENTS.md")
        if len(found) + len(below) >= MAX_FILES:
            break
    return found + below[: max(0, MAX_FILES - len(found))]


def declared_packs(start: Path) -> list[str]:
    """Every declared pack name once, in the order first seen."""
    seen: dict[str, None] = {}
    for path in agent_files(start):
        try:
            if path.stat().st_size > MAX_FILE_BYTES:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for name in declared_in(text):
            seen.setdefault(name, None)
    return list(seen)


def render(names: list[str], packs_directory: Path) -> str:
    sections: list[str] = []
    for name in names:
        try:
            body = (packs_directory / f"{name}.md").read_text(encoding="utf-8").strip()
        except OSError:
            continue
        sections.append(f"<pack name=\"{name}\">\n{body}\n</pack>")
    if not sections:
        return ""
    header = (
        "This repository declares these house packs in AGENTS.md. A pack states hazards, evidence and deviations "
        "only: run just the commands the repo itself declares, and the repo's own rules and the user's "
        "instructions win over a pack."
    )
    return "\n\n".join([header, *sections])[:MAX_CONTEXT_CHARACTERS]


def packs_directory_from(arguments: list[str]) -> Path | None:
    if arguments:
        return Path(arguments[0])
    root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    return Path(root) / "packs" if root else None


def main(arguments: list[str], stdin_text: str) -> str:
    """The hook's JSON output, or an empty string when there is nothing to inject."""
    payload = json.loads(stdin_text) if stdin_text.strip() else {}
    packs_directory = packs_directory_from(arguments)
    if packs_directory is None or not packs_directory.is_dir():
        return ""
    start = Path(payload.get("cwd") or os.getcwd()).resolve()
    context = render(declared_packs(start), packs_directory)
    if not context:
        return ""
    return json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}})


if __name__ == "__main__":
    try:
        output = main(sys.argv[1:], sys.stdin.read())
        if output:
            print(output)
    except Exception:
        pass
    sys.exit(0)
