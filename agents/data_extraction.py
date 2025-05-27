# agents/data_extraction.py
import pytesseract
from pdfplumber import open as pdf_open
from PIL import Image
import pandas as pd

def extract_data(files: dict) -> dict:
    """
    Extract data from uploaded documents.
    files: dict with keys like 'id_image', 'bank_statement', 'resume', 'excel_sheet'
    Returns: dict of structured extracted information
    """
    extracted = {}

    # OCR from ID image
    if 'id_image' in files:
        id_text = pytesseract.image_to_string(Image.open(files['id_image']))
        extracted['id_info'] = id_text

    # PDF text extraction
    if 'bank_statement' in files:
        with pdf_open(files['bank_statement']) as pdf:
            pages = [page.extract_text() for page in pdf.pages]
            extracted['bank_info'] = "\n".join(pages)

    # Resume text
    if 'resume' in files:
        with open(files['resume'], 'r', encoding='utf-8') as f:
            extracted['resume_text'] = f.read()

    # Excel sheet for assets/liabilities
    if 'excel_sheet' in files:
        df = pd.read_excel(files['excel_sheet'])
        extracted['assets_liabilities'] = df.to_dict(orient='records')

    return extracted
