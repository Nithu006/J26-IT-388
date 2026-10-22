
# J26-IT-388 — Component 4
## Explainable AI & Adaptive Decision Support

**Research Project:** Real-Time Explainable AI-Based Mental Health Risk Prediction Using Social Media  
**Research Stage:** PP1 — Proof of Concept  
**Component:** Component 4 — Explainable AI & Adaptive Decision Support  
**Institution:** Sri Lanka Institute of Information Technology (SLIIT)

---

## 1. Project Overview

The overall research project aims to develop an AI-based system for analyzing social media information to support mental-health-related risk prediction and decision-making.

The research consists of four interconnected components:

| Component | Responsibility |
|---|---|
| Component 1 | Social Media Text Analysis using NLP |
| Component 2 | Behavioral and Temporal Analysis |
| Component 3 | Multimodal Prediction and Risk Estimation |
| Component 4 | Explainable AI, Adaptive Scoring and Decision Support |

### Component 4 Overview

Component 4 focuses on making AI predictions more understandable and providing transparent decision-support information.

The main objectives are:

1. Explain AI predictions using SHAP and LIME.
2. Identify features influencing model predictions.
3. Develop an experimental adaptive scoring mechanism.
4. Generate traceable, rule-based recommendations.
5. Handle uncertain predictions and missing observations.
6. Provide an interactive interface for reviewing results.

**Important:** This is a research prototype, not a clinical mental-health diagnosis or emergency alert system.

---

## 2. PP1 Implementation Scope

The final Component 4 is intended to integrate with the multimodal prediction outputs developed by Component 3.

However, the final Component 3 model was not available during the initial PP1 implementation.

Therefore, a provisional stress-related text classifier was developed using the Dreaddit dataset.

This allowed the explainability and decision-support pipeline to be implemented, tested and demonstrated independently.

### Completed PP1 Work

- Dataset validation and exploratory data analysis
- Provisional text-classification model development
- SHAP global and local explanations
- LIME local explanations
- SHAP and LIME evaluation and comparison
- Experimental adaptive temporal scoring
- Missing-data and uncertainty safeguards
- Rule-based recommendation engine
- FastAPI backend integration
- Interactive Streamlit dashboard
- Automated software testing
- Reproducible experimental reports and visualizations

The provisional classifier does not replace the final Component 3 multimodal model.

---

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.12 | Main programming language |
| Pandas and NumPy | Data processing and analysis |
| Scikit-learn | Machine-learning model development |
| TF-IDF | Text feature extraction |
| Logistic Regression | Binary text classification |
| SHAP | Model feature attribution |
| LIME | Local model explanation |
| FastAPI | Backend REST API |
| Pydantic | Request and response validation |
| Streamlit | Interactive research dashboard |
| Altair and Matplotlib | Data visualization |
| Pytest | Automated testing |
| Joblib | Trained model serialization |

The saved classifier was trained using **scikit-learn 1.9.1**. The compatible version is recorded in the project requirements.

---

## 4. Dataset

### Dreaddit Dataset

The PP1 prototype uses Dreaddit, a publicly available research dataset containing Reddit posts annotated for stress-related text classification.

The original dataset is used for binary classification:

- **Class 0:** Non-stress-related text
- **Class 1:** Stress-related text

### Dataset Statistics

| Dataset | Records |
|---|---:|
| Training | 2,838 |
| Testing | 715 |
| Total | 3,553 |

The main fields used for model development were:

- `text` — Social media text content
- `label` — Binary stress-related classification label

### Dataset Files

```text
data/
├── raw/
│   └── dreaddit/
│       ├── dreaddit-train.csv
│       └── dreaddit-test.csv
├── processed/
└── synthetic/
```

### Dataset Validation

The dataset was examined for:

- Missing values
- Class distribution
- Duplicate text
- Train/test overlap
- Conflicting labels
- Text-length distribution
- Subreddit distribution

The audit identified some duplicated and overlapping texts and labeling inconsistencies.

These issues are documented as data-quality limitations.

**Dataset limitation:** Dreaddit provides stress-related text labels. It does not provide clinically verified mental-health diagnoses or genuine longitudinal histories of individual users.

---

## 5. Research Notebooks

