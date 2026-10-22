"""Read-only vector audit and training preflight; no fitted model is produced."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from mental_health_ml.data.validate_data import audit_vectors
from mental_health_ml.training.train import training_readiness


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        result = audit_vectors(args.dataset)
        result["training"] = training_readiness(result)
    except (OSError, ValueError, UnicodeError):
        print("Audit failed: check access, CSV encoding and expected schema.", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, allow_nan=False))
    return 1 if result["training"]["decision"] == "NO-GO" else 0


if __name__ == "__main__":
    raise SystemExit(main())
