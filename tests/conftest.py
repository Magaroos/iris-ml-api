import pytest
from fastapi.testclient import TestClient
from app.main import app
import joblib
from app.config import settings


@pytest.fixture
def client():
    # ✅ manually load model for tests
    app.state.model = joblib.load(settings.MODEL_PATH)
    app.state.le = joblib.load("ml/saved_model/label_encoder.joblib")

    return TestClient(app)