The implementation process was divided into five notebooks for reproducibility and easier evaluation.

### Notebook 01 — Dataset Validation

**File:** `notebooks/01_dataset_validation.ipynb`

Activities:

- Loaded the Dreaddit training and testing datasets.
- Examined dataset structure and label distribution.
- Checked missing values and duplicated records.
- Investigated train/test text overlap.
- Generated exploratory analysis charts.
- Saved data-quality reports.

**Output:** Dataset validation evidence and exploratory figures.

### Notebook 02 — Provisional ML Baseline

**File:** `notebooks/02_provisional_baseline.ipynb`

Activities:

- Prepared text and binary labels.
- Applied TF-IDF feature extraction.
- Trained a Logistic Regression classifier.
- Compared against a DummyClassifier baseline.
- Performed grouped cross-validation.
- Evaluated predictions on the held-out test dataset.
- Performed duplicate-sensitivity checks.
- Saved the trained model.

**Saved model:**

`models/dreaddit_tfidf_logreg.joblib`

### Notebook 03 — SHAP Explainability

**File:** `notebooks/03_shap_explainability.ipynb`

Activities:

- Loaded the frozen classifier.
- Created a training-data background reference.
- Applied SHAP LinearExplainer.
- Generated global and local feature explanations.
- Analyzed correctly and incorrectly classified examples.
- Verified SHAP additivity.
- Investigated explanation stability and background sensitivity.

SHAP feature contributions are expressed in **class-1 log-odds**.

### Notebook 04 — LIME Explainability

**File:** `notebooks/04_lime_explanations.ipynb`

Activities:

- Loaded the same frozen classifier.
- Applied LIME Text Explainer.
- Used 1,000 perturbations per explanation.
- Generated local feature-contribution plots.
- Evaluated local surrogate fidelity.
- Tested explanation stability.
- Compared selected explanation features with SHAP.
- Recorded explanation execution time.

LIME feature weights approximate the behavior of a local surrogate operating on the classifier's probability outputs.

SHAP and LIME values should not be compared directly as equivalent numerical quantities.

### Notebook 05 — Adaptive Scoring

**File:** `notebooks/05_adaptive_risk_scoring.ipynb`

Activities:

- Implemented Exponential Moving Average (EMA) scoring.
- Created explicitly synthetic temporal scenarios.
- Compared static and adaptive scores.
- Evaluated different EMA smoothing parameters.
- Tested missing-data handling.
- Verified deterministic behavior.
- Generated scoring charts and validation reports.

The temporal sequences are fictional demonstrations, not actual individual social media histories.

---

## 6. Model Training and Evaluation

### Model Architecture

The provisional model uses:

**Text Input → TF-IDF Vectorizer → Logistic Regression → Binary Prediction**

The trained model is stored as a Scikit-learn Pipeline.

### Held-Out Test Results

| Metric | Result |
|---|---:|
| Accuracy | 71.61% |
| Macro-F1 | 0.7132 |
| Stress-related class recall | 79.13% |
| ROC-AUC | 0.8162 |

These results were obtained from the Dreaddit held-out test dataset.

### Understanding the Output

The model returns:

- Predicted class: 0 or 1
- Class-1 probability: a value between 0 and 1

For example:

```json
{
  "predicted_class": 1,
  "probability_stress": 0.6175,
  "model_type": "TF-IDF + Logistic Regression",
  "is_clinical_assessment": false
}
```

The probability indicates the model's estimated probability for the stress-related text label.

It does **not** represent a clinically validated probability of a person's mental-health condition.

---

## 7. Explainable AI

### SHAP

SHAP is used to identify how individual model features contribute toward or away from the stress-related text prediction.

The PP1 experiments included:

- Global feature-importance analysis
- Local explanations
- Mathematical reconstruction checks
- Background-sensitivity evaluation
- Explanation runtime analysis

For the verified API demonstration, the SHAP reconstruction error was approximately zero.

### LIME

LIME generates perturbed versions of the input text and fits a local surrogate model to approximate the classifier's behavior near the selected prediction.

#### LIME Experimental Results

| Metric | Result |
|---|---:|
| Mean local surrogate R² | 0.8099 |
| Mean absolute approximation error | 0.0060 |
| Mean top-term Jaccard similarity | 0.8585 |
| Mean sign agreement for shared terms | 100% |

