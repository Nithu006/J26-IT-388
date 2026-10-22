# Development status and acceptance gates

Current documentation review: 2026-10-22. This table describes implementation, not
research approval. Earlier phase notes remain in the historical structure mapping.

| Area | Current status | Next acceptance condition |
| --- | --- | --- |
| Requirements | Original guide review documented; guide excluded from publication | Resolve remaining supervisor decisions |
| Data auditing | General audit and vector audit implemented; original 220-row audit documented | Obtain verified permissions and an approved data contract; no CSV is bundled |
| Dependencies | Backend pins and frontend lockfile exist; copied frontend installation verified | Reproducible independent Python setup and reviewed ML dependency plan |
| Input and inference contract | Strict 16-vector validation and trusted-bundle interface implemented | Broader contract tests and eventual authorized real-bundle verification |
| Backend demo | Health/model-info/predict work, including 422 and model-unavailable 503 | Keep unavailable behavior; complete contracts before integrating any approved artifact |
| Frontend demo | Numeric form, API integration, loading/errors and result interface work | Expand test discovery and accessibility checks |
| Split and preprocessing | ML placeholders; no research split created | Approved groups, time rules and upstream leakage review |
| Models and hybrid design | No fitting; text, behavior and fusion modules are placeholders | Approved data, target, feature lineage, paired text and architecture |
| Research evaluation | Plan only; no model metrics | Freeze comparison protocol, then evaluate legitimately trained models |
| Explanations | Placeholders | Agree teammate ownership, method and research scope |
| Authentication and persistence | Placeholders; no working storage or login | Establish need and approved privacy/access/retention design first |
| CI and packaging | Root component workflow added; actual CI result must be checked; Docker files are scaffolding | Review a root workflow and packaging separately |

## Work that can proceed without training

Clarify documentation, improve reproducible setup, activate suitable CI after review,
strengthen API/UI validation tests, improve error handling and accessibility, and
review model-bundle validation. Use software fixtures rather than participant records.
These activities must preserve explicit model-unavailable behavior.

## Research work that remains blocked

The original audited file had 220 records, below the supervisor's reported minimum
of 1,000 for final training. It is not present in the GitHub checkout. More records
alone would not resolve missing permission, label definitions or feature provenance.
An exploratory pilot still needs documented permission and agreed scope; it would
not satisfy the final-study minimum.

Resolve [open questions](open_questions.md), verify dataset and vector lineage,
agree participant/time/source leakage controls, and approve the proposed
[research evaluation plan](research_readiness_next_steps.md) before fitting.
Text-only and hybrid experiments need authorized, correctly paired real text.
Never invent labels, text, approvals or results to complete a phase.

See the [local demo guide](local_demo.md) for working commands and the distinction
between earlier runtime verification and this documentation-only review.

See [engineering progress and deferred tasks](engineering_progress.md) for the latest
local checks and the backend-environment blocker.
