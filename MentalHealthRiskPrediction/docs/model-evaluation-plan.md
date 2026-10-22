# Proposed evaluation protocol and acceptance criteria

Status: proposal for supervisor review, not an approved experiment. No model has
been trained or evaluated for this component. This document specifies what must be
agreed and verified before experiments begin; it does not authorize data use.
See the detailed [readiness review](research_readiness_next_steps.md),
[decision register](open_questions.md), and [evaluation status](evaluation_report.md).

## Evidence and decisions required

| Gate | Required evidence or decision | Decision register |
| --- | --- | --- |
| Use rights | Sources, versions, licenses/written permission covering derived vectors and proposed use; applicable ethics approval | D1 |
| Target | Label meanings, annotation process, timing and compatibility across sources; positive label for score-based metrics | D2, D16 |
| Features | Vector generator/version, raw inputs, fitted population, label use and prediction-time availability | D4, D5, D17 |
| Independent observations | Participant identity scope, aliases, repeated observations and overlap across datasets | D6, D20 |
| Study size | Confirm minimum counting unit and sufficient class/group support; written scope for any exploratory exception | D15 |
| Generalization | Unseen participants, future observations or unseen sources; agree which claim is primary | D5, D6, D19 |
| Modalities | Authorized text, language review, correct participant/window pairing and approved architecture | D3, D7, D21 |

The supervisor/data custodian must provide or review this evidence. Record the owner,
reference, date and permitted scope in the decision register. No field is considered
approved just because an example configuration exists. The original audited file had
220 rows, below the stated 1,000-record final-study minimum; it is excluded from Git.
A permitted smaller pilot must remain explicitly exploratory. More rows alone do not
resolve provenance, class support or leakage.

## Proposed experiment sequence

1. Freeze the approved target, cohort, prediction unit, observation window and
   prediction horizon. Hash the authorized data snapshot and version its generator.
   Do not include raw records, identity mappings or private split manifests in Git.
2. Review upstream leakage before splitting. If vectors were learned using the
   evaluation population or labels, regenerate them inside training folds as needed.
   Excluding `risk_oof` does not repair leakage already present in the vectors.
3. Reserve an untouched test partition using the approved participant/time rules.
   Keep linked observations together. Use chronological boundaries only when reliable
   timestamps and a temporal research question exist. Check aliases and overlapping
   windows. Never relax participant separation just to obtain stratification.
4. Propose seed 42 for reproducibility. Select holdout size and cross-validation folds
   only after checking independent group and class support. Store the agreed split
   once; do not choose a seed or partition because it yields better performance.
5. Fit imputation, scaling, feature selection and imbalance treatment only inside
   development training folds. Never resample the validation or final test data.
   Use development validation for model selection and any threshold/calibration work.
6. Compare a training-only majority baseline, Logistic Regression and Random Forest
   when the approved data supports them. Keep ID, source, target and `risk_oof` out of
   model inputs. Call opaque vectors vector-only until behavioral lineage is verified.
7. Compare text-only, verified behavior-only and hybrid models on the same eligible
   paired cohort and splits. Report pairing exclusions. Do not join unrelated rows
   or generate text to create a missing modality. Encoder and XGBoost choices remain
   subject to review and dependency approval.
8. Lock the model, features, preprocessing, hyperparameters and threshold before final
   evaluation. Evaluate the untouched test set once. Any later design change needs a
   documented new evaluation plan rather than repeated tuning against that test set.

## Reporting criteria

Report actual accuracy, per-class precision/recall/F1, macro-F1, confusion matrix,
class supports and ROC-AUC where valid. ROC-AUC requires both classes and suitable
scores with an approved positive-class interpretation. Explicitly mark undefined
metrics and disclose any zero-division convention; zero support is not evidence of
successful classification. Model scores are not clinical risk estimates.

Predefine source-specific sensitivity analysis and its limits. The original audit
found source-label confounding, including a source with only label 1. A random split
can reproduce that confounding; removing the source column cannot prove its absence
from learned vectors. Do not calculate a two-class ROC-AUC for a single-class subset.

Agree uncertainty estimation at the participant/group level. Small minority samples
and missing-class resamples limit precision. Do not treat correlated fold scores as
independent evidence. Report negative or inconclusive comparisons as observed.

Record data and split versions, seeds, feature order, encoder revision, environment,
selection decisions and approved aggregate results. Measure end-to-end inference
latency on stated hardware before making a real-time claim. A working UI or passing
software test is not research performance or clinical validation.

## Acceptance before reporting a completed experiment

- Permission and scope evidence reviewed, with unresolved limits stated.
- Dataset, label, feature and upstream leakage checks completed for that scope.
- Locked splits verified for overlap and feasible class/group support.
- Train-only fitting and final-test separation demonstrated by software checks.
- Actual reproducible evaluation produced; no estimated or fabricated metrics.
- Public report checked for privacy and faithful interpretation of the evidence.

Until those conditions are met, retain the application's explicit unavailable-model
state. Software fixtures and mocks may test contracts but must never be counted as
research observations, fitted research artifacts or experimental findings.
