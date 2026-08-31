from fastapi import APIRouter, HTTPException, Request
import numpy as np

from app.models.schemas import PredictionInput, PredictionOutput
from app.logging_config import logger

router = APIRouter(prefix="/api/v1")


@router.post("/predict", response_model=PredictionOutput)
def predict(request: Request, input_data: PredictionInput):
    request_id = request.state.request_id

    try:
        # ✅ Access model from app.state
        model = request.app.state.model
        le = request.app.state.le

        data = np.array([[
            input_data.sepal_length,
            input_data.sepal_width,
            input_data.petal_length,
            input_data.petal_width
        ]])

        prediction = model.predict(data)[0]
        confidence = float(model.predict_proba(data).max())
        result = le.inverse_transform([prediction])[0]

        logger.info(
            f"Prediction success | request_id={request_id} | "
            f"result={result} | confidence={confidence}"
        )

        return PredictionOutput(
            prediction=result,
            confidence=confidence,
            request_id=request_id
        )

    except Exception as e:
        logger.error(
            f"Prediction failed | request_id={request_id} | error={str(e)}"
        )

        raise HTTPException(status_code=500, detail="Prediction failed")


@router.get("/health")
def health_check(request: Request):
    return {
        "status": "ok",
        "model_loaded": hasattr(request.app.state, "model")
    }