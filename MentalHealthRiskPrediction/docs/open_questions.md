# Decision register

**2026-10-22 authorization check:** no actual source URL, applicable license or
written permission for this derived CSV was found. Supply that evidence plus any
required supervisor/university approval for exploratory fitting. No authorization
reference has been invented. The local UI/API demo works without training;
see [local demo guide](local_demo.md).

Current update (2026-10-21): `dataset/raw/behavior_vectors.csv` is now present;
D1's file-location question is resolved, but use permissions/provenance remain open.
Final training is NO-GO: 220 records versus the user-reported supervisor minimum 1,000.

All decisions below are unanswered as of 2026-10-20. Record the answer, owner,
supporting reference and approval date here when available.

| ID | Decision / evidence needed | Blocks |
| --- | --- | --- |
| D1 | Exact dataset/file, source, license/terms, permitted research use and ethics approval/reference | Real-data processing and training |
| D2 | Actual target column, class meanings, annotation/proxy/self-report provenance and label timing | Supervised learning and output semantics |
| D3 | Text column, unit of prediction, language(s), Sinhala/code-mixed coverage | Text preprocessing and encoder selection |
| D4 | Available numeric behavior columns, formulas, units, missingness policy and valid ranges | Feature contract and frontend inputs |
| D5 | Observation window, timezone, prediction cutoff/horizon and feature availability time | Temporal leakage prevention |
| D6 | Pseudonymous user/group key, repeated users and chronology; approved split method | Evaluation validity |
| D7 | Does Transformer + XGBoost satisfy supervisor's hybrid requirement? Is a neural comparison mandatory? | Final architecture and experiment scope |
| D8 | Who owns upstream NLP and explanations? Interface/schema and availability? | Optional teammate integration |
| D9 | Is persistence required? Approved storage, access, retention/deletion and backups? | Optional database |
| D10 | Local demo or hosted deployment, access controls and latency target/hardware? | Deployment and real-time claim |

D1–D7 must be resolved before final training. D8–D10 need not prevent a local
model experiment once its own gates are met. No database or explainability service
is assumed. The PDF explicitly calls these implementation gates (pp. 12–13).

## Scaffold review decisions added 2026-10-20

- D11: Choose whether future data lives in `data/` or `dataset/`, and model bundles
  in `models/` or `ml/artifacts/`. Both existing and requested locations remain;
  no data or artifacts were moved.
- D12: Review the structure before pinning/installing ML, FastAPI, React/Vite and
  test dependencies. Empty dependency declarations are intentional at this stage.
- D13: Confirm whether new package modules will wrap or later absorb the existing
  audit implementation. Existing imports and configuration remain authoritative.
- D14: Confirm the explanation teammate's ownership before implementing SHAP/LIME;
  the new explainability files reserve interfaces only.

## Dataset readiness refinements — 2026-10-20

Inspection found no dataset in `data/` or `dataset/`; all existing decisions remain
unresolved. These questions refine D1–D7 rather than approve new assumptions:

- D1/D4: Does the chosen authorized dataset pair text with actual behavior for the
  same records/users and observation window? If it is text-only, what approved
  source or revised research scope supplies the behavioral modality?
- D2/D5: Are targets post-level, user-level or window-level, and when were they
  assigned relative to prediction time? Are they mutually exclusive categories?
  Who assigned them and what evidence supports their interpretation?
- D3: Which languages and code-mixing patterns need coverage, and what evaluation
  will support selecting a frozen encoder? No encoder ID/revision is configured.
- D4/D5: Which timestamps and event definitions establish that every behavioral
  feature is available at prediction time? How are overlapping windows handled?
- D6: Is the goal generalization to unseen users, future observations of known users,
  or both? Which group/time holdout design and duplicate exclusions match that goal?
- D6/D7: After audit, are there enough independent groups and observations per class
  for the agreed comparisons? Define the evaluation/uncertainty plan based on actual
  counts rather than inventing a minimum sample size or split percentage now.
- D7: Does Transformer + XGBoost satisfy the supervisor's hybrid requirement, and
  is an additional neural-model comparison required?

Before configuring the audit, the data custodian must also confirm that mapped
label/language values are safe categorical fields: the report includes their values
and counts. If labels are absent, approve an exploratory-audit extension rather than
assigning a fabricated label column.

See [readiness assessment](data_readiness_assessment.md). No training, data acquisition
or implementation was authorized by the completion of this assessment.

## Vector dataset decisions — 2026-10-21

- D15: Supply the signed/dated minimum-size requirement and clarify its counting unit.
  Current file is short by 780 records. No documented pilot exception was found;
  any exception must explicitly authorize an exploratory study, never final-study claims.
- D16: Provide the meaning of `label=0` and `label=1`, annotation process, timing,
  positive-class interpretation and evidence that source datasets use compatible labels.
- D17: Provide `bvec_0`–`bvec_15` generator code/version, raw inputs, dimension meaning,
  fitted population, label use, normalization and observation windows. Can vectors be
  regenerated within leakage-safe training folds when necessary?
- D18: Explain `risk_oof` origin and fold construction, group separation, upstream
  fitting, prediction-time availability and independent test handling. It remains
  excluded; its name does not establish leakage safety.
- D19: Explain collection provenance and the source tokens, including `thai`. Why
  are all 100 reddit records labeled 1? Agree a source-confounding/generalization check.
- D20: Confirm that participant IDs identify distinct people across sources and files;
  provide any permitted linkage and timestamps required for group/time validation.
- D21: Supply authorized raw text paired to the same participant/window for text-only
  and hybrid comparison, or obtain a documented scope change. No fake text is allowed.

See [current audit](data_audit_report.md) and [training preparation](model_training.md).

## Exploratory demonstration request — 2026-10-21

The user now requests a conditional exploratory classifier for the recorded 0/1
tokens without assuming clinical meaning. No dataset-use authorization was supplied
or found; `authorization_reference` remains null. Confirm the right to use this
specific CSV for exploratory fitting and provide the applicable source/license or
authorization reference. Fitting is blocked by this missing permission under the
user's explicit condition. The final-study minimum remains 1,000 records.

No new clinical interpretation or synthetic research data is required for the
proposed recorded-label demo. Vector provenance/source confounding remain limitations
to disclose; trained-model performance must not be presented as real-world validity.
See [demo status](exploratory_demo_status.md) for completed interface work and next steps.
