# Folder structure mapping

Historical original-workspace inventory: excluded PDF, generator and temporary
assets below are not present in the GitHub checkout. See the component README for
publication scope; original scaffold-stage status is retained for traceability.

Scope: current workspace only; phase 1 inspection and phase 2 scaffold. No files deleted or renamed.
Git inspection: not a Git repository. Existing 8 audit tests passed before changes.
The complete 13-page guide was read earlier in this chat and remains unchanged.

## Naming overlaps and reuse

- `training/` remains the working audit implementation; `ml/src/` is reserved, not a duplicate implementation.
- `config/dataset.example.json` remains the canonical dataset contract; new YAML points to it.
- `data/` and `models/` remain intact; `dataset/` and `ml/artifacts/` are reserved new locations. Migration needs review.
- Hyphenated documentation links to existing underscore-named documents when purposes match.
- New history/auth/database/explanation modules do not implement or choose providers.
- Frontend sources are not yet runnable; dependency pins, mounting and test runner await review.

## Existing inventory

- `.gitignore`
- `README.md`
- `config/.gitignore`
- `config/dataset.example.json`
- `data/README.md`
- `docs/Hybrid_Mental_Health_Risk_Prediction_Engineer_Guide.pdf`
- `docs/architecture.md`
- `docs/data_audit_report.md`
- `docs/data_dictionary.md`
- `docs/development_plan.md`
- `docs/evaluation_report.md`
- `docs/known_limitations.md`
- `docs/open_questions.md`
- `docs/privacy_and_ethics.md`
- `docs/requirements_summary.md`
- `docs/validation.md`
- `models/README.md`
- `reports/README.md`
- `scaffold_workspace.py`
- `tests/test_audit.py`
- `training/__init__.py`
- `training/data.py`
- `training/inspect_data.py`

## Requested file mapping

