"""Dependency-free structure, syntax and configuration checks; no model execution."""
import ast
import json
from pathlib import Path
import re
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT / "docs/scaffold_manifest.json").read_text(encoding="utf-8"))
    errors = []
    for name in manifest["requested"]:
        if name not in manifest["omitted"] and not (ROOT / name).is_file():
            errors.append(f"Missing requested file: {name}")
    python_files = []
    for base in ("training", "tests", "ml", "backend", "scripts"):
        for path in (ROOT / base).rglob("*.py"):
            python_files.append(path)
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except SyntaxError as exc:
                errors.append(f"Invalid Python syntax: {path.relative_to(ROOT)}:{exc.lineno}")
    for base in ("backend/app", "ml/src/mental_health_ml"):
        folders = [ROOT / base, *(ROOT / base).rglob("*")]
        for folder in folders:
            if folder.is_dir() and "__pycache__" not in folder.parts:
                if not (folder / "__init__.py").is_file():
                    errors.append(f"Missing package marker: {folder.relative_to(ROOT)}")
    for name in ("ml/pyproject.toml", "backend/pyproject.toml"):
        with (ROOT / name).open("rb") as stream:
            tomllib.load(stream)
    package = json.loads((ROOT / "frontend/package.json").read_text(encoding="utf-8"))
    if not package.get("private") or package.get("type") != "module":
        errors.append("Frontend package must remain private and use ES modules.")
    for path in (ROOT / "frontend/src").rglob("*"):
        if path.suffix in (".js", ".jsx"):
            source = path.read_text(encoding="utf-8")
            for relative in re.findall(r"""(?:from\s+|import\s*)['"](\.[^'"]+)['"]""", source):
                if not (path.parent / relative).is_file():
                    errors.append(f"Missing frontend import from {path.relative_to(ROOT)}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"PASS: requested scaffold files present; {len(python_files)} Python files parse.")
    print("PASS: Python package markers, TOML/JSON metadata and relative frontend imports.")
    print(f"Documented notebook omissions: {len(manifest['omitted'])}.")
    print("This is static validation, not runtime/API/UI/ML verification.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
