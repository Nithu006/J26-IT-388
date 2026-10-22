# Supervisor demonstration status — 2026-10-21

**Update 2026-10-22:** UI and API are now implemented and tested for the unavailable-
model demonstration. See [local startup guide](local_demo.md). No authorization or
trained model was found; training remains disabled. Earlier application handoff
steps below are historical.

Meeting target: 2026-10-22. **No model was trained. No evaluation metrics or fitted
artifacts exist.** The latest user request permits an exploratory classifier of the
recorded label conditionally on dataset permissions. It does not supply those permissions.

## Permission decision

Inspected the current audit/training/design/decision documentation, raw-data directory,
configuration and artifact directories. `authorization_reference` remains null in
the dataset configuration. No dataset-use license/authorization or label dictionary
was found in those locations. The source tokens are not permission evidence.
Per the user's explicit instruction, fitting was not performed while permission is
unresolved. No packages were installed or model downloads attempted.

The request allows treating 0 and 1 as uninterpreted recorded labels for an exploratory
demo; no clinical meanings need to be invented. Final research remains NO-GO under
the 1,000-record requirement. Confirm permitted exploratory use of the supplied data
and record the applicable source/license/authorization before fitting. The existing
final-training preflight remains unchanged; it is not an exploratory training runner.

## Application preparation completed

Modified existing modules:

- `ml/src/mental_health_ml/inference/prediction_pipeline.py`: ordered vector selection,
  strict finite-number validation, explicit trust and metadata/checksum validation
  before joblib loading, unavailable-model errors, literal-label prediction interface.
- `ml/src/mental_health_ml/inference/predict.py`: prediction CLI; no dummy output.
- Added `ml/tests/test_inference_contract.py`: feature exclusion, input rejection,
  missing/untrusted artifact handling, metadata/hash rejection and mocked loading.
- Added this status document and appended current status to `docs/model_training.md`
  and `docs/open_questions.md`.

No backend/frontend was implemented. Original CSV, audit code, existing tests and
configuration remain unchanged. Mocked estimators are isolated software test doubles;
they are not saved models, synthetic research records or measured model performance.

## Proposed future artifact contract (no files created)

Directory: `ml/artifacts/models/exploratory_vectors/`.
Expected files: `pipeline.joblib` (fitted preprocessing and estimator together),
`metadata.json` (schema_version 1, purpose `exploratory_recorded_label`, exact ordered
feature_names bvec_0–bvec_15, classes [0,1], nonempty model_version, pipeline_sha256).
Also record dataset hash, training-only transformations, split/seed, dependency
versions and permissions in the eventual training report. Metadata labels are tokens,
not clinical class definitions. No probability/calibration claim is implemented.

Only an operator-approved local artifact may be loaded. Joblib deserialization can
execute code; checksum equality detects corruption but does not establish trust.
The loader checks interface compatibility, not whether training provenance is valid.
No actual sklearn/joblib pipeline serialization round trip has been tested yet.

## Commands

Available now, from the root:

```powershell
python -m unittest discover -s ml/tests -p test_inference_contract.py -v
```

Future prediction command, **only after an authorized model is trained and saved**:

```powershell
$env:PYTHONPATH = (Resolve-Path 'ml/src').Path
python -m mental_health_ml.inference.predict --model-dir ml/artifacts/models/exploratory_vectors --input dataset/sample/vector_input.local.json --trusted-artifact
```

The input file must contain exactly the 16 named finite numeric vector fields. It
has not been created. Current CLI invocation reports model unavailable before
attempting to read input. No successful real prediction can be demonstrated yet.

## Actual checks

- Root suite: 8 passed.
- ML suite: 10 passed, 7 existing placeholders skipped (5 new inference-contract tests).
- Static scaffold validation passed: 105 Python files parsed.
- Prediction CLI executed against the absent bundle: explicit model-unavailable error.
- Tests of successful loading/prediction used mocks only; no real estimator fitted.

## Next steps for the existing backend

1. Confirm dataset authorization for this exploratory use. Implement an explicit
   exploratory runner separate from the final-study gate, with a fixed stratified
   split, training-only preprocessing and class weighting. Compare Logistic Regression
   and Random Forest only after dependencies are available/approved. Report small-N,
   imbalance, source confounding and unverified upstream-vector leakage limitations.
2. Save the real preprocessing-plus-estimator bundle and metadata to the planned
   directory; run actual save/load equivalence and recorded-label prediction tests.
3. In existing `backend/app/services/model_service.py`, load the trusted bundle once
   at application startup. Keep readiness false and prediction unavailable if absent.
4. In existing `backend/app/services/prediction_service.py`, call `predict_record`;
   validate exactly 16 numeric inputs, return literal predicted_label/model_version/
   notice, and map input errors to 422 and model-unavailable errors to 503.
5. Integrate with the existing router/schema modules and add real API integration
   tests. Do not use source, risk_oof, IDs or label as inputs; do not log record contents.

For tomorrow, the honest available demonstration is the data audit, feature-input
validation and explicit unavailable-model behavior—not a trained risk predictor.
