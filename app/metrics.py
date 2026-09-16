from prometheus_client import Counter

prediction_counter = Counter(
    "prediction_counter_total",
    "Total number of predictions",
    ["prediction"]   # ✅ THIS LINE IS MANDATORY
)