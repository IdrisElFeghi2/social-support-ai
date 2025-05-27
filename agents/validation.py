# agents/validation.py
def validate_data(extracted_data: dict) -> dict:
    """
    Validates extracted data for consistency across documents.
    Returns cleaned and flagged data.
    """
    validated = extracted_data.copy()
    flags = []

    # Example check: income vs. bank info
    if 'bank_info' in extracted_data and 'resume_text' in extracted_data:
        if "salary" not in extracted_data['bank_info'].lower():
            flags.append("No salary detected in bank statement")

    validated['validation_flags'] = flags
    return validated
