# Engineering progress and remaining blockers

Review date: 2026-10-22. Changes apply only to the copied GitHub component.
No dataset was accessed, no package version changed, no dependency installed and no
model trained during this engineering sequence. Temporary fixtures and mocks verify
software behavior only.

## Completed engineering work

- Clarified current implementation, historical evidence and dataset exclusion.
- Added a uniquely named repository-root CI workflow without changing group files or
  the original nested workflow. CI success requires an actual Actions result.
- Normalized backend paths, CORS settings and explicit trust with four passing tests.
- Added frontend response validation and protection against stale connection refreshes.
- Added first-invalid-field focus, error summaries and correction feedback.
- Replaced frontend test placeholders with focused suites and broader discovery.
- Strengthened trusted bundle tests and rejection of boolean class/prediction values.
- Documented evaluation gates and a proposed protocol without authorizing experiments.

## Actual local verification

- Frontend: 15 tests passed across four suites; production build passed.
- Configuration: four dependency-free tests passed.
- ML: 17 active tests passed; seven placeholders skipped. Of these, 12 active tests
  cover the inference contract using mocks. Pandas was already available in system Python.
- General audit: eight tests passed.
- Static scaffold validation: passed; 107 Python sources parsed.
- One initial frontend test failed because its newly written Unicode selector was
  corrupted during command input. The selector was corrected; subsequent runs passed.

These are software verification results, not research metrics. No new live browser
or full API verification is claimed. Prior API results remain historical.

## Tasks deferred and why

- Reproducible independent Python setup: the checkout has no backend virtual
  environment, and neither inspected independent Python runtime provides FastAPI.
  Verifying installation requires permission to install the existing pinned backend
  requirements. No new environment or packaging success is claimed.
- Comprehensive API request tests and explicit response schemas: deferred because
  their runtime verification needs the unavailable FastAPI environment. Existing API
  validation and response behavior remain in place; no untested replacement was added.
- Backend application suite: not rerun locally for the same dependency reason. Only
  configuration tests can run without FastAPI. CI is configured to install the existing
  pinned requirements, but that is not a claim that the CI job has passed.
- Real artifact serialization and prediction: no authorized fitted model exists.
- Dataset splitting, training, text/hybrid experiments and performance reporting:
  blocked by the permissions, provenance, definitions, size and pairing requirements
  in the [decision register](open_questions.md).

No empty commits were created to meet a numeric target. CI, configuration and frontend
improvements do not resolve research approvals. See the
[proposed evaluation protocol](model-evaluation-plan.md) before planning experiments.
