from fastapi import APIRouter, HTTPException, Request, Depends
import numpy as np

from app.models.schemas import PredictionInput
from app.logging_config import logger
from app.security import verify_api_key

router = APIRouter(prefix="/api/v2")


# 🔐 V2 Prediction (Protected)
@router.post("/predict")
def predict_v2(
    request: Request,
    input_data: PredictionInput,
    dep=Depends(verify_api_key)   
):
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
        probability = float(model.predict_proba(data).max())
        result = le.inverse_transform([prediction])[0]

        logger.info(
            f"V2 Prediction success | request_id={request_id}"
        )

        return {
            "prediction": result,
            "probability": probability,
            "model_version": "v2",
            "request_id": request_id
        }

    except Exception as e:
        logger.error(
            f"V2 Prediction failed | request_id={request_id} | error={str(e)}"
        )
        raise HTTPException(status_code=500, detail="Prediction failed")