"""Synthetic software fixtures only; no classifier fitting or research evidence."""
import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from mental_health_ml.data.validate_data import audit_vectors, REQUIRED_COLUMNS
from mental_health_ml.training.train import training_readiness


def fixture():
    header = ",".join(REQUIRED_COLUMNS)
    rows = []
    for identifier, source, label in [("private-a", "reddit", 1), ("private-a", "twitter", 0)]:
        rows.append(",".join([identifier, source, *(["0.1"] * 16), "0.8", str(label)]))
    return (header + "\n" + "\n".join(rows)).encode()


class ReadinessTests(unittest.TestCase):
    def audit(self, raw=None):
        with patch.object(Path, "read_bytes", return_value=raw or fixture()):
            return audit_vectors("synthetic.csv")

    def test_aggregates_do_not_disclose_participants(self):
        result = self.audit()
        self.assertEqual(result["rows"], 2)
        self.assertEqual(result["unique_participants"], 1)
        self.assertEqual(result["rows_with_repeated_participants"], 2)
        self.assertEqual(result["participant_ids_in_multiple_sources"], 1)
        self.assertEqual(result["duplicate_vectors"], 1)
        self.assertEqual(result["label_distribution"], {"0": 1, "1": 1})
        self.assertNotIn("private-a", str(result))

    def test_final_minimum_and_provenance_both_block(self):
        result = self.audit()
        result["rows"] = 220
        decision = training_readiness(result)
        self.assertIn("shortfall 780", decision["blockers"][0])
        self.assertFalse(decision["fitting_performed"])
        enough = copy.deepcopy(result)
        enough["rows"] = 1000
        self.assertEqual(training_readiness(enough)["decision"], "NO-GO")
        self.assertIn("risk_oof", decision["excluded_inputs"])
        self.assertNotIn("risk_oof", decision["candidate_vectors_not_approved"])

    def test_invalid_numeric_and_unknown_categories(self):
        raw = fixture().replace(b"0.1", b"inf").replace(b"reddit", b"private-source")
        result = self.audit(raw)
        self.assertEqual(result["invalid_or_nonfinite_numeric"]["bvec_0"], 2)
        self.assertEqual(result["unrecognized_source_rows"], 1)
        self.assertNotIn("private-source", str(result))

    def test_duplicate_or_missing_schema_rejected(self):
        for raw in (b"label,label\n0,1\n", b"text,label\nprivate,1\n"):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                self.audit(raw)

    def test_audit_is_deterministic(self):
        self.assertEqual(self.audit(), self.audit())
