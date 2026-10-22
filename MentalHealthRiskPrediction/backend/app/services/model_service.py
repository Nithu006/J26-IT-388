"""Load the shared ML bundle once at startup, only with explicit operator trust."""
import sys
from backend.app.config import ROOT
sys.path.insert(0, str(ROOT / "ml/src"))
from mental_health_ml.inference.prediction_pipeline import load_bundle, ModelUnavailable, FEATURES

def load_model(path, trusted):
    try:
        return load_bundle(path, trusted=trusted)
    except ModelUnavailable:
        return None

def model_info(bundle):
    return {"available": bundle is not None,
            "message": "Model ready" if bundle else "Model not trained / unavailable",
            "model_version": bundle[1]["model_version"] if bundle else None,
            "features": list(FEATURES), "purpose": "exploratory_recorded_label"}
