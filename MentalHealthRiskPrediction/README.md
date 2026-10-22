# Mental Health Risk Prediction

Research title: Real-Time Explainable AI-Based Mental Health Risk Prediction Using Social Media.
IT4010 / J26-IT-388 / Multimodal AI Fusion & Risk Prediction component.

## Current implementation

The local React/Vite interface and FastAPI backend demonstrate a request flow without
a trained model. No model has been trained for this component, and no research
performance or clinical validity has been established.

| Area | Works now | Incomplete or unavailable |
| --- | --- | --- |
| Frontend | 16 numeric vector inputs, validation, loading/errors, API connection status and result display interface | Real trained-model results, text input workflow, history, login and dashboards |
| Backend | GET `/health`, GET `/model-info`, POST `/predict`, strict input validation and local CORS configuration | Authentication, persistence and explanation services |
| ML | Aggregate audit tools, training readiness checks, input validation and trusted-bundle loading interface | Model fitting, learned preprocessing, text embeddings, fusion, model comparisons and research evaluation |

A valid request without a loaded model returns HTTP 503 and `Model not trained /
unavailable`. Invalid requests return HTTP 422. The application does not substitute
a fake prediction. An API connection is not evidence that a model is ready.

## Checkout contents and research limits

The GitHub checkout intentionally excludes the original dataset. The documented
220-record audit describes a CSV inspected in the original working project, not a
CSV bundled here. The 1,000-record final-study requirement remains unmet by that
original file. Label meanings, vector provenance, dataset-use permissions and
applicable approvals remain unresolved. `risk_oof` is excluded from model inputs.
There is no paired text dataset supporting text-only or complete hybrid experiments.
The proposed Transformer plus behavioral features plus XGBoost design needs review.

Dataset directories contain only documentation and empty-directory markers. Private
configuration, dependencies, build output and fitted artifacts are not tracked.
Dependencies may be installed locally; they are not supplied by a Git clone.
Only safe `.env.example` templates are provided, and they are not loaded automatically.

The engineering guide PDF, screenshot, temporary renderings and personal scaffold
generator were excluded from publication. Historical documents and
`docs/scaffold_manifest.json` retain references to the original workspace; those
references do not mean the excluded files are available in this checkout.

## Start here

- [Local startup, endpoint behavior and verification history](docs/local_demo.md)
- [Backend implementation](backend/README.md)
- [Frontend implementation](frontend/README.md)
- [ML implementation and limitations](ml/README.md)
- [Development status and next steps](docs/development_plan.md)
- [Research decisions and missing evidence](docs/open_questions.md)
- [Original dataset audit](docs/data_audit_report.md)
- [Research readiness assessment and proposed evaluation plan](docs/research_readiness_next_steps.md)
- [Requirements and source traceability](docs/requirements_summary.md)
- [Proposed architecture](docs/architecture.md)
- [Data contract template](docs/data_dictionary.md)

## Audit tools

Run component commands from this `MentalHealthRiskPrediction/` directory unless
otherwise stated. The general audit uses the Python standard library:

```powershell
python -m training.inspect_data --help
python -m unittest discover -s tests -v
python scripts/validate_scaffold.py
```

For authorized data only, create a private configuration from
`config/dataset.example.json` if one does not already exist. Fill it from reviewed
source definitions; paths are relative to that configuration's directory. Then use:

```powershell
python -m training.inspect_data --config config/dataset.local.json --output reports/data_audit.json
```

The empty template is not a valid dataset mapping. The general audit exits 0 for
no detected quality issues, 1 for quality issues, and 2 for configuration/file errors.
A successful audit is not permission to train. The separate vector audit needs pandas;
see [training preparation](docs/model_training.md). Keep real data and private audit
outputs out of Git. Test fixtures are software checks, not research evidence.

## Automation and remaining scaffolding

The nested `.github/workflows/tests.yml` is not discovered by GitHub Actions.
Activating CI requires a reviewed repository-root workflow and the component working
directory, while preserving group workflows. No CI run is claimed here.
Docker files, many optional pages/services and most model modules remain placeholders.
Their presence does not establish working features. See the
[historical structure mapping](docs/folder_structure_migration.md) and
[notebook guidance](notebooks/README.md).
