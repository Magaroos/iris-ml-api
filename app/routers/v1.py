from fastapi import APIRouter, HTTPException, Request
import numpy as np

from app.models.schemas import (
    PredictionInput,
    PredictionOutput,
    PredictionBatchInput,
    PredictionBatchOutput
)
from app.logging_config import logger

router = APIRouter(prefix="/api/v1")


# 🔹 Single Prediction
@router.post("/predict", response_model=PredictionOutput)
def predict(request: Request, input_data: PredictionInput):
    request_id = request.state.request_id

    try:
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


# 🔹 Batch Prediction (SIMPLIFIED)
@router.post("/predict-batch", response_model=PredictionBatchOutput)
def predict_batch(request: Request, input_data: PredictionBatchInput):
    request_id = request.state.request_id

    try:
        model = request.app.state.model
        le = request.app.state.le

        # ✅ Convert list → NumPy
        data = np.array([
            [
                item.sepal_length,
                item.sepal_width,
                item.petal_length,
                item.petal_width
            ]
            for item in input_data.inputs
        ])

        # ✅ Predict ALL at once
        preds = model.predict(data)
        probs = model.predict_proba(data)

        results = []

        # ✅ Loop only to format output (NOT prediction)
        for i in range(len(preds)):
            label = le.inverse_transform([preds[i]])[0]
            confidence = float(max(probs[i]))

            results.append(
                PredictionOutput(
                    prediction=label,
                    confidence=confidence,
                    request_id=request_id
                )
            )

        logger.info(
            f"Batch success | request_id={request_id} | count={len(results)}"
        )

        return PredictionBatchOutput(predictions=results)

    except Exception as e:
        logger.error(
            f"Batch failed | request_id={request_id} | error={str(e)}"
        )
        raise HTTPException(status_code=500, detail="Batch prediction failed")


# 🔹 Health Check
@router.get("/health")
def health_check(request: Request):
    return {
        "status": "ok",
        "model_loaded": hasattr(request.app.state, "model")
    }

# 🔹 It tells the user what model is running behind your API
@router.get("/model-info")
def model_info():
    return {
        "model_name": "RandomForestClassifier",
        "version": "v1",
        "features": [
            "sepal_length",
            "sepal_width",
            "petal_length",
            "petal_width"
        ]
    }