# Research readiness and next steps

Review date: 2026-10-22. Scope: read-only research review, with this document as
the sole requested output. No model training, predictions, data generation, package
installation or application changes were performed. The working demo is preserved.

## Decision

**NO-GO for final research training.** The file contains 220 records, 780 below the
user-reported supervisor minimum of 1,000. Authorization and research definitions
also remain unresolved; reaching 1,000 alone would not resolve those issues.

An exploratory classifier of uninterpreted recorded labels is a narrower possible
study, not a validated mental-health predictor. It still requires permission to use
this derived dataset and agreement on exploratory scope. No such permission is
established by the inspected documents. No fitting is authorized by this review.

## Verified current data

File: `dataset/raw/behavior_vectors.csv`, 79,284 bytes.
SHA-256: `1f12b8936ea610fba22bec5c2c64267086c7a204303568c85333ba42d1457e23`.

| Property | Recomputed finding |
| --- | --- |
| Rows / columns | 220 / 20 |
| Distinct participant ID strings | 220; no repeated IDs within this file |
| Missing values | 0 in every column under pandas default NA recognition |
| Exact duplicate rows | 0 |
| Recorded label 0 | 34 (15.45%) |
| Recorded label 1 | 186 (84.55%) |
| Raw text / timestamps | No such columns in this CSV |

All column names:

```text
participant_id, source,
bvec_0, bvec_1, bvec_2, bvec_3, bvec_4, bvec_5, bvec_6, bvec_7,
bvec_8, bvec_9, bvec_10, bvec_11, bvec_12, bvec_13, bvec_14, bvec_15,
risk_oof, label
```

Pandas inferred strings for participant_id/source, float64 for the 16 vectors and
risk_oof, and int64 for label. These storage types do not establish semantics.
Distinct ID strings are not independent evidence of distinct people across sources.

| Source token | Records | Label 0 | Label 1 | Label-1 share |
| --- | ---: | ---: | ---: | ---: |
| reddit | 100 | 0 | 100 | 100% |
| twitter | 72 | 8 | 64 | 88.89% |
| thai | 48 | 26 | 22 | 45.83% |

This source-label association is observed, not a model result. A classifier might
exploit source-specific representation or collection differences instead of the
intended construct. Excluding the source column does not remove source information
encoded in the vectors. Random stratification can preserve this confounding in both
train and test. The absent reddit/label-0 cell prevents within-reddit assessment of
both classes; reweighting cannot manufacture missing evidence. The token `thai`
does not by itself prove a language, platform, population or data source.

## Evidence still missing

| Evidence to obtain | Required content and why it matters | Existing decision |
| --- | --- | --- |
| Dataset use rights | Exact source URLs, versions, provider/owner, applicable license or written authorization for derived vectors, model fitting and demonstration; evidence covering all contributing sources | D1 |
| Study approval | Applicable university/ethics and supervisor approval; confirm minimum counting unit and explicit scope of any below-minimum exploratory pilot | D7, D15 |
| Target dictionary | Meaning of 0/1, annotation/proxy/self-report origin, annotator procedure, label timing, harmonization across sources, approved positive-class interpretation | D2, D16 |
| Vector lineage | Raw inputs, feature or latent-dimension definitions, generator code/version, normalization, pretrained/fitted models, training population, label use, observation windows and availability at prediction time | D4–D5, D17 |
| OOF lineage | Meaning of risk_oof, model inputs/targets, folds and participant separation, fitting of preprocessing, independent holdout treatment and deployment availability | D18 |
| Identity and time | Stable permitted participant linkage across sources/files, prediction unit and horizon, event timestamps, overlapping windows, duplicate/near-duplicate detection | D5–D6, D20 |
| Sampling provenance | Source definitions, recruitment/selection rules, reasons for source-specific label distributions, intended deployment population and source coverage | D19 |
| Text pairing | Authorized text and language metadata linked to each eligible participant/record/window; reliable alignment with behavior and target | D3, D21 |

The example configuration still has null authorization_reference,
label_definition_reference, observation_window, prediction_time_definition,
split_strategy and supervisor_architecture_approval. The model configuration has
no encoder ID/revision or label mapping. Empty templates are not evidence of approval.

The general source audit does not establish whether any permission exists outside
the inspected workspace. Request the supporting documents from the data provider
and supervisor; do not invent a citation or infer permission from public visibility.
No definition of a recorded label is inferred here.

## Requirements by experiment

| Experiment | Required inputs and approvals | Current status |
| --- | --- | --- |
| Behavior-only | Authorized behavioral signals or documented behavior-derived vectors, target provenance, prediction-time windows and leakage-safe lineage | 16 opaque numeric dimensions exist. Until lineage is confirmed, call any permitted experiment vector-only, not verified behavior-only |
| Text-only | Authorized real text, same target/prediction unit, language/code-mixing review, frozen encoder ID/revision and consistent text processing | No text column or paired text files found in the dataset inventory |
| Hybrid | Both approved modalities paired by record/participant/window; aligned row IDs, fixed feature order, train-only learned processing and supervisor agreement on Transformer + XGBoost | Not supported by this CSV alone |

Never join unrelated datasets merely because their row counts match. Never generate
fake text or labels, or duplicate records to reach the minimum. Compare modalities
on a common eligible paired cohort and identical splits; report exclusions and any
selection bias from requiring both modalities. Other unpaired analyses, if approved,
must be reported separately from the fair modality comparison.

## Proposed leakage-safe evaluation plan (not executed)

1. **Define the claim first.** Agree whether the objective is unseen participants,
   future observations, unseen sources, or a combination. Freeze the target definition,
   observation window and prediction horizon before choosing split rules. The existing
   file cannot support a chronological evaluation without timestamps.
