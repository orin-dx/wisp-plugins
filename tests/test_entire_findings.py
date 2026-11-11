import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("entire_findings", ROOT / "tools/entire-findings.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def row(repo, change, status, severity):
    return {"repo": repo, "change": change, "status": status, "severity": severity}


class SummarizeTests(unittest.TestCase):
    def test_counts_by_repo_status_and_severity(self):
        rows = [
            row("a", "a/1", "open", "low"),
            row("a", "a/1", "resolved", "medium"),
            row("b", "b/2", "dismissed", "low"),
        ]
        summary = MODULE.summarize(rows)
        self.assertEqual(3, summary["total"])
        self.assertEqual(2, summary["changes_with_findings"])
        self.assertEqual({"status:open": 1, "severity:low": 1, "status:resolved": 1, "severity:medium": 1}, summary["by_repo"]["a"])
        self.assertEqual([("a/1", 2), ("b/2", 1)], summary["top_changes"])

    def test_empty_snapshot(self):
        summary = MODULE.summarize([])
        self.assertEqual(0, summary["total"])
        self.assertEqual(0, summary["median_per_change_with_findings"])


if __name__ == "__main__":
    unittest.main()
