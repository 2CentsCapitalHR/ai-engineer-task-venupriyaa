from docx import Document
import pdfplumber

def docx_to_text(path):
    doc = Document(path)
    paragraphs = [p.text for p in doc.paragraphs if p.text and p.text.strip()]
    return "\n".join(paragraphs)

def pdf_to_text(path):
    text_pages = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                if page_text.strip():
                    text_pages.append(page_text)
    except Exception:
        return ""
    return "\n".join(text_pages)

def file_to_text(path):
    path = path.lower()
    if path.endswith(".docx"):
        return docx_to_text(path)
    if path.endswith(".pdf"):
        return pdf_to_text(path)
    return ""
