
from dataclasses import dataclass, asdict
from typing import Optional

from src.adaptive_scoring.scorer import AdaptiveScorer
from src.recommendations.engine import evaluate_recommendation


@dataclass(frozen=True)
class DecisionSupportResult:
    model_probability: Optional[float]
    adaptive_score: Optional[float]
    data_state: str
    consecutive_missing: int
    alert_eligible: bool

    rule_id: str
    display_band: str
    attention_flag: bool
    recommendation: str
    explanation: str
    is_clinical_assessment: bool = False

    def to_dict(self):
        return asdict(self)


class DecisionSupportPipeline:
    """
    Combines the experimental adaptive scoring and
    non-clinical decision-support modules.

    Each instance represents one independent sequence.

    This is a research prototype, not a diagnostic system.
    """

    def __init__(self, alpha: float = 0.35, max_gap: int = 2):
        self.scorer = AdaptiveScorer(
            alpha=alpha,
            max_gap=max_gap,
        )

    def reset(self):
        self.scorer.reset()

    def process(
        self,
        model_probability: Optional[float],
    ) -> DecisionSupportResult:

        scoring = self.scorer.update(model_probability)

        decision = evaluate_recommendation(
            adaptive_score=scoring.adaptive_score,
            data_state=scoring.data_state,
            alert_eligible=scoring.alert_eligible,
            model_probability=scoring.model_probability,
        )

        # Explicit consistency safeguard:
        # the decision layer cannot activate an indicator
        # when the scoring layer considers it ineligible.
        if decision.attention_flag and not scoring.alert_eligible:
            raise RuntimeError(
                "Attention indicator violated scoring eligibility"
            )

        return DecisionSupportResult(
            model_probability=scoring.model_probability,
            adaptive_score=scoring.adaptive_score,
            data_state=scoring.data_state,
            consecutive_missing=scoring.consecutive_missing,
            alert_eligible=scoring.alert_eligible,
            rule_id=decision.rule_id,
            display_band=decision.display_band,
            attention_flag=decision.attention_flag,
            recommendation=decision.recommendation,
            explanation=decision.explanation,
            is_clinical_assessment=decision.is_clinical_assessment,
        )
