import joblib

# Load saved model
model = joblib.load("ml/saved_model/model.joblib")

# Sample input (flower data)
sample = [[5.1, 3.5, 1.4, 0.2]]

# Predict
prediction = model.predict(sample)

print("Prediction:", prediction)