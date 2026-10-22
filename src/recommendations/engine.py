
from dataclasses import dataclass, asdict
from math import isfinite
from typing import Optional


# Experimental UI thresholds from Notebook 05.
# These are NOT clinical risk thresholds.
LOW_BOUND = 0.35
HIGH_BOUND = 0.65

# Provisional uncertainty band around the model's
# decision boundary, not a calibrated confidence interval.
UNCERTAIN_LOW = 0.45
UNCERTAIN_HIGH = 0.55

FRESH_STATES = {
    "fresh_updated",
    "fresh_reinitialized",
}


@dataclass(frozen=True)
class DecisionResult:
    rule_id: str
    display_band: str
    attention_flag: bool
    recommendation: str
    explanation: str
    is_clinical_assessment: bool = False

    def to_dict(self):
        return asdict(self)


def evaluate_recommendation(
    adaptive_score: Optional[float],
    data_state: str,
    alert_eligible: bool,
    model_probability: Optional[float] = None,
) -> DecisionResult:
    """
    Generate non-diagnostic decision-support information
    from an existing adaptive-scoring result.

    The caller must obtain data_state and alert_eligible
    from the validated temporal scoring module.
    """

    allowed_states = FRESH_STATES | {
        "held_stale",
        "unavailable_stale",
    }

    if data_state not in allowed_states:
        raise ValueError("Unknown data state")

    if not isinstance(alert_eligible, bool):
        raise ValueError("alert_eligible must be boolean")

    for name, value in (
        ("adaptive_score", adaptive_score),
        ("model_probability", model_probability),
    ):
        if value is not None:
            if isinstance(value, bool):
                raise ValueError(f"Invalid {name}")
            if not isinstance(value, (int, float)):
                raise ValueError(f"Invalid {name}")
            if not isfinite(value) or not 0 <= value <= 1:
                raise ValueError(f"Invalid {name}")

    # Freshness is authoritative. Do not create an alert
    # merely because a stale score is still available.
    if (
        data_state not in FRESH_STATES
        or not alert_eligible
        or adaptive_score is None
    ):
        return DecisionResult(
            rule_id="DATA_001",
            display_band="unavailable",
            attention_flag=False,
            recommendation=(
                "Recent information is unavailable. "
                "No new interpretation is provided."
            ),
            explanation=(
                "The observation is missing, stale, "
                "or ineligible for an attention indicator."
            ),
        )

    if model_probability is None:
        return DecisionResult(
            rule_id="DATA_001",
            display_band="unavailable",
            attention_flag=False,
            recommendation=(
                "A current model output is required "
                "before displaying an interpretation."
            ),
            explanation="Current prediction input is missing.",
        )

    if UNCERTAIN_LOW <= model_probability <= UNCERTAIN_HIGH:
        return DecisionResult(
            rule_id="UNCERTAIN_001",
            display_band="uncertain",
            attention_flag=False,
            recommendation=(
                "The model output is close to its decision "
                "boundary. Avoid drawing conclusions "
                "from this prediction."
            ),
            explanation=(
                "An illustrative uncertainty safeguard "
                "was applied to the current model output."
            ),
        )

    if adaptive_score < LOW_BOUND:
        return DecisionResult(
            rule_id="INFO_001",
            display_band="lower-score",
            attention_flag=False,
            recommendation=(
                "General wellbeing information is available "
                "if you would like to explore it."
            ),
            explanation=(
                "The experimental adaptive score is in "
                "the lower display band."
            ),
        )

    if adaptive_score < HIGH_BOUND:
        return DecisionResult(
            rule_id="INFO_002",
            display_band="middle-score",
            attention_flag=False,
            recommendation=(
                "You may explore general wellbeing resources "
                "or speak with someone you trust."
            ),
            explanation=(
                "The experimental adaptive score is in "
                "the middle display band."
            ),
        )

    return DecisionResult(
        rule_id="INFO_003",
        display_band="higher-score",
        attention_flag=True,
        recommendation=(
            "This text-based model produced an elevated "
            "experimental score. It is not a medical "
            "assessment. If you have concerns about your "
            "wellbeing, consider speaking with a qualified "
            "professional."
        ),
        explanation=(
            "Fresh eligible input and an experimental "
            "adaptive score at or above 0.65 activated "
            "the informational attention indicator."
        ),
    )
