from fastapi import APIRouter, Request
from backend.app.services.model_service import model_info
router = APIRouter()
@router.get("/model-info")
def info(request: Request):
    return model_info(request.app.state.bundle)
