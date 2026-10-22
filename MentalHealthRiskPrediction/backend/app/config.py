"""Local demo settings; no dataset access or training side effects."""
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = Path(os.environ.get("MODEL_DIR", str(ROOT / "ml/artifacts/models/exploratory_vectors")))
TRUSTED_MODEL = os.environ.get("TRUSTED_MODEL", "false").lower() == "true"
CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://127.0.0.1:5173,http://localhost:5173").split(",")
