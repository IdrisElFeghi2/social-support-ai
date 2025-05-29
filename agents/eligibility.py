# agents/eligibility.py

import pickle
import numpy as np

# Load a pre-trained model
MODEL_PATH = "models/classifier.pkl"
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    model = None

def check_eligibility(data: dict) -> str:
    """
    Predict eligibility based on extracted and validated data.
    """
    if model is None:
        return "Model not available"

    # Dummy features (replace with real ones later)
    try:
        features = np.array([[5000, 4, 1]])  # income, family_size, employment_status
        prediction = model.predict(features)[0]
        return "Eligible" if prediction == 1 else "Not Eligible"
    except Exception as e:
        return f"Prediction failed: {e}"
