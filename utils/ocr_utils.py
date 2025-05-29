import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import os
import io
import mimetypes

def extract_text_auto(file_path: str, temp_image_folder: str = "temp_images") -> str:
    """
    Automatically detect file type (image or PDF) and extract text using the appropriate method.
    Falls back to OCR for scanned PDFs.
    """
    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type is None:
        print(f"❌ Could not determine file type for: {file_path}")
        return ""

    if mime_type.startswith("image/"):
        print(f"🖼️ Detected image file: {file_path}")
        return extract_text_from_image(file_path)

    elif mime_type == "application/pdf":
        print(f"📄 Detected PDF file: {file_path}")
        return extract_text_from_pdf_with_ocr(file_path, temp_image_folder=temp_image_folder)

    else:
        print(f"❌ Unsupported file type: {mime_type}")
        return ""

def extract_text_from_image(image_path: str) -> str:
    """
    Extract text from image using Tesseract OCR.
    """
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='eng+ara')  # Add 'ara' if Arabic text
        return text
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return ""


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from PDF using PyMuPDF (fitz).
    """
    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()
        return full_text
    except Exception as e:
        print(f"Error processing PDF {pdf_path}: {e}")
        return ""


def extract_images_from_pdf(pdf_path: str, output_folder: str) -> list:
    """
    Extract images from PDF and save to a folder (used for OCR if needed).
    Returns list of saved image paths.
    """
    saved_images = []
    try:
        os.makedirs(output_folder, exist_ok=True)
        doc = fitz.open(pdf_path)
        for page_index in range(len(doc)):
            page = doc[page_index]
            image_list = page.get_images(full=True)
            for image_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image_path = os.path.join(output_folder, f"page{page_index + 1}_{image_index + 1}.{image_ext}")
                with open(image_path, "wb") as f:
                    f.write(image_bytes)
                saved_images.append(image_path)
        doc.close()
        return saved_images
    except Exception as e:
        print(f"Error extracting images from PDF: {e}")
        return []


def extract_text_from_pdf_with_ocr(pdf_path: str, temp_image_folder: str) -> str:
    """
    For scanned PDFs with no extractable text, extract images and OCR them.
    """
    extracted_text = extract_text_from_pdf(pdf_path)
    if extracted_text.strip():
        return extracted_text
    else:
        # fallback to OCR from images
        images = extract_images_from_pdf(pdf_path, temp_image_folder)
        all_text = ""
        for img_path in images:
            all_text += extract_text_from_image(img_path) + "\n"
    return all_text

