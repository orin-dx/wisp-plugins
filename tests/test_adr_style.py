"""Cover scripts/check-adr-style.py: it warns on session-log material and stays quiet on a decision."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPOSITORY_ROOT / "scripts" / "check-adr-style.py"

GOOD = """# ADR-099: Gates stop after two rounds

**Status:** Accepted
**Date:** 2026-11-14

## Decision

Exit gates get one retry. A second failing round goes to a human.

## Why

Later rounds repeated wording changes without finding defects.

## Rejected

Three rounds, because the third found nothing the first two missed.

## Consequences

A defect only a third round would catch reaches a human. Revisit when gate misses show up after merge.

Evidence: docs/evaluations/example.md.
"""


class AdrStyleTests(unittest.TestCase):
    def run_on(self, text: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "099-example.md").write_text(text, encoding="utf-8")
            return subprocess.run([sys.executable, str(TOOL), directory], capture_output=True, text=True, check=False)

    def test_a_short_record_without_session_detail_passes_quietly(self) -> None:
        result = self.run_on(GOOD)
        self.assertEqual(result.returncode, 0)
        self.assertNotIn("WARN", result.stdout)

    def test_session_log_material_is_flagged_but_never_fails(self) -> None:
        noisy = GOOD.replace("Later rounds repeated", "A live run on 2026-10-20 over 14 rounds in this session showed later rounds repeated")
        result = self.run_on(noisy)
        self.assertEqual(result.returncode, 0)
        for fragment in ("live run", "this session", "14 rounds", "2026-10-20"):
            self.assertIn(fragment, result.stdout)

    def test_a_long_record_is_flagged(self) -> None:
        result = self.run_on(GOOD + "\n" + ("Another sentence of discussion. " * 200))
        self.assertIn("often holds several decisions", result.stdout)

    def test_the_title_status_and_date_lines_do_not_count(self) -> None:
        dated = GOOD.replace("**Date:** 2026-11-14", "**Date:** 2026-11-14\n**Amends:** 012 as of 2026-11-14")
        self.assertNotIn("WARN", self.run_on(dated).stdout)


if __name__ == "__main__":
    unittest.main()
