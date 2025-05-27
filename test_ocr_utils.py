from utils.ocr_utils import (
    extract_text_from_image,
    extract_text_from_pdf,
    extract_text_from_pdf_with_ocr
)
import os


def test_image_ocr():
    image_path = "test_data/emirates_id.jpg"    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return
    text = extract_text_from_image(image_path)
    print("\n🖼️ OCR Text from Image:")
    print(text)


def test_pdf_ocr():
    pdf_path = "test_data/Bank-Statement.pdf"
    if not os.path.exists(pdf_path):
        print(f"❌ PDF not found: {pdf_path}")
        return
    text = extract_text_from_pdf(pdf_path)
    print("\n📄 Text Extracted from PDF (without OCR):")
    print(text)


def test_scanned_pdf_with_ocr():
    pdf_path = "test_data/Scanned_Resume.png"
    if not os.path.exists(pdf_path):
        print(f"❌ PDF not found: {pdf_path}")
        return
    text = extract_text_from_pdf_with_ocr(pdf_path, temp_image_folder="temp_images")
    print("\n📄 OCR Text from Scanned PDF:")
    print(text)


if __name__ == "__main__":
    print("🔍 Running OCR Tests...\n")
    #test_image_ocr()
    #test_pdf_ocr()
    test_scanned_pdf_with_ocr()
