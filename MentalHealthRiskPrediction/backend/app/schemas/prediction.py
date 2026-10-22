"""Strict 16-vector request contract; excludes target, source and risk_oof."""
from pydantic import BaseModel, ConfigDict, field_validator
from backend.app.services.model_service import FEATURES
from mental_health_ml.inference.prediction_pipeline import validate_input

class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    features: dict[str, float]

    @field_validator("features", mode="before")
    @classmethod
    def validate_features(cls, value):
        validate_input(value)
        return value
