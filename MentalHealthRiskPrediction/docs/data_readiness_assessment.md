# Dataset and ML readiness assessment

**Superseded inventory update — 2026-10-21:** the vector CSV is now present.
The [current audit](data_audit_report.md) verifies 220 records and a NO-GO decision
against the 1,000-record minimum. Labels/vector provenance and paired text remain
unresolved. The earlier assessment below is retained as history.

Assessment date: 2026-10-20. Scope: local files, existing audit implementation and
proposed architecture only. **Not ready to start training.**

## Verified inventory

Recursively inspected `data/` and `dataset/`, including hidden files.

| Location | Actual files | Interpretation |
| --- | --- | --- |
| `data/` | `README.md` | Documentation only |
| `dataset/` | `README.md` | Documentation only |
| `dataset/raw/` | `.gitkeep` (0 bytes) | Empty storage placeholder |
| `dataset/interim/` | `.gitkeep` (0 bytes) | Empty storage placeholder |
| `dataset/processed/` | `.gitkeep` (0 bytes) | Empty storage placeholder |
| `dataset/sample/` | `README.md` | No sample data |

**Actual dataset files found: none.** No data format, row count, column names,
target-label candidates, target definition, class mapping, missing-value rates,
class balance, language coverage or sample sufficiency can be established.
These are unknown, not zero-valued measurements. No individual records were displayed.
This finding concerns the inspected local locations; it does not establish whether
the user has data elsewhere.

`config/` contains `.gitignore` and `dataset.example.json`, with no local dataset
configuration. The example's dataset path, text/label/group/language columns and
approval references are null; its behavioral feature list is empty.
`ml/config/config.yaml` references this existing example contract.
`ml/config/model_config.yaml` names the proposed XGBoost classifier but has no encoder
ID, revision or label mapping. It explicitly marks supervisor confirmation pending.

`models/` and `ml/artifacts/` contain README files and empty placeholders only.
Inspected embedding, behavior, fusion, hybrid model, split and training modules
are scaffolds; their presence is not an implemented or validated training pipeline.

## Existing audit: capabilities and limits

The working entry point is `training/inspect_data.py`, with
`training/data.py` as its loader. The new `ml/scripts/check_dataset.py` is a scaffold,
not a replacement audit command.

Verified from source:

- Reads CSV strings using configured encoding/delimiter, validates header uniqueness,
  required column mappings and row widths. Does not clean or rewrite source data.
- Reports SHA-256, row count, per-column missingness, exact duplicate rows,
  whitespace-normalized duplicate text counts, label/language distributions,
  repeated-group counts and numeric missing/invalid/nonfinite/out-of-range counts.
- Trims surrounding whitespace in category counts; missing tokens are configurable.
  The default only recognizes blank values, so dataset-specific sentinel tokens
  must be reviewed. Numeric strings are checked, not silently imputed.
- Does not print text previews or group values. It does emit configured label and
  language values as distribution keys. Do not map an identifier or sensitive
  free-text field into either role; review aggregates before sharing.
- Only supports in-memory CSV. It requires a mapped label column even for an
  exploratory audit. An unlabeled dataset needs a reviewed audit extension, not
  invented labels or an arbitrary surrogate column.
- Does not verify permissions, label validity, actual language, direct identifiers
  in text, near duplicates, cross-split leakage or future-derived features.
- Flags repeated groups as aggregate counts, without itself enforcing a group split.
- Blocks an output path equal to the resolved dataset/config path, but otherwise
  writes to the supplied output path. Choose a new report file, never a data path,
  link/alias to data, or an existing report you want preserved.
- A successful exit is not training authorization. Missing approval metadata is
  listed separately and does not necessarily cause a nonzero exit code.

### Safe audit workflow after authorization and schema review

Do not run a real-data audit until permitted use is documented. Use a stable,
restricted, read-only source snapshot so the records and computed hash refer to the
same version. The script needs read access to the dataset and write access only to
the chosen report directory. Keep the source outside actively changing exports.

From the repository root, using an existing Python environment:

```powershell
python -m training.inspect_data --help
if (-not (Test-Path -LiteralPath 'config/dataset.local.json')) {
    Copy-Item -LiteralPath 'config/dataset.example.json' -Destination 'config/dataset.local.json'
}
```

