# Dataset audit status

**Latest result (2026-10-21): NO-GO for final training.** The newly supplied CSV
has 220 records, below the user-reported supervisor minimum of 1,000. Earlier
no-data findings below are historical. See the current audit at the end.

Workspace inventory on 2026-10-20: only the 13-page engineering guide existed.
No CSV, Parquet, annotations, code, pretrained artifacts or experimental reports
were supplied. Therefore row counts, columns, language and class distribution are
unknown; no real-data audit or model training has occurred.

Implemented tool: `python -m training.inspect_data --config ... --output ...`.
It reports file SHA-256, row count, missingness, exact duplicate rows, normalized
duplicate texts, class/language distributions, repeated-group counts, numeric
invalid/missing/out-of-range counts, configuration gaps and quality findings.

Manual review still required: authorization, anonymization (including identifiers
inside free text), label validity, near duplicates, language verification, group
semantics, future-feature leakage, split overlap and collection bias.
An aggregate audit is not ethical clearance and does not certify readiness to train.

## Post-scaffold readiness assessment — 2026-10-20

The opening inventory describes the original workspace. The current workspace now
contains the scaffold, but recursive inspection of `data/` and `dataset/` still
found no dataset: only three README files and three zero-byte `.gitkeep` files.
Columns, target labels, missingness, class balance and leakage remain unknown.
No local dataset mapping or trained artifacts were found in their designated folders.
Training is not ready to begin.

See [dataset and ML readiness assessment](data_readiness_assessment.md) for the exact
inventory, audit limitations, safe commands and model decisions. No actual dataset
audit or research metrics were produced during this assessment.

## Real vector dataset audit — 2026-10-21

Input: `dataset/raw/behavior_vectors.csv` (79,284 bytes). Read with pandas 3.0.1;
no source data modified or individual records printed.
SHA-256: `1f12b8936ea610fba22bec5c2c64267086c7a204303568c85333ba42d1457e23`.

| Check | Actual finding |
| --- | --- |
| Rows / columns | 220 / 20 |
| Distinct participant IDs | 220 |
| Repeated participant IDs / cross-source shared IDs | 0 / 0 |
| Exact duplicate rows / duplicate 16-dimensional vectors | 0 / 0 |
| Missing values | 0 in every column under pandas default NA recognition |
| Blank participant/source values | 0 / 0 |
| Invalid/nonfinite numeric entries | 0 |
| Label 0 | 34 (15.45%) |
| Label 1 | 186 (84.55%) |
| Minimum requirement | 1,000 records; 220 available (22%); shortfall 780 |

Actual schema and pandas types:

- `participant_id`, `source`: strings (pandas infers `str`; reusable audit explicitly
  uses nullable `string` to preserve identifiers).
- `bvec_0`, `bvec_1`, `bvec_2`, `bvec_3`, `bvec_4`, `bvec_5`, `bvec_6`, `bvec_7`,
  `bvec_8`, `bvec_9`, `bvec_10`, `bvec_11`, `bvec_12`, `bvec_13`, `bvec_14`,
  `bvec_15`: `float64`.
- `risk_oof`: `float64`.
- `label`: `int64`, observed values 0 and 1. Their meanings are **unverified**.

| Recorded source token | Rows | Label 0 | Label 1 |
| --- | ---: | ---: | ---: |
| reddit | 100 | 0 | 100 |
| twitter | 72 | 8 | 64 |
| thai | 48 | 26 | 22 |

These tokens are CSV values, not verified collection provenance; `thai` does not
establish language, population or platform. Source/label association is a potential
confounding risk, especially the absence of label 0 in the reddit group.

### Definitions and leakage review

No supporting vector-generation code, annotation guide, label dictionary or OOF
generation manifest was found in the inspected project documentation/configuration.
Numeric 0/1 values establish a target candidate, not a validated research target.
Do not call them low/high risk, healthy/depressed or equivalent without evidence.

`bvec_0`–`bvec_15` are opaque numeric vector dimensions. Their raw signals, encoder,
training population, normalization, use of labels and time windows are unknown.
They are not approved raw behavioral measurements. Even excluding `risk_oof` cannot
remove leakage already embedded in vectors derived from a model fitted globally.

`risk_oof` is excluded from candidate inputs. The name may suggest out-of-fold
predictions, but that is not evidence of its origin or safety. Require generator
code, base-model inputs/labels, group-aware fold assignments, preprocessing fitting
scope and prediction-time availability. OOF generation for training does not by
itself establish an untouched final test set. Any future stacking design needs
separate review; the current code has no option to enable this field.

No train/validation/test split has been created. No repeated ID is observed inside
the file, but cross-file overlap, identity aliases across sources, near-duplicates,
upstream fitted-transform leakage and future-event leakage are unverified.
No timestamp or raw-text column is present. A text-only or complete text/behavior
hybrid experiment cannot be supported by this CSV alone.

### Decision and permitted work

**NO-GO for final training; no exploratory training authorized either.** At least
780 additional eligible, authorized records are needed to reach the numerical
minimum, followed by review of independence, quality, provenance and class support.
Duplicate/synthetic expansion does not satisfy this requirement. A written pilot
exception would still require approved label and feature definitions and would not
satisfy the final-study minimum. There is no such exception in the inspected files.

Implemented only an aggregate vector audit and fail-closed training preflight in
the existing ML modules. Fitting, splits, preprocessing and model comparisons are
not implemented or run because the prerequisite approvals are absent.
See [training preparation plan](model_training.md) for the exact preflight command,
future leakage-safe workflow and validation results. No model metrics exist.
