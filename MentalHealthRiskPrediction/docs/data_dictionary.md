# Data contract — mapping template, not an observed dataset

No real schema or target classes were provided. `config/dataset.example.json` deliberately
contains null mappings and no behavioral feature names. Copy it to `dataset.local.json`
and populate only from reviewed dataset definitions.

| Configuration | Meaning |
| --- | --- |
| dataset_path | Authorized CSV; relative to configuration directory or absolute |
| encoding / delimiter | Explicit file decoding and one-character delimiter |
| text_column | Actual text column; empty/whitespace values flagged |
| label_column | Actual categorical target; no classes invented or remapped |
| group_column | Optional pseudonymous grouping key, used for leakage checks only |
| language_column | Optional existing language annotations; never inferred by this tool |
| behavior_features | Ordered objects with `name`, `min`, `max`; bounds numeric or null |
| missing_values | Exact tokens considered missing after whitespace trimming |
| source / authorization_reference | Source and evidence of permitted use |
| label_definition_reference | Class definitions, assignment process and provenance |
| languages | Reviewed dataset languages; not automatic language detection |
| observation_window / timezone | Feature window and timezone definitions |
| prediction_time_definition | Prediction cutoff and target horizon |
| split_strategy | Reviewed group/chronological strategy; not applied by audit |
| supervisor_architecture_approval | Reference to architecture decision |

Each real behavioral feature also needs a documented formula, unit, missing-value policy,
availability time and exclusion of future events. Bounds must come from its definition.
Do not select identifiers as features. No default median imputation, scaling or
label encoding is performed by the audit.

CSV loader rejects duplicate/empty headers and malformed row widths. It retains string
values for audit; numbers are checked as finite values without silently coercing
invalid content into missing data. Reports include only counts, column names and
configured label/language distributions. No text samples or group values are emitted.
