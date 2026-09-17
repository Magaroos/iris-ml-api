def test_predict_invalid_input(client):
    payload = {
        "sepal_length": 2.0  
    }

    response = client.post("/api/v1/predict", json=payload)

    assert response.status_code == 422