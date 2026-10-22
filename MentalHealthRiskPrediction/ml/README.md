# ml

Update 2026-10-21: vector auditing and a fail-closed training preflight are now
implemented. See [training preparation](../docs/model_training.md). No model fitting
is available; historical scaffold descriptions below apply to the remaining modules.

Purpose: reserved location for ml.
Status: starter structure only; implementation and contracts await review.
No real data, trained model, results, authentication or persistence is provided.
Research use only; not a clinical diagnostic system.

`src/mental_health_ml/` reserves data, preprocessing, features, models, training,
evaluation, explainability and inference modules. None train or predict yet.
Use the existing `python -m training.inspect_data` from the repository root for
actual audits. Its canonical configuration remains `config/dataset.example.json`.

The YAML files reserve model configuration and reference the existing data contract.
No YAML loader or duplicate dataset schema is implemented. After review, define
packaging, compatible pinned dependencies and API/shared inference contracts.
`python -m unittest discover -s ml/tests -v` reports seven intentional skips.
