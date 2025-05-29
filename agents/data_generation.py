import random
import pandas as pd
import os

# Arabic name data
male_first_names = [
    "أحمد", "محمد", "علي", "سعيد", "يوسف", "عبدالله", "إبراهيم", "خالد", "فهد", "راشد",
    "سليمان", "عبدالرحمن", "عمر", "سعود", "جاسم", "مازن", "أنور", "طارق", "بدر", "سامي"
]

female_first_names = [
    "فاطمة", "مريم", "خديجة", "ليلى", "سارة", "أمينة", "زينب", "هند", "جميلة", "نورة",
    "عائشة", "لطيفة", "شيماء", "دلال", "نجلاء", "عبير", "أروى", "ريما", "عهد", "منيرة"
]

family_names = [
    "النعيمي", "الكتبي", "الهاشمي", "الأنصاري", "الظاهري", "التميمي", "الشيخ", "المهيري", "العلي", "السويدي",
    "الحمادي", "الشامسي", "الرشيدي", "القاسمي", "المنصوري", "الدوسري", "الحربي", "الزيدي", "العنزي", "الهاجري"
]

# Emirates ID generator
def generate_emirates_id():
    return f"784-{random.randint(1000,9999)}-{random.randint(1000000,9999999)}-{random.randint(0,9)}"

# Name mismatch logic
def introduce_name_mismatch(original_name):
    while True:
        new_name = f"{random.choice(male_first_names + female_first_names)} {random.choice(family_names)}"
        if new_name != original_name:
            return new_name

# Eligibility assessment (age-aware)
def assess_eligibility(row):
    score = 0

    if 18 <= row["age"] < 60:
        if row["employment_status"] == 0:
            score += 1
        if row["family_size"] == 1:
            score += 1
        if row["assets"] == 0:
            score += 1
        if row["liabilities"] == 1:
            score += 1
        if row["credit_score"] == 0:
            score += 1

    elif row["age"] >= 60:
        if row["nationality"] == 1 and (row["assets"] == 0 or row["credit_score"] == 0):
            score = 5

    if score >= 5:
        return "Strong Approve"
    elif score >= 3:
        return "Approve"
    elif score >= 1:
        return "Soft Decline"
    else:
        return "Reject"

# Enablement recommendations
def recommend_support(row):
    recs = []

    if row["employment_status"] == 0 and 18 <= row["age"] < 60:
        recs.append("Job matching / training")

    if row["credit_score"] == 0:
        recs.append("Financial counseling")

    if row["full_name"] != row["name_in_bank"]:
        recs.append("KYC verification")

    if row["age"] >= 60 and row["nationality"] == 1:
        recs.append("Retirement financial assistance")

    return ", ".join(recs) if recs else "No recommendation"

# Main data generation
def generate_applicants(n=800, mismatch_bank=30, mismatch_resume=20, non_uae_count=10):
    applicants = []
    non_uae_indices = set(random.sample(range(n), non_uae_count))

    for i in range(n):
        gender = random.choice([0, 1])
        first_name = random.choice(male_first_names) if gender == 0 else random.choice(female_first_names)
        last_name = random.choice(family_names)
        full_name = f"{first_name} {last_name}"
        eid = generate_emirates_id()
        age = random.choices(
            population=list(range(18, 80)),
            weights=[2 if x < 60 else 1 for x in range(18, 80)],
            k=1
        )[0]

        name_in_bank = introduce_name_mismatch(full_name) if i < mismatch_bank else full_name
        name_in_resume = introduce_name_mismatch(full_name) if i < mismatch_resume else full_name
        nationality = 0 if i in non_uae_indices else 1

        applicant = {
            "full_name": full_name,
            "gender": gender,
            "emirates_id": eid,
            "age": age,
            "nationality": nationality,
            "name_in_bank": name_in_bank,
            "name_in_resume": name_in_resume,
            "employment_status": random.choice([0, 1]),
            "family_size": random.choice([0, 1]),
            "assets": random.choice([0, 1]),
            "liabilities": random.choice([0, 1]),
            "credit_score": random.choice([0, 1])
        }
        applicants.append(applicant)

    df = pd.DataFrame(applicants)
    df["eligibility_decision"] = df.apply(assess_eligibility, axis=1)
    df["enablement_recommendation"] = df.apply(recommend_support, axis=1)
    return df

# Create and save the dataset
df = generate_applicants()

output_path = "test_data/mock_test_data.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

df.to_csv(output_path, index=False, encoding="utf-8-sig")
print(f"Saved mock data to: {output_path}")
print(df.head())