| File | Action |
| --- | --- |
| `README.md` | Reused unchanged |
| `.gitignore` | Reused unchanged |
| `.env.example` | Created scaffold |
| `docker-compose.yml` | Created scaffold |
| `Dockerfile` | Created scaffold |
| `docs/project-overview.md` | Created scaffold |
| `docs/system-architecture.md` | Created scaffold |
| `docs/requirements.md` | Created scaffold |
| `docs/database-design.md` | Created scaffold |
| `docs/api-documentation.md` | Created scaffold |
| `docs/ai-model-design.md` | Created scaffold |
| `docs/model-evaluation-plan.md` | Created scaffold |
| `docs/privacy-and-ethics.md` | Created scaffold |
| `docs/testing-plan.md` | Created scaffold |
| `docs/folder_structure_migration.md` | Created scaffold |
| `dataset/README.md` | Created scaffold |
| `dataset/raw/.gitkeep` | Created scaffold |
| `dataset/interim/.gitkeep` | Created scaffold |
| `dataset/processed/.gitkeep` | Created scaffold |
| `dataset/sample/README.md` | Created scaffold |
| `notebooks/01_dataset_exploration.ipynb` | Not created: notebook tooling unavailable |
| `notebooks/02_data_preprocessing.ipynb` | Not created: notebook tooling unavailable |
| `notebooks/03_text_feature_extraction.ipynb` | Not created: notebook tooling unavailable |
| `notebooks/04_behavioral_feature_analysis.ipynb` | Not created: notebook tooling unavailable |
| `notebooks/05_hybrid_model_experiments.ipynb` | Not created: notebook tooling unavailable |
| `notebooks/06_model_evaluation.ipynb` | Not created: notebook tooling unavailable |
| `ml/README.md` | Created scaffold |
| `ml/requirements.txt` | Created scaffold |
| `ml/pyproject.toml` | Created scaffold |
| `ml/config/config.yaml` | Created scaffold |
| `ml/config/model_config.yaml` | Created scaffold |
| `ml/src/mental_health_ml/__init__.py` | Created scaffold |
| `ml/src/mental_health_ml/config.py` | Created scaffold |
| `ml/src/mental_health_ml/data/__init__.py` | Created scaffold |
| `ml/src/mental_health_ml/data/load_data.py` | Created scaffold |
| `ml/src/mental_health_ml/data/validate_data.py` | Created scaffold |
| `ml/src/mental_health_ml/data/clean_data.py` | Created scaffold |
| `ml/src/mental_health_ml/data/split_data.py` | Created scaffold |
| `ml/src/mental_health_ml/data/prevent_leakage.py` | Created scaffold |
| `ml/src/mental_health_ml/preprocessing/__init__.py` | Created scaffold |
| `ml/src/mental_health_ml/preprocessing/text_preprocessor.py` | Created scaffold |
| `ml/src/mental_health_ml/preprocessing/behavior_preprocessor.py` | Created scaffold |
| `ml/src/mental_health_ml/preprocessing/feature_scaler.py` | Created scaffold |
| `ml/src/mental_health_ml/features/__init__.py` | Created scaffold |
| `ml/src/mental_health_ml/features/text_embeddings.py` | Created scaffold |
| `ml/src/mental_health_ml/features/behavioral_features.py` | Created scaffold |
| `ml/src/mental_health_ml/features/feature_fusion.py` | Created scaffold |
| `ml/src/mental_health_ml/models/__init__.py` | Created scaffold |
| `ml/src/mental_health_ml/models/baseline_model.py` | Created scaffold |
| `ml/src/mental_health_ml/models/text_only_model.py` | Created scaffold |
| `ml/src/mental_health_ml/models/behavior_only_model.py` | Created scaffold |
| `ml/src/mental_health_ml/models/hybrid_model.py` | Created scaffold |
| `ml/src/mental_health_ml/models/model_factory.py` | Created scaffold |
| `ml/src/mental_health_ml/training/__init__.py` | Created scaffold |
| `ml/src/mental_health_ml/training/train.py` | Created scaffold |
| `ml/src/mental_health_ml/training/tune_hyperparameters.py` | Created scaffold |
| `ml/src/mental_health_ml/training/cross_validation.py` | Created scaffold |
| `ml/src/mental_health_ml/training/save_model.py` | Created scaffold |
| `ml/src/mental_health_ml/evaluation/__init__.py` | Created scaffold |
| `ml/src/mental_health_ml/evaluation/evaluate.py` | Created scaffold |
| `ml/src/mental_health_ml/evaluation/metrics.py` | Created scaffold |
| `ml/src/mental_health_ml/evaluation/compare_models.py` | Created scaffold |
| `ml/src/mental_health_ml/evaluation/generate_report.py` | Created scaffold |
| `ml/src/mental_health_ml/explainability/__init__.py` | Created scaffold |
| `ml/src/mental_health_ml/explainability/shap_explainer.py` | Created scaffold |
| `ml/src/mental_health_ml/explainability/lime_explainer.py` | Created scaffold |
| `ml/src/mental_health_ml/explainability/explanation_service.py` | Created scaffold |
| `ml/src/mental_health_ml/inference/__init__.py` | Created scaffold |
| `ml/src/mental_health_ml/inference/predict.py` | Created scaffold |
| `ml/src/mental_health_ml/inference/prediction_pipeline.py` | Created scaffold |
| `ml/artifacts/README.md` | Created scaffold |
| `ml/artifacts/models/.gitkeep` | Created scaffold |
| `ml/artifacts/encoders/.gitkeep` | Created scaffold |
| `ml/artifacts/evaluation/.gitkeep` | Created scaffold |
| `ml/scripts/check_dataset.py` | Created scaffold |
| `ml/scripts/run_training.py` | Created scaffold |
| `ml/scripts/run_evaluation.py` | Created scaffold |
| `ml/scripts/export_model.py` | Created scaffold |
| `ml/tests/test_data_validation.py` | Created scaffold |
| `ml/tests/test_preprocessing.py` | Created scaffold |
| `ml/tests/test_text_embeddings.py` | Created scaffold |
| `ml/tests/test_behavioral_features.py` | Created scaffold |
| `ml/tests/test_hybrid_model.py` | Created scaffold |
| `ml/tests/test_evaluation.py` | Created scaffold |
| `ml/tests/test_prediction_pipeline.py` | Created scaffold |
| `backend/README.md` | Created scaffold |
| `backend/requirements.txt` | Created scaffold |
| `backend/pyproject.toml` | Created scaffold |
| `backend/.env.example` | Created scaffold |
| `backend/app/__init__.py` | Created scaffold |
| `backend/app/main.py` | Created scaffold |
| `backend/app/config.py` | Created scaffold |
| `backend/app/dependencies.py` | Created scaffold |
| `backend/app/api/__init__.py` | Created scaffold |
| `backend/app/api/router.py` | Created scaffold |
| `backend/app/api/v1/__init__.py` | Created scaffold |
| `backend/app/api/v1/health.py` | Created scaffold |
| `backend/app/api/v1/model_info.py` | Created scaffold |
| `backend/app/api/v1/predictions.py` | Created scaffold |
| `backend/app/api/v1/explanations.py` | Created scaffold |
| `backend/app/api/v1/history.py` | Created scaffold |
| `backend/app/api/v1/auth.py` | Created scaffold |
| `backend/app/schemas/prediction.py` | Created scaffold |
| `backend/app/schemas/explanation.py` | Created scaffold |
| `backend/app/schemas/user.py` | Created scaffold |
| `backend/app/schemas/common.py` | Created scaffold |
| `backend/app/services/prediction_service.py` | Created scaffold |
| `backend/app/services/explanation_service.py` | Created scaffold |
| `backend/app/services/model_service.py` | Created scaffold |
| `backend/app/services/history_service.py` | Created scaffold |
| `backend/app/repositories/prediction_repository.py` | Created scaffold |
| `backend/app/repositories/user_repository.py` | Created scaffold |
| `backend/app/models/prediction_record.py` | Created scaffold |
| `backend/app/models/user.py` | Created scaffold |
| `backend/app/db/session.py` | Created scaffold |
| `backend/app/db/base.py` | Created scaffold |
| `backend/app/db/migrations/README.md` | Created scaffold |
| `backend/app/core/security.py` | Created scaffold |
| `backend/app/core/logging.py` | Created scaffold |
| `backend/app/core/exceptions.py` | Created scaffold |
| `backend/app/core/rate_limit.py` | Created scaffold |
| `backend/app/utils/validators.py` | Created scaffold |
| `backend/app/utils/datetime_utils.py` | Created scaffold |
| `backend/tests/conftest.py` | Created scaffold |
| `backend/tests/test_health.py` | Created scaffold |
| `backend/tests/test_model_info.py` | Created scaffold |
| `backend/tests/test_predictions.py` | Created scaffold |
| `backend/tests/test_explanations.py` | Created scaffold |
| `backend/tests/test_history.py` | Created scaffold |
| `backend/tests/test_security.py` | Created scaffold |
| `frontend/README.md` | Created scaffold |
| `frontend/package.json` | Created scaffold |
| `frontend/vite.config.js` | Created scaffold |
| `frontend/index.html` | Created scaffold |
| `frontend/.env.example` | Created scaffold |
| `frontend/public/favicon.svg` | Created scaffold |
| `frontend/public/images/README.md` | Created scaffold |
| `frontend/src/main.jsx` | Created scaffold |
| `frontend/src/App.jsx` | Created scaffold |
| `frontend/src/index.css` | Created scaffold |
| `frontend/src/assets/images/README.md` | Created scaffold |
| `frontend/src/assets/icons/README.md` | Created scaffold |
| `frontend/src/components/layout/AppLayout.jsx` | Created scaffold |
| `frontend/src/components/layout/Sidebar.jsx` | Created scaffold |
| `frontend/src/components/layout/Header.jsx` | Created scaffold |
| `frontend/src/components/layout/Footer.jsx` | Created scaffold |
| `frontend/src/components/dashboard/SummaryCard.jsx` | Created scaffold |
| `frontend/src/components/dashboard/RiskDistributionChart.jsx` | Created scaffold |
| `frontend/src/components/dashboard/RecentPredictions.jsx` | Created scaffold |
| `frontend/src/components/prediction/PredictionForm.jsx` | Created scaffold |
| `frontend/src/components/prediction/TextInput.jsx` | Created scaffold |
| `frontend/src/components/prediction/BehaviorInput.jsx` | Created scaffold |
| `frontend/src/components/prediction/PredictionResult.jsx` | Created scaffold |
| `frontend/src/components/prediction/RiskIndicator.jsx` | Created scaffold |
| `frontend/src/components/explainability/ExplanationPanel.jsx` | Created scaffold |
| `frontend/src/components/explainability/FeatureImportanceChart.jsx` | Created scaffold |
| `frontend/src/components/explainability/ExplanationDisclaimer.jsx` | Created scaffold |
| `frontend/src/components/common/Button.jsx` | Created scaffold |
| `frontend/src/components/common/Input.jsx` | Created scaffold |
| `frontend/src/components/common/Loading.jsx` | Created scaffold |
| `frontend/src/components/common/ErrorMessage.jsx` | Created scaffold |
| `frontend/src/components/common/ConfirmDialog.jsx` | Created scaffold |
| `frontend/src/pages/Home.jsx` | Created scaffold |
| `frontend/src/pages/Dashboard.jsx` | Created scaffold |
| `frontend/src/pages/Predict.jsx` | Created scaffold |
| `frontend/src/pages/PredictionHistory.jsx` | Created scaffold |
| `frontend/src/pages/ModelInformation.jsx` | Created scaffold |
| `frontend/src/pages/AboutProject.jsx` | Created scaffold |
| `frontend/src/pages/PrivacyPolicy.jsx` | Created scaffold |
| `frontend/src/pages/Login.jsx` | Created scaffold |
| `frontend/src/pages/NotFound.jsx` | Created scaffold |
| `frontend/src/services/apiClient.js` | Created scaffold |
| `frontend/src/services/predictionService.js` | Created scaffold |
| `frontend/src/services/explanationService.js` | Created scaffold |
| `frontend/src/services/historyService.js` | Created scaffold |
| `frontend/src/services/authService.js` | Created scaffold |
| `frontend/src/hooks/usePrediction.js` | Created scaffold |
| `frontend/src/hooks/useModelInfo.js` | Created scaffold |
| `frontend/src/context/AuthContext.jsx` | Created scaffold |
| `frontend/src/utils/validators.js` | Created scaffold |
| `frontend/src/utils/formatters.js` | Created scaffold |
| `frontend/src/utils/constants.js` | Created scaffold |
| `frontend/src/tests/PredictionForm.test.jsx` | Created scaffold |
| `frontend/src/tests/PredictionResult.test.jsx` | Created scaffold |
| `frontend/src/tests/apiClient.test.js` | Created scaffold |
| `reports/README.md` | Reused unchanged |
| `reports/model_comparison/README.md` | Created scaffold |
| `reports/evaluation/README.md` | Created scaffold |
| `reports/figures/README.md` | Created scaffold |
| `.github/workflows/tests.yml` | Created scaffold |