These metrics describe explanation approximation and stability in the tested cases, not clinical accuracy.

### SHAP vs LIME

Both methods were implemented to investigate how different explainability techniques represent the same model prediction.

A key preliminary observation was that SHAP and LIME can highlight different important features, even when their contribution directions agree for shared terms.

The methods use different explanation assumptions and numerical scales.

---

## 8. Adaptive Scoring

An experimental Exponential Moving Average (EMA) mechanism was implemented to demonstrate time-dependent score updating.

### EMA Formula

```text
Adaptive Score =
    0.35 × Current Model Probability
    + 0.65 × Previous Adaptive Score
```

The default EMA parameter is:

`alpha = 0.35`

### Purpose

EMA provides a smoothed representation of an input sequence by combining the latest observation with the previous adaptive score.

This can reduce short-term fluctuations, although it also introduces response delay.

### Synthetic Scenarios

The PP1 evaluation included:

- Increasing scores
- Decreasing scores
- Oscillating scores
- Constant scores
- Missing observations
- Sudden synthetic changes
- Completely unavailable observations

### Results

- 7 synthetic scenarios evaluated
- 63 synthetic observations processed
- 13 validation checks passed
- Missing-data handling verified
- Deterministic behavior verified
- Sensitivity to EMA parameters evaluated

The selected smoothing parameter has not been clinically optimized.

---

## 9. Recommendation and Decision-Support Engine

A transparent, rule-based recommendation engine was developed using the adaptive score, input freshness and a provisional uncertainty safeguard.

### Decision Rules

| Rule ID | Purpose |
|---|---|
| `INFO_001` | Lower-score informational guidance |
| `INFO_002` | Middle-score informational guidance |
| `INFO_003` | Higher-score informational indicator |
| `DATA_001` | Missing or stale data safeguard |
| `UNCERTAIN_001` | Near-boundary prediction safeguard |

### Experimental Settings

- Lower display boundary: `0.35`
- Higher display boundary: `0.65`
- Illustrative uncertainty interval: `0.45–0.55`
- Maximum consecutive missing observations before unavailable state: `2`

These parameters are prototype choices and are not clinical thresholds.

### Decision-Support Evaluation

| Metric | Result |
|---|---:|
| Synthetic scenarios | 7 |
| Observations | 31 |
| Rules exercised | 5/5 |
| Informational attention indicators | 10 |
| Stale-alert violations | 0 |

All outputs are non-diagnostic.

No automatic third-party notifications or medical interventions are implemented.

---

## 10. Project Structure

```text
J26-IT-388/
├── .streamlit/
│   └── config.toml
├── dashboard/
│   └── app.py
├── data/
│   ├── raw/
│   │   └── dreaddit/
│   │       ├── dreaddit-train.csv
│   │       └── dreaddit-test.csv
│   ├── processed/
│   └── synthetic/
├── docs/
├── experiments/
│   ├── figures/
│   ├── metrics/
│   └── generate_decision_support_evidence.py
├── models/
│   └── dreaddit_tfidf_logreg.joblib
├── notebooks/
│   ├── 01_dataset_validation.ipynb
│   ├── 02_provisional_baseline.ipynb
│   ├── 03_shap_explainability.ipynb
│   ├── 04_lime_explanations.ipynb
│   └── 05_adaptive_risk_scoring.ipynb
├── src/
│   ├── adaptive_scoring/
│   │   ├── __init__.py
│   │   └── scorer.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── lime_service.py
│   │   ├── main.py
│   │   ├── model_service.py
│   │   ├── schemas.py
│   │   └── shap_service.py
│   ├── data/
│   ├── explainability/
│   ├── models/
│   ├── recommendations/
│   │   ├── __init__.py
│   │   └── engine.py
│   └── decision_support.py
├── tests/
│   ├── test_api.py
│   └── test_decision_support.py
├── .gitignore
├── requirements.txt
├── requirements-lock.txt
└── README.md
```

### Important Folders

