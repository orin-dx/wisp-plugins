#!/usr/bin/env python3
"""Paired analysis of an evaluation with two or more arms, using only the standard library.

Input is a JSON list (or JSON Lines) of trials:
  {"task": "t1", "arm": "baseline", "run": 1, "score": 0.5, "cost": 0.21, "turns": 14, "error": false}
Any numeric field other than task and run can be compared; "score" is treated as the quality
outcome. Rules, taken from the paired benchmarks this repository learned from:

  * Pair by task. Repeated runs of a task in one arm are reduced to their median.
  * A task that has no successful trial in some arm is excluded from every arm, so one crash cannot
    skew a comparison. The number excluded is reported.
  * Compare each other arm with the baseline on every metric: median of the per-task differences,
    the median relative change, an exact two-sided Wilcoxon signed-rank p-value (normal approximation
    above 60 pairs), and for the quality score an exact two-sided sign test on the non-ties with the
    counts of better, worse and tied tasks.
  * Report the power limit: a small number of pairs can only rule out large effects.

A tool's self-reported saving is a claim about its counterfactual, not about your bill; analyse the
measured cost and the graded outcome, never the tool's own scoreboard.

Subcommands:
  compare <trials-file> --baseline ARM [--metrics cost,turns,tokens] [--json]
  agreement <labels-file>   Cohen's kappa between two raters; the file is a JSON list of
                            {"a": label, "b": label}. Use it to calibrate an LLM judge against
                            human labels before trusting the judge.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

EXACT_WILCOXON_LIMIT = 60


def load_trials(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8").strip()
    if text.startswith("["):
        return json.loads(text)
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def sign_test(positive: int, negative: int) -> float:
    """Exact two-sided sign test on the non-tied pairs."""
    n = positive + negative
    if n == 0:
        return 1.0
    k = min(positive, negative)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / 2**n
    return min(1.0, 2 * tail)


def wilcoxon_signed_rank(differences: list[float]) -> float:
    """Two-sided Wilcoxon signed-rank p-value; zeros are dropped, ties get average ranks."""
    values = [d for d in differences if d != 0]
    n = len(values)
    if n == 0:
        return 1.0
    ordered = sorted(range(n), key=lambda i: abs(values[i]))
    ranks = [0.0] * n
    start = 0
    while start < n:
        end = start
        while end + 1 < n and abs(values[ordered[end + 1]]) == abs(values[ordered[start]]):
            end += 1
        average = (start + end) / 2 + 1
        for position in range(start, end + 1):
            ranks[ordered[position]] = average
        start = end + 1
    observed = sum(rank for rank, value in zip(ranks, values) if value > 0)
    if n > EXACT_WILCOXON_LIMIT:
        mean = n * (n + 1) / 4
        deviation = math.sqrt(n * (n + 1) * (2 * n + 1) / 24)
        z = (abs(observed - mean) - 0.5) / deviation
        return min(1.0, math.erfc(z / math.sqrt(2)))
    doubled = [round(2 * rank) for rank in ranks]  # half-integer ranks become integers
    total = sum(doubled)
    counts = [0] * (total + 1)
    counts[0] = 1
    for weight in doubled:
        for value in range(total, weight - 1, -1):
            counts[value] += counts[value - weight]
    ways = 2**n
    target = round(2 * observed)
    lower = sum(counts[: target + 1]) / ways
    upper = sum(counts[target:]) / ways
    return min(1.0, 2 * min(lower, upper))


def cohen_kappa(pairs: list[tuple[Any, Any]]) -> float:
    n = len(pairs)
    if n == 0:
        return float("nan")
    observed = sum(1 for a, b in pairs if a == b) / n
    labels = {label for pair in pairs for label in pair}
    expected = sum((sum(1 for a, _ in pairs if a == label) / n) * (sum(1 for _, b in pairs if b == label) / n) for label in labels)
    return 1.0 if expected == 1 else (observed - expected) / (1 - expected)


def per_task_medians(trials: list[dict[str, Any]], metric: str) -> dict[str, dict[str, float]]:
    grouped: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for trial in trials:
        if trial.get("error") or not isinstance(trial.get(metric), (int, float)):
            continue
        grouped[trial["arm"]][trial["task"]].append(float(trial[metric]))
    return {arm: {task: statistics.median(values) for task, values in tasks.items()} for arm, tasks in grouped.items()}


def successful_tasks(trials: list[dict[str, Any]]) -> dict[str, set[str]]:
    result: dict[str, set[str]] = defaultdict(set)
    for trial in trials:
        if not trial.get("error"):
            result[trial["arm"]].add(trial["task"])
    return result


def compare(trials: list[dict[str, Any]], baseline: str, metrics: list[str]) -> dict[str, Any]:
    arms = sorted({trial["arm"] for trial in trials})
    if baseline not in arms:
        raise SystemExit(f"baseline arm {baseline!r} not found; arms are {arms}")
    all_tasks = {trial["task"] for trial in trials}
    ok = successful_tasks(trials)
    kept = sorted(all_tasks.intersection(*(ok[arm] for arm in arms)))
    report: dict[str, Any] = {"arms": arms, "baseline": baseline, "tasks": len(all_tasks), "paired": len(kept), "excluded": len(all_tasks) - len(kept), "comparisons": {}}
    for arm in arms:
        if arm == baseline:
            continue
        rows: dict[str, Any] = {}
        for metric in metrics:
            medians = per_task_medians(trials, metric)
            deltas, relative = [], []
            for task in kept:
                a, b = medians.get(baseline, {}).get(task), medians.get(arm, {}).get(task)
                if a is None or b is None:
                    continue
                deltas.append(b - a)
                if a != 0:
                    relative.append((b - a) / abs(a))
            if not deltas:
                continue
            row: dict[str, Any] = {
                "pairs": len(deltas),
                "median_delta": statistics.median(deltas),
                "median_relative_change": statistics.median(relative) if relative else None,
                "wilcoxon_p": wilcoxon_signed_rank(deltas),
            }
            if metric == "score":
                better = sum(1 for d in deltas if d > 0)
                worse = sum(1 for d in deltas if d < 0)
                row.update({"better": better, "worse": worse, "tied": len(deltas) - better - worse, "sign_test_p": sign_test(better, worse)})
            rows[metric] = row
        report["comparisons"][arm] = rows
    return report


def print_report(report: dict[str, Any]) -> None:
    print(f"{report['tasks']} tasks, {report['paired']} paired, {report['excluded']} excluded from every arm (an arm had no successful trial)")
    for arm, rows in report["comparisons"].items():
        print(f"\n{arm} versus {report['baseline']}")
        for metric, row in rows.items():
            relative = "n/a" if row["median_relative_change"] is None else f"{row['median_relative_change']:+.1%}"
            line = f"  {metric}: median delta {row['median_delta']:+.4g} ({relative}), Wilcoxon p={row['wilcoxon_p']:.3g}, n={row['pairs']}"
            if "sign_test_p" in row:
                line += f"; better {row['better']}, worse {row['worse']}, tied {row['tied']}, sign test p={row['sign_test_p']:.3g}"
            print(line)
    print("\nPower: with this many pairs only large effects can be ruled out; a null result is not proof of no effect.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    compare_parser = sub.add_parser("compare")
    compare_parser.add_argument("trials")
    compare_parser.add_argument("--baseline", required=True)
    compare_parser.add_argument("--metrics", default="score,cost,turns")
    compare_parser.add_argument("--json", action="store_true")
    agreement_parser = sub.add_parser("agreement")
    agreement_parser.add_argument("labels")
    args = parser.parse_args(argv)
    if args.command == "agreement":
        rows = json.loads(Path(args.labels).read_text(encoding="utf-8"))
        kappa = cohen_kappa([(row["a"], row["b"]) for row in rows])
        agreement = sum(1 for row in rows if row["a"] == row["b"]) / len(rows)
        print(f"{len(rows)} items, raw agreement {agreement:.1%}, Cohen's kappa {kappa:.2f}")
        return 0
    report = compare(load_trials(Path(args.trials)), args.baseline, [m.strip() for m in args.metrics.split(",") if m.strip()])
    print(json.dumps(report, indent=2) if args.json else "", end="" if not args.json else "\n")
    if not args.json:
        print_report(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
