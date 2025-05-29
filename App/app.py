import streamlit as st
import pandas as pd
from joblib import load
import os

# --- Load model ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, '..', 'models', 'random_forest_model.pkl')
model = load(model_path)

# --- Translation dictionary ---
translations = {
    "en": {
        "title": "Support Recommendation",
        "gender": "Gender",
        "gender_options": ["Male", "Female"],
        "age": "Age",
        "employment_status": "Employment Status",
        "employment_options": ["Employed", "Unemployed", "Self-employed", "Student"],
        "family_size": "Family Size",
        "assets": "Assets ($)",
        "liabilities": "Liabilities ($)",
        "credit_score": "Credit Score",
        "predict_button": "Get Recommendation",
        "result_prefix": "Recommended Support:",
        "predictions": [
            "Financial counseling",
            "Job matching / training",
            "No recommendation",
            "Retirement financial assistance"
        ]
    },
    "ar": {
        "title": "توصية بالدعم",
        "gender": "الجنس",
        "gender_options": ["ذكر", "أنثى"],
        "age": "العمر",
        "employment_status": "حالة التوظيف",
        "employment_options": ["موظف", "عاطل عن العمل", "عمل حر", "طالب"],
        "family_size": "حجم الأسرة",
        "assets": "الممتلكات (دولار)",
        "liabilities": "الالتزامات (دولار)",
        "credit_score": "درجة الائتمان",
        "predict_button": "احصل على التوصية",
        "result_prefix": "الدعم الموصى به:",
        "predictions": [
            "الاستشارات المالية",
            "توفير وظيفة / تدريب",
            "لا توجد توصية",
            "مساعدة مالية للتقاعد"
        ]
    }
}

# --- Language selection ---
lang = st.selectbox("Language / اللغة", ["English", "العربية"], key="language_select")
lang_code = "en" if lang == "English" else "ar"
t = translations[lang_code]

# --- Optional RTL Styling for Arabic ---
if lang_code == "ar":
    st.markdown("""
        <style>
        html, body, [class*="css"] {
            direction: rtl;
            text-align: right;
        }
        </style>
    """, unsafe_allow_html=True)

# --- Title ---
st.title(t["title"])

# --- User Inputs ---
gender = st.selectbox(t["gender"], t["gender_options"], key="gender_select")
age = st.number_input(t["age"], min_value=18, max_value=100, value=30)
employment_status = st.selectbox(t["employment_status"], t["employment_options"], key="employment_select")
family_size = st.number_input(t["family_size"], min_value=1, max_value=20, value=3)
assets = st.number_input(t["assets"], min_value=0.0, value=50000.0)
liabilities = st.number_input(t["liabilities"], min_value=0.0, value=10000.0)
credit_score = st.number_input(t["credit_score"], min_value=0, max_value=850, value=650)

# --- Encode Inputs for Model ---
gender_encoded = 1 if gender in ["Male", "ذكر"] else 0
employment_map = {
    "Employed": 0, "موظف": 0,
    "Unemployed": 1, "عاطل عن العمل": 1,
    "Self-employed": 2, "عمل حر": 2,
    "Student": 3, "طالب": 3
}
employment_encoded = employment_map[employment_status]

input_data = pd.DataFrame([{
    "gender": gender_encoded,
    "age": age,
    "employment_status": employment_encoded,
    "family_size": family_size,
    "assets": assets,
    "liabilities": liabilities,
    "credit_score": credit_score
}])

# --- Predict & Display Result ---
if st.button(t["predict_button"]):
    prediction = model.predict(input_data)[0]
    label = t["predictions"][prediction] if prediction < len(t["predictions"]) else "Unknown"
    st.success(f"{t['result_prefix']} {label}")