| Folder | Purpose |
|---|---|
| `data/` | Raw, processed and synthetic data |
| `notebooks/` | Research experiments and evaluations |
| `models/` | Frozen trained classifier |
| `experiments/` | Evaluation reports, figures and metrics |
| `src/` | Reusable implementation code |
| `src/api/` | FastAPI endpoints and model/explanation services |
| `src/adaptive_scoring/` | EMA scoring logic |
| `src/recommendations/` | Recommendation rules |
| `tests/` | Automated regression tests |
| `dashboard/` | Interactive Streamlit application |

---

## 11. FastAPI Backend

FastAPI provides five REST endpoints.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | API availability check |
| POST | `/predict` | Frozen text-classifier prediction |
| POST | `/explain/shap` | SHAP local explanation |
| POST | `/explain/lime` | LIME local explanation |
| POST | `/decision-support` | Adaptive scoring and recommendations |

### Important Backend Files

**`src/api/main.py`**  
Defines the FastAPI application and API routes.

**`src/api/schemas.py`**  
Defines validated request and response schemas using Pydantic.

**`src/api/model_service.py`**  
Loads the frozen Joblib classifier and performs text prediction.

**`src/api/shap_service.py`**  
Generates SHAP explanations.

**`src/api/lime_service.py`**  
Generates LIME explanations.

**`src/adaptive_scoring/scorer.py`**  
Implements EMA scoring and missing-data handling.

**`src/recommendations/engine.py`**  
Applies rule-based decision-support logic.

**`src/decision_support.py`**  
Integrates the adaptive scorer and recommendation engine.

---

## 12. Interactive Dashboard

The Streamlit dashboard provides an interactive demonstration of the completed PP1 functionality.

The prototype interface was provisionally branded **MindLens AI** during development. This dashboard name is not the official research project title.

### Dashboard Sections

#### Overview
- Enter or select demonstration text.
- Run frozen-model prediction.
- Display the predicted text label.
- Show the class-1 probability.
- Explain the research workflow.

#### Explainability
- Generate SHAP explanations.
- Generate LIME explanations.
- View positive and negative feature contributions.
- View SHAP reconstruction and LIME fidelity metrics.

#### Adaptive Scoring
- Select a fictional temporal scenario.
- Compare static probabilities against adaptive EMA scores.
- Inspect missing observations and freshness states.
- View generated informational indicator counts.

#### Decision Support
- Display selected rule IDs.
- Show recommendation text and explanation.
- Inspect the sequence decision trace.
- Export a synthetic decision trace to CSV.

The dashboard communicates with the existing FastAPI backend.

---

## 13. Installation and Setup

### Requirements

- Python 3.12
- Windows or a compatible Python environment
- Visual Studio Code (recommended)
- Internet connection for initial dependency installation

### Step 1 — Open the Project

Open the repository root in VS Code.

### Step 2 — Create a Virtual Environment

If a virtual environment does not already exist:

```powershell
python -m venv .venv
```

Activate on Windows:

```powershell
.venv\Scripts\activate
```

### Step 3 — Install Dependencies

Install project requirements:

```powershell
python -m pip install -r requirements.txt
```

Alternatively, for the recorded environment:

```powershell
python -m pip install -r requirements-lock.txt
```

Check dependency compatibility:

```powershell
python -m pip check
```

### Step 4 — Verify the Saved Model

```powershell
python -c "from src.api.model_service import load_model; m=load_model(); print(type(m).__name__, m.classes_)"
```

Expected model type:

`Pipeline`

Expected classes:

`[0 1]`

Only trusted model artifacts should be loaded with Joblib.

---

## 14. Running the Application

Start FastAPI and Streamlit from the repository root in separate terminals.

### Terminal 1 — FastAPI Backend

```powershell
python -m uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000
```

FastAPI documentation:

http://127.0.0.1:8000/docs

Health endpoint:

http://127.0.0.1:8000/health

### Terminal 2 — Streamlit Dashboard

```powershell
python -m streamlit run dashboard/app.py
```

Dashboard URL:

http://localhost:8501

Both processes must remain running for the complete local demonstration.

---

## 15. Automated Testing

The project uses Pytest for backend and integration testing.

### Test Files

**`tests/test_decision_support.py`**

Covers:

- EMA calculations
- Missing-data handling
- Boundary conditions
- Uncertainty safeguards
- Rule selection
- State reset and deterministic behavior

