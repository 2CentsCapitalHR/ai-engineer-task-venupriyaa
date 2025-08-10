import os
import re
import csv
import time
import requests
from html import unescape
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


SAVE_DIR = "reference_docs"
LOG_CSV = "download_log.csv"
PDF_SOURCE = "Data Sources.pdf"
URLS = [
    "https://www.adgm.com/registration-authority/registration-and-incorporation",
    "https://assets.adgm.com/download/assets/adgm-ra-resolution-multiple-incorporate-shareholders-LTD-incorporation-v2.docx/186a12846c3911efa4e6c6223862cd87",
    "https://www.adgm.com/setting-up",
    "https://www.adgm.com/legal-framework/guidance-and-policy-statements",
    "https://www.adgm.com/documents/registration-authority/registration-and-incorporation/checklist/branch-non-financial-services-20231228.pdf",
    "https://www.adgm.com/documents/registration-authority/registration-and-incorporation/checklist/private-company-limited-by-guarantee-non-financial-services-20231228.pdf",
    "https://assets.adgm.com/download/assets/ADGM+Standard+Employment+Contract+Template+-+ER+2024+(Feb+2025).docx/ee14b252edbe11efa63b12b3a30e5e3a",
    "https://assets.adgm.com/download/assets/ADGM+Standard+Employment+Contract+-+ER+2019+-+Short+Version+(May+2024).docx/33b57a92ecfe11ef97a536cc36767ef8",
    "https://www.adgm.com/documents/office-of-data-protection/templates/adgm-dpr-2021-appropriate-policy-document.pdf",
    "https://www.adgm.com/operating-in-adgm/obligations-of-adgm-registered-entities/annual-filings/annual-accounts",
    "https://www.adgm.com/operating-in-adgm/post-registration-services/letters-and-permits",
    "https://en.adgm.thomsonreuters.com/rulebook/7-company-incorporation-package",
    "https://assets.adgm.com/download/assets/Templates_SHReso_AmendmentArticles-v1-20220107.docx/97120d7c5af911efae4b1e183375c0b2?forcedownload=1"
]
DOC_EXTS = (".pdf", ".docx", ".doc", ".xlsx", ".xls", ".rtf", ".txt")

os.makedirs(SAVE_DIR, exist_ok=True)


def safe_filename(url):
    name = url.split("/")[-1].split("?")[0]
    name = unescape(name)
    name = re.sub(r'[\\/*?:"<>|]', "_", name)
    return name[:200] or "file"

def extract_links_from_pdf(pdf_path):
    urls = []
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            if "/Annots" in page:
                for annot in page["/Annots"]:
                    obj = annot.get_object()
                    if "/A" in obj and "/URI" in obj["/A"]:
                        urls.append(obj["/A"]["/URI"])
    except Exception as e:
        print(f"[WARN] Could not read {pdf_path}: {e}")
    return list(dict.fromkeys(urls))  

def download_file(url):
    try:
        r = requests.get(url, stream=True, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        fname = safe_filename(url)
        path = os.path.join(SAVE_DIR, fname)
        base, ext = os.path.splitext(path)
        count = 1
        while os.path.exists(path):
            path = f"{base}_{count}{ext}"
            count += 1
        with open(path, "wb") as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)
        print(f"[SAVED] {fname}")
        return path, "downloaded"
    except Exception as e:
        print(f"[ERROR] {url} -> {e}")
        return "", f"error: {e}"

def scrape_with_selenium(page_url, driver):
    try:
        driver.get(page_url)
        time.sleep(3)
    except Exception as e:
        print(f"[SELENIUM ERROR] {page_url} -> {e}")
        return []


    try:
        for panel in driver.find_elements(By.TAG_NAME, "adgm-expansion-panel"):
            driver.execute_script("arguments[0].setAttribute('open','true')", panel)
        time.sleep(1)
        for btn in driver.find_elements(By.TAG_NAME, "button"):
            try:
                driver.execute_script("arguments[0].click();", btn)
            except:
                pass
        time.sleep(1)
    except Exception as e:
        print(f"[WARN] Could not expand panels/buttons: {e}")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = set()
    for a in soup.find_all("a", href=True):
        full_url = urljoin(page_url, unescape(a["href"].strip()))
        links.add(full_url)
    for btn in soup.find_all("adgm-link-button"):
        href = btn.get("href") or btn.get("data-href") or ""
        if href:
            full_url = urljoin(page_url, unescape(href.strip()))
            links.add(full_url)
    for tag in soup.find_all(True):
        onclick = tag.get("onclick")
        if onclick:
            matches = re.findall(r"(https?://[^\)\'\"\s]+)", onclick)
            for m in matches:
                links.add(m)

 
    doc_links = [l for l in links if any(l.lower().endswith(ext) for ext in DOC_EXTS)]
    return list(set(doc_links))

def main():
    all_urls = list(URLS)

    if os.path.exists(PDF_SOURCE):
        pdf_urls = extract_links_from_pdf(PDF_SOURCE)
        print(f"[INFO] Extracted {len(pdf_urls)} links from {PDF_SOURCE}")
        for u in pdf_urls:
            if u not in all_urls:
                all_urls.append(u)

    chrome_opts = Options()
    chrome_opts.add_argument("--headless=new")
    chrome_opts.add_argument("--disable-gpu")
    chrome_opts.add_argument("--no-sandbox")
    chrome_opts.add_experimental_option('excludeSwitches', ['enable-logging'])

 
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_opts)

    seen_files = set()

    with open(LOG_CSV, "w", newline="", encoding="utf-8") as csvf:
        writer = csv.DictWriter(csvf, fieldnames=["input_url", "child_url", "status", "saved_path"])
        writer.writeheader()

        for url in all_urls:
            ext = os.path.splitext(urlparse(url).path)[1].lower()

            if ext in DOC_EXTS:
                path, status = download_file(url)
                if path:
                    seen_files.add(path)
                writer.writerow({"input_url": url, "child_url": "", "status": status, "saved_path": path})
                continue

            doc_links = scrape_with_selenium(url, driver)
            if not doc_links:
                writer.writerow({"input_url": url, "child_url": "", "status": "no_docs_found", "saved_path": ""})
                print(f"[INFO] No documents found on {url}")
                continue

            for doc_url in doc_links:
                path, status = download_file(doc_url)
                if path:
                    seen_files.add(path)
                writer.writerow({"input_url": url, "child_url": doc_url, "status": status, "saved_path": path})

    driver.quit()
    print(f"[DONE] Downloaded {len(seen_files)} unique documents.")

if __name__ == "__main__":
    main()
