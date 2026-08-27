# 🌸 Iris Flower Classification API

## 🚀 Project Overview

This project is a **Machine Learning API** built using FastAPI that predicts the species of an Iris flower based on its measurements.

The API takes user input, validates it, sends it to a trained ML model, and returns:
- 🌼 Predicted flower species
- 📊 Confidence score
- 🆔 Unique request ID

---

## 🧠 Features

- ✅ ML model using RandomForest
- ✅ FastAPI backend
- ✅ Input validation using Pydantic
- ✅ Structured API responses
- ✅ Error handling (422, 500)
- ✅ Custom exception handling
- ✅ Health check endpoint
- ✅ Confidence score output

---

## 🛠️ Tech Stack

- ⚡ FastAPI
- 🤖 Scikit-learn
- 🐼 Pandas
- 🔢 NumPy
- 📦 Joblib

---

📁 Project Structure (Cleaned)
## 📁 Project Structure


ml-api-project1/
├── app/
│ ├── main.py # FastAPI app
│ └── models/
│ └── schemas.py # Pydantic schemas
│
├── ml/
│ ├── train.py # Model training
│ └── saved_model/
│ ├── model.joblib
│ └── label_encoder.joblib
│
├── data/
│ └── iris_dataset.csv
│
├── tests/
│ └── test_model.py
│
└── README.md


---

## ⚙️ How It Works (Cleaner)

```md
## ⚙️ How It Works

1. Train model using `train.py`
2. Save model using `joblib`
3. FastAPI loads model at startup
4. User sends request via Swagger UI
5. Pydantic validates input
6. Model predicts output
7. API returns structured response
📡 API Endpoints (Clean Look)
## 📡 API Endpoints

### 🔹 POST `/predict`

**Request:**
```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}

Response:

{
  "prediction": "setosa",
  "confidence": 0.95,
  "request_id": "abc-123"
}
🔹 GET /health
{
  "status": "ok",
  "model_loaded": true
}

---

## ❗ Error Handling (Table Fix)

```md
## ❗ Error Handling

| Code | Meaning          |
|------|------------------|
| 200  | Success          |
| 422  | Invalid input    |
| 400  | Bad request      |
| 500  | Server error     |