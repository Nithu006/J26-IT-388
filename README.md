# J26-IT-388
Real -Time Explainable AI-Based Mental Health Risk Predic?on Using Social Media
# Behavioral Analytics & Temporal Learning

**Project J26-IT-388: Real-Time Explainable AI-Based Mental Health Risk Prediction Using Social Media**
Component owner: Nithursanan S (IT23222090), SLIIT B.Sc. (Hons) in Information Technology

This component turns a user's posting timeline into behaviour features, learns temporal patterns with an LSTM, compares it with non-temporal baselines, and outputs a **16-number behaviour vector and a risk score** for the multimodal fusion module. A web dashboard shows the results.

> Research prototype. It produces a risk *signal*, not a diagnosis. Labels come from the datasets (self-reported or dataset-provided), not from clinicians.

## How it works

1. **Posts**: a user timeline (timestamp and text). Users need at least 20 posts; the first 60 are used.
2. **Windows**: posts are grouped into windows of 5 consecutive posts, in time order (up to 12 windows per user).
3. **Features** (5 per window): average gap between posts (log hours), gap variability, night-time ratio (00:00 to 04:59), average post length, mentions per post.
4. **Models**: Logistic Regression and Random Forest (per-user averages, non-temporal) versus an LSTM (16 hidden units) that reads the windows in order.
5. **Output**: risk score (0 to 1) and the 16-dimensional LSTM state as the behaviour vector.

Evaluation is **user-level** 5-fold cross-validation repeated 5 times, with the scaler fitted on training users only, so no user appears in both train and test.

## Requirements

- Python 3.9+
- `pip install numpy pandas scikit-learn`

TensorFlow is not needed. The LSTM is implemented in NumPy (`behavior_system/nplstm.py`, gradient-checked). `behavior_system/models.py` holds optional Keras LSTM and Transformer models for use in Colab.

## Quick start

```
cd behavior_system
python3 run.py train --users users_annonym.csv --timelines timelines_annonym.csv
python3 run.py serve
```

Then open http://127.0.0.1:8000. To use a specific trained model folder:

```
python3 run.py serve --art artifacts_thai_only --port 8000
```

Run `python3 run.py train --help` for all options, including the Twitter-STMHD sampling options. Test the software with fake data only: `python3 run.py train --synthetic` (never report those numbers). Smoke test: `python3 tests/test_smoke.py`.

### Input format

- `timelines_annonym.csv`: `participant_id`, `created_date`, `anonymised_text`
- `users_annonym.csv`: `participant_id`, `depression` (0 or 1), optionally `anxiety`

## Dashboard

| Tab | What it shows |
|---|---|
| Overview | Pipeline and dataset numbers |
| Cohort Explorer | Per-user risk (out-of-fold) and behaviour over time |
| Analyse New Timeline | Paste timestamps (CSV), get a live risk score, feature deviations and the behaviour vector |
| Model Results | Baselines versus LSTM, and the limitations |

The dashboard uses plain HTML, CSS, JavaScript (inline SVG charts) and Python's built-in web server. No internet is needed to run it.

## Project structure

```
run.py                     train / serve commands
behavior_system/
  data.py                  cleaning, windows, features
  nplstm.py                NumPy LSTM
  models.py                baselines and optional Keras models
  pipeline.py              repeated CV, final model, export
  predict.py               score a new timeline
  server.py, ui.html       web dashboard
  loaders.py               dataset loaders
  synthetic.py             fake data for software tests only
tests/test_smoke.py
artifacts*/                trained models and results (not committed)
```

Outputs per trained model folder: `behavior_lstm.npz` (weights), `behavior_vectors.csv` (vectors for the fusion module), `results_table_repeated.csv`, `meta.json`.

## Preliminary results (ROC-AUC, user-level CV)

| Dataset | Logistic Regression | Random Forest | LSTM |
|---|---|---|---|
| Thai corpus (48 users) | 0.713 | 0.748 | 0.760 |
| Twitter-STMHD (2,000 users, balanced) | 0.663 | 0.668 | 0.635 |

The Thai spread across folds is about ±0.11, so its LSTM lead may be luck. On the larger, more reliable Twitter-STMHD data, the simple models are slightly ahead. Behaviour features alone carry a modest signal (AUC about 0.65). Merging datasets was tested and dropped: Thai performance fell and overall scores were inflated by the dataset source.

## Limitations

- Small labelled samples; results are preliminary.
- Labels are dataset-provided, not clinical.
- Timestamps carry mixed UTC offsets, so night ratio is relative.
- No likes or replies in the data; post length and mentions are proxies.
- Trained on Twitter data; not validated on other platforms.
- Dashboard risk thresholds (0.40 and 0.65) are illustrative.
- Datasets are not included in this repository; obtain them from their original sources and follow their licences.

## Next steps

Transformer comparison, richer features (engagement, time zones), integration with the fusion module, validation on more datasets and platforms.
