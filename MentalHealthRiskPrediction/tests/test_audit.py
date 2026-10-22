"""All records are synthetic software fixtures, never research evidence."""

import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest

from training.data import ContractError, load_config, load_csv, validate_config
from training.inspect_data import audit, main


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / "synthetic.csv"
        self.config = {
            "dataset_path": "synthetic.csv",
            "text_column": "content",
            "label_column": "target",
            "group_column": "group",
            "behavior_features": [{"name": "value", "min": 0, "max": 1}],
        }

    def write(self, text):
        self.path.write_text(text, encoding="utf-8")

    def test_aggregate_counts_and_no_record_disclosure(self):
        self.write(
            "content,target,group,value\n"
            "private synthetic text,A,secret-group,0.5\n"
            "private synthetic text,A,secret-group,0.5\n"
            "different fixture,B,another-group,2\n"
            " ,B,,NaN\n"
            "third fixture,,another-group,\n"
        )
        result = audit(self.path, self.config)
        self.assertEqual(result["row_count"], 5)
        self.assertEqual(result["duplicate_rows"], 1)
        self.assertEqual(result["duplicate_normalized_texts"], 1)
        self.assertEqual(result["label_distribution"], {"A": 2, "B": 2})
        self.assertEqual(result["behavior"]["value"], {
            "missing": 1, "invalid_numeric": 1, "out_of_range": 1,
        })
        self.assertEqual(result["groups"]["repeated_groups"], 2)
        self.assertEqual(result["groups"]["missing_group_rows"], 1)
        serialized = json.dumps(result)
        self.assertNotIn("private synthetic text", serialized)
        self.assertNotIn("secret-group", serialized)
        self.assertTrue(result["quality_issues"])

    def test_reproducible_audit_and_input_unchanged(self):
        self.write("content,target,group,value\none,A,u,0\ntwo,B,v,1\n")
        before = self.path.read_bytes()
        first = audit(self.path, self.config)
        self.assertEqual(first, audit(self.path, self.config))
        self.assertEqual(before, self.path.read_bytes())
        self.assertEqual(first["quality_issues"], [])
        self.assertTrue(first["unresolved_configuration"])

    def test_rejects_malformed_files(self):
        for text in (
            "", "content,target,group,value,value\n",
            "content,target,group,value\none,A,u\n",
            "content,target,group,value\none,A,u,1,extra\n",
            "other,target,group,value\n", ",target,group,value\n",
            'content,target,group,value\n"unclosed,A,u,1\n',
        ):
            with self.subTest(text=text):
                self.write(text)
                with self.assertRaises(ContractError):
                    load_csv(self.path, self.config)

    def test_contract_rejects_overlap_and_bad_bounds(self):
        for patch in (
            {"text_column": None},
            {"label_column": "content"},
            {"behavior_features": [{"name": "group"}]},
            {"behavior_features": [{"name": "value", "min": 2, "max": 1}]},
            {"behavior_features": [{"name": "value", "min": float("nan")}]},
            {"behavior_features": [{"name": "value", "min": True}]},
            {"delimiter": "::"},
            {"missing_values": "NA"},
        ):
            with self.subTest(patch=patch):
                with self.assertRaises(ContractError):
                    validate_config(self.config | patch)

    def test_relative_path_and_cli(self):
        self.write("content,target,group,value\none,A,u,0\ntwo,B,v,1\n")
        config_path = self.root / "config.json"
        config_path.write_text(json.dumps(self.config), encoding="utf-8")
        _, dataset = load_config(config_path)
        self.assertEqual(dataset, self.path.resolve())
        output = self.root / "report.json"
        with contextlib.redirect_stdout(io.StringIO()):
            code = main(["--config", str(config_path), "--output", str(output)])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.read_text())["row_count"], 2)
        before = self.path.read_bytes()
        with contextlib.redirect_stderr(io.StringIO()):
            code = main(["--config", str(config_path), "--output", str(self.path)])
        self.assertEqual(code, 2)
        self.assertEqual(before, self.path.read_bytes())

    def test_missing_file_safe_error(self):
        config_path = self.root / "config.json"
        config_path.write_text(json.dumps(self.config), encoding="utf-8")
        error = io.StringIO()
        with contextlib.redirect_stderr(error):
            code = main(["--config", str(config_path), "--output", str(self.root / "out.json")])
        self.assertEqual(code, 2)
        self.assertNotIn(str(self.root), error.getvalue())

    def test_missing_tokens_nonfinite_numbers_and_language(self):
        config = copy.deepcopy(self.config)
        config["missing_values"] = ["", "NA"]
        config["language_column"] = "lang"
        self.write("content,target,group,value,lang\none,A,u,inf,si\ntwo,B,v,NA,en\n")
        result = audit(self.path, config)
        self.assertEqual(result["behavior"]["value"]["invalid_numeric"], 1)
        self.assertEqual(result["behavior"]["value"]["missing"], 1)
        self.assertEqual(result["language_distribution"], {"en": 1, "si": 1})

    def test_empty_dataset_and_single_class_flagged(self):
        for rows in ("", "one,A,u,0\n"):
            self.write("content,target,group,value\n" + rows)
            self.assertTrue(audit(self.path, self.config)["quality_issues"])


if __name__ == "__main__":
    unittest.main()
