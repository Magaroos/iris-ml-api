from app.config import settings

def test_batch_limit(client):
    payload = {
        "inputs": [
            {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            },
            {
                "sepal_length": 6.2,
                "sepal_width": 2.8,
                "petal_length": 4.8,
                "petal_width": 1.8
            },
            {
                "sepal_length": 7.0,
                "sepal_width": 3.2,
                "petal_length": 5.0,
                "petal_width": 1.5
            }
        ]
    }

    # 👇 only fails if MAX_BATCH_SIZE < 3
    if settings.MAX_BATCH_SIZE < 3:
        response = client.post("/api/v1/predict-batch", json=payload)
        assert response.status_code == 400