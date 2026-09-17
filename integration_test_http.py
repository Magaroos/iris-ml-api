# integration_test_http.py
import requests
import os
import sys
import time
from typing import Any

BASE = os.getenv("BASE_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "mysecretkey")
HEADERS = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}
TIMEOUT = 10

def call(method: str, path: str, json: Any = None):
    url = f"{BASE}{path}"
    try:
        if method.lower() == "get":
            r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        else:
            r = requests.post(url, headers=HEADERS, json=json, timeout=TIMEOUT)
        return r
    except Exception as e:
        print(f"ERROR calling {url}: {e}")
        return None

def pretty_check(r, expected_status=200, show_body=True):
    if r is None:
        print("  -> Request failed (no response)\n")
        return False
    ok = (r.status_code == expected_status)
    print(f"  URL: {r.request.method} {r.url}")
    print(f"  Status: {r.status_code} (expected {expected_status})")
    if show_body:
        try:
            print("  Body:", r.json())
        except Exception:
            text = r.text or "<no body>"
            print("  Body (text):", text[:400])
    print()
    return ok

def main():
    print("Integration test: hitting running container at", BASE)
    all_ok = True

    # 1) /api/v1/predict
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    print("1) POST /api/v1/predict")
    r = call("post", "/api/v1/predict", json=payload)
    ok = pretty_check(r, expected_status=200)
    all_ok &= ok

    # 2) /api/v1/predict-batch
    batch_payload = {
        "inputs": [
            {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2},
            {"sepal_length": 6.2, "sepal_width": 2.8, "petal_length": 4.8, "petal_width": 1.8}
        ]
    }
    print("2) POST /api/v1/predict-batch")
    r = call("post", "/api/v1/predict-batch", json=batch_payload)
    ok = pretty_check(r, expected_status=200)
    all_ok &= ok

    # 3) /api/v1/health
    print("3) GET /api/v1/health")
    r = call("get", "/api/v1/health")
    ok = pretty_check(r, expected_status=200)
    all_ok &= ok

    # 4) /api/v1/model-info
    print("4) GET /api/v1/model-info")
    r = call("get", "/api/v1/model-info")
    ok = pretty_check(r, expected_status=200)
    all_ok &= ok

    # 5) /metrics
    print("5) GET /metrics (Prometheus metrics endpoint)")
    r = call("get", "/metrics")
    ok = pretty_check(r, expected_status=200, show_body=False)
    if r is not None:
        print("  metrics snippet:")
        print(r.text[:800])
        print()
    all_ok &= (r is not None and r.status_code == 200)

    print("SUMMARY: All checks passed?" , all_ok)
    if not all_ok:
        sys.exit(2)
    else:
        print("Integration test PASSED.")
        sys.exit(0)

if __name__ == "__main__":
    main()