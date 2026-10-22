# Working local demonstration — 2026-10-22

This guide retains historical checks from the original working project. The GitHub
checkout does not include dependencies, datasets, or trained models. Commands below
start from the GitHub repository root in each terminal; install dependencies only
after approval. Historical results are not fresh-checkout verification.

## Final meeting readiness check — 2026-10-22

Re-read this guide and exploratory_demo_status.md; inspected actual frontend request,
form, result and validation code, API routes/schema/startup/model service, model
directories and evaluation reports. No application defect requiring a fix was found.

- Frontend tests: 5 passed; production build passed again.
- Backend tests: 5 passed, 6 historical placeholders skipped; root tests: 8 passed.
- Live frontend HTTP 200; browser displayed all 16 inputs and API connected.
- Live health returned status ok and model_ready false; model-info returned available
  false and model_version null.
- A valid all-zero software test vector returned HTTP 503 with the unavailable message.
- Live API checks omitted each feature individually: all 16 requests returned 422.
- UI visibly states 220 records, required 1,000, unverified label/feature provenance,
  no established performance and model not trained / unavailable.
- No fitted/fabricated model artifacts found in the model directories. No fabricated
  research predictions, probabilities or metrics found in application/result code or
  evaluation reports. Isolated mocks in software tests are not research results.
- CSV hash remains `1f12b8936ea610fba22bec5c2c64267086c7a204303568c85333ba42d1457e23`.
- Existing TestClient/httpx deprecation warning remains non-blocking. No training,
  package changes, authorization claims or application source changes in this check.

Meeting checklist:

1. Open the local frontend and show API connected plus model-unavailable status.
2. Point out the 220/1,000 limitation and unverified definitions/permission.
3. Submit an empty form to demonstrate required-field validation.
4. For interface testing only, enter zeros in all 16 fields and submit. Show the
   unavailable response, explicitly explaining these are not participant records.
5. Show `/health` or `/docs`; explain that the API/UI work but model fitting and
   research performance remain unavailable pending permission and study requirements.

Servers were already running during verification. Do not start duplicate processes
on occupied ports. Restart commands follow below.

The existing React/Vite frontend and FastAPI backend now run together without a
trained model. No model was fitted, no metrics were produced and no dataset records
were used as demonstration inputs. The original CSV is preserved.

## Authorization still unresolved

Reviewed audit, training, demo and decision documents plus dataset/configuration
metadata. No actual source URL, license text, data-provider authorization or supervisor
pilot approval was found. `authorization_reference` remains null. The recorded source
tokens reddit/twitter/thai do not establish where this particular derived CSV came
from or its permitted use. No credible source can be identified from those tokens
alone, so no permission was inferred from unrelated online datasets.

Needed: the exact source/download URL and version for each contributing dataset;
applicable license or written permission covering this derived vector file and
exploratory model fitting/demo; any required university/supervisor approval. Label
meaning and vector-generation provenance remain unverified. Model fitting remains
disabled; final research still falls short of the 1,000-record minimum.

## Start in two PowerShell terminals

Terminal 1 (backend):

```powershell
Set-Location .\MentalHealthRiskPrediction
# Fresh checkout: these setup steps require approval before running:
# python -m venv .venv
# .\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Terminal 2 (frontend; tested Node 22.14.0):

```powershell
Set-Location .\MentalHealthRiskPrediction\frontend
# Dependencies are excluded. After approval, run npm.cmd ci before starting.
npm.cmd run dev
```

Open http://127.0.0.1:5173/ . API docs: http://127.0.0.1:8000/docs .
Stop each server with Ctrl+C. If a port is occupied by the demo already running,
use the existing server or stop that terminal before restarting; Vite uses strictPort.

Frontend API base defaults to http://127.0.0.1:8000. Override with
`$env:VITE_API_BASE_URL='http://127.0.0.1:8000'` before starting Vite.
Backend CORS allows only localhost/127.0.0.1 port 5173 by default. Override via
`CORS_ORIGINS` (comma-separated origins) if changing the UI origin. Backend variables
are read from the process environment; .env files are examples, not auto-loaded.

## Actual endpoint contract

- GET `/health`: 200 with process status and model_ready false when unavailable.
- GET `/model-info`: availability, literal feature list, purpose and optional version.
- POST `/predict`: body `{ "features": { "bvec_0": number, ..., "bvec_15": number } }`.
  Exactly 16 finite numeric fields required. Strings, booleans, omitted/extra fields,
  and extra root fields are rejected with 422 without echoing inputs.
- Valid input with no model returns 503 and `Model not trained / unavailable`.
  No fabricated label/probability is returned.

For a future authorized model, `MODEL_DIR` selects the operator-controlled local
bundle and `TRUSTED_MODEL=true` explicitly permits loading. Defaults are untrusted
and unavailable. The bundle loads once at startup through the existing ML loader.
Actual fitted-bundle integration remains untested because no artifact exists.

The UI remains usable if API/model is unavailable. It provides 16 numeric fields,
input validation, request loading, network/422/503 errors, connection refresh,
result clearing before requests and a result section for actual API responses.
No history, authentication, persistence, explanation service, probability chart or
raw-text/hybrid model has been implemented. Local-only demo; not production deployment.

## Validation and limitations

```powershell
# Component directory (MentalHealthRiskPrediction), with dependencies available
.\.venv\Scripts\python.exe -m unittest discover -s backend/tests -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
python scripts/validate_scaffold.py
# frontend directory
npm.cmd test
npm.cmd run build
```

Frontend: five active tests passed; production build passed. Backend: five active
tests passed, six historical placeholders skipped. Runtime checks cover health,
missing artifacts, 503, strict validation and CORS. Frontend tests cover required
inputs, feature ordering, loading, connection errors and 503/422 handling. Live
browser verification showed API connected, 16 missing-field errors on empty submit,
then the real API unavailable response using all-zero software test inputs.
These test inputs were not added to the dataset or used as research records.
Root tests: eight passed. Static scaffold validation passed (106 Python sources).
The CSV SHA-256 was verified unchanged after implementation.

Initial sandbox runs stalled/denied local sockets. Tests and preview succeeded
outside that restriction. TestClient emits an httpx deprecation warning with the
installed Starlette version, but all active backend assertions passed.

## Files changed

- Backend: `app/main.py`, `app/config.py`, `app/api/router.py`, v1 health/model_info/
  predictions modules, schemas/prediction.py, services/model_service.py and
  prediction_service.py; requirements.txt pins the installed environment;
  pyproject.toml and .env.example reflect current runtime requirements/settings;
  tests/test_demo_api.py adds runtime tests.
- Frontend: package.json and package-lock.json, vite.config.js, main.jsx, App.jsx,
  index.css, PredictionForm/PredictionResult, apiClient/predictionService,
  validators.js, tests/setup.js and tests/demo.test.jsx.
- Documentation: this guide plus current-status pointers in root/backend/frontend
  READMEs, exploratory_demo_status.md and open_questions.md.
- Local-only ignored outputs: .venv, node_modules, dist and tmp implementation helper.

Existing dataset, original audit/tests, PDF, unrelated scaffold modules and training
gates were preserved. No new project, hosted Site, duplicate frontend or backend.
