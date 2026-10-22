"""Interface tests with mocked estimators, not research records or fitted models."""
import hashlib
import json
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from mental_health_ml.inference.prediction_pipeline import (
    FEATURES, ModelUnavailable, load_bundle, predict_record,
    select_candidate_features, validate_input,
)


class InferenceContractTests(unittest.TestCase):
    def setUp(self):
        self.record = {key: float(i) for i, key in enumerate(FEATURES)}
        self.metadata = {"schema_version": 1, "purpose": "exploratory_recorded_label",
                         "feature_names": list(FEATURES), "classes": [0, 1],
                         "model_version": "software-test-only",
                         "pipeline_sha256": hashlib.sha256(b"test").hexdigest()}

    def test_selection_excludes_every_non_vector_field(self):
        record = dict(reversed(list(self.record.items())))
        record.update(participant_id="test-only", source="test-only", label=1, risk_oof=999)
        self.assertEqual(select_candidate_features(record), list(map(float, range(16))))

    def test_strict_prediction_validation(self):
        cases = [self.record | {"risk_oof": 0.5}, {}, None]
        cases += [self.record | {"bvec_0": x} for x in (True, "1", None, float("nan"), float("inf"))]
        for record in cases:
            with self.subTest(record_type=type(record)), self.assertRaises(ValueError):
                validate_input(record)

    def test_missing_bundle_and_trust_rejected(self):
        with self.assertRaises(ModelUnavailable):
            load_bundle("unused")
        with patch.object(Path, "read_text", side_effect=FileNotFoundError), self.assertRaises(ModelUnavailable):
            load_bundle("unused", trusted=True)
        with self.assertRaises(ModelUnavailable):
            predict_record(None, self.record)

    def test_load_and_predict_with_mock_only(self):
        estimator = Mock(classes_=[0, 1], n_features_in_=16)
        estimator.predict.return_value = [0]
        loader = Mock(return_value=estimator)
        with patch.object(Path, "read_text", return_value=json.dumps(self.metadata)), \
             patch.object(Path, "read_bytes", return_value=b"test"), \
             patch.dict(sys.modules, {"joblib": types.SimpleNamespace(load=loader)}):
            bundle = load_bundle("unused", trusted=True)
            self.assertEqual(predict_record(bundle, self.record)["predicted_label"], 0)
            estimator.predict.assert_called_once_with([list(map(float, range(16)))])

    def test_mismatch_rejected_before_deserialization(self):
        for change in ({"feature_names": list(reversed(FEATURES))}, {"pipeline_sha256": "bad"}, {"classes": [1, 0]}):
            loader = Mock()
            with patch.object(Path, "read_text", return_value=json.dumps(self.metadata | change)), \
                 patch.object(Path, "read_bytes", return_value=b"test"), \
                 patch.dict(sys.modules, {"joblib": types.SimpleNamespace(load=loader)}), \
                 self.assertRaises(ModelUnavailable):
                load_bundle("unused", trusted=True)
            loader.assert_not_called()

    def test_untrusted_bundle_never_reads_files_or_deserializes(self):
        loader = Mock()
        with patch.object(Path, 'read_text') as read, patch.dict(sys.modules, {'joblib': types.SimpleNamespace(load=loader)}):
            with self.assertRaises(ModelUnavailable):
                load_bundle('unused', trusted=False)
            read.assert_not_called()
            loader.assert_not_called()

    def test_metadata_failures_rejected_before_loading(self):
        invalid = [None, [], {}, self.metadata | {'schema_version': True},
                   self.metadata | {'classes': [False, True]},
                   self.metadata | {'model_version': ' '},
                   self.metadata | {'purpose': 'unapproved'},
                   self.metadata | {'feature_names': list(FEATURES[:-1])}]
        for metadata in invalid:
            loader = Mock()
            with self.subTest(kind=type(metadata).__name__), \
                 patch.object(Path, 'read_text', return_value=json.dumps(metadata)), \
                 patch.object(Path, 'read_bytes', return_value=b'test'), \
                 patch.dict(sys.modules, {'joblib': types.SimpleNamespace(load=loader)}):
                with self.assertRaises(ModelUnavailable):
                    load_bundle('unused', trusted=True)
                loader.assert_not_called()

    def test_invalid_json_and_corrupt_artifact_do_not_load(self):
        for text, artifact in [('{', b'test'), (json.dumps(self.metadata), b'corrupt')]:
            loader = Mock()
            with patch.object(Path, 'read_text', return_value=text), \
                 patch.object(Path, 'read_bytes', return_value=artifact), \
                 patch.dict(sys.modules, {'joblib': types.SimpleNamespace(load=loader)}):
                with self.assertRaises(ModelUnavailable):
                    load_bundle('unused', trusted=True)
                loader.assert_not_called()

    def test_incompatible_estimators_are_unavailable(self):
        estimators = [Mock(classes_=[0,1], n_features_in_=15),
                      Mock(classes_=[False,True], n_features_in_=16),
                      Mock(classes_=[1,0], n_features_in_=16),
                      types.SimpleNamespace(classes_=[0,1], n_features_in_=16, predict=None)]
        for estimator in estimators:
            with patch.object(Path, 'read_text', return_value=json.dumps(self.metadata)), \
                 patch.object(Path, 'read_bytes', return_value=b'test'), \
                 patch.dict(sys.modules, {'joblib': types.SimpleNamespace(load=Mock(return_value=estimator))}):
                with self.assertRaises(ModelUnavailable):
                    load_bundle('unused', trusted=True)

    def test_loader_failure_hides_internal_details(self):
        with patch.object(Path, 'read_text', return_value=json.dumps(self.metadata)), \
             patch.object(Path, 'read_bytes', return_value=b'test'), \
             patch.dict(sys.modules, {'joblib': types.SimpleNamespace(load=Mock(side_effect=RuntimeError('private path')))}):
            with self.assertRaises(ModelUnavailable) as caught:
                load_bundle('unused', trusted=True)
            self.assertNotIn('private path', str(caught.exception))

    def test_invalid_prediction_outputs_fail_closed(self):
        for output in [[], [0,1], [True], [0.0], ['0'], [2], None]:
            estimator = Mock(); estimator.predict.return_value = output
            with self.subTest(output_type=type(output).__name__), self.assertRaises(ModelUnavailable):
                predict_record((estimator, self.metadata), self.record)

    def test_estimator_failure_hides_internal_details(self):
        estimator = Mock(); estimator.predict.side_effect = RuntimeError('private vector')
        with self.assertRaises(ModelUnavailable) as caught:
            predict_record((estimator, self.metadata), self.record)
        self.assertNotIn('private vector', str(caught.exception))
