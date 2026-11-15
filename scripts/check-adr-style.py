#!/usr/bin/env python3
"""Warn when a decision record carries what a reader two years on does not need.

Usage: python3 scripts/check-adr-style.py [directory]   (default docs/adr)

A record keeps the decision, the lasting reasons, the rejected options and why, what it costs and when to
revisit it, and a pointer to its evidence. Measurements, run counts, one-off test dates and a tour of the
investigation belong in the evaluation log, the commit or the pull request. The check only warns: judgment
stays with the writer, and a long record that earns its length can say so in review. See
shared/references/architecture/decision-records.md.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

WORD_REVIEW = 450
MARKERS = (
    (re.compile(r"\blive runs?\b", re.I), "a live run is evidence for the log, not the record"),
    (re.compile(r"\b(?:in|during) this session\b", re.I), "session narration"),
    (re.compile(r"\b\d[\d,]*\s+(?:runs?|calls?|rounds?|sessions?|transcripts?|findings|tokens)\b", re.I), "a count from one investigation"),
    (re.compile(r"\bone run (?:each|per)\b", re.I), "a run count"),
    (re.compile(r"\b(?:on|since|as of)\s+20\d\d-\d\d-\d\d\b", re.I), "a one-off date"),
    (re.compile(r"\bnot yet (?:measured|verified|tested)\b", re.I), "an open-measurement list; keep one `Revisit when` instead"),
)


def body(text: str) -> str:
    """The record without its title, Status and Date lines, which legitimately carry dates and links."""
    lines = [line for line in text.splitlines() if not line.startswith(("# ", "**Status:**", "**Date:**", "**Amends:**", "**Supersedes:**"))]
    return "\n".join(lines)


def review(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    notes = []
    words = len(body(text).split())
    if words > WORD_REVIEW:
        notes.append(f"{words} words (review above {WORD_REVIEW}): cut what a reader two years on does not need")
    for pattern, reason in MARKERS:
        hits = pattern.findall(body(text))
        if hits:
            notes.append(f"transient detail ({reason}): {hits[0]!r}")
    return notes


def main(argv: list[str]) -> int:
    directory = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent / "docs" / "adr"
    records = sorted(path for path in directory.glob("[0-9][0-9][0-9]-*.md"))
    flagged = 0
    for path in records:
        notes = review(path)
        if notes:
            flagged += 1
            print(f"WARN: {path.name}")
            for note in notes:
                print(f"    {note}")
    if flagged:
        print(f"WARN: {flagged} of {len(records)} decision record(s) cross the review signal; this does not fail validation.")
    else:
        print(f"OK: {len(records)} decision record(s) read as decisions, not session logs.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
