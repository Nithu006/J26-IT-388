# Requirements summary

The guide cited below was reviewed in the original workspace and is not distributed
in this checkout; publication suitability remains unverified.

Reviewed 2026-10-20: all 13 pages of
`Hybrid_Mental_Health_Risk_Prediction_Engineer_Guide.pdf`.
The supplied guide is the primary source; its referenced TAF was not supplied separately.
The workspace originally contained only that PDF, with no code, dataset or AGENTS.md.

## Objective and ownership

Build a reproducible research decision-support prototype using authorized social-media
text and behavioral signals. Project J26-IT-388; assigned component: Multimodal AI Fusion
& Risk Prediction (guide pp. 1–2, 13).

The individual owns text/behavior fusion, prediction architecture, training and
optimization, ML/DL comparisons, evaluation, model packaging, and API/React integration.
Dataset audit, leakage prevention, reproducibility and handover support those duties.
The guide does not identify other members by name. Main sentiment/emotion model
development and SHAP/LIME engine implementation are outside this component if assigned
to teammates; agree interfaces instead (pp. 2–3, 8–9).

## Requirement traceability

| Source pages | Requirement | Planned evidence |
| --- | --- | --- |
| 1–3, 12–13 | Confirm hybrid definition, data and labels; no diagnosis | Decision register; visible research notice |
| 4–5 | Audit source, permissions, schema, language, duplicates and labels | Config, audit JSON, data dictionary, manual review |
| 5–6 | Group/time-aware splits; training-only preprocessing; aligned vectors | Saved split manifest and leakage/preprocessing tests |
| 3, 6 | Proposed frozen Transformer + numeric behavior + XGBoost | Approved architecture and reproducible training code |
| 7 | Text-only, behavior-only, hybrid and simple baseline comparisons | Same split; actual metric reports and error analysis |
| 7 | Persist encoder revision, feature order, labels and transforms | Versioned trusted model bundle |
| 8 | Validated API; startup loading; safe operational logging | Health/model-info/predict contracts and tests |
| 8–9 | React validation, loading/error/result states | Integration tests and demo |
| 9–10 | Authorized access, data minimization and responsible use | Privacy decisions and deployment controls |
| 10–12 | Testing and repeatable handover | Executed checks, setup guide and limitations |

## Fixed versus proposed

Fixed: assigned responsibilities, multimodal fusion, honest experiments, ethical data
handling, consistent preprocessing and reproducibility.
Proposed: frozen Transformer plus XGBoost; Logistic Regression/Random Forest comparison;
Python/FastAPI/React; local CSV/Parquet artifacts. Exact encoder, label classes, feature
names, database and deployment design are not approved choices. The example English
MiniLM encoder and behavioral columns in the guide are not dataset facts.

## Dependencies, risks and limits

Training depends on an authorized labeled dataset with actual behavioral measurements,
documented language, observation windows and leakage-safe split design.
Supervisor approval must clarify whether the proposed hybrid satisfies the viva feedback.
Possible risks include proxy/invalid labels, repeated-user leakage, future-derived
features, language mismatch, imbalance and misleading interpretation (p. 12).
No performance superiority, real-time latency or clinical validity is established.

Additional engineering recommendations, not source requirements: use a standard-library
CSV audit first to avoid unnecessary dependencies; make configuration incomplete by
default; output aggregate findings without record previews; keep a separate manual
approval checklist because a data-quality scan cannot verify consent or ethics.
