# Notebook 02 — PP1 model evidence

- Task: binary **stress-related text** classification using Dreaddit (NOT clinical risk diagnosis).
- Model: fixed TF-IDF + Logistic Regression, compared with DummyClassifier.
- Data: original train/test split; training-only 5-fold `StratifiedGroupKFold` using `post_id`.
- Metrics: original held-out test once; contamination-excluded metrics and training dedup sensitivity reported separately.
- Outputs: CSV/JSON metrics, PNG figures and local-only saved pipeline.
- Restrictions: do not retune using original test labels; do not treat Reddit stress as mental-health diagnosis.