2. **Approve and freeze data.** Version the permitted dataset and generation code;
   review duplicates, aliases, label consistency and source sampling. Verify enough
   eligible records for the final-study minimum and enough independent groups per
   class/source for useful uncertainty estimates. Record exclusions. Do not specify
   a guaranteed sufficient sample size from row count alone.
3. **Repair upstream leakage before downstream splitting.** Determine whether the
   vector generator used labels or all participants. Regenerate learned vectors and
   transformations inside each training fold when required. A frozen external encoder
   is acceptable only with documented provenance/overlap assessment. If upstream
   leakage cannot be resolved, do not claim an unbiased generalization evaluation.
4. **Lock a final holdout.** Seed 42 is proposed for reproducibility, not performance
   optimization. For an authorized exploratory 220-row pilot, a tentative 20% holdout
   would have 44 rows and only roughly seven label-0 records under label stratification:
   this is a planning estimate, not an executed split or adequate precision claim.
   Revisit the fraction after cohort expansion. Hold out whole participants; if verified
   participants each occur once, group splitting reduces to a row partition. Where
   future prediction is intended, use time boundaries and appropriate window purge
   gaps, with participant separation appropriate to the agreed claim.
5. **Stratify only where feasible.** Preserve class support and, when sufficient,
   source-by-label composition for a within-source evaluation. Check all fold counts
   before training. Never silently abandon group separation to force stratification.
   Current small cells, especially eight twitter label-0 records, limit feasible
   folds. Zero reddit label-0 support cannot be fixed by a different random seed.
6. **Use development data for selection.** Within the non-test data, propose three-fold
   stratified group cross-validation if class/group/source counts support it; reduce
   complexity or revisit the design otherwise. Fix a small tuning budget. Fit imputation,
   scaling, feature selection and any calibration only within training folds. Compute
   class weights from those training labels; any resampling stays within the fold.
   Neither validation nor final test data is resampled or used to choose features.
7. **Compare declared baselines.** After permission and dependencies are approved,
   compare Logistic Regression and Random Forest on the same folds. Add a training-only
   majority baseline to contextualize imbalance. Evaluate the proposed XGBoost hybrid
   only after paired modalities and supervisor approval exist. Exclude participant_id,
   source, risk_oof and label from candidate feature inputs. Keep risk_oof excluded;
   a stacking experiment would require a separate leakage-safe design and approval.
8. **Audit source generalization separately.** Report per-source supports and errors.
   Consider leave-one-source-out sensitivity analysis only after deciding that domains
   and labels are comparable. Predefine it before viewing final-test performance;
   it is a separate experiment, not repeated reuse of a locked test set for tuning.
   A reddit-only test set has one observed class, so ROC-AUC is undefined there and
   label-0 recall cannot be estimated. A full confusion matrix with fixed class order
   can still show zero support, but must not imply both classes were tested.
9. **Evaluate once after selection.** Lock features, model, threshold and hyperparameters
   before final-test evaluation. Report accuracy, per-class precision/recall/F1,
   macro-F1, confusion matrix and supports. Use continuous scores and a declared
   positive label for ROC-AUC only when both classes are present. Mark undefined
   quantities explicitly; explain any software zero-division convention. PR-AUC, if
   used, also needs a declared positive class and reported prevalence. Do not reinterpret
   label 1 as clinical risk. Probabilities are not clinical risk estimates.
10. **Report uncertainty and limits.** For an adequate cohort, consider participant-level
    paired bootstrap intervals for model differences, respecting the independent
    sampling unit. With very few minority test participants, estimates are unstable;
    disclose missing-class resamples and method limitations. Do not treat fold scores
    as independent observations for naive significance tests. Small-N, label validity,
    source confounding and residual upstream leakage limit every claim.
11. **Preserve reproducibility.** Save data hash, restricted split manifest, seeds,
    generator/encoder revision, ordered features, preprocessing, class mapping, package
    versions, tuning decisions and actual results. Measure full inference latency on
    specified hardware before any real-time performance claim. A working UI does not
    establish research or model validity.

## Immediate next steps for the supervisor

1. Obtain data-use evidence and clarify permitted exploratory versus final-study use.
2. Obtain the label dictionary and vector/OOF generation code, including fold lineage.
3. Agree prediction unit, independent identity, source-generalization and time objectives.
4. Acquire at least 780 additional eligible authorized records for the numerical
   final-study requirement, with better class/source support; reassess after exclusions.
5. Obtain correctly paired text or formally revise the experiment scope.
6. Approve the data contract and evaluation protocol before implementing model fitting.

## Actual checks in this review

- Read all five requested documents; inspected dataset inventory and existing dataset/
  model configuration. Earlier no-data/scaffold passages were treated as historical,
  not current findings; the user-reported successful demo is distinct from ML readiness.
- Used installed pandas to read a single byte snapshot and compute aggregate shape,
  schema/types, missingness, exact duplicates, unique IDs, distributions and crosstab.
- The read-only command completed successfully. Input bytes were identical before and
  after reading; SHA-256 matches the prior audit. No individual record values printed.
- No frontend/backend tests rerun: this task is documentation-only and does not alter
  application code, services or dependencies. Prior test results are not new evidence
  of training readiness.
- Only this document was created. No predictions, splits, metrics, model artifacts,
  synthetic labels, destructive commands or service restarts were produced.

Local references: [audit](data_audit_report.md), [readiness history](data_readiness_assessment.md),
[decisions](open_questions.md), [model design](ai-model-design.md),
[training preparation](model_training.md). The evaluation plan above is a proposal
for review, not an approved protocol or an experimental finding.
