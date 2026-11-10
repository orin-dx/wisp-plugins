#!/usr/bin/env python3
"""Snapshot Entire review findings for one or more repositories and summarize them.

Subcommands (standard library only; `pull` needs the `entire` CLI, logged in, with network access):

  pull     Write every finding (open, resolved, dismissed) on every change of the given repositories to a JSON file.
  summary  Print counts per repository by status and severity, changes with findings, and findings per change,
           for one snapshot or for two snapshots side by side (before and after).

Examples:
  python3 tools/entire-findings.py pull --project gh/orin-dx --repos caliper callisto monokl --out findings-2026-11-06.json
  python3 tools/entire-findings.py summary findings-2026-11-06.json
  python3 tools/entire-findings.py summary before.json after.json
"""

from __future__ import annotations

import argparse
import collections
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

STATUSES = ("open", "resolved", "dismissed")


def entire(*args: str) -> Any:
    done = subprocess.run(["entire", *args, "--json"], capture_output=True, text=True)
    if done.returncode:
        raise SystemExit(f"entire {' '.join(args)}: {done.stderr.strip()[-300:]}")
    return json.loads(done.stdout)


def trail_numbers(project: str, repo: str) -> list[int]:
    numbers: set[int] = set()
    for status in ("open", "closed"):
        token = None
        while True:
            args = ["trail", "list", "--project", project, "--repo", f"{project}/{repo}", "--status", status, "--limit", "100"]
            if token:
                args += ["--page-token", token]
            page = entire(*args)
            numbers.update(item["number"] for item in page.get("items", []))
            token = page.get("nextPageToken")
            if not token:
                break
    return sorted(numbers)


def pull(project: str, repos: list[str]) -> list[dict[str, Any]]:
    changes: dict[tuple[str, str, int], str] = {}
    for repo in repos:
        for number in trail_numbers(project, repo):
            shown = entire("trail", "show", str(number), "--project", project, "--repo", f"{project}/{repo}")
            for change in shown.get("changes", []):
                changes[(repo, change.get("repository", repo), change["number"])] = change.get("branch", "")
    rows: list[dict[str, Any]] = []
    for (repo, name, number), branch in sorted(changes.items()):
        for status in STATUSES:
            found = entire("trail", "finding", "list", f"{name}/{number}", "--project", project, "--freshness", "any", "--status", status)
            for finding in found.get("findings", []):
                rows.append(
                    {
                        "repo": repo,
                        "change": f"{name}/{number}",
                        "branch": branch,
                        "status": status,
                        "severity": finding.get("severity"),
                        "created": (finding.get("createdAt") or "")[:10],
                        "id": finding["id"],
                        "body": finding.get("body", ""),
                        "reason": finding.get("statusReason"),
                    }
                )
    return rows


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_repo: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    per_change: collections.Counter = collections.Counter()
    for row in rows:
        by_repo[row["repo"]][f"status:{row['status']}"] += 1
        by_repo[row["repo"]][f"severity:{row['severity']}"] += 1
        per_change[row["change"]] += 1
    return {
        "total": len(rows),
        "by_repo": {repo: dict(counts) for repo, counts in sorted(by_repo.items())},
        "changes_with_findings": len(per_change),
        "median_per_change_with_findings": sorted(per_change.values())[len(per_change) // 2] if per_change else 0,
        "top_changes": per_change.most_common(5),
    }


def load(path: str) -> list[dict[str, Any]]:
    return json.loads(Path(path).read_text())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    pulled = sub.add_parser("pull")
    pulled.add_argument("--project", required=True)
    pulled.add_argument("--repos", nargs="+", required=True)
    pulled.add_argument("--out", required=True)
    summed = sub.add_parser("summary")
    summed.add_argument("snapshots", nargs="+")
    args = parser.parse_args(argv)
    if args.command == "pull":
        rows = pull(args.project, args.repos)
        Path(args.out).write_text(json.dumps(rows, indent=1))
        print(f"wrote {len(rows)} findings to {args.out}")
        return 0
    for path in args.snapshots:
        print(path)
        print(json.dumps(summarize(load(path)), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
