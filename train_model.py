import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
df = pd.read_csv("disease_dataset.csv")

# Features and labels
X = df[["temperature", "bpm", "spo2"]]
y = df["disease"]

# Encode labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Train model
model = LogisticRegression()
model.fit(X, y_encoded)

# Save model and encoder
joblib.dump(model, "disease_model.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")

print("✅ Model and label encoder saved.")
