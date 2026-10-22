from fastapi import APIRouter
from backend.app.api.v1 import health, model_info, predictions
router = APIRouter()
for module in (health, model_info, predictions):
    router.include_router(module.router)
