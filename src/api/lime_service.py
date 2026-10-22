
import math

import numpy as np
from lime.lime_text import LimeTextExplainer

from src.api.model_service import load_model


LIME_SEED = 42
LIME_NUM_SAMPLES = 1000


def explain_text_lime(
    text: str,
    top_k: int = 12,
) -> dict:
    """
    Explain one prediction using LIME.

    Uses the existing frozen TF-IDF + Logistic
    Regression pipeline without retraining it.

    The local surrogate is fitted to perturbed
    versions of the supplied text.
    """

    if not isinstance(text, str) or not text.strip():
        raise ValueError("Text must not be empty")

    if (
        isinstance(top_k, bool)
        or not isinstance(top_k, int)
        or not 1 <= top_k <= 20
    ):
        raise ValueError("top_k must be between 1 and 20")

    pipeline = load_model()

    if list(pipeline.classes_) != [0, 1]:
        raise ValueError("Unexpected classifier classes")

    original_probability = float(
        pipeline.predict_proba([text])[0, 1]
    )

    predicted_class = int(
        pipeline.predict([text])[0]
    )

    # Create a new seeded explainer for each request.
    # This avoids sharing mutable random state across
    # concurrent API requests.
    explainer = LimeTextExplainer(
        class_names=[
            "Non-stress-related",
            "Stress-related",
        ],
        random_state=LIME_SEED,
        bow=True,
    )

    explanation = explainer.explain_instance(
        text_instance=text,
        classifier_fn=pipeline.predict_proba,
        labels=(1,),
        num_features=top_k,
        num_samples=LIME_NUM_SAMPLES,
    )

    local_terms = []

    for feature, weight in explanation.as_list(label=1):
        weight = float(weight)

        local_terms.append({
            "feature": str(feature),
            "lime_weight": weight,
            "direction": (
                "toward_class_1"
                if weight > 0
                else "toward_class_0"
                if weight < 0
                else "neutral"
            ),
        })

    local_fidelity_r2 = float(explanation.score)

    surrogate_probability = float(
        np.asarray(
            explanation.local_pred
        ).reshape(-1)[0]
    )

    approximation_error = abs(
        original_probability - surrogate_probability
    )

    numeric_values = (
        original_probability,
        local_fidelity_r2,
        surrogate_probability,
        approximation_error,
    )

    if not all(math.isfinite(v) for v in numeric_values):
        raise RuntimeError(
            "LIME produced non-finite explanation values"
        )

    return {
        "predicted_class": predicted_class,
        "probability_stress": original_probability,
        "surrogate_probability": surrogate_probability,
        "local_fidelity_r2": local_fidelity_r2,
        "absolute_approximation_error": (
            approximation_error
        ),
        "contributions": local_terms,
        "method": "LIME Text Explainer",
        "explanation_units": (
            "class_1_local_probability_surrogate"
        ),
        "num_perturbations": LIME_NUM_SAMPLES,
        "random_seed": LIME_SEED,
        "is_clinical_assessment": False,
    }
