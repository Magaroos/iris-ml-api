from fastapi import FastAPI
import joblib
import pandas as pd
from app.models.schemas import PredictionInput
import uuid

app = FastAPI()

model = None  # global variable
le = None

# ✅ Load model ONCE at startup
@app.on_event("startup")
def load_model():
    global model, le
    model = joblib.load("ml/saved_model/model.joblib")
    le = joblib.load("ml/saved_model/label_encoder.joblib")
    print("✅ Model & Encoder loaded!")

@app.get("/")
def root():
    return {"message": "ML API is alive"}

# ✅ Accept input and predict
@app.post("/predict")
def predict(input_data: PredictionInput):

    data = {
        "sepal length (cm)": input_data.sepal_length,
        "sepal width (cm)": input_data.sepal_width,
        "petal length (cm)": input_data.petal_length,
        "petal width (cm)": input_data.petal_width
    }

    df = pd.DataFrame([data])

    prediction = model.predict(df)

    # ✅ confidence score
    probabilities = model.predict_proba(df)
    confidence = max(probabilities[0])

    # ✅ convert number → label
    predicted_label = le.inverse_transform(prediction)

    # ✅ unique request id
    request_id = str(uuid.uuid4())

    return {
        "prediction": predicted_label[0],
        "confidence": round(float(confidence), 3),
        "request_id": request_id
    }

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model_loaded": model is not None
    }