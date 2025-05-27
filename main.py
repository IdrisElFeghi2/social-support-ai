from agents.data_extraction import extract_data
from agents.validation import validate_data
from agents.eligibility import check_eligibility
from agents.recommendation import generate_recommendation

def run_pipeline(user_files):
    extracted = extract_data(user_files)
    validated = validate_data(extracted)
    eligibility = check_eligibility(validated)
    recommendation = generate_recommendation(validated)
    return {"eligibility": eligibility, "recommendation": recommendation}

if __name__ == "__main__":
    # Dummy file inputs for testing
    user_files = {}
    print(run_pipeline(user_files))
