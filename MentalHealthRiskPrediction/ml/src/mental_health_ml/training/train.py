"""Fail-closed training preflight. No fitting path exists before contract approval."""
from mental_health_ml.data.validate_data import VECTOR_COLUMNS

MINIMUM_FINAL_RECORDS = 1000
RANDOM_SEED = 42


def training_readiness(audit):
    """Document blockers; row-count success alone must never authorize fitting."""
    blockers = []
    if audit["rows"] < MINIMUM_FINAL_RECORDS:
        blockers.append(f"Final training needs at least 1000 records; shortfall {1000 - audit['rows']}.")
    if any(audit["missing"].values()) or any(audit["invalid_or_nonfinite_numeric"].values()):
        blockers.append("Missing/invalid data needs an approved handling policy.")
    if any(audit["blank_identifiers_or_sources"].values()):
        blockers.append("Blank grouping/source fields require review.")
    if audit["duplicate_rows"] or audit["duplicate_vectors"]:
        blockers.append("Duplicate records/vectors require leakage review.")
    if audit["unrecognized_label_rows"] or audit["unrecognized_source_rows"]:
        blockers.append("Unexpected categories require a revised contract.")
    if any(n == 0 for n in audit["label_distribution"].values()):
        blockers.append("Both observed label tokens are required for a binary comparison.")
    blockers.extend([
        "Label meanings 0/1 and annotation provenance are not approved.",
        "Vector generation, fitting population, feature meaning and prediction-time availability are unverified.",
        "Dataset permissions, participant identity scope and split design need documented review.",
        "No documented exploratory-pilot exception is available.",
        "No paired raw text is available for text-only or full hybrid experiments.",
        "Training implementation and dependencies await approved contracts.",
    ])
    return {"decision": "NO-GO", "fitting_performed": False,
            "minimum_final_records": MINIMUM_FINAL_RECORDS, "random_seed": RANDOM_SEED,
            "candidate_vectors_not_approved": list(VECTOR_COLUMNS),
            "excluded_inputs": ["participant_id", "source", "label", "risk_oof"],
            "blockers": blockers}
