# Development plan and acceptance gates

| Phase | Scope and acceptance | Current status |
| --- | --- | --- |
| 1 | Read complete PDF, inspect workspace, trace requirements and decisions | Complete |
| 2 | Configurable loader/auditor; real source, label and leakage review | Tools implemented; real audit blocked by missing data |
| 3 | Establish modules as needed, pin tested dependencies | Minimal audit structure only |
| 4 | Validated text/numerics; approved group/time split; training-only fitting | Pending dataset contract |
| 5 | Approved encoder, aligned fusion, binary/multiclass training and bundle | Pending data and architecture approval |
| 6 | Four comparable experiments, tuning, held-out metrics and error analysis | Pending training |
| 7 | Startup-loaded FastAPI, readiness, strict validation and API tests | Pending model/input contract |
| 8 | Responsive React form, result/error states and API integration tests | Pending API contract |
| 9 | Persistence only when justified and approved | No database required currently |
| 10 | Preprocessing/fusion/serialization/API/UI tests and reproducibility | Audit tests available; later checks pending |
| 11 | Setup, actual results, limitations, privacy and handover | Living documentation; final handover pending |

Next: provide authorized data and complete `open_questions.md`; run the audit, review
its findings, then freeze a versioned data contract and split strategy. Agree supervisor
hybrid interpretation before model implementation. Do not substitute generated labels
or synthetic data for these gates.

Later dependency work: choose a compatible pinned Python ML/API stack and React
toolchain, install in an isolated environment, run smoke tests, and retain lockfiles.
No untested dependency pins or nonexistent run commands are supplied now.
