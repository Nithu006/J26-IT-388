# Behavioral Analytics & Temporal Learning — J26-IT-388
Nithursanan S (IT23222090). Extracts posting-behaviour features, builds time windows, learns temporal patterns with an LSTM,
compares withh5 non-temporal baselines, and outputs a 16-dim behaviour vector + risk signal for the Fusion module.

## Run on your Mac / laptop (no TensorFlow needed)
```..s
pip install numpy pandas scikit-learn          # one time
cd behavior_system
python run.py train --users users_annonym.csv --timelines timelines_annonym.csv     # ~2-5 min
python run.py serve                                                                  # opens http://127.0.0.1:8000
```
Add more datasets (merged into one training set, results also reported per dataset):
```
python run.py train --users users_annonym.csv --timelines timelines_annonym.csv \
    --stmhd ~/Downloads/data_sample --reddit ~/Desktop/ic_small.csv [--reddit-max-users 100]
# full STMHD dump (300 depression + 300 neg users, 20-60 tweets each):
python run.py train --users users_annonym.csv --timelines timelines_annonym.csv --art artifacts_stmhd \
    --stmhd-pos ~/Downloads/media-2/data_dump/udit/submission/dataset/depression/cleaned_data_depression \
    --stmhd-neg ~/Downloads/media-3/data_dump/udit/submission/dataset/neg/cleaned_data_neg [--stmhd-per-class 300]
```
- `--stmhd`: Twitter-STMHD folder (`<disorder>/<pre|post>covid/<id>/tweets.json`, `neg/<id>/tweets.json`); label 1 = any disorder, 0 = neg
- `--reddit`: Reddit identity-claim CSV (`user, created_utc`); all users label 1, no text, sampled to `--reddit-max-users`
- A "Source-only" baseline checks whether models just learn which dataset a user came from. Per-dataset results go in `artifacts/results_by_source.csv`.

Software test with fake data (NEVER present as results): `python run.py train --synthetic`
Quick check: `python tests/test_smoke.py`

## UI tabs
Overview (pipeline) · Cohort Explorer (per-user risk, behaviour over time) · Analyse New Timeline (paste CSV) · Model Results (table + limitations)

## Files
- `behavior_system/loaders.py` per-dataset loaders · `data.py` cleaning, windows, features · `nplstm.py` NumPy LSTM (gradient-checked) · `pipeline.py` repeated CV + final model + export
- `predict.py` scoring new timelines · `server.py` + `ui.html` web UI · `models.py` optional Keras LSTM/Transformer (needs TensorFlow, e.g. Colab)
- Outputs in `artifacts/`: `results_table_repeated.csv`, `behavior_vectors.csv` (for Kaveeja), `behavior_lstm.npz`, `meta.json`

## Honest limitations
Small labelled sample, dataset-provided labels (not clinical), night ratio relative (mixed UTC offsets), mentions/length are engagement proxies,
demo thresholds (0.40 / 0.65) illustrative. Research prototype — not a diagnosis tool.
