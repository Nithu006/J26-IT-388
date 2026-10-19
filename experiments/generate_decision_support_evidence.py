
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from src.decision_support import DecisionSupportPipeline


OUTPUT_DIR = Path("experiments/metrics/decision_support")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Explicitly synthetic sequences; not real user histories.
SCENARIOS = {
    "low_stable": [0.20, 0.25, 0.22, 0.24],
    "high_stable": [0.85, 0.90, 0.88, 0.86],
    "increasing": [0.20, 0.40, 0.60, 0.80, 0.95],
    "decreasing": [0.95, 0.80, 0.60, 0.40, 0.20],
    "missing_recovery": [0.90, None, None, None, 0.30],
    "uncertain": [0.50, 0.52, 0.48],
    "oscillating": [0.20, 0.90, 0.25, 0.85, 0.30],
}

records = []

for scenario, probabilities in SCENARIOS.items():
    pipeline = DecisionSupportPipeline()

    for step, probability in enumerate(probabilities, start=1):
        result = pipeline.process(probability).to_dict()

        records.append({
            "scenario": scenario,
            "step": step,
            **result,
        })

assert all(
    record["is_clinical_assessment"] is False
    for record in records
)

assert all(
    not record["attention_flag"]
    for record in records
    if not record["alert_eligible"]
)

assert all(
    record["rule_id"] == "DATA_001"
    for record in records
    if record["model_probability"] is None
)

# Export detailed, auditable decisions.
csv_path = OUTPUT_DIR / "decision_support_scenarios.csv"

with csv_path.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)

# Summarize rule coverage.
rule_counts = dict(Counter(
    record["rule_id"] for record in records
))

summary = {
    "project": "J26-IT-388 Component 4",
    "experiment": "Decision Support Engine Validation",
    "generated_utc": datetime.now(timezone.utc).isoformat(),
    "scenario_type": "synthetic",
    "clinical_validation": False,
    "n_scenarios": len(SCENARIOS),
    "n_observations": len(records),
    "rule_counts": rule_counts,
    "attention_flags": sum(
        record["attention_flag"] for record in records
    ),
    "stale_alert_violations": sum(
        bool(record["attention_flag"])
        for record in records
        if not record["alert_eligible"]
    ),
    "all_nonclinical": all(
        not record["is_clinical_assessment"]
        for record in records
    ),
    "configuration": {
        "alpha": 0.35,
        "max_gap": 2,
        "illustrative_lower_bound": 0.35,
        "illustrative_higher_bound": 0.65,
    },
}

json_path = OUTPUT_DIR / "decision_support_summary.json"

json_path.write_text(
    json.dumps(summary, indent=2),
    encoding="utf-8",
)

print(json.dumps(summary, indent=2))
print("\nEvidence successfully saved.")
print(csv_path)
print(json_path)
