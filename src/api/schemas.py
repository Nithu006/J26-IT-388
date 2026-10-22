
import math
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


# ============================================================
# 1. Health Response
# ============================================================

class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: str
    version: str
    component: str


# ============================================================
# 2. Prediction Request and Response
# ============================================================

class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(
        min_length=1,
        max_length=10000,
        description=(
            "Input text for the provisional Dreaddit "
            "stress-related text classifier."
        ),
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        cleaned = value.strip()

        if not cleaned:
            raise ValueError(
                "Text cannot contain only whitespace"
            )

        return cleaned


class PredictionResponse(BaseModel):
    predicted_class: int = Field(ge=0, le=1)

    probability_stress: float = Field(
        ge=0,
        le=1,
        description=(
            "Classifier probability for stress-related "
            "text class 1. Not a clinical risk probability."
        ),
    )

    model_type: str
    is_clinical_assessment: Literal[False] = False


# ============================================================
# 3. Adaptive Scoring Request
# ============================================================

class ScoringRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    probabilities: list[float | None] = Field(
        min_length=1,
        max_length=100,
        description=(
            "An explicitly synthetic or appropriately "
            "authorized temporal sequence. Each value "
            "must be between 0 and 1, or null for a "
            "missing observation."
        ),
    )

    @field_validator("probabilities")
    @classmethod
    def validate_probabilities(
        cls,
        values: list[float | None],
    ) -> list[float | None]:

        for value in values:
            if value is not None:
                if not math.isfinite(value):
                    raise ValueError(
                        "Probabilities must be finite"
                    )

                if not 0 <= value <= 1:
                    raise ValueError(
                        "Probabilities must be between 0 and 1"
                    )

        return values


# ============================================================
# 4. Individual Decision-Support Result
# ============================================================

class DecisionSupportResponse(BaseModel):
    model_probability: float | None = Field(
        default=None,
        ge=0,
        le=1,
    )

    adaptive_score: float | None = Field(
        default=None,
        ge=0,
        le=1,
    )

    data_state: Literal[
        "fresh_updated",
        "fresh_reinitialized",
        "held_stale",
        "unavailable_stale",
    ]

    consecutive_missing: int = Field(ge=0)

    alert_eligible: bool

    rule_id: Literal[
        "INFO_001",
        "INFO_002",
        "INFO_003",
        "DATA_001",
        "UNCERTAIN_001",
    ]

    display_band: Literal[
        "lower-score",
        "middle-score",
        "higher-score",
        "unavailable",
        "uncertain",
    ]

    attention_flag: bool
    recommendation: str
    explanation: str

    is_clinical_assessment: Literal[False] = False


# ============================================================
# 5. Complete Sequence Response
# ============================================================

class DecisionSupportSequenceResponse(BaseModel):
    sequence_length: int = Field(ge=1)

    results: list[DecisionSupportResponse]

    is_clinical_assessment: Literal[False] = False


# ============================================================
# 6. SHAP Explanation Schemas
# ============================================================

class ShapRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(
        min_length=1,
        max_length=10000,
    )

    top_k: int = Field(
        default=12,
        ge=1,
        le=20,
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("Text cannot be blank")

        return cleaned


class ShapFeatureContribution(BaseModel):
    feature: str
    shap_value_log_odds: float

    direction: Literal[
        "toward_class_1",
        "toward_class_0",
    ]


class ShapResponse(BaseModel):
    predicted_class: int = Field(ge=0, le=1)
    probability_stress: float = Field(ge=0, le=1)

    baseline_log_odds: float
    model_log_odds: float
    reconstructed_log_odds: float
    additivity_error: float = Field(ge=0)

    reconstructed_probability: float = Field(
        ge=0,
        le=1,
    )

    probability_error: float = Field(ge=0)

    contributions: list[ShapFeatureContribution]

    method: str
    explanation_units: Literal["class_1_log_odds"]

    background_size: int = Field(ge=1)

    is_clinical_assessment: Literal[False] = False



# ============================================================
# 7. LIME Explanation Schemas
# ============================================================

class LimeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(
        min_length=1,
        max_length=10000,
    )

    top_k: int = Field(
        default=12,
        ge=1,
        le=20,
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("Text cannot be blank")

        return cleaned


class LimeFeatureContribution(BaseModel):
    feature: str
    lime_weight: float

    direction: Literal[
        "toward_class_1",
        "toward_class_0",
        "neutral",
    ]


class LimeResponse(BaseModel):
    predicted_class: int = Field(ge=0, le=1)

    probability_stress: float = Field(ge=0, le=1)

    surrogate_probability: float

    local_fidelity_r2: float

    absolute_approximation_error: float = Field(ge=0)

    contributions: list[LimeFeatureContribution]

    method: str

    explanation_units: Literal[
        "class_1_local_probability_surrogate"
    ]

    num_perturbations: int = Field(ge=1)

    random_seed: int

    is_clinical_assessment: Literal[False] = False
