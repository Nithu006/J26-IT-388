# backend

**Update 2026-10-22:** a working local ASGI app now serves health/model-info/predict.
See [local demo guide](../docs/local_demo.md) for commands, environment and test results.
Earlier scaffold-only statements below are historical. Model training remains blocked.

Purpose: reserved location for backend.
Status: starter structure only; implementation and contracts await review.
No real data, trained model, results, authentication or persistence is provided.
Research use only; not a clinical diagnostic system.

`app/main.py` does not expose an ASGI application yet. Do not start uvicorn.
API/schema/service files reserve contracts; repository/db/auth/history files do
not select a database or claim working security. No records are stored.

After review, pin FastAPI/Pydantic/uvicorn and test dependencies, then implement
health/readiness and explicit unavailable-model behavior before prediction.
The existing data contract will determine request feature names and bounds.
`python -m unittest discover -s backend/tests -v` reports six intentional skips.
