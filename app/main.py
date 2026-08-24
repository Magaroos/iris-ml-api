from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

model = None  # global variable

# ✅ Load model ONCE at startup
@app.on_event("startup")
def load_model():
    global model
    model = joblib.load("ml/saved_model/model.joblib")
    print("✅ Model loaded successfully!")

@app.get("/")
def root():
    return {"message": "ML API is alive"}

# ✅ Accept input and predict
@app.post("/predict")
def predict():
    data = {
        "sepal length (cm)": 5.1,
        "sepal width (cm)": 3.5,
        "petal length (cm)": 1.4,
        "petal width (cm)": 0.2
    }

    df = pd.DataFrame([data])

    prediction = model.predict(df)

    return {"prediction": int(prediction[0])}