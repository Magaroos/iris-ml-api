from fastapi import FastAPI
import joblib
import pandas as pd
from app.models.schemas import PredictionInput

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
def predict(input: PredictionInput):

    data = {
        "sepal length (cm)": input.sepal_length,
        "sepal width (cm)": input.sepal_width,
        "petal length (cm)": input.petal_length,
        "petal width (cm)": input.petal_width
    }

    df = pd.DataFrame([data])

    prediction = model.predict(df)

    predicted_label = le.inverse_transform(prediction)

    return {"prediction": predicted_label[0]}