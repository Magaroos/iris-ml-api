🚀 ML Prediction API (Dockerized with Compose)

📌 Overview

This project is a **production-style Machine Learning API** built using **FastAPI** and fully containerized using **Docker and Docker Compose**.

It serves predictions from a trained ML model (Iris dataset) and demonstrates **real-world backend + DevOps practices**.

---

🧠 What This API Does

The API predicts the class of an input flower using a trained Machine Learning model.

It supports:

- ✅ Single prediction
- ✅ Batch prediction (multiple inputs)
- ✅ Input validation
- ✅ API versioning (v1 & v2)
- ✅ Structured responses
- ✅ Logging & request tracking

---

⚙️ Tech Stack

- **Backend**: FastAPI
- **Machine Learning**: Scikit-learn
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Testing**: Pytest
- **Config Management**: Environment Variables (.env)

---

⚙️ API Endpoints

🔹 Health Check

`GET /api/v1/health`

```json
{
  "status": "ok",
  "model_loaded": true
}
 
🔹 Single Prediction (v1)
  POST /api/v1/predict
  {
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
  }
  Response : 
  {
  "prediction": "setosa",
  "confidence": 0.95,
  "request_id": "abc-123"
  }
  
🔹 Batch Prediction
  POST /api/v1/predict-batch
  {
  "inputs": [
    { ... },
    { ... }
  ]
  }
  
🔹 Model Info
  GET /api/v1/model-info
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
  {
    "prediction": "setosa",
    "probability": 0.95,
    "model_version": "v2",
    "request_id": "abc-123"
  }
  
🔄 API Versioning
  Version	    Purpose
  v1	        Stable API
  v2	        Improved response
  
Key Differences
v1	                        v2
confidence	                probability

❌ No version info	        ✅ Includes model_version


📦 Project Structure
ml-api-project/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── routers/
│   │   ├── v1.py
│   │   └── v2.py
│   ├── models/
│   │   └── schemas.py
│   ├── logging_config.py
│
├── ml/
│   └── saved_model/
│
├── tests/
│
├── .env
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

⚙️ Configuration (.env)

Environment variables are used instead of hardcoding values.

Example:
      MODEL_PATH=ml/saved_model/model.joblib
      MAX_BATCH_SIZE=5
      API_TITLE=ML Prediction API
      LOG_LEVEL=INFO

👉 Used by Docker Compose at runtime

🐳 Docker & Containerization

This project is fully containerized.

🔹 Dockerfile :
    -> Defines how the application is built
    -> Installs dependencies
    -> Runs FastAPI using Uvicorn

🔹 Docker Compose :
    -> Manages container setup
    -> Handles environment variables
    -> Maps ports
    -> Supports volume mounting

🔹 Volume Usage
    ./ml/saved_model:/app/ml/saved_model

    👉 Allows real-time model updates without rebuilding image


🧪 Testing (Pytest)
Run tests:
    pytest -v

Covered Cases:
    ✅ Health check
    ✅ Valid prediction
    ✅ Invalid input (422)
    ✅ Batch prediction
    ✅ Batch limit validation
    ✅ API version testing


🛡️ Validation & Error Handling
Handled using Pydantic:
    - Missing fields → 422
    - Invalid data types → 422
    - Batch overflow → 400
    - Server errors → 500

📊 Logging
Each request includes:
  -> request_id
  -> logs for debugging
  -> error tracking


🚀 Key Concepts Demonstrated
    - FastAPI API development
    - ML model serving
    - Docker containerization
    - Docker Compose orchestration
    - Environment-based configuration
    - API versioning
    - Automated testing
    - Logging & validation



📌 Conclusion

This project demonstrates how to build a scalable, maintainable, and production-ready ML API with modern backend and DevOps practices.

It is designed to be:
    ✅ Portable (runs anywhere using Docker)
    ✅ Reproducible
    ✅ Easy to deploy
    ✅ Industry-ready

## 🚀 How to Run This Project (Using Docker Compose)

### 📌 Prerequisites

- Docker installed  
- Docker Desktop running  

---

### ▶️ Step 1: Clone the Repository

```bash
git clone <your-repo-link>
cd ml-api-project
```

---

### ▶️ Step 2: Run the Application

```bash
docker compose up --build
```

---

### ▶️ Step 3: Access the API

Open your browser:

```
http://localhost:8000/docs
```

Swagger UI will open.

---

### ▶️ Step 4: Stop the Application

```bash
docker compose down
```

---

### ⚡ Optional: Run in Background

```bash
docker compose up -d
```

---

### 📌 Notes

- Environment variables are loaded from `.env`  
- Model is loaded using volume mapping  
- No manual setup required  