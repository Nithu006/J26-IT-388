
from fastapi import FastAPI, HTTPException

from src.api.shap_service import explain_text_shap

from src.api.lime_service import explain_text_lime

from src.api.schemas import (
    HealthResponse,
    PredictionRequest,
    PredictionResponse,
    ScoringRequest,
    DecisionSupportResponse,
    DecisionSupportSequenceResponse,
    ShapRequest,
    ShapResponse,
    LimeRequest,
    LimeResponse,
)


from src.api.model_service import predict_text

from src.decision_support import DecisionSupportPipeline


# ============================================================
# FastAPI Application Configuration
# ============================================================

app = FastAPI(
    title="J26-IT-388 Component 4 API",
    description=(
        "Research prototype for Explainable AI and "
        "Adaptive Decision Support using stress-related "
        "text classification. "
        "Not a clinical diagnostic service."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# ============================================================
# 1. Health Check Endpoint
# GET /health
# ============================================================

@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["System"],
)
def health_check() -> HealthResponse:
    """
    Check basic FastAPI service availability.

    This does not verify that the prediction model
    or explanation modules are loaded.
    """

    return HealthResponse(
        status="ok",
        service="component4-api",
        version=app.version,
        component="Explainable AI & Adaptive Decision Support",
    )


# ============================================================
# 2. Frozen Model Prediction Endpoint
# POST /predict
# ============================================================

@app.post(
    "/predict",
    response_model=PredictionResponse,
    tags=["Prediction"],
)
def predict(
    request: PredictionRequest,
) -> PredictionResponse:
    """
    Classify a text sample using the existing frozen
    TF-IDF + Logistic Regression model.

    No retraining is performed.

    Predictions concern stress-related text labels,
    not clinical mental health diagnoses.
    """

    try:
        result = predict_text(request.text)

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail="Prediction model unavailable",
        ) from exc

    except (ValueError, TypeError, RuntimeError) as exc:
        raise HTTPException(
            status_code=503,
            detail="Prediction service unavailable",
        ) from exc

    return PredictionResponse(**result)


# ============================================================
# 3. Adaptive Scoring and Recommendation Endpoint
# POST /decision-support
# ============================================================

@app.post(
    "/decision-support",
    response_model=DecisionSupportSequenceResponse,
    tags=["Decision Support"],
)
def decision_support(
    request: ScoringRequest,
) -> DecisionSupportSequenceResponse:
    """
    Process one independent probability sequence.

    Steps:
    1. Receive validated model probabilities.
    2. Apply EMA adaptive scoring.
    3. Handle missing and stale observations.
    4. Apply non-clinical recommendation rules.
    5. Return traceable decision-support results.

    Each request creates a new pipeline instance.
    No scoring state is shared between requests.

    Thresholds and recommendations are experimental
    and are not clinically validated.
    """

    # IMPORTANT:
    # A new instance prevents different submitted
    # sequences from sharing adaptive-scoring state.
    pipeline = DecisionSupportPipeline(
        alpha=0.35,
        max_gap=2,
    )

    results = []

    for probability in request.probabilities:
        result = pipeline.process(
            model_probability=probability,
        )

        results.append(
            DecisionSupportResponse(
                **result.to_dict()
            )
        )

    return DecisionSupportSequenceResponse(
        sequence_length=len(results),
        results=results,
        is_clinical_assessment=False,
    )



# ============================================================
# 4. SHAP Local Explanation Endpoint
# POST /explain/shap
# ============================================================

@app.post(
    "/explain/shap",
    response_model=ShapResponse,
    tags=["Explainability"],
)
def explain_shap(
    request: ShapRequest,
) -> ShapResponse:
    """
    Explain a frozen stress-related text prediction.

    SHAP contributions use class-1 log-odds.
    No model retraining is performed.
    """

    try:
        result = explain_text_shap(
            text=request.text,
            top_k=request.top_k,
        )

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail="SHAP reference data unavailable",
        ) from exc

    except (ValueError, TypeError, RuntimeError) as exc:
        raise HTTPException(
            status_code=503,
            detail="SHAP explanation unavailable",
        ) from exc

    return ShapResponse(**result)


# ============================================================
# 5. LIME Local Explanation Endpoint
# POST /explain/lime
# ============================================================

@app.post(
    "/explain/lime",
    response_model=LimeResponse,
    tags=["Explainability"],
)
def explain_lime(
    request: LimeRequest,
) -> LimeResponse:
    """
    Generate a LIME explanation for the frozen
    stress-related text classifier.

    Returns local surrogate weights, fidelity,
    and approximation error.

    No model retraining is performed.
    """

    try:
        result = explain_text_lime(
            text=request.text,
            top_k=request.top_k,
        )

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail="Prediction model unavailable",
        ) from exc

    except (ValueError, TypeError, RuntimeError) as exc:
        raise HTTPException(
            status_code=503,
            detail="LIME explanation unavailable",
        ) from exc

    return LimeResponse(**result)
