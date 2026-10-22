"""Prediction CLI for a future trusted bundle; never substitutes a dummy model."""
import argparse
import json
from pathlib import Path
import sys

from .prediction_pipeline import load_bundle, predict_record, ModelUnavailable


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-dir", required=True, type=Path)
    parser.add_argument("--input", required=True, type=Path, help="JSON with exactly 16 vector fields")
    parser.add_argument("--trusted-artifact", action="store_true")
    args = parser.parse_args(argv)
    try:
        bundle = load_bundle(args.model_dir, trusted=args.trusted_artifact)
        record = json.loads(args.input.read_text(encoding="utf-8"))
        result = predict_record(bundle, record)
    except ModelUnavailable as exc:
        print(str(exc), file=sys.stderr)
        return 3
    except (OSError, ValueError):
        print("Invalid or unreadable prediction input.", file=sys.stderr)
        return 2
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
