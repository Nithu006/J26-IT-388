"""Prevent leakage scaffold for ml/src/mental_health_ml/data.

Status: reserved, not implemented. No runtime side effects.
TODO: agree the contract, implement after review, and add meaningful tests.
See docs/development_plan.md and docs/open_questions.md at repository root.
"""

# Contract to implement: detect shared groups and duplicate content across splits;
# enforce prediction-time feature cutoffs; record exclusions and split identifiers.
# Never infer absence of user leakage just because no group column is available.
