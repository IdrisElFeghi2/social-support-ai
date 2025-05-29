import os
from utils.ocr_utils import (
    extract_text_from_image,
    extract_text_from_pdf,
    extract_text_from_pdf_with_ocr,
    extract_text_auto  # ✅ new unified function
)

def test_image_ocr():
    image_path = "test_data/emirates_id.jpg"
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return
    text = extract_text_from_image(image_path)
    print("\n🖼️ OCR Text from Image:")
    print(text)


def test_pdf_text_extraction():
    pdf_path = "test_data/Bank-Statement.pdf"
    if not os.path.exists(pdf_path):
        print(f"❌ PDF not found: {pdf_path}")
        return
    text = extract_text_from_pdf(pdf_path)
    print("\n📄 Extracted Text from PDF (without OCR):")
    print(text)


def test_scanned_image_or_pdf():
    file_path = "test_data/Scanned_Resume.png"  # Can be .png, .jpg, or .pdf
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    text = extract_text_auto(file_path, temp_image_folder="temp_images")
    print("\n📦 Extracted Text (auto-detected type):")
    print(text)


if __name__ == "__main__":
    print("🔍 Running OCR Tests...\n")
    # Uncomment to test individual functions
    #test_image_ocr()
    #test_pdf_text_extraction()
    test_scanned_image_or_pdf()
