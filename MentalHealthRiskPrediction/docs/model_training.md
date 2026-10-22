# Training preparation and execution gates — 2026-10-21

Latest exploratory-demo request: dataset authorization remains unresolved, so no
fitting occurred. The input/artifact interface is now prepared; see
[demo status and backend handoff](exploratory_demo_status.md). Original final-study
gates and historical test results below are retained.

Status: **NO-GO**. No approved fitting command exists. The current training entry
point performs only an audit and readiness check, always stopping before fitting.
It is not a completed baseline-training pipeline and has no override/pilot flag.

## Executable preparation

From the component directory (`MentalHealthRiskPrediction/`) with pandas available
and an independently authorized local dataset (the CSV is excluded from Git):

```powershell
python ml/scripts/check_dataset.py --dataset dataset/raw/behavior_vectors.csv
python ml/scripts/run_training.py --dataset dataset/raw/behavior_vectors.csv
```

Both print aggregate audit and readiness JSON. Exit 1 means NO-GO; exit 2 means
input/schema/access failure. Neither writes a model, creates splits or alters the
dataset. The schema deliberately matches this reviewed CSV; unknown categories
are counted without printing their values. This is not a general dataset loader.
The existing text-oriented `training/inspect_data.py` remains unchanged and should
not be used by inventing a text column for this vector-only dataset.

Historical environment: the original audit used pandas 3.0.1; scikit-learn and
XGBoost were unavailable in that runtime. That environment is not bundled with
this checkout. Use an approved Python environment for the commands above; package
installation remains a separate approved step. No fitting command is approved.

## Workflow to implement after approval (not executed)

1. Freeze a hash/versioned, authorized dataset and approved label dictionary.
   Verify at least 1,000 eligible records for final training. Establish whether the
   minimum counts records, distinct participants or another unit with the supervisor.
2. Approve vector provenance and ensure upstream learned embeddings/transforms were
   fitted without validation/test information. If not, regenerate from raw permitted
   signals within training folds; a downstream split alone is insufficient.
3. Use seed 42 consistently. Group by verified participant identity; determine
   whether future-time prediction also requires chronological boundaries/purge gaps.
   Stratify only when class/group counts make it feasible. Do not silently fall back
   to a row-random split when group stratification fails. Save split identifiers in
   restricted artifacts and verify disjoint groups, duplicate content and time bounds.
4. Hold out final test rows before learned preprocessing, tuning or feature selection.
   Use training/validation or training-only grouped cross-validation for selection.
   Source-specific analysis is necessary given the observed source/label association;
   a single-class source subset cannot provide ROC-AUC for both classes.
5. Use an explicitly approved feature allowlist. IDs are grouping metadata; source is
   audit metadata; label is the target. Exclude `risk_oof`. The 16 bvec columns remain
   candidates only, not approved features. No raw-text data is fabricated.
6. Fit imputation on training rows only, reject all-missing/uninterpretable features,
   and fit scaling on training rows for Logistic Regression. Keep transformation and
   model in one shared pipeline. Compare Logistic Regression and Random Forest on
   identical eligible splits; XGBoost requires an available/approved installation.
   Evaluate class weighting using training labels only; any resampling belongs inside
   each training fold, never before splitting or on validation/test data.
7. Choose using validation results, freeze configuration, then evaluate final test
   once. Report accuracy, per-class precision/recall/F1, macro-F1, confusion matrix
   and class supports. State undefined precision/recall cases and the chosen zero-
   division convention. Compute ROC-AUC only with both classes, suitable continuous
   scores and an approved positive-class definition; otherwise report unavailable
   with a reason. Do not assume token 1 is the clinically positive class.
8. Save the actual baseline comparison, limitations, training configuration, feature
   order, transforms, class mapping and dependency versions. Record model size and
   encoding/inference latency if making a real-time claim. No metric table is filled
   until legitimate training/evaluation occurs.
9. Text-only and hybrid comparisons additionally require approved raw text paired to
   each behavioral record/window and a language-appropriate frozen encoder. Current
   CSV-only preparation cannot establish either experiment or a behavioral interpretation.

## Actual validation

- Root audit tests: 8 passed (existing tests unchanged).
- ML discovery: 5 new audit/readiness tests passed; 7 original placeholders skipped.
- Static scaffold validation: passed, 104 Python sources parsed.
- Real CSV preflight executed: exit 1, explicit NO-GO, no model fitted.
- Input hash matched the initial audit after preflight.

Tests use clearly synthetic in-memory software fixtures for grouping, category privacy,
invalid numerics, schema rejection, deterministic auditing and the 1,000-record gate.
Even 1,000 rows still yields NO-GO while provenance and approvals are unresolved.
No classifier, split, preprocessing or metric runtime validation is claimed.

Inspected: current readiness/audit/design/architecture/decision documents, data
dictionary, existing audit code/tests/configuration, ML package/configuration and
training/evaluation stubs, backend model service, CSV and surrounding dataset files.
Changed: `data/validate_data.py` and `training/train.py` under `ml/src/mental_health_ml/`,
`ml/scripts/check_dataset.py`, `ml/scripts/run_training.py`; added
`ml/tests/test_training_readiness.py`. Documentation updates preserve historical
findings. Root audit code/tests/config, original CSV, PDF and backend are unchanged.
