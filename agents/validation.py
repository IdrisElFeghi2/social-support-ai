import pandas as pd
import os

# Load the original mock data
df = pd.read_csv("test_data/mock_test_data.csv", encoding="utf-8-sig")
print(f"📥 Loaded dataset with {len(df)} rows")

# Apply validation rules:
# 1. Must be UAE national
# 2. Must be adult (age >= 18)
# 3. No KYC risk: name must match across documents
df_clean = df[
    (df["nationality"] == 1) &
    (df["age"] >= 18) &
    (df["full_name"] == df["name_in_bank"]) &
    (df["full_name"] == df["name_in_resume"])
]

# Save the validated clean dataset
output_path = "test_data/mock_test_data_validated.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df_clean.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"✅ Validated data saved to: {output_path}")
print(f"🧮 Remaining valid rows: {len(df_clean)}")
