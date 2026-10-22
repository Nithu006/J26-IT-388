
import pytest
from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"text": ""},
        {"text": "   "},
        {"text": "a" * 10001},
        {"text": None},
        {"text": 123},
        {"text": "Valid", "unknown": True},
    ],
)
def test_prediction_input_validation(payload):
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"probabilities": []},
        {"probabilities": [1.1]},
        {"probabilities": [-0.1]},
        {"probabilities": [None] * 101},
        {"probabilities": "invalid"},
        {"probabilities": [0.5], "unexpected": "field"},
    ],
)
def test_scoring_input_validation(payload):
    response = client.post(
        "/decision-support",
        json=payload,
    )
    assert response.status_code == 422


@pytest.mark.parametrize(
    "endpoint",
    ["/explain/shap", "/explain/lime"],
)
@pytest.mark.parametrize(
    "top_k",
    [0, -1, 21],
)
def test_explanation_feature_limits(endpoint, top_k):
    response = client.post(
        endpoint,
        json={
            "text": "I feel overwhelmed with assignments.",
            "top_k": top_k,
        },
    )
    assert response.status_code == 422


def test_missing_data_never_activates_indicator():
    response = client.post(
        "/decision-support",
        json={
            "probabilities": [
                0.9, None, None, None, 0.3
            ]
        },
    )

    assert response.status_code == 200

    results = response.json()["results"]

    for result in results[1:4]:
        assert result["attention_flag"] is False
        assert result["alert_eligible"] is False
        assert result["rule_id"] == "DATA_001"

    assert results[3]["adaptive_score"] is None

    assert results[4]["adaptive_score"] == pytest.approx(0.3)


def test_sequence_requests_do_not_share_state():
    payload = {"probabilities": [0.2, 0.8, 0.9]}

    first = client.post("/decision-support", json=payload)
    second = client.post("/decision-support", json=payload)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()


def test_nonclinical_output_for_sequence():
    response = client.post(
        "/decision-support",
        json={"probabilities": [0.2, 0.8, None]},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["is_clinical_assessment"] is False

    for result in data["results"]:
        assert result["is_clinical_assessment"] is False
