# Testing plan

Existing runnable suite: `python -m unittest discover -s tests -v`.
Scaffold validation: `python scripts/validate_scaffold.py`.

New ML/backend test files are explicitly skipped unittest placeholders, compatible
with later pytest discovery. They are not assertions that functionality works.
Frontend test files record pending cases; they are not executable tests yet.
After implementation, pin pytest/httpx and frontend test dependencies, then test
leakage, feature ordering, unavailable artifacts, strict request validation,
frontend loading/errors and research-only result presentation.
