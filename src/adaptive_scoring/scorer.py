
from dataclasses import dataclass, asdict
from math import isfinite
from typing import Optional


DEFAULT_ALPHA = 0.35
DEFAULT_MAX_GAP = 2

LOW_BOUND = 0.35
HIGH_BOUND = 0.65


@dataclass(frozen=True)
class ScoringResult:
    model_probability: Optional[float]
    adaptive_score: Optional[float]
    data_state: str
    consecutive_missing: int
    display_band: str
    alert_eligible: bool
    prototype_attention_flag: bool

    def to_dict(self):
        return asdict(self)


class AdaptiveScorer:
    """
    Reusable EMA scoring implementation from Notebook 05.

    One instance represents ONE synthetic temporal sequence.

    Do not share an instance across different users or sequences.

    Scores are experimental and are NOT clinically
    calibrated mental-health probabilities.
    """

    def __init__(
        self,
        alpha: float = DEFAULT_ALPHA,
        max_gap: int = DEFAULT_MAX_GAP,
    ):
        if (
            isinstance(alpha, bool)
            or not isinstance(alpha, (int, float))
            or not isfinite(alpha)
            or not 0 < alpha <= 1
        ):
            raise ValueError("alpha must be in (0, 1]")

        if (
            isinstance(max_gap, bool)
            or not isinstance(max_gap, int)
            or max_gap < 0
        ):
            raise ValueError("max_gap must be a nonnegative integer")

        self.alpha = float(alpha)
        self.max_gap = max_gap

        self.previous_score: Optional[float] = None
        self.consecutive_missing = 0

    @staticmethod
    def get_band(score: Optional[float]) -> str:
        if score is None:
            return "unavailable"

        if score < LOW_BOUND:
            return "lower-score"

        if score < HIGH_BOUND:
            return "middle-score"

        return "higher-score"

    def reset(self):
        """Start a completely new temporal sequence."""
        self.previous_score = None
        self.consecutive_missing = 0

    def update(
        self,
        model_probability: Optional[float],
    ) -> ScoringResult:

        # None or NaN represents a missing observation.
        if model_probability is None:
            valid = False
        elif isinstance(model_probability, bool):
            raise ValueError("Boolean is not a probability")
        elif not isinstance(model_probability, (int, float)):
            raise ValueError("Probability must be numeric")
        elif model_probability != model_probability:
            valid = False
        elif not isfinite(model_probability):
            raise ValueError("Probability must be finite")
        elif not 0 <= model_probability <= 1:
            raise ValueError("Probability must be between 0 and 1")
        else:
            valid = True

        if valid:
            incoming = float(model_probability)

            reinitialize = (
                self.previous_score is None
                or self.consecutive_missing > self.max_gap
            )

            if reinitialize:
                current = incoming
                state = "fresh_reinitialized"
            else:
                current = (
                    self.alpha * incoming
                    + (1 - self.alpha) * self.previous_score
                )
                state = "fresh_updated"

            self.previous_score = current
            self.consecutive_missing = 0
            available = True

        else:
            incoming = None
            self.consecutive_missing += 1

            available = (
                self.previous_score is not None
                and self.consecutive_missing <= self.max_gap
            )

            current = (
                self.previous_score if available else None
            )

            state = (
                "held_stale"
                if available
                else "unavailable_stale"
            )

        alert_eligible = bool(valid and available)

        attention_flag = bool(
            alert_eligible
            and current is not None
            and current >= HIGH_BOUND
        )

        return ScoringResult(
            model_probability=incoming,
            adaptive_score=current,
            data_state=state,
            consecutive_missing=self.consecutive_missing,
            display_band=self.get_band(current),
            alert_eligible=alert_eligible,
            prototype_attention_flag=attention_flag,
        )
