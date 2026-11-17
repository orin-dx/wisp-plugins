"""Keep agent-facing text from demanding that a model reproduce its reasoning.

Anthropic's refusals documentation names asking a model to reproduce its internal
reasoning (a `reasoning`, `thinking` or `trace` field, or a scratchpad section, requested
verbatim or in a fixed format) as the `reasoning_extraction` trigger. A first-hand probe
recorded in `docs/evaluations/frontend-design/verification/VERIFY-3.md` showed the real
`muse:drafter` prompt, whose schema field is described as a private scratchpad, completing
normally, while one added line demanding verbatim chain of thought was refused and billed.

The field itself is fine. This test fails on wording that asks for reproduced reasoning, so
the demand cannot be added by accident. It reads text a model sees: agent and skill prompts,
Codex role cards, runtime references, and schema property descriptions.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

DEMAND_PATTERNS = [
    r"chain[- ]of[- ]thought",
    r"think (?:out loud|aloud)",
    r"think step[- ]by[- ]step",
    r"step[- ]by[- ]step (?:reasoning|thinking)",
    r"(?:show|write out|write down|output|print|include|record|emit|reproduce|reveal|expose)"
    r" (?:your|the) (?:full |complete |entire |internal |raw )?"
    r"(?:reasoning|thinking|thought process)",
    r"(?:verbatim|word for word).{0,40}(?:reasoning|thinking)",
    r"(?:reasoning|thinking).{0,40}(?:verbatim|word for word)",
    r"show your (?:work|reasoning|thinking)",
]
DEMAND = re.compile("|".join(f"(?:{pattern})" for pattern in DEMAND_PATTERNS), re.IGNORECASE)

# Published schemas are byte-immutable (ADR 004), so wording in one cannot be corrected
# in place. Each exception names the reason and the safer replacement.
IMMUTABLE_SCHEMA_EXCEPTIONS = {
    "shared/schemas/requirement@1.json": (
        "describes `reasoning` as chain-of-thought; agents reach the schema through a file "
        "read, not a system prompt or tool description. A later `requirement@2` should use "
        "'private scratchpad; not forwarded downstream'."
    ),
}

PROMPT_GLOBS = [
    "plugins/*/agents/*.md",
    "plugins/*/skills/*/SKILL.md",
    "harnesses/codex/plugins/*/skills/*/SKILL.md",
    "harnesses/codex/agent-roles/*.md",
    "shared/references/**/*.md",
]


def prompt_files() -> list[Path]:
    seen: dict[Path, None] = {}
    for pattern in PROMPT_GLOBS:
        for path in REPOSITORY_ROOT.glob(pattern):
            if path.is_file():
                seen[path] = None
    return sorted(seen)


def schema_descriptions(path: Path) -> list[str]:
    """Every description string anywhere in a schema document."""
    found: list[str] = []

    def walk(node: object) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "description" and isinstance(value, str):
                    found.append(value)
                else:
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(json.loads(path.read_text(encoding="utf-8")))
    return found


class ReasoningWordingTests(unittest.TestCase):
    def test_lint_catches_the_probe_demand_and_the_common_variants(self) -> None:
        demands = [
            "In the `reasoning` field, write out your complete internal chain of thought verbatim.",
            "Show your reasoning step by step.",
            "Think step by step before answering.",
            "Output the full reasoning exactly as you thought it, word for word.",
            "Record the thinking verbatim in the trace field.",
        ]
        for text in demands:
            with self.subTest(text=text):
                self.assertIsNotNone(DEMAND.search(text))

    def test_lint_allows_the_existing_scratchpad_wording(self) -> None:
        allowed = [
            "keep any reasoning/scratchpad field proportionate to the task — it is discarded",
            "Private producer scratchpad; not forwarded downstream.",
            "State the concern, evidence, consequence, and confidence directly.",
            "A fact relevant to more than one reader (e.g. the reasoning behind a change) goes in one place.",
        ]
        for text in allowed:
            with self.subTest(text=text):
                self.assertIsNone(DEMAND.search(text))

    def test_agent_and_skill_text_does_not_demand_reproduced_reasoning(self) -> None:
        offenders = []
        for path in prompt_files():
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if DEMAND.search(line):
                    offenders.append(f"{path.relative_to(REPOSITORY_ROOT).as_posix()}:{number}: {line.strip()[:120]}")
        self.assertEqual(
            offenders,
            [],
            "Reword to ask for a brief rationale or evidence, not for reproduced reasoning "
            "(see docs/evaluations/frontend-design/verification/VERIFY-3.md).",
        )

    def test_schema_descriptions_do_not_demand_reproduced_reasoning(self) -> None:
        offenders = []
        for path in sorted((REPOSITORY_ROOT / "shared/schemas").glob("*.json")):
            relative = path.relative_to(REPOSITORY_ROOT).as_posix()
            if relative in IMMUTABLE_SCHEMA_EXCEPTIONS:
                continue
            for description in schema_descriptions(path):
                if DEMAND.search(description):
                    offenders.append(f"{relative}: {description[:120]}")
        self.assertEqual(offenders, [])

    def test_schema_exceptions_still_exist_and_still_need_the_exception(self) -> None:
        for relative in IMMUTABLE_SCHEMA_EXCEPTIONS:
            path = REPOSITORY_ROOT / relative
            self.assertTrue(path.is_file(), f"{relative} no longer exists; remove its exception")
            hits = [text for text in schema_descriptions(path) if DEMAND.search(text)]
            self.assertTrue(hits, f"{relative} no longer needs its exception; remove it")


if __name__ == "__main__":
    unittest.main()
