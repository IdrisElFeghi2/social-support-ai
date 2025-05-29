import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import warnings
warnings.filterwarnings("ignore")

# Load the cleaned dataset
df = pd.read_csv("test_data/mock_test_data_validated.csv", encoding="utf-8-sig")
print(f"✅ Loaded {len(df)} valid rows")

# Extract the first recommendation only (if multiple)
df["main_recommendation"] = df["enablement_recommendation"].apply(lambda x: x.split(",")[0].strip())

# Encode recommendation labels
label_encoder = LabelEncoder()
df["recommendation_label"] = label_encoder.fit_transform(df["main_recommendation"])

# Features to use
feature_cols = ["gender", "age", "employment_status", "family_size", "assets", "liabilities", "credit_score"]
X = df[feature_cols]
y = df["recommendation_label"]

# Shuffle and split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.5, shuffle=True, random_state=42
)

# Train a classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Predict on test set
y_pred = clf.predict(X_test)

model_path = "models/random_forest_model.pkl"
joblib.dump(clf, model_path)
print(f"✅ Model saved to {model_path}")

# Show confusion matrix
cm = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=label_encoder.classes_)

print("📊 Confusion Matrix:")
print(cm)

print("\n📋 Classification Report:")
print(report)

# 🔥 Plot Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=label_encoder.classes_,
            yticklabels=label_encoder.classes_)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix - Random Forest Recommendation Model')
plt.tight_layout()
plt.savefig("test_data/confusion_matrix_rf.png", dpi=300)
print("🖼️ Saved confusion matrix plot to: test_data/confusion_matrix_rf.png")
plt.show()
