"""Local demo settings; no dataset access or training side effects."""
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]


def model_directory(value):
    """Resolve relative configured paths against the component, not the shell cwd."""
    path = Path(value.strip()) if value and value.strip() else Path("ml/artifacts/models/exploratory_vectors")
    return path if path.is_absolute() else ROOT / path


def cors_origins(value):
    """Normalize the comma-separated origin list without adding permissive defaults."""
    return list(dict.fromkeys(origin.strip() for origin in value.split(",") if origin.strip()))


MODEL_DIR = model_directory(os.environ.get("MODEL_DIR"))
TRUSTED_MODEL = os.environ.get("TRUSTED_MODEL", "false").strip().lower() == "true"
CORS_ORIGINS = cors_origins(os.environ.get(
    "CORS_ORIGINS", "http://127.0.0.1:5173,http://localhost:5173"))