## Validation commands (PowerShell, workspace root)

```powershell
python -m unittest discover -s tests -v
python scripts/validate_scaffold.py
python -m unittest discover -s ml/tests -v
python -m unittest discover -s backend/tests -v
```

New ML/backend tests intentionally skip; no functional success is implied.
No dependency install, model download, training, database or deployment is needed.
After review: agree package versions and contracts, then implement one tested module at a time.

## Final scaffold inventory and review

- **62 new folders**, excluding interpreter cache folders.
- **194 new files**, including the one-time scaffold builder, static validator,
  manifest and notebook instructions; excluding generated bytecode.
- **6 requested notebook files omitted** because `nbformat` was unavailable.
  See [creation commands](../notebooks/README.md).
- Existing root README and `.gitignore` were extended; decision and validation
  records were appended. No existing file was removed or renamed.
- `reports/README.md`, existing docs, `training/`, `tests/`, `config/`, `data/`,
  `models/` and the engineering PDF were reused/preserved.
- No naming conflict required overwriting a file. Parallel directory names remain
  explicit review decisions D11–D14 in [open questions](open_questions.md).

The manifest records the requested inventory and original file hashes. Its created
list describes the initial scaffold batch; the totals above also include
`scaffold_workspace.py`, `.dockerignore`, `scripts/validate_scaffold.py`, and
`notebooks/README.md`. The one-time builder records how the scaffold was generated
from the user's local attachment; it is not required for validation or normal use.

VS Code next steps:

1. Review this mapping, `open_questions.md`, and the component READMEs.
2. Select Python 3.11+ (validation used 3.12.14) and run the root validation commands.
3. Review the scaffold before authorizing implementation. Runtime installation,
   notebook creation and executable application setup remain next-phase work.
