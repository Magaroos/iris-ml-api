# 🚀 ML Prediction API (Dockerized with Compose)

## 📌 Overview
This is a **production-style Machine Learning API** built with **FastAPI** and containerized with **Docker / Docker Compose**.  
It serves predictions from a trained model (Iris dataset) and demonstrates backend + DevOps practices: validation, versioned endpoints, logging, Prometheus metrics, integration & load testing, and containerized runs.

---

## 🧠 What this API does
- Predicts the Iris flower class from 4 numeric features.
- Supports single and batch predictions.
- Exposes Prometheus-format metrics for monitoring.
- Has basic API key protection for endpoints (header `X-API-Key`).

### Key features
- ✅ Single prediction (`/api/v1/predict`)  
- ✅ Batch prediction (`/api/v1/predict-batch`)  
- ✅ Input validation with Pydantic  
- ✅ API versioning (`/api/v1`, `/api/v2`)  
- ✅ Logging with request IDs  
- ✅ Prometheus metrics (`/metrics`) with labeled prediction counts  
- ✅ Dockerized + Compose orchestration  
- ✅ Unit tests (pytest), integration test (HTTP against running container), and a basic load test

---

## ⚙️ Tech stack
- Backend: **FastAPI**  
- ML: **scikit-learn** (pretrained RandomForest)  
- Containerization: **Docker**, **Docker Compose**  
- Monitoring: **Prometheus** (optional service), in-app metrics via `prometheus_fastapi_instrumentator`  
- Testing: **pytest**, custom `integration_test_http.py`, `load_test.py`  
- Config: environment variables from `.env`

---

## 📁 Project structure (short)

ml-api-project/
├── app/
│ ├── main.py
│ ├── config.py
│ ├── metrics.py
│ ├── security.py
│ ├── routers/
│ │ ├── v1.py
│ │ └── v2.py
│ ├── models/
│ │ └── schemas.py
│ ├── logging_config.py
├── ml/
│ └── saved_model/
│ ├── model.joblib
│ └── label_encoder.joblib
├── tests/
├── integration_test_http.py
├── load_test.py
├── TESTING.md
├── test_results.txt
├── .env
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md


---

## ⚙️ Configuration (.env)
Use environment variables (do **not** commit secrets). Example `.env`:

MODEL_PATH=ml/saved_model/model.joblib
LABEL_ENCODER_PATH=ml/saved_model/label_encoder.joblib
API_TITLE=ML API
MAX_BATCH_SIZE=3
LOG_LEVEL=INFO
API_KEY=mysecretkey

> The app reads these at startup via `pydantic-settings`.

---

## 🔌 API Endpoints & Examples

### 🔹 Health check
**GET** `/api/v1/health`  
Response:
```json
{
  "status": "ok",
  "model_loaded": true
}
🔹 Single prediction (v1)

POST /api/v1/predict
Request body:

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
  "request_id": "uuid"
}
🔹 Batch prediction (v1)

POST /api/v1/predict-batch
Request:

{
  "inputs": [
    {"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2},
    {"sepal_length":6.2,"sepal_width":2.8,"petal_length":4.8,"petal_width":1.8}
  ]
}

Response:

{
  "predictions": [
    {"prediction":"setosa","confidence":1.0,"request_id":"uuid"},
    {"prediction":"virginica","confidence":0.95,"request_id":"uuid"}
  ]
}
🔹 Model info

GET /api/v1/model-info
Response:

{
  "model_name": "RandomForestClassifier",
  "version": "v1",
  "features": ["sepal_length","sepal_width","petal_length","petal_width"]
}
🔹 V2 prediction

POST /api/v2/predict
Response includes model_version and uses the key probability instead of confidence.

🔐 Authorization (local dev)

Protected endpoints expect header:

X-API-Key: mysecretkey

You can use Swagger UI (http://localhost:8000/docs) → Authorize to set X-API-Key.

📊 Metrics (Prometheus)
Endpoint: GET /metrics
The app uses prometheus_fastapi_instrumentator and registers a labeled counter:
prediction_counter_total{prediction="<label>"}
Example snippet:
# TYPE prediction_counter_total counter
prediction_counter_total{prediction="setosa"}  17.0
prediction_counter_total{prediction="virginica"} 10.0

Note: You can optionally add a Prometheus container in docker-compose.yml to scrape /metrics and add Grafana for dashboards.

🧪 Testing
Unit tests (pytest)

Run locally in venv:

python -m pytest -q

Expected (project): 9 passed (your local run may vary).

Saved test output: test_results.txt

Integration test (hits running container)

File: integration_test_http.py — runs HTTP requests against http://localhost:8000.
Run after docker compose up --build:

python integration_test_http.py

Expect: "Integration test PASSED."

Load test (basic)

File: load_test.py — sends concurrent requests to /api/v1/predict to exercise the service and metrics. Example random input snippet:

import random
DATA = {
  "sepal_length": random.uniform(4.0, 7.0),
  "sepal_width": random.uniform(2.0, 4.5),
  "petal_length": random.uniform(1.0, 6.0),
  "petal_width": random.uniform(0.1, 2.5)
}

Run:

python load_test.py

Watch /metrics to confirm counters increment.

🐳 Docker & run
Prerequisites
Docker (Desktop) installed and running
(Optional) Docker Compose v2 (or docker compose CLI)
Start (development / local)

From project root:

docker compose up --build

App will be at: http://localhost:8000
Swagger UI: http://localhost:8000/docs

Stop:

docker compose down

Notes:

Compose may show a warning about the top-level version field — harmless but you can remove version: "3.9" from docker-compose.yml if you prefer.

If container starts then immediately exits (Exited 0), check container logs:

docker compose ps -a
docker logs ml-api-container --tail 200
🛠 Troubleshooting (common issues)
Docker can't connect: ensure Docker Desktop (daemon) is running.
500 / 401 errors in Swagger: ensure X-API-Key is set in Authorize or when calling endpoints.
Pytest fails with encoding error reading test_results.txt: ensure test_results.txt is plain text (UTF-8). If binary got in accidentally, remove/replace it.
Port conflict: ensure nothing else listens on 8000.
✅ What was added in Task 18 & 19 (short)
Task 18: Prometheus instrumentation and metrics (app exposes /metrics and prediction_counter_total).
Task 19: Integration tests (HTTP against running container) and load test script; fixed issues found; documented testing in TESTING.md, saved test_results.txt.
🔮 Next steps / suggestions
Add Grafana dashboard to visualize /metrics.
Add GitHub Actions to run pytest on PRs.
Add CI job to run integration test against a Docker Compose environment.
Add graceful shutdown logging and liveness/readiness endpoints for Kubernetes readiness probes.
🧾 Useful commands (copy-paste)

Start locally (build + run):

docker compose up --build

Run unit tests locally:

python -m pytest -q

Run integration test against running container:

python integration_test_http.py

Run load test:

python load_test.py

Open Swagger UI:

http://localhost:8000/docs

Check metrics:

http://localhost:8000/metrics
📌 Conclusion

This repo demonstrates how to serve an ML model with a robust FastAPI service, containerize it, add observability (Prometheus metrics), and test it end-to-end (unit, integration, load). It’s portable, reproducible, and ready for the next steps: CI/CD, monitoring dashboards, and more advanced deployment.