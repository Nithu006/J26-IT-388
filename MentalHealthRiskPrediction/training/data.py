"""Explicit CSV contract and loader. No dataset-specific defaults or label invention."""

import csv
import json
import math
from pathlib import Path


class ContractError(ValueError):
    """Safe, record-free configuration or file-format error."""


def validate_config(config):
    if not isinstance(config, dict):
        raise ContractError("Configuration must be a JSON object.")
    for key in ("dataset_path", "text_column", "label_column"):
        if not isinstance(config.get(key), str) or not config[key].strip():
            raise ContractError(f"Set {key} from the authorized dataset.")
    delimiter = config.get("delimiter", ",")
    if not isinstance(delimiter, str) or len(delimiter) != 1 or delimiter in "\r\n":
        raise ContractError("delimiter must be one non-newline character.")
    if not isinstance(config.get("encoding", "utf-8-sig"), str):
        raise ContractError("encoding must be a string.")
    missing = config.get("missing_values", [""])
    if not isinstance(missing, list) or not all(isinstance(x, str) for x in missing):
        raise ContractError("missing_values must be a list of strings.")
    roles = [config["text_column"], config["label_column"]]
    for key in ("group_column", "language_column"):
        value = config.get(key)
        if value is not None:
            if not isinstance(value, str) or not value.strip():
                raise ContractError(f"{key} must be a column name or null.")
            roles.append(value)
    features = config.get("behavior_features", [])
    if not isinstance(features, list):
        raise ContractError("behavior_features must be a list.")
    for feature in features:
        if not isinstance(feature, dict) or not isinstance(feature.get("name"), str):
            raise ContractError("Each behavior feature needs a string name.")
        if not feature["name"].strip():
            raise ContractError("Behavior feature names cannot be blank.")
        roles.append(feature["name"])
        for bound in ("min", "max"):
            value = feature.get(bound)
            if value is not None and (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(value)
            ):
                raise ContractError("Feature bounds must be finite numbers or null.")
        low, high = feature.get("min"), feature.get("max")
        if low is not None and high is not None and low > high:
            raise ContractError("Feature minimum cannot exceed maximum.")
    if len(roles) != len(set(roles)):
        raise ContractError("Text, label, group, language and feature columns must be distinct.")
    return config


def load_config(path):
    path = Path(path)
    with path.open(encoding="utf-8") as stream:
        config = validate_config(json.load(stream))
    dataset = Path(config["dataset_path"])
    if not dataset.is_absolute():
        dataset = path.resolve().parent / dataset
    return config, dataset.resolve()


def load_csv(path, config):
    """Load strings without guessing numeric types, targets, or missing values."""
    validate_config(config)
    with Path(path).open(
        encoding=config.get("encoding", "utf-8-sig"), newline=""
    ) as stream:
        reader = csv.reader(stream, delimiter=config.get("delimiter", ","), strict=True)
        try:
            columns = next(reader)
            if not columns or any(not name.strip() for name in columns):
                raise ContractError("CSV headers cannot be empty.")
            if len(columns) != len(set(columns)):
                raise ContractError("CSV contains duplicate headers.")
            required = [config["text_column"], config["label_column"]]
            required += [config[k] for k in ("group_column", "language_column") if config.get(k)]
            required += [feature["name"] for feature in config.get("behavior_features", [])]
            if any(name not in columns for name in required):
                raise ContractError("CSV is missing one or more configured columns.")
            rows = []
            for values in reader:
                if len(values) != len(columns):
                    raise ContractError("CSV row width differs from header width.")
                rows.append(dict(zip(columns, values)))
        except StopIteration:
            raise ContractError("CSV file has no header.") from None
        except csv.Error:
            raise ContractError("CSV syntax is malformed.") from None
    return columns, rows
