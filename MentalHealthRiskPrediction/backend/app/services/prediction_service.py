"""Use the existing shared inference implementation; never fabricate results."""
from backend.app.services.model_service import ModelUnavailable
from mental_health_ml.inference.prediction_pipeline import predict_record

def predict(bundle, features):
    return predict_record(bundle, features)
