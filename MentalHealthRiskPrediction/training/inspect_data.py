"""Aggregate CSV audit. Run with python -m training.inspect_data."""

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import sys

from training.data import ContractError, load_config, load_csv


REVIEW_FIELDS = (
    "source", "authorization_reference", "label_definition_reference",
    "languages", "observation_window", "prediction_time_definition",
    "timezone", "split_strategy", "supervisor_architecture_approval",
)


def audit(path, config):
    columns, rows = load_csv(path, config)
    missing_tokens = {value.strip() for value in config.get("missing_values", [""])}
    missing_tokens.add("")

    def missing(value):
        return value.strip() in missing_tokens

    def distribution(column):
        return dict(sorted(Counter(
            row[column].strip() for row in rows if not missing(row[column])
        ).items()))

    missing_counts = {col: sum(missing(row[col]) for row in rows) for col in columns}
    duplicate_rows = len(rows) - len({tuple(row[col] for col in columns) for row in rows})
    texts = [
        " ".join(row[config["text_column"]].split())
        for row in rows if not missing(row[config["text_column"]])
    ]
    duplicate_texts = len(texts) - len(set(texts))
    labels = distribution(config["label_column"])
    behavior = {}
    for feature in config.get("behavior_features", []):
        name = feature["name"]
        counts = {"missing": 0, "invalid_numeric": 0, "out_of_range": 0}
        for row in rows:
            if missing(row[name]):
                counts["missing"] += 1
                continue
            try:
                value = float(row[name])
                if not math.isfinite(value):
                    raise ValueError
            except ValueError:
                counts["invalid_numeric"] += 1
                continue
            low, high = feature.get("min"), feature.get("max")
            if (low is not None and value < low) or (high is not None and value > high):
                counts["out_of_range"] += 1
        behavior[name] = counts

    groups = None
    if config.get("group_column"):
        sizes = list(distribution(config["group_column"]).values())
        groups = {
            "unique_groups": len(sizes),
            "repeated_groups": sum(size > 1 for size in sizes),
            "rows_in_repeated_groups": sum(size for size in sizes if size > 1),
            "missing_group_rows": missing_counts[config["group_column"]],
        }
    issues = []
    if not rows:
        issues.append("No data rows.")
    if missing_counts[config["text_column"]]:
        issues.append("Missing text requires an explicit handling policy.")
    if missing_counts[config["label_column"]]:
        issues.append("Missing target labels.")
    if len(labels) < 2:
        issues.append("Fewer than two observed classes; classification not ready.")
    if duplicate_rows or duplicate_texts:
        issues.append("Duplicate rows/text require leakage review before splitting.")
    if groups and groups["missing_group_rows"]:
        issues.append("Missing group keys prevent reliable group separation.")
    if any(any(counts.values()) for counts in behavior.values()):
        issues.append("Behavioral values require missingness/type/range review.")

    gaps = [key for key in REVIEW_FIELDS if not config.get(key)]
    if not config.get("behavior_features"):
        gaps.append("behavior_features")
    if not config.get("group_column"):
        gaps.append("group_column_or_documented_independent_record_evidence")
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return {
        "audit_schema_version": 1,
        "dataset_sha256": digest.hexdigest(),
        "row_count": len(rows),
        "columns": columns,
        "missing_counts": missing_counts,
        "duplicate_rows": duplicate_rows,
        "duplicate_normalized_texts": duplicate_texts,
        "label_distribution": labels,
        "language_distribution": (
            distribution(config["language_column"]) if config.get("language_column") else None
        ),
        "language_verification": "Manual review required; no language inference performed.",
        "groups": groups,
        "behavior": behavior,
        "quality_issues": issues,
        "unresolved_configuration": gaps,
        "training_readiness": "Not certified: human approval and leakage review required.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        config, path = load_config(args.config)
        if args.output.resolve() in (path, args.config.resolve()):
            raise ContractError("Output must not overwrite the dataset or configuration.")
        report = audit(path, config)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
            encoding="utf-8",
        )
    except ContractError as exc:
        print(f"Audit error: {exc}", file=sys.stderr)
        return 2
    except (OSError, UnicodeError, ValueError, LookupError):
        # Do not expose data-bearing parser messages, file contents or private paths.
        print("Audit error: unable to read configuration/data or write report.", file=sys.stderr)
        return 2
    print("Aggregate audit written. Human review is required before training.")
    return 1 if report["quality_issues"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
