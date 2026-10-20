"""Check the exploration schemas (option-set@1, spike-report@1) accept real shapes and reject the cases their rules exist for."""

from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
specification = importlib.util.spec_from_file_location("validate_handback", REPOSITORY_ROOT / "tools" / "validate-handback.py")
assert specification is not None and specification.loader is not None
validator = importlib.util.module_from_spec(specification)
specification.loader.exec_module(validator)

OPTION_SET = validator.load_schema("option-set@1")
SPIKE_REPORT = validator.load_schema("spike-report@1")


def option(identifier: str, status: str = "open", **extra) -> dict:
    return {
        "id": identifier,
        "title": f"Option {identifier}",
        "summary": "A navigation rail that stays visible on wide screens.",
        "structure": "Persistent side rail instead of a top bar",
        **({"reason": "Fits the content width"} if status != "open" else {}),
        "status": status,
        **extra,
    }


def sketch(**changes) -> dict:
    document = {
        "id": "SKETCH-001",
        "title": "Site navigation",
        "brief": {"problem": "Visitors cannot find the case studies", "audience": "Prospective clients", "constraints": ["Astro site"], "non_goals": ["Search"]},
        "status": "exploring",
        "round": 1,
        "options": [option("OPT-rail"), option("OPT-top"), option("OPT-sheet")],
        "fidelity": "sketch",
        "reasoning": "Three structurally different layouts.",
    }
    document.update(changes)
    return document


def spike(**changes) -> dict:
    document = {
        "id": "SPIKE-001",
        "question": "Does the headless dialog render in the Astro island setup?",
        "approach": "Mount it on a scratch page and open it by keyboard",
        "observed": ["Dialog opened and trapped focus", "Hydration warning in the console"],
        "verified": ["Opens and closes by keyboard in Chromium"],
        "unverified": ["Safari", "Server rendering"],
        "conclusion": "partly",
        "fidelity": "spike",
        "reasoning": "One page, one browser.",
    }
    document.update(changes)
    return document


class OptionSetTests(unittest.TestCase):
    def errors(self, document: dict) -> list[str]:
        return validator.validate(document, OPTION_SET)

    def test_an_exploring_sketch_with_open_questions_is_valid(self) -> None:
        document = sketch(options=[option("OPT-rail", open_questions=["Does the rail fit at 768px?"], assumptions=["Six nav items"]), option("OPT-top")])
        self.assertEqual(self.errors(document), [])

    def test_a_decided_sketch_needs_a_decision_log_and_reasons(self) -> None:
        decided = sketch(
            status="decided",
            options=[option("OPT-rail", "chosen"), option("OPT-top", "rejected"), option("OPT-sheet", "parked")],
            decisions=[{"option_id": "OPT-rail", "decision": "chosen", "reason": "Fits the content width", "date": "2026-10-20"}],
        )
        self.assertEqual(self.errors(decided), [])
        self.assertTrue(any("decisions" in error for error in self.errors(sketch(status="decided"))))

    def test_every_status_except_open_requires_a_reason(self) -> None:
        for status in ("parked", "chosen", "rejected"):
            with self.subTest(status=status):
                bare = option("OPT-rail", status)
                del bare["reason"]
                self.assertTrue(any("reason" in error for error in self.errors(sketch(options=[bare]))))

    def test_the_sketch_marker_and_scratchpad_are_required(self) -> None:
        for field in ("fidelity", "reasoning", "brief", "options"):
            with self.subTest(field=field):
                document = sketch()
                del document[field]
                self.assertTrue(any(field in error for error in self.errors(document)))
        self.assertTrue(any("expected 'sketch'" in error for error in self.errors(sketch(fidelity="spec"))))

    def test_option_count_and_identifier_shape_are_bounded(self) -> None:
        many = [option(f"OPT-a{index}") for index in range(6)]
        self.assertTrue(any("at most 5" in error for error in self.errors(sketch(options=many))))
        self.assertTrue(any("expected at least 1" in error for error in self.errors(sketch(options=[]))))
        self.assertTrue(any("expected to match" in error for error in self.errors(sketch(id="sketch-1"))))
        self.assertTrue(any("expected to match" in error for error in self.errors(sketch(options=[option("rail")]))))

    def test_unknown_fields_and_bad_dates_are_rejected(self) -> None:
        self.assertTrue(any("unexpected property" in error for error in self.errors(sketch(extra=True))))
        bad_date = sketch(status="decided", options=[option("OPT-rail", "chosen")], decisions=[{"option_id": "OPT-rail", "decision": "chosen", "reason": "r", "date": "20 Oct"}])
        self.assertTrue(any("expected to match" in error for error in self.errors(bad_date)))

    def test_a_render_needs_a_known_kind(self) -> None:
        good = sketch(options=[option("OPT-rail", renders=[{"kind": "screenshot", "location": "sketches/001/rail-390.png", "viewport": "390x844", "theme": "dark"}])])
        self.assertEqual(self.errors(good), [])
        bad = copy.deepcopy(good)
        bad["options"][0]["renders"][0]["kind"] = "video"
        self.assertTrue(any("expected one of" in error for error in self.errors(bad)))


class SpikeReportTests(unittest.TestCase):
    def errors(self, document: dict) -> list[str]:
        return validator.validate(document, SPIKE_REPORT)

    def test_a_partial_result_is_valid(self) -> None:
        self.assertEqual(self.errors(spike()), [])

    def test_works_cannot_be_claimed_without_something_verified(self) -> None:
        self.assertTrue(any("expected at least 1 items" in error for error in self.errors(spike(conclusion="works", verified=[]))))
        self.assertEqual(self.errors(spike(conclusion="works")), [])
        self.assertEqual(self.errors(spike(conclusion="fails", verified=[])), [])

    def test_observations_and_the_marker_are_required(self) -> None:
        self.assertTrue(any("expected at least 1 items" in error for error in self.errors(spike(observed=[]))))
        self.assertTrue(any("expected 'spike'" in error for error in self.errors(spike(fidelity="sketch"))))
        for field in ("question", "approach", "unverified", "conclusion"):
            with self.subTest(field=field):
                document = spike()
                del document[field]
                self.assertTrue(any(field in error for error in self.errors(document)))

    def test_identifier_shape_and_unknown_fields(self) -> None:
        self.assertTrue(any("expected to match" in error for error in self.errors(spike(id="spike1"))))
        self.assertTrue(any("unexpected property" in error for error in self.errors(spike(extra=1))))


class SchemaConventionTests(unittest.TestCase):
    def test_new_schemas_follow_the_repository_conventions(self) -> None:
        for name, schema in (("option-set@1", OPTION_SET), ("spike-report@1", SPIKE_REPORT)):
            with self.subTest(schema=name):
                self.assertEqual(schema["$id"], name)
                self.assertIs(schema["additionalProperties"], False)
                self.assertIn("reasoning", schema["properties"])
                self.assertIn("scratchpad", schema["properties"]["reasoning"]["description"].lower())


if __name__ == "__main__":
    unittest.main()
