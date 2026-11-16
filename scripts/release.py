#!/usr/bin/env python3
"""Tag and publish a release the way the owner has always done it, in one command you run yourself.

Usage: python3 scripts/release.py [--dry-run] [--yes] [--notes FILE]   (or: just release)

On a clean checkout of origin/main whose checks pass, it creates one annotated ecosystem tag (`vX.Y.Z`, the
marketplace version) and one `<plugin>--vA.B.C` tag per plugin version not yet tagged, pushes them, and creates the
GitHub release from the notes. Tags are signed by your git configuration. It shows the plan and asks before it
changes anything; `--dry-run` stops after showing it.

Notes: `--notes FILE`, else `docs/releases/vX.Y.Z.md` if it exists, else the top CHANGELOG.md entry.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENTRY = re.compile(r"^## \[(?P<version>\d+\.\d+\.\d+)\][^\n]*?(?: — (?P<name>[^\n]+))?\n(?P<body>.*?)(?=^## \[|\Z)", re.M | re.S)


def tags_to_create(root: Path, existing: set[str]) -> list[tuple[str, str]]:
    """The ecosystem tag and each plugin tag that does not exist yet, as (tag, annotation)."""
    ecosystem = json.loads((root / "marketplace.json").read_text(encoding="utf-8"))["version"]
    planned = [(f"v{ecosystem}", f"v{ecosystem}")]
    for manifest in sorted(root.glob("plugins/*/plugin.json")):
        data = json.loads(manifest.read_text(encoding="utf-8"))
        planned.append((f"{manifest.parent.name}--v{data['version']}", f"{manifest.parent.name} {data['version']}"))
    return [(tag, note) for tag, note in planned if tag not in existing]


def split_tags(planned: list[tuple[str, str]], local: set[str], remote: set[str]) -> tuple[list[tuple[str, str]], list[str]]:
    """What a rerun still has to do: tags to create (missing locally) and tags to push (missing on the remote)."""
    to_create = [(tag, note) for tag, note in planned if tag not in local]
    to_push = [tag for tag, _ in planned if tag not in remote]
    return to_create, to_push


def changelog_top(root: Path) -> tuple[str, str, str]:
    """(version, name, body) of the newest CHANGELOG.md entry."""
    match = ENTRY.search((root / "CHANGELOG.md").read_text(encoding="utf-8"))
    if match is None:
        raise SystemExit("CHANGELOG.md has no `## [x.y.z]` entry")
    return match.group("version"), (match.group("name") or "").strip(), match.group("body").strip()


def run(*command: str, check: bool = True) -> str:
    done = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    if check and done.returncode != 0:
        raise SystemExit(f"{' '.join(command)} failed:\n{done.stdout}{done.stderr}")
    return done.stdout.strip()


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--dry-run", action="store_true", help="show the plan and stop")
    parser.add_argument("--yes", action="store_true", help="do not ask for confirmation")
    parser.add_argument("--notes", type=Path, help="release notes file")
    args = parser.parse_args(argv)

    run("/usr/bin/git", "fetch", "-q", "origin", "--tags")
    if run("/usr/bin/git", "status", "--porcelain"):
        raise SystemExit("working tree is not clean")
    if run("/usr/bin/git", "rev-parse", "HEAD") != run("/usr/bin/git", "rev-parse", "origin/main"):
        raise SystemExit("HEAD is not origin/main; check out the merged commit to release")
    local = set(run("/usr/bin/git", "tag", "--list").split())
    remote = {line.split("refs/tags/")[1].removesuffix("^{}") for line in run("/usr/bin/git", "ls-remote", "--tags", "origin").splitlines() if "refs/tags/" in line}
    version, name, body = changelog_top(ROOT)
    published = bool(run("gh", "release", "view", f"v{version}", "--json", "tagName", check=False))
    if f"v{version}" in remote and published:
        raise SystemExit(f"v{version} is already released; bump the version and changelog first")
    planned = tags_to_create(ROOT, set())
    to_create, to_push = split_tags(planned, local, remote)
    notes = args.notes or (ROOT / "docs" / "releases" / f"v{version}.md")
    if not notes.is_file():
        notes = None

    print(f"Commit {run('/usr/bin/git', 'rev-parse', '--short', 'HEAD')} on origin/main")
    print("Tags to create:" + ("" if to_create else " none"))
    for tag, _ in to_create:
        print(f"  {tag}")
    print("Tags to push:" + ("" if to_push else " none"))
    for tag in to_push:
        print(f"  {tag}")
    print(f"GitHub release: v{version}" + (f" — {name}" if name else "") + (" (already exists, skipped)" if published else f" (notes: {notes.relative_to(ROOT) if notes and notes.is_relative_to(ROOT) else notes or 'top CHANGELOG entry'})"))
    if args.dry_run:
        return 0
    if not args.yes and input("Run just check, create and push these tags, and publish the release? [y/N] ").strip().lower() != "y":
        print("Nothing changed.")
        return 1

    run("just", "check")
    for tag, note in to_create:
        run("/usr/bin/git", "tag", "-a", tag, "-m", f"{note} — {name}" if tag == f"v{version}" and name else note)
    if to_push:
        run("/usr/bin/git", "push", "origin", *to_push)
    if published:
        print(f"Released v{version}: pushed {len(to_push)} tag(s); the GitHub release already existed.")
        return 0
    notes_file = notes
    if notes_file is None:
        notes_file = ROOT / ".release-notes.tmp"
        notes_file.write_text(body + "\n", encoding="utf-8")
    title = f"v{version}" + (f" — {name}" if name else "")
    run("gh", "release", "create", f"v{version}", "--title", title, "--notes-file", str(notes_file), "--verify-tag")
    if notes is None:
        notes_file.unlink()
    print(f"Released v{version}: pushed {len(to_push)} tag(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
