from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import time
import uuid
import joblib
import numpy as np

from app.logging_config import logger
from app.models.schemas import PredictionInput, PredictionOutput

app = FastAPI()

# ✅ Middleware (logs every request)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    # Generate request ID
    request.state.request_id = str(uuid.uuid4())

    response = await call_next(request)

    process_time = time.time() - start_time

    logger.info(
        f"{request.method} {request.url.path} | "
        f"request_id={request.state.request_id} | "
        f"time={process_time:.4f}s"
    )

    return response


# Global variables
model = None
le = None

# ✅ Load model once
@app.on_event("startup")
def load_model():
    global model, le
    model = joblib.load("ml/saved_model/model.joblib")
    le = joblib.load("ml/saved_model/label_encoder.joblib")

    logger.info("Model & Encoder loaded successfully")


# Root
@app.get("/")
def root():
    return {"message": "ML API is alive"}


# ✅ Predict endpoint
@app.post("/predict", response_model=PredictionOutput)
def predict(request: Request, input_data: PredictionInput):
    request_id = request.state.request_id  

    try:
        data = np.array([[  
            input_data.sepal_length,
            input_data.sepal_width,
            input_data.petal_length,
            input_data.petal_width
        ]])

        prediction = model.predict(data)[0]
        confidence = float(model.predict_proba(data).max())

        result = le.inverse_transform([prediction])[0]

        # ✅ SUCCESS LOG
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
        # ✅ ERROR LOG
        logger.error(
            f"Prediction failed | request_id={request_id} | error={str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        )


# ✅ Health endpoint
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model_loaded": model is not None
    }


# ✅ Custom Exception Handler
@app.exception_handler(ValueError)
def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={
            "error": "Invalid data format",
            "detail": str(exc)
        }
    )