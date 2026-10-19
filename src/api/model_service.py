
from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "dreaddit_tfidf_logreg.joblib"
)


@lru_cache(maxsize=1)
def load_model():
    """
    Load the previously trained classifier once.

    Only load our own trusted model artifact.
    Never load untrusted joblib files.
    """

    if not MODEL_PATH.is_file():
        raise FileNotFoundError(
            f"Frozen classifier not found: {MODEL_PATH}"
        )

    model = joblib.load(MODEL_PATH)

    if not hasattr(model, "predict"):
        raise TypeError("Model lacks predict()")

    if not hasattr(model, "predict_proba"):
        raise TypeError("Model lacks predict_proba()")

    if not hasattr(model, "classes_"):
        raise TypeError("Model lacks classes_")

    if set(model.classes_) != {0, 1}:
        raise ValueError(
            "Expected binary classifier with classes 0 and 1"
        )

    return model


def predict_text(text: str) -> dict:
    """
    Predict the Dreaddit stress-related text label.

    Class 0: non-stress-related
    Class 1: stress-related

    Not a mental-health diagnosis.
    """

    if not isinstance(text, str) or not text.strip():
        raise ValueError("Text must not be empty")

    model = load_model()

    predicted_class = int(model.predict([text])[0])

    probabilities = model.predict_proba([text])[0]
    class_one_index = list(model.classes_).index(1)

    probability_stress = float(
        probabilities[class_one_index]
    )

    if not np.isfinite(probability_stress):
        raise RuntimeError("Non-finite model probability")

    return {
        "predicted_class": predicted_class,
        "probability_stress": probability_stress,
        "model_type": "TF-IDF + Logistic Regression",
        "is_clinical_assessment": False,
    }
