"""Aggregate audit of the supplied vector schema; no semantic approvals inferred."""
import csv
import hashlib
import io
import math
from pathlib import Path

import pandas as pd

VECTOR_COLUMNS = tuple(f"bvec_{i}" for i in range(16))
REQUIRED_COLUMNS = ("participant_id", "source", *VECTOR_COLUMNS, "risk_oof", "label")


def audit_vectors(path):
    """Read one immutable byte snapshot; emit no participant IDs or vector values."""
    raw = Path(path).read_bytes()
    header = next(csv.reader(io.StringIO(raw.decode("utf-8-sig"))), [])
    if len(header) != len(set(header)) or set(header) != set(REQUIRED_COLUMNS):
        raise ValueError("Expected the reviewed vector schema with unique headers.")
    frame = pd.read_csv(io.BytesIO(raw), dtype={"participant_id": "string", "source": "string"})
    missing = frame.isna().sum().astype(int).to_dict()
    blank = {c: int(frame[c].dropna().str.strip().eq("").sum())
             for c in ("participant_id", "source")}
    invalid = {}
    for column in (*VECTOR_COLUMNS, "risk_oof", "label"):
        numeric = pd.to_numeric(frame[column], errors="coerce")
        invalid[column] = int(sum(not math.isfinite(float(x)) for x in numeric))
    # Only verified category tokens are printed. Unexpected values are counted, not echoed.
    labels = pd.to_numeric(frame["label"], errors="coerce")
    sources = frame["source"].str.strip()
    source_counts = {s: int(sources.eq(s).sum()) for s in ("reddit", "twitter", "thai")}
    groups = frame["participant_id"].str.strip().replace("", pd.NA)
    counts = groups.value_counts()
    cross = {s: {str(k): int((sources.eq(s) & labels.eq(k)).sum()) for k in (0, 1)}
             for s in source_counts}
    return {
        "dataset_sha256": hashlib.sha256(raw).hexdigest(),
        "pandas_version": pd.__version__, "rows": len(frame),
        "columns": list(frame.columns), "dtypes": frame.dtypes.astype(str).to_dict(),
        "missing": missing, "blank_identifiers_or_sources": blank,
        "invalid_or_nonfinite_numeric": invalid,
        "duplicate_rows": int(frame.duplicated().sum()),
        "duplicate_vectors": int(frame.duplicated(list(VECTOR_COLUMNS)).sum()),
        "unique_participants": int(groups.nunique()),
        "repeated_participants": int((counts > 1).sum()),
        "rows_with_repeated_participants": int(counts[counts > 1].sum()),
        "participant_ids_in_multiple_sources": int(
            frame.assign(_group=groups).groupby("_group")["source"].nunique().gt(1).sum()),
        "label_distribution": {str(k): int(labels.eq(k).sum()) for k in (0, 1)},
        "unrecognized_label_rows": int((~labels.isin([0, 1])).sum()),
        "source_distribution": source_counts,
        "unrecognized_source_rows": int((~sources.isin(source_counts)).sum()),
        "source_by_label": cross,
        "raw_text_available": False,
    }
