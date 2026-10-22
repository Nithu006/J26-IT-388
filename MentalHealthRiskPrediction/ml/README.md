# ML tools and scaffolding

No model has been trained for this component. There is no fitted bundle or measured
research performance in this checkout. The original vector dataset is intentionally
excluded; audit commands need a separately authorized local file.

## Implemented tools

- The standard-library audit in `training/` at the component root reads a reviewed
  private configuration and reports aggregate quality checks.
- `scripts/check_dataset.py` and `data/validate_data.py` audit the reviewed vector
  schema with pandas. They do not verify label meaning or permission.
- `scripts/run_training.py` calls a readiness check. It always reports NO-GO after a
  valid audit and never fits a model. An absent CSV causes an input error, not training.
- `inference/prediction_pipeline.py` validates exactly 16 finite numeric inputs,
  excludes non-vector fields when selecting candidates, and checks trust, metadata
  and checksum before loading a joblib bundle. It contains a future recorded-label
  prediction interface; no real fitted artifact has been tested with it.
- The prediction CLI reports model unavailable when a usable trusted bundle is absent.

## Not implemented or approved

Splitting, learned preprocessing, Transformer embeddings, behavior interpretation,
fusion, classifier training, tuning, research evaluation and explainability remain
scaffolding. YAML files are proposed configuration, not an implemented configuration
loader. ML dependency packaging is incomplete; `requirements.txt` does not currently
install the dependencies needed for vector auditing or future model fitting.

The 0/1 tokens have no verified clinical interpretation. The bvec dimensions are
candidate vectors with unverified provenance, not established raw behavioral measures.
`participant_id`, `source`, `label` and `risk_oof` are excluded from candidate inputs.
Permission, upstream leakage, target definitions, split design and architecture still
need review. See [training gates](../docs/model_training.md),
[decisions](../docs/open_questions.md) and
[research readiness](../docs/research_readiness_next_steps.md).

## Software checks

From the component directory, with the required dependencies available:

```powershell
python -m unittest discover -s ml/tests -v
```

The suite defines ten active audit/readiness/inference tests and seven skipped
placeholders. Some active tests require pandas; successful artifact loading is tested
with mocks. These checks do not establish real model training, performance or a
serialization round trip for a fitted estimator. This documentation update does not
claim a new ML test run.
