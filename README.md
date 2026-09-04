🚀 ML Prediction API
📌 Overview

This project is a production-style Machine Learning API built using FastAPI.
It serves predictions from a trained model and demonstrates real-world backend practices like:

API design
Input validation
Batch processing
Configuration management
Logging
Automated testing
API versioning
🧠 What This API Does

The API predicts the class of an input using a trained ML model (Iris dataset).

It supports:

Single prediction
Batch prediction (multiple inputs)
Input validation
Versioned responses
⚙️ API Endpoints
🔹 Health Check
GET /api/v1/health
Response
{
  "status": "ok",
  "model_loaded": true
}
🔹 Single Prediction (v1)
POST /api/v1/predict
Request
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
Response
{
  "prediction": "setosa",
  "confidence": 0.95,
  "request_id": "abc-123"
}
🔹 Batch Prediction
POST /api/v1/predict-batch
Request
{
  "inputs": [
    { ... },
    { ... }
  ]
}
Response
{
  "predictions": [
    { "prediction": "...", "confidence": 0.9 },
    { "prediction": "...", "confidence": 0.8 }
  ]
}
🔹 Model Info
GET /api/v1/model-info
Response
{
  "model_name": "RandomForestClassifier",
  "version": "v1",
  "features": [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width"
  ]
}
🔹 Prediction (v2 - Updated API)
POST /api/v2/predict
Response
{
  "prediction": "setosa",
  "probability": 0.95,
  "model_version": "v2",
  "request_id": "abc-123"
}

👉 This version introduces changes without breaking older clients.

🔄 API Versioning

Two versions of the API exist:

Version	Purpose
v1	Original stable API
v2	Updated API with improved response
Key Differences
v1	v2
confidence	probability
❌ No version info	✅ Includes model_version

👉 This ensures backward compatibility

📦 Project Structure
ml-api-project/
│
├── app/
│   ├── main.py            # Entry point
│   ├── config.py         # Environment settings
│   ├── routers/
│   │   ├── v1.py         # Version 1 API
│   │   └── v2.py         # Version 2 API
│   ├── models/
│   │   └── schemas.py    # Request/Response models
│   ├── logging_config.py # Logging setup
│
├── ml/
│   └── saved_model/      # Trained model files
│
├── tests/                # Automated tests
│   ├── conftest.py
│   ├── test_health.py
│   ├── test_predict.py
│   ├── test_batch.py
│   ├── test_batch_limit.py
│   ├── test_predict_fail.py
│   └── test_v2.py
│
├── .env                  # Environment variables
├── requirements.txt
└── README.md
⚙️ Configuration (.env)

The project uses environment variables for flexibility.

Example:

MAX_BATCH_SIZE=5
MODEL_PATH=ml/saved_model/model.joblib

👉 Changes require server restart

🧪 Testing (Pytest)

Automated tests ensure API reliability.

Covered Cases:
✅ Health check
✅ Successful prediction
✅ Invalid input (422 error)
✅ Batch prediction
✅ Batch size limit (400 error)
✅ Version comparison (v1 vs v2)
▶ Run Tests
python -m pytest -v
Example Output
6 passed, 0 failed
🛡️ Validation & Error Handling

The API uses Pydantic for validation.

Handles:
Missing fields → 422 Unprocessable Entity
Invalid types → 422
Batch overflow → 400 Bad Request
Internal errors → 500 Internal Server Error
📊 Logging

Each request is tracked with:

request_id
Response status
Errors

👉 Helps in debugging and monitoring

🚀 How to Run
1. Install dependencies
pip install -r requirements.txt
2. Start server
uvicorn app.main:app --reload
3. Open Swagger UI
http://127.0.0.1:8000/docs
🧠 Key Concepts Demonstrated
API development using FastAPI
Machine Learning model serving
Config-driven architecture
Batch processing
API versioning
Automated testing
Error handling and validation
📌 Conclusion

This project demonstrates how to build a scalable, testable, and production-ready ML API with proper engineering practices.