Then edit the local JSON to map the **actual** authorized CSV and reviewed text,
label, optional group/language and behavioral columns. Document numeric ranges,
missing tokens, permission and label provenance, observation window, timezone,
prediction cutoff and split plan. Relative dataset paths resolve from `config/`,
not the shell directory. Do not alter the shared example or original dataset.

Only after completing that review:

```powershell
if (Test-Path -LiteralPath 'reports/data_audit.review.json') {
    throw 'Choose a new report filename to preserve the existing report.'
}
python -m training.inspect_data --config config/dataset.local.json --output reports/data_audit.review.json
$auditExitCode = $LASTEXITCODE
Write-Output "Audit exit code: $auditExitCode"
```

Exit codes: 0 = no flagged structural/data-quality issues; 1 = quality findings;
2 = configuration/file/output failure. Review both `quality_issues` and
`unresolved_configuration`, plus manual approval/leakage checks, in all cases.
Reports and local mappings are ignored by source-control rules, which do not
provide access control or anonymization. No actual audit report was generated here.

## Proposed architecture: implications, not approved decisions

The engineering guide (pp. 3, 5–7, 12–13) proposes a frozen Transformer encoder,
engineered numeric behavior features, row-aligned concatenation and XGBoost.
The guide was read in full earlier; relevant data/model pages were re-read during
this assessment. Its hash matches the preserved scaffold snapshot; all 13 pages
remain accessible.

| Design aspect | Consequence for readiness |
| --- | --- |
| Paired modalities | Each eligible text record/aggregate must align with permitted behavior for the same prediction unit and observation window. Separate unrelated text and behavior datasets cannot simply be concatenated. |
| Text representation | Language coverage, encoder license/revision, normalization, truncation and embedding size need an explicit choice. The example English encoder is not approved for Sinhala/code-mixed data. |
| Behavior preprocessing | Verify formulas, units, feature availability and missing-value policy. Fit any learned imputation/scaling on training rows only; preserve column order. |
| Fusion | Preserve row identities, not only row counts; test alignment and dimensions. Dense embeddings add compute/memory requirements that depend on the eventual data and encoder. |
| Classifier | Objective and class mapping depend on verified target semantics and observed classes. The guide's example multiclass objective is not a default. |
| Validation | Establish group/time boundaries before learned preprocessing. Freeze common eligible test rows for text-only, behavior-only, hybrid and simpler-baseline comparisons. |
| Model bundle | Persist encoder revision, transforms, feature order, labels, dataset hash, splits, seed and tested dependencies. No bundle currently exists. |
| Explanation | SHAP/LIME ownership and representation must be agreed. Importance over embedding dimensions is not automatically a human-readable explanation of words. This is an engineering implication, not an existing result. |
| Real-time claim | Measure end-to-end encoding plus preprocessing/classification on specified hardware; no latency target or achieved performance is confirmed. |

Potential leakage checks, **not observed findings**: shared users, exact/near-duplicate
posts, overlapping aggregation windows, behavior after prediction cutoff, labels
or annotation cues embedded in inputs, and preprocessing fitted on test rows.
Without data and target timing, their presence or absence cannot be determined.

Supervisor confirmation is required for the exact hybrid definition, approved
dataset/use, target meaning and provenance, prediction unit/horizon, behavioral
windows, language/encoder evaluation, split design and required comparisons.
See D1–D7 and the assessment refinements in [open questions](open_questions.md).

## Checks executed and next step

- Recursive file inventory and audit/config/source inspection completed.
- PDF page-count/hash verification passed; relevant source pages read.
- `python -m training.inspect_data --help` completed successfully (exit 0).
- Prior results remain historical: root tests 8 passed, scaffold validation passed,
  ML tests 7 skipped and backend tests 6 skipped. They were not rerun because this
  assessment changes documentation only.
- No packages installed, models downloaded, training/evaluation run or API/frontend/
  authentication/database functionality implemented.

Recommended next step, after user approval: obtain the authorized dataset with its
data dictionary, label provenance and feature-window definitions; populate the local
mapping and run the existing audit. Then agree the leakage-safe data contract and
implement data validation/splitting with meaningful tests before model training.
If the chosen data lacks behavior or valid labels, resolve that with the supervisor
before implementing the proposed multimodal model.

Assessment complete; further work awaits user approval.
