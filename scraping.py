import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm

BASE_URL = "https://uaelegislation.gov.ae"
LIST_URL = f"{BASE_URL}/en/legislations"
DOWNLOAD_DIR = "data/laws"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def get_legislation_pages():
    print("🔍 Fetching legislation list page...")
    res = requests.get(LIST_URL)
    soup = BeautifulSoup(res.text, "html.parser")

    law_links = []
    for a in soup.select("a[href^='/en/legislations/']"):
        href = a["href"]
        full_url = urljoin(BASE_URL, href)
        if full_url not in law_links:
            law_links.append(full_url)
    print(f"✅ Found {len(law_links)} legislation pages.")
    return law_links

def get_pdf_url(legislation_url):
    res = requests.get(legislation_url)
    soup = BeautifulSoup(res.text, "html.parser")
    for a in soup.select("a[href$='.pdf']"):
        pdf_url = a["href"]
        return pdf_url if pdf_url.startswith("http") else urljoin(BASE_URL, pdf_url)
    return None

def download_pdf(pdf_url):
    filename = pdf_url.split("/")[-1]
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    if os.path.exists(filepath):
        return
    try:
        pdf = requests.get(pdf_url)
        with open(filepath, "wb") as f:
            f.write(pdf.content)
    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")

def main():
    pages = get_legislation_pages()
    for page_url in tqdm(pages, desc="📥 Downloading PDFs"):
        pdf_url = get_pdf_url(page_url)
        if pdf_url:
            download_pdf(pdf_url)

if __name__ == "__main__":
    main()
