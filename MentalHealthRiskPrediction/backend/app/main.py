"""Local research demo API; model absence does not prevent startup."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.app import config
from backend.app.services.model_service import load_model
from backend.app.api.router import router

@asynccontextmanager
async def lifespan(app):
    app.state.bundle = load_model(config.MODEL_DIR, config.TRUSTED_MODEL)
    yield
    app.state.bundle = None

app = FastAPI(title="Research vector demonstration", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=config.CORS_ORIGINS,
                   allow_methods=["GET", "POST"], allow_headers=["Content-Type"])
app.include_router(router)

@app.exception_handler(RequestValidationError)
async def invalid_request(request, exc):
    # Do not echo submitted vectors or identifiers in error responses.
    return JSONResponse(status_code=422, content={"detail": "Provide exactly 16 finite numeric vector features."})
