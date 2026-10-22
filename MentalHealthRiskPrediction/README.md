# Mental Health Risk Prediction

## GitHub checkout scope

Run component commands from this `MentalHealthRiskPrediction/` directory, unless
otherwise specified. Dependencies, datasets and fitted models are not included.
Only safe `.env.example` templates are included; no credentials are supplied.

Historical documentation and `docs/scaffold_manifest.json` describe the original
workspace. The engineering guide PDF, UI screenshot, temporary renderings and
personal-path scaffold generator were intentionally excluded from this checkout.
Their historical references and hashes do not imply those assets are distributed.

The nested `.github/workflows/tests.yml` is retained as source but is not discovered
by GitHub Actions. Future activation requires a reviewed repository-root workflow
with `defaults.run.working-directory: MentalHealthRiskPrediction`, preserving group
workflows. No CI execution is claimed for this checkout.


**Current demo (2026-10-22):** React/Vite and FastAPI now run locally with strict
vector validation and honest HTTP 503 model-unavailable behavior. No model trained.
See [startup commands and verified behavior](docs/local_demo.md). Earlier scaffold
status below is retained as historical context and superseded for these components.

IT4010 · J26-IT-388 · Individual component: Multimodal AI Fusion & Risk Prediction.

Status: requirements reviewed; configurable CSV loading and aggregate auditing implemented.
No dataset, approved labels, trained model, API, frontend, or measured research results exist yet.
The proposed Transformer + behavioral features + XGBoost architecture requires supervisor confirmation.

## Start here

- [Requirements and source traceability](docs/requirements_summary.md)
- [Proposed architecture](docs/architecture.md)
- [Implementation stages](docs/development_plan.md)
- [Decisions needed before training](docs/open_questions.md)
- [Data contract](docs/data_dictionary.md)
- [Current audit status](docs/data_audit_report.md)

## Run the available tools

The audit uses only the Python standard library. Python 3.12.14 was used for validation.
No pip packages are required at this stage. ML/backend/frontend dependencies will be
selected, pinned and tested when their implementation gates are resolved.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m unittest discover -s tests -v
python -m training.inspect_data --help
Copy-Item config\dataset.example.json config\dataset.local.json
# Edit dataset.local.json to match authorized data and reviewed column definitions.
python -m training.inspect_data --config config/dataset.local.json --output reports/data_audit.json
```

Paths in the configuration are relative to its directory. The example deliberately has
no dataset path or column mappings and will fail with a configuration error until filled.
The audit exits 0 when structurally valid, 1 when data quality issues need review, and 2
for configuration/file errors. Exit 0 is not permission to train: approval, language,
label provenance, near-duplicate and temporal leakage review remain manual gates.

Only aggregate results are written. Reports can still contain sensitive class counts
and column names: keep them restricted. Do not commit real data, local configuration,
model artifacts or audit reports. Synthetic records in tests verify software only.

Training and application startup commands will be added when those components exist.
Predictions, when implemented, are research estimates, not clinical diagnoses.

## Full-stack scaffold added

The requested ML, backend and React/Vite source structure now exists in this same
workspace. These are starter files, not implemented applications. Existing audit
tools and configuration remain the working code. See
[file-by-file migration mapping](docs/folder_structure_migration.md).

No third-party runtime dependencies were installed. ML/backend requirements files
and frontend dependency maps are deliberately deferred until review; do not use
`uvicorn`, `npm run dev`, Docker or training commands yet. New test placeholders
explicitly skip and do not count as functional verification.

```powershell
python -m unittest discover -s tests -v
python scripts/validate_scaffold.py
python -m unittest discover -s ml/tests -v
python -m unittest discover -s backend/tests -v
```

Notebook tooling was unavailable; see [notebook creation instructions](notebooks/README.md).
Review the structure and unresolved decisions before the next implementation phase.
