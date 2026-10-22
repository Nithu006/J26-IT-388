
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
import shap
from scipy.special import expit

from src.api.model_service import load_model


PROJECT_ROOT = Path(__file__).resolve().parents[2]

TRAIN_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "dreaddit"
    / "dreaddit-train.csv"
)

BACKGROUND_SIZE = 128
RANDOM_SEED = 42


def stratified_indices(labels, requested, seed):
    """
    Reproduce Notebook 03's deterministic,
    class-stratified background selection.
    """
    labels = np.asarray(labels)
    groups = np.unique(labels)

    rng = np.random.default_rng(seed)

    allocations = [
        requested // len(groups)
        + (i < requested % len(groups))
        for i in range(len(groups))
    ]

    chosen = []

    for group, count in zip(groups, allocations):
        pool = np.flatnonzero(labels == group)

        if count > len(pool):
            raise ValueError(
                "Not enough training samples for SHAP background"
            )

        selected = rng.choice(
            pool,
            size=count,
            replace=False,
        )

        chosen.extend(selected.tolist())

    return np.asarray(sorted(chosen), dtype=int)


@lru_cache(maxsize=1)
def load_shap_explainer():
    """
    Initialize SHAP once using training data only.

    The frozen classifier is not modified or retrained.
    """
    pipeline = load_model()

    if list(pipeline.named_steps) != ["tfidf", "model"]:
        raise ValueError("Unexpected classifier pipeline")

    if not TRAIN_PATH.is_file():
        raise FileNotFoundError(
            "Dreaddit training CSV is unavailable"
        )

    vectorizer = pipeline.named_steps["tfidf"]
    classifier = pipeline.named_steps["model"]

    if not hasattr(classifier, "decision_function"):
        raise TypeError("Expected a linear classifier")

    if classifier.coef_.shape[0] != 1:
        raise ValueError("Expected binary logistic regression")

    train = pd.read_csv(
        TRAIN_PATH,
        usecols=["text", "label"],
    )

    if train["text"].isna().any():
        raise ValueError("Training texts contain missing values")

    selected = stratified_indices(
        train["label"].to_numpy(),
        BACKGROUND_SIZE,
        RANDOM_SEED,
    )

    background_texts = (
        train.iloc[selected]["text"]
        .astype(str)
        .tolist()
    )

    background_matrix = vectorizer.transform(
        background_texts
    )

    explainer = shap.LinearExplainer(
        classifier,
        shap.maskers.Independent(background_matrix),
    )

    return vectorizer, classifier, explainer


def explain_text_shap(
    text: str,
    top_k: int = 12,
) -> dict:
    """
    Explain one frozen-model prediction.

    SHAP contributions are measured in class-1
    log-odds, not probability percentage points.
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Text must not be empty")

    if not isinstance(top_k, int) or not 1 <= top_k <= 20:
        raise ValueError("top_k must be between 1 and 20")

    pipeline = load_model()

    vectorizer, classifier, explainer = (
        load_shap_explainer()
    )

    matrix = vectorizer.transform([text])

    explanation = explainer(matrix)

    values = explanation.values

    if hasattr(values, "toarray"):
        values = values.toarray()

    values = np.asarray(values, dtype=float).reshape(-1)

    baseline = float(
        np.asarray(explanation.base_values).reshape(-1)[0]
    )

    model_log_odds = float(
        classifier.decision_function(matrix)[0]
    )

    reconstructed_log_odds = float(
        baseline + values.sum()
    )

    additivity_error = abs(
        model_log_odds - reconstructed_log_odds
    )

    if not np.isfinite(additivity_error):
        raise RuntimeError("Non-finite SHAP reconstruction")

    if additivity_error > 1e-5:
        raise RuntimeError(
            "SHAP explanation failed additivity check"
        )

    original_probability = float(
        pipeline.predict_proba([text])[0, 1]
    )

    reconstructed_probability = float(
        expit(reconstructed_log_odds)
    )

    probability_error = abs(
        original_probability - reconstructed_probability
    )

    if probability_error > 1e-5:
        raise RuntimeError(
            "SHAP probability reconstruction failed"
        )

    feature_names = vectorizer.get_feature_names_out()

    # Highest absolute local contributions.
    selected_indices = np.argsort(
        np.abs(values)
    )[::-1][:top_k]

    contributions = []

    for index in selected_indices:
        contribution = float(values[index])

        if abs(contribution) < 1e-12:
            continue

        contributions.append({
            "feature": str(feature_names[index]),
            "shap_value_log_odds": contribution,
            "direction": (
                "toward_class_1"
                if contribution > 0
                else "toward_class_0"
            ),
        })

    return {
        "predicted_class": int(
            pipeline.predict([text])[0]
        ),
        "probability_stress": original_probability,
        "baseline_log_odds": baseline,
        "model_log_odds": model_log_odds,
        "reconstructed_log_odds": reconstructed_log_odds,
        "additivity_error": float(additivity_error),
        "reconstructed_probability": (
            reconstructed_probability
        ),
        "probability_error": float(probability_error),
        "contributions": contributions,
        "method": "SHAP LinearExplainer",
        "explanation_units": "class_1_log_odds",
        "background_size": BACKGROUND_SIZE,
        "is_clinical_assessment": False,
    }
