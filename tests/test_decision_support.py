
import math

import pytest

from src.adaptive_scoring.scorer import AdaptiveScorer
from src.recommendations.engine import evaluate_recommendation
from src.decision_support import DecisionSupportPipeline


def test_initial_score():
    result = AdaptiveScorer().update(0.2)
    assert result.adaptive_score == pytest.approx(0.2)
    assert result.data_state == "fresh_reinitialized"


def test_ema_calculation():
    scorer = AdaptiveScorer()
    scorer.update(0.2)
    result = scorer.update(0.8)
    assert result.adaptive_score == pytest.approx(0.41)


def test_alpha_one():
    scorer = AdaptiveScorer(alpha=1.0)
    scorer.update(0.2)
    assert scorer.update(0.8).adaptive_score == pytest.approx(0.8)


@pytest.mark.parametrize(
    "alpha", [-0.1, 0, 1.1, True, float("nan")]
)
def test_invalid_alpha(alpha):
    with pytest.raises(ValueError):
        AdaptiveScorer(alpha=alpha)


@pytest.mark.parametrize(
    "value", [-0.1, 1.1, float("inf"), True, "0.5"]
)
def test_invalid_probability(value):
    with pytest.raises(ValueError):
        AdaptiveScorer().update(value)


def test_missing_data_suppresses_indicators():
    scorer = AdaptiveScorer()
    scorer.update(0.9)

    for _ in range(3):
        result = scorer.update(None)
        assert result.alert_eligible is False
        assert result.prototype_attention_flag is False


def test_unavailable_after_gap():
    scorer = AdaptiveScorer(max_gap=2)
    scorer.update(0.9)
    scorer.update(None)
    scorer.update(None)

    result = scorer.update(None)

    assert result.data_state == "unavailable_stale"
    assert result.adaptive_score is None


def test_reinitialize_after_gap():
    scorer = AdaptiveScorer()
    scorer.update(0.9)

    for _ in range(3):
        scorer.update(None)

    result = scorer.update(0.3)

    assert result.adaptive_score == pytest.approx(0.3)
    assert result.data_state == "fresh_reinitialized"


@pytest.mark.parametrize(
    "score,expected",
    [
        (0.0, "INFO_001"),
        (0.3499, "INFO_001"),
        (0.35, "INFO_002"),
        (0.6499, "INFO_002"),
        (0.65, "INFO_003"),
        (1.0, "INFO_003"),
    ],
)
def test_recommendation_boundaries(score, expected):
    probability = 0.8

    result = evaluate_recommendation(
        adaptive_score=score,
        data_state="fresh_updated",
        alert_eligible=True,
        model_probability=probability,
    )

    assert result.rule_id == expected


def test_uncertain_probability_suppresses_indicator():
    result = evaluate_recommendation(
        adaptive_score=0.85,
        data_state="fresh_updated",
        alert_eligible=True,
        model_probability=0.5,
    )

    assert result.rule_id == "UNCERTAIN_001"
    assert result.attention_flag is False


def test_stale_data_has_priority():
    result = evaluate_recommendation(
        adaptive_score=0.9,
        data_state="held_stale",
        alert_eligible=False,
        model_probability=None,
    )

    assert result.rule_id == "DATA_001"
    assert result.attention_flag is False


def test_integrated_pipeline():
    pipeline = DecisionSupportPipeline()

    first = pipeline.process(0.2)
    second = pipeline.process(0.8)

    assert first.rule_id == "INFO_001"
    assert second.rule_id == "INFO_002"
    assert second.adaptive_score == pytest.approx(0.41)


def test_high_score_attention():
    result = DecisionSupportPipeline().process(0.85)

    assert result.rule_id == "INFO_003"
    assert result.attention_flag is True
    assert result.is_clinical_assessment is False


def test_no_attention_for_missing_input():
    pipeline = DecisionSupportPipeline()
    pipeline.process(0.9)

    result = pipeline.process(None)

    assert result.rule_id == "DATA_001"
    assert result.attention_flag is False


def test_pipeline_reset():
    pipeline = DecisionSupportPipeline()
    pipeline.process(0.9)
    pipeline.reset()

    result = pipeline.process(0.2)

    assert result.adaptive_score == pytest.approx(0.2)


def test_deterministic_sequence():
    sequence = [0.2, 0.8, None, 0.9, None]

    first = DecisionSupportPipeline()
    second = DecisionSupportPipeline()

    results_a = [first.process(x).to_dict() for x in sequence]
    results_b = [second.process(x).to_dict() for x in sequence]

    assert results_a == results_b


def test_no_clinical_assessment_claims():
    pipeline = DecisionSupportPipeline()

    for value in [0.1, 0.4, 0.85, None]:
        result = pipeline.process(value)
        assert result.is_clinical_assessment is False
