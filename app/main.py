from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time
import uuid
import joblib

from app.logging_config import logger
from app.routers.v1 import router as v1_router
from app.config import settings
from app.routers.v2 import router as v2_router


app = FastAPI(title=settings.API_TITLE)

# ✅ Load model once at startup
@app.on_event("startup")
def load_model():
    app.state.model = joblib.load(settings.MODEL_PATH)
    app.state.le = joblib.load("ml/saved_model/label_encoder.joblib")

    logger.info(f"Model loaded from {settings.MODEL_PATH}")


# ✅ Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    request.state.request_id = str(uuid.uuid4())

    response = await call_next(request)

    process_time = time.time() - start_time

    logger.info(
        f"{request.method} {request.url.path} | "
        f"request_id={request.state.request_id} | "
        f"time={process_time:.4f}s"
    )

    return response


# ✅ Include router
app.include_router(v1_router)
app.include_router(v2_router)


@app.get("/")
def root():
    return {"message": "ML API is alive (v1 ready)"}


# ✅ Global Exception Handler
@app.exception_handler(ValueError)
def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={
            "error": "Invalid data format",
            "detail": str(exc)
        }
    )