"""Check evaluation packet integrity, not model performance or source accuracy."""

import importlib
import json
import unittest
from datetime import date
from pathlib import Path


class EvaluationPacketTests(unittest.TestCase):
    def test_fixed_packets_have_cutoffs_rubrics_and_linked_regressions(self):
        for filename, count in (("skill-evaluation-cases.json", 8), ("normalization-evidence-cases.json", 2)):
            with self.subTest(corpus=filename):
                self.check_packet(filename, count)

    def check_packet(self, filename, count):
        path = Path(__file__).parent / "fixtures" / filename
        corpus = json.loads(path.read_text(encoding="utf-8"))
        cutoff = date.fromisoformat(corpus["data_cutoff"])
        self.assertEqual(corpus["version"], 1)
        self.assertTrue(corpus["evidence_policy"])
        self.assertTrue(corpus["run_protocol"])
        ids = [case["id"] for case in corpus["cases"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(ids), count)
        for case in corpus["cases"]:
            with self.subTest(case=case["id"]):
                self.assertTrue(case["user_prompt"])
                for field in ("evidence_packet", "expected_checks", "forbidden_claims", "regression_tests"):
                    self.assertTrue(case[field], field)
                source_ids = [source["id"] for source in case["evidence_packet"]]
                self.assertEqual(len(source_ids), len(set(source_ids)))
                for source in case["evidence_packet"]:
                    self.assertLessEqual(date.fromisoformat(source["published_at"]), cutoff)
                    self.assertTrue(source["facts"])
                for reference in case["regression_tests"]:
                    module, class_name, method = reference.split(".")
                    test_class = getattr(importlib.import_module(module), class_name)
                    self.assertTrue(issubclass(test_class, unittest.TestCase))
                    self.assertTrue(callable(getattr(test_class, method)))


if __name__ == "__main__":
    unittest.main()
