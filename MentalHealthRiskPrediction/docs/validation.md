# Executed validation — 2026-10-20

Runtime: bundled CPython 3.12.14, Windows.

| Check | Result |
| --- | --- |
| Complete PDF extraction | All 13 pages read; rendered contact sheet inspected |
| `python -m unittest discover -s tests -v` | 8 tests passed |
| `python -m training.inspect_data --help` | Passed; CLI options displayed |

Initial test execution failed because the sandbox denied access to temporary test
files. The same test suite then passed outside the sandbox. No failing software
assertions were observed in the successful rerun.

Coverage: aggregate counts and record non-disclosure, deterministic results and
unchanged inputs, malformed CSV rejection, invalid contract/bounds, relative paths,
CLI report output, overwrite protection, missing-file errors, missing/nonfinite
numbers, language annotations, empty datasets and single-class data.

All test records are synthetic software fixtures in temporary directories.
No actual dataset audit, model training, ML metrics, API or frontend checks were run.

## Structure expansion checks — 2026-10-20

- Existing audit tests rerun before scaffolding: **8 passed**, CPython 3.12.14.
- `python scripts/validate_scaffold.py`: passed; 103 Python sources parsed,
  requested files checked, package markers and TOML/JSON validated, relative
  frontend imports resolved.
- `python -m unittest discover -s ml/tests -v`: **7 skipped** placeholders.
- `python -m unittest discover -s backend/tests -v`: **6 skipped** placeholders.
- `node --check frontend/src/services/apiClient.js`: passed syntax check only.
- Original audit source, tests, config and PDF hashes remained unchanged.
- Git status could not run: the workspace has no Git repository.
- `nbformat` unavailable; six notebooks intentionally omitted with creation commands.

No ML dependencies or pretrained models were installed. No runtime API, React build,
browser integration, Docker build or model evaluation was attempted. Source stubs
must not be interpreted as working features. The first scaffolder attempt stopped
at the existing `.gitignore`; handling was corrected before the successful run.