**`tests/test_api.py`**

Covers:

- API health checks
- Prediction requests
- Invalid input validation
- Adaptive scoring endpoint
- Sequence isolation
- SHAP reconstruction
- LIME outputs
- Consistency between explanation and prediction endpoints

### Run All Tests

```powershell
python -m pytest tests/ -q
```

### Last Verified Results

| Test Suite | Passed |
|---|---:|
| Decision-support tests | 30 |
| API tests | 15 |
| **Total** | **45** |

All 45 tests passed in the recorded PP1 verification run.

Four dependency-related deprecation warnings were reported; no test failures occurred.

---

## 16. Recommended PP1 Demonstration Flow

1. Start the FastAPI backend.
2. Start the Streamlit dashboard.
3. Open the Overview tab.
4. Enter the prepared university-stress sample.
5. Show the predicted text label and probability.
6. Open the Explainability tab.
7. Generate SHAP and LIME explanations.
8. Explain important features and contribution directions.
9. Open Adaptive Scoring.
10. Run a fictional increasing-score scenario.
11. Compare the static and adaptive score trends.
12. Open Decision Support.
13. Explain the rule ID, recommendation and trace.
14. Demonstrate the missing-data safeguard.
15. Show the automated test results and research figures.

---

## 17. Research Limitations

The current PP1 implementation has several important limitations.

### Provisional Prediction Model

The classifier was developed for independent Component 4 experimentation.

The final Component 3 multimodal predictor has not yet been integrated.

### Dataset Limitations

Dreaddit provides stress-related text labels, not verified clinical mental-health outcomes.

### Language Coverage

The provisional baseline primarily supports the language characteristics represented in Dreaddit. Multilingual performance has not been established.

### Classification Errors

The classifier has imperfect accuracy and can produce false positives and false negatives.

### Explainability Limitations

SHAP and LIME explain model behavior but do not establish psychological causation or guarantee that explanations are meaningful to human users.

### Synthetic Temporal Data

Adaptive scoring was evaluated using fictional temporal sequences rather than genuine per-person longitudinal data.

### Experimental Thresholds

EMA alpha, score bands and uncertainty intervals were selected for demonstration and have not been clinically validated or optimized.

### Clinical Validation

The system has not undergone clinical validation, clinician review, or real-world longitudinal evaluation.

### Performance Evaluation

Local execution benchmarks were collected, but production-scale performance and end-to-end deployment latency have not been established.

### Integration Limitations

The four research components have not yet been fully integrated into the final proposed group architecture.

---

## 18. Future Work

The next stages of the research should focus on:

1. Integrating the final Component 3 multimodal prediction model.
2. Aligning component input/output interfaces.
3. Evaluating explanations for the integrated model.
4. Investigating real longitudinal data where ethically and legally appropriate.
5. Improving uncertainty handling and probability calibration.
6. Validating multilingual and domain-generalization performance.
7. Conducting user-centered explanation evaluation.
8. Investigating clinically appropriate thresholds only with relevant expert oversight.
9. Extending robustness, security, privacy and integration testing.
10. Evaluating the complete system against the final research objectives.

---

## 19. PP1 Development Summary

Component 4 successfully produced a working research prototype containing:

- A validated Dreaddit dataset workflow
- A trained and frozen text-classification baseline
- SHAP model explanations
- LIME local explanations
- Explanation fidelity and stability experiments
- EMA-based adaptive scoring
- Missing-data safeguards
- Five transparent recommendation rules
- Five FastAPI endpoints
- An interactive Streamlit dashboard
- Forty-five passing automated software tests
- Reproducible experimental metrics and figures

The completed prototype demonstrates the technical feasibility of explainability and adaptive decision-support mechanisms within the limited PP1 scope.

The final research system will require integration with the upstream group components and further empirical validation.

---

## Disclaimer

**This project is intended for academic research and demonstration only.**

The provisional model classifies stress-related text labels. Its outputs must not be interpreted as medical diagnoses, clinically calibrated mental-health risk probabilities, or emergency assessments.

Adaptive timelines and recommendation thresholds used during PP1 are experimental and should not be used for real-world clinical decision-making.
