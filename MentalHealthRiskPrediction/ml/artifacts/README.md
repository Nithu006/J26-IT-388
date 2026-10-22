# ML artifacts

No fitted model is supplied. These directories contain documentation and empty
markers only; generated bundles and evaluation outputs must remain ignored by Git.

The existing loader expects a future operator-trusted bundle containing
`pipeline.joblib` and `metadata.json` under the selected model directory. Metadata
must match the supported schema, ordered features, recorded classes, purpose, model
version and checksum. A checksum is not evidence of trust or research permission.

See the [inference and artifact contract](../../docs/exploratory_demo_status.md)
and [ML implementation status](../README.md). Current loading tests use mocks;
a fitted-estimator serialization round trip has not been verified. Missing or
untrusted bundles keep the demo in its model-unavailable state.
