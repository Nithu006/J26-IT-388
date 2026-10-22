# Backend

The FastAPI application in `app/main.py` implements the local model-unavailable demo.
Start it from the component directory, not from `backend/`; see the
[local demo guide](../docs/local_demo.md) for environment setup and commands.

## Working routes

- GET `/health`: returns API status and `model_ready`.
- GET `/model-info`: reports availability, the 16 feature names and model version
  (`null` when no bundle is loaded).
- POST `/predict`: accepts exactly `bvec_0` through `bvec_15` under `features`.
  Values must be finite numbers; strings, booleans and extra/missing fields are rejected.
  Invalid input returns 422 without echoing submitted values. Valid input without a
  trusted model returns 503 and `Model not trained / unavailable`.
- `/docs`: FastAPI's generated API documentation.

The service attempts trusted bundle loading once at startup. Missing, incompatible
or untrusted bundles leave the API running with the model unavailable. No fitted
bundle is included, and successful real-model integration has not been verified.
The trust setting is not dataset permission or research approval.

## Limits and checks

Authentication, history, database repositories, persistence and explanations are
placeholders and are not connected as working API routes. CORS is configured for
local frontend origins; it is not authentication. This is a local research demo,
not a production service or clinical system. No dataset is needed for the demo.

With backend dependencies available, run from `MentalHealthRiskPrediction/`:

```powershell
python -m unittest discover -s backend/tests -v
```

`test_demo_api.py` contains five active tests for health/model information,
unavailable responses, validation, CORS and absent artifacts. Six older placeholder
tests are skipped. Prior verification passed all five active tests; see the guide
for its scope. Skipped tests do not verify unfinished features.

## Environment configuration

Relative `MODEL_DIR` paths resolve against the component directory regardless of
where the process starts. Blank paths use the unavailable-model default directory.
`CORS_ORIGINS` entries are trimmed and deduplicated; an explicitly empty list permits
no cross-origin frontend access. Trust requires the literal value `true`, ignoring
case and surrounding whitespace. These settings do not grant research permission.
Configuration tests run independently with:

```powershell
python -B -m unittest discover -s backend/tests -p test_config.py -v
```
