"""Check tools/paired-analysis.py against hand-computed statistics and the pairing rules."""

from __future__ import annotations

import importlib.util
import json
import math
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPOSITORY_ROOT / "tools" / "paired-analysis.py"

specification = importlib.util.spec_from_file_location("paired_analysis", TOOL)
assert specification is not None and specification.loader is not None
analysis = importlib.util.module_from_spec(specification)
specification.loader.exec_module(analysis)


def trial(task: str, arm: str, run: int = 1, error: bool = False, **fields) -> dict:
    return {"task": task, "arm": arm, "run": run, "error": error, **fields}


class StatisticsTests(unittest.TestCase):
    def test_sign_test_matches_the_exact_binomial(self) -> None:
        self.assertAlmostEqual(analysis.sign_test(9, 1), 2 * (1 + 10) / 1024)
        self.assertEqual(analysis.sign_test(0, 0), 1.0)
        self.assertEqual(analysis.sign_test(5, 5), 1.0)

    def test_wilcoxon_exact_values(self) -> None:
        # all five differences positive: W+ = 15 is the maximum, P(W+ >= 15) = 1/32, two-sided 2/32
        self.assertAlmostEqual(analysis.wilcoxon_signed_rank([1, 2, 3, 4, 5]), 2 / 32)
        # symmetric differences give the centre of the distribution
        self.assertEqual(analysis.wilcoxon_signed_rank([-1, 1]), 1.0)
        # zeros are dropped
        self.assertEqual(analysis.wilcoxon_signed_rank([0, 0, 0]), 1.0)
        # ties use average ranks: |d| = 1, 1, 2 -> ranks 1.5, 1.5, 3; all positive gives 2/8
        self.assertAlmostEqual(analysis.wilcoxon_signed_rank([1, 1, 2]), 2 / 8)

    def test_wilcoxon_normal_approximation_agrees_with_the_exact_limit(self) -> None:
        differences = [(-1) ** i * (i + 1) for i in range(40)]
        exact = analysis.wilcoxon_signed_rank(differences)
        analysis.EXACT_WILCOXON_LIMIT = 10
        try:
            approximate = analysis.wilcoxon_signed_rank(differences)
        finally:
            analysis.EXACT_WILCOXON_LIMIT = 60
        self.assertLess(abs(exact - approximate), 0.05)

    def test_cohen_kappa(self) -> None:
        self.assertAlmostEqual(analysis.cohen_kappa([(1, 1), (1, 0), (0, 0), (0, 0)]), 0.5)
        self.assertEqual(analysis.cohen_kappa([(1, 1), (0, 0)]), 1.0)
        self.assertTrue(math.isnan(analysis.cohen_kappa([])))


class ComparisonTests(unittest.TestCase):
    def trials(self) -> list[dict]:
        rows = []
        for index in range(1, 7):
            task = f"t{index}"
            rows.append(trial(task, "base", 1, score=0.5, cost=1.0))
            rows.append(trial(task, "base", 2, score=0.5, cost=3.0))
            rows.append(trial(task, "with", 1, score=0.5 + (0.25 if index <= 2 else 0), cost=1.1))
            rows.append(trial(task, "with", 2, score=0.5 + (0.25 if index <= 2 else 0), cost=1.3))
        rows.append(trial("crashed", "base", score=1.0, cost=1.0))
        rows.append(trial("crashed", "with", error=True))
        return rows

    def test_repeated_runs_reduce_to_a_median_and_crashes_drop_from_every_arm(self) -> None:
        report = analysis.compare(self.trials(), "base", ["score", "cost"])
        self.assertEqual((report["tasks"], report["paired"], report["excluded"]), (7, 6, 1))
        row = report["comparisons"]["with"]
        self.assertAlmostEqual(row["cost"]["median_delta"], 1.2 - 2.0)  # medians of two runs: 2.0 vs 1.2
        self.assertAlmostEqual(row["cost"]["median_relative_change"], (1.2 - 2.0) / 2.0)
        self.assertEqual((row["score"]["better"], row["score"]["worse"], row["score"]["tied"]), (2, 0, 4))
        self.assertAlmostEqual(row["score"]["sign_test_p"], 0.5)

    def test_unknown_baseline_is_an_error(self) -> None:
        with self.assertRaises(SystemExit):
            analysis.compare(self.trials(), "nope", ["score"])

    def test_three_arms_each_compare_with_the_baseline(self) -> None:
        trials = self.trials() + [trial(f"t{i}", "terse", score=0.5, cost=2.5) for i in range(1, 7)]
        report = analysis.compare(trials, "base", ["cost"])
        self.assertEqual(sorted(report["comparisons"]), ["terse", "with"])

    def test_command_line_reads_json_lines_and_lists(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            as_lines = Path(directory) / "trials.jsonl"
            as_lines.write_text("\n".join(json.dumps(row) for row in self.trials()), encoding="utf-8")
            as_list = Path(directory) / "trials.json"
            as_list.write_text(json.dumps(self.trials()), encoding="utf-8")
            self.assertEqual(len(analysis.load_trials(as_lines)), len(analysis.load_trials(as_list)))
            self.assertEqual(analysis.main(["compare", str(as_lines), "--baseline", "base", "--metrics", "score,cost"]), 0)
            labels = Path(directory) / "labels.json"
            labels.write_text(json.dumps([{"a": 1, "b": 1}, {"a": 1, "b": 0}, {"a": 0, "b": 0}, {"a": 0, "b": 0}]), encoding="utf-8")
            self.assertEqual(analysis.main(["agreement", str(labels)]), 0)


if __name__ == "__main__":
    unittest.main()
