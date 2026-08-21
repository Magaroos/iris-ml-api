import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset from CSV
data = pd.read_csv("data/iris_dataset.csv")

# Show data (for checking)
print(data.head())
print("Columns:", data.columns)

# Split into input (X) and output (y)
X = data.drop("species", axis=1)   # features
y = data["species"]                # target

# Convert text labels to numbers (setosa → 0, etc.)
le = LabelEncoder()
y = le.fit_transform(y)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Train size:", len(X_train))
print("Test size:", len(X_test))

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Save model
joblib.dump(model, "ml/saved_model/model.joblib")
print("Model saved successfully!")