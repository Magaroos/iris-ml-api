from prometheus_client import Counter

prediction_counter = Counter(
    "prediction_requests_total",
    "Total number of prediction API calls"
)