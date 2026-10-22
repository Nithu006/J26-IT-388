"""Strict vector interface and trusted local bundle loading; no fallback predictions."""
import hashlib
import json
import math
from numbers import Integral, Real
from pathlib import Path

FEATURES = tuple(f"bvec_{i}" for i in range(16))
NOTICE = "Exploratory classification of an unverified dataset label; not a mental-health diagnosis."


class ModelUnavailable(RuntimeError):
    """No trusted compatible fitted artifact is available."""


def select_candidate_features(record):
    """Select vectors only from a dataset row; never use IDs, source or risk_oof."""
    if not isinstance(record, dict) or any(key not in record for key in FEATURES):
        raise ValueError("All 16 vector features are required.")
    return validate_input({key: record[key] for key in FEATURES})


def validate_input(record):
    """Return ordered finite numeric values; reject extra fields and coercion."""
    if not isinstance(record, dict) or set(record) != set(FEATURES):
        raise ValueError("Input must contain exactly bvec_0 through bvec_15.")
    values = []
    for key in FEATURES:
        value = record[key]
        if isinstance(value, bool) or not isinstance(value, Real):
            raise ValueError("Vector values must be finite numbers.")
        try:
            value = float(value)
        except (ValueError, OverflowError):
            raise ValueError("Vector values must be finite numbers.") from None
        if not math.isfinite(value):
            raise ValueError("Vector values must be finite numbers.")
        values.append(value)
    return values


def load_bundle(directory, *, trusted=False):
    """Only load operator-approved joblib files: deserialization can execute code.

    A matching checksum detects corruption, not trust. Never accept upload paths.
    The pipeline artifact must include all fitted preprocessing and the classifier.
    """
    if not trusted:
        raise ModelUnavailable("Explicit operator trust is required for model loading.")
    root = Path(directory)
    try:
        metadata = json.loads((root / "metadata.json").read_text(encoding="utf-8"))
        if (not isinstance(metadata, dict)
                or type(metadata.get("schema_version")) is not int
                or metadata.get("schema_version") != 1
                or metadata.get("purpose") != "exploratory_recorded_label"
                or metadata.get("feature_names") != list(FEATURES)
                or metadata.get("classes") != [0, 1]
                or any(type(value) is not int for value in metadata["classes"])
                or not isinstance(metadata.get("model_version"), str)
                or not metadata["model_version"].strip()):
            raise ValueError("Incompatible metadata")
        artifact = root / "pipeline.joblib"
        if hashlib.sha256(artifact.read_bytes()).hexdigest() != metadata.get("pipeline_sha256"):
            raise ValueError("Artifact checksum mismatch")
        import joblib
        pipeline = joblib.load(artifact)
        if (list(pipeline.classes_) != [0, 1]
                or any(isinstance(value, bool) or not isinstance(value, Integral) for value in pipeline.classes_)
                or pipeline.n_features_in_ != 16
                or not callable(getattr(pipeline, "predict", None))):
            raise ValueError("Incompatible estimator")
    except Exception:
        raise ModelUnavailable("Model unavailable: missing, incompatible or unreadable bundle.") from None
    return pipeline, metadata


def predict_record(bundle, record):
    """Return the literal recorded label, never inferred clinical semantics."""
    values = validate_input(record)
    if bundle is None:
        raise ModelUnavailable("No trained model is loaded.")
    pipeline, metadata = bundle
    try:
        outputs = pipeline.predict([values])
        if (len(outputs) != 1 or isinstance(outputs[0], bool)
                or not isinstance(outputs[0], Integral) or outputs[0] not in (0, 1)):
            raise ValueError("Invalid prediction")
    except Exception:
        raise ModelUnavailable("Model could not produce a valid recorded-label prediction.") from None
    return {"predicted_label": int(outputs[0]), "model_version": metadata["model_version"],
            "purpose": "exploratory_recorded_label", "notice": NOTICE}
