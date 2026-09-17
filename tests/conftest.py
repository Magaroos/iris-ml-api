# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
import joblib
from app.config import settings
from app.main import app

@pytest.fixture(scope="session")
def client():
    """
    Create a TestClient for the FastAPI app with the ML model and label encoder
    loaded into app.state. DO NOT add a global X-API-Key header here — tests
    that validate security depend on missing/wrong headers.
    """
    # load model & label encoder once for tests
    app.state.model = joblib.load(settings.MODEL_PATH)
    # If your Settings includes LABEL_ENCODER_PATH use it else fallback
    try:
        le_path = settings.LABEL_ENCODER_PATH
    except AttributeError:
        le_path = "ml/saved_model/label_encoder.joblib"

    app.state.le = joblib.load(le_path)

    with TestClient(app) as client:
        yield client