def test_v1_vs_v2_difference(client):
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }

    res_v1 = client.post("/api/v1/predict", json=payload)
    res_v2 = client.post("/api/v2/predict", json=payload)

    assert res_v1.status_code == 200
    assert res_v2.status_code == 200

    data_v1 = res_v1.json()
    data_v2 = res_v2.json()

    # v1 vs v2 difference
    assert "confidence" in data_v1
    assert "probability" in data_v2

    # responses must be different
    assert data_v1 != data_v2

    # v2 has new field
    assert "model_version" in data_v2