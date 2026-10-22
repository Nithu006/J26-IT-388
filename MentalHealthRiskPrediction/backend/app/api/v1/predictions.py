from fastapi import APIRouter, Request, HTTPException
from backend.app.schemas.prediction import PredictionRequest
from backend.app.services.prediction_service import predict, ModelUnavailable
router = APIRouter()
@router.post("/predict")
def prediction(payload: PredictionRequest, request: Request):
    try:
        return predict(request.app.state.bundle, payload.features)
    except ModelUnavailable:
        raise HTTPException(503, "Model not trained / unavailable") from None
    except ValueError:
        raise HTTPException(422, "Invalid vector inputs") from None
