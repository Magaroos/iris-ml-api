def test_no_api_key(client):
    response = client.post("/api/v1/predict", json={
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    })
    assert response.status_code == 422 or response.status_code == 401


def test_wrong_api_key(client):
    response = client.post(
        "/api/v1/predict",
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        },
        headers={"X-API-Key": "wrong"}
    )
    assert response.status_code == 401


def test_extra_field(client):
    response = client.post(
        "/api/v1/predict",
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
            "extra": 123
        },
        headers={"X-API-Key": "mysecretkey"}
    )
    assert response.status_code == 422