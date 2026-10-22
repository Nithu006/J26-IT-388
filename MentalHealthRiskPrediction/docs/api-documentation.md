# API plan — endpoints not implemented

Current implementation and startup instructions are documented in the
[local demo guide](local_demo.md). The scaffold notes below are historical;
the current API supports health/model-info and an unavailable-model prediction response.

Proposed routes: GET `/health`, GET `/model-info`, POST `/predict`.
The `api/v1` directory reserves a versioned route organization; final URL prefixes
remain to be agreed. Explanations, history and auth files are reserved only.

Prediction input names/ranges and labels await the data contract. Future unavailable
models must return an explicit unavailable error, never fabricated predictions.
See [architecture](architecture.md). No backend startup command is available yet.
