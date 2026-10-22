
import math

import pytest
from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)

SAMPLE_TEXT = (
    "I have been feeling overwhelmed with my "
    "university assignments and deadlines."
)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict():
    response = client.post(
        "/predict",
        json={"text": SAMPLE_TEXT},
    )
    assert response.status_code == 200

    result = response.json()
    assert result["predicted_class"] in (0, 1)
    assert 0 <= result["probability_stress"] <= 1
    assert result["is_clinical_assessment"] is False


@pytest.mark.parametrize(
    "text",
    ["", "   "],
)
def test_blank_text_rejected(text):
    response = client.post(
        "/predict",
        json={"text": text},
    )
    assert response.status_code == 422


def test_extra_fields_rejected():
    response = client.post(
        "/predict",
        json={
            "text": SAMPLE_TEXT,
            "unexpected": "value",
        },
    )
    assert response.status_code == 422


def test_decision_support_sequence():
    response = client.post(
        "/decision-support",
        json={
            "probabilities": [
                0.2, 0.8, 0.9,
                None, None, None, 0.3,
            ]
        },
    )

    assert response.status_code == 200

    result = response.json()
    rows = result["results"]

    assert result["sequence_length"] == 7

    assert rows[0]["adaptive_score"] == pytest.approx(0.2)
    assert rows[1]["adaptive_score"] == pytest.approx(0.41)
    assert rows[2]["adaptive_score"] == pytest.approx(0.5815)

    for row in rows[3:6]:
        assert row["rule_id"] == "DATA_001"
        assert row["attention_flag"] is False

    assert rows[5]["adaptive_score"] is None
    assert rows[6]["adaptive_score"] == pytest.approx(0.3)


def test_sequence_state_isolation():
    payload = {"probabilities": [0.85, 0.9]}

    first = client.post(
        "/decision-support",
        json=payload,
    )

    second = client.post(
        "/decision-support",
        json=payload,
    )

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()


@pytest.mark.parametrize(
    "probabilities",
    [
        [0.2, 1.5],
        [-0.1, 0.5],
        [],
    ],
)
def test_invalid_sequence_rejected(probabilities):
    response = client.post(
        "/decision-support",
        json={"probabilities": probabilities},
    )
    assert response.status_code == 422


@pytest.fixture(scope="module")
def shap_result():
    response = client.post(
        "/explain/shap",
        json={
            "text": SAMPLE_TEXT,
            "top_k": 10,
        },
    )
    assert response.status_code == 200, response.text
    return response.json()


@pytest.fixture(scope="module")
def lime_result():
    response = client.post(
        "/explain/lime",
        json={
            "text": SAMPLE_TEXT,
            "top_k": 10,
        },
    )
    assert response.status_code == 200, response.text
    return response.json()


def test_shap_additivity(shap_result):
    assert shap_result["additivity_error"] < 1e-5
    assert shap_result["probability_error"] < 1e-5
    assert shap_result["explanation_units"] == (
        "class_1_log_odds"
    )
    assert len(shap_result["contributions"]) <= 10


def test_lime_fidelity(lime_result):
    assert math.isfinite(
        lime_result["local_fidelity_r2"]
    )
    assert math.isfinite(
        lime_result["absolute_approximation_error"]
    )
    assert lime_result["num_perturbations"] == 1000
    assert len(lime_result["contributions"]) <= 10


def test_explainers_match_frozen_prediction(
    shap_result,
    lime_result,
):
    prediction = client.post(
        "/predict",
        json={"text": SAMPLE_TEXT},
    )

    assert prediction.status_code == 200

    expected = prediction.json()["probability_stress"]

    assert shap_result["probability_stress"] == (
        pytest.approx(expected, abs=1e-8)
    )

    assert lime_result["probability_stress"] == (
        pytest.approx(expected, abs=1e-8)
    )

    assert shap_result["is_clinical_assessment"] is False
    assert lime_result["is_clinical_assessment"] is False


@pytest.mark.parametrize(
    "endpoint",
    ["/explain/shap", "/explain/lime"],
)
def test_explanation_limits(endpoint):
    response = client.post(
        endpoint,
        json={
            "text": SAMPLE_TEXT,
            "top_k": 100,
        },
    )
    assert response.status_code == 422
