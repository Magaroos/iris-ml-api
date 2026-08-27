from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request

import joblib
from app.models.schemas import PredictionInput, PredictionOutput
import uuid
import numpy as np

app = FastAPI()

model = None  # global variable
le = None     # label encoder

# ✅ Load model ONCE at startup
@app.on_event("startup")
def load_model():
    global model, le
    model = joblib.load("ml/saved_model/model.joblib")
    le = joblib.load("ml/saved_model/label_encoder.joblib")
    print("✅ Model & Encoder loaded!")

# ✅ Root endpoint
@app.get("/")
def root():
    return {"message": "ML API is alive"}

# ✅ Predict endpoint
@app.post("/predict", response_model=PredictionOutput)
def predict(input_data: PredictionInput):
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

        return PredictionOutput(
            prediction=result,
            confidence=confidence,
            request_id=str(uuid.uuid4())
        )

    except Exception as e:
        print("❌ Internal Error:", e)

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

# ✅ Custom Exception Handler (GLOBAL)
@app.exception_handler(ValueError)
def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={
            "error": "Invalid data format",
            "detail": str(exc)
        }
    )