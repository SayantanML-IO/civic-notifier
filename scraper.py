import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import pdfplumber

def get_links_from_url(base_url):
    print(f"🔎 Scraping {base_url} for links...")
    found_links = set()
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(base_url, headers=headers, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            if link['href'].lower().endswith('.pdf'):
                found_links.add(urljoin(base_url, link['href']))
    except Exception as e:
        print(f"Failed to scrape links. Error: {e}")
    return list(found_links)

def download_pdf(pdf_url, save_path="temp.pdf", size_limit_mb=10):
    print(f"  Downloading PDF: {pdf_url}")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        response = requests.head(pdf_url, headers=headers, timeout=20, allow_redirects=True)
        response.raise_for_status()
        
        file_size = int(response.headers.get('Content-Length', 0))
        
        size_limit_bytes = size_limit_mb * 1024 * 1024
        
        if file_size > size_limit_bytes:
            print(f"Skipping file: Size ({file_size / 1024 / 1024:.2f} MB) exceeds limit of {size_limit_mb} MB.")
            return None

        response = requests.get(pdf_url, headers=headers, timeout=60)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return save_path
        
    except Exception as e:
        print(f"Failed to download PDF. Error: {e}")
        return None

def extract_text_from_pdf(pdf_path):
    full_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"
    except Exception as e:
        print(f"Failed to extract text. Error: {e}")
    finally:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
    return full_text

def find_keywords_in_text(text, keywords):
    found = [kw for kw in keywords if kw.lower() in text.lower()]
    return found
