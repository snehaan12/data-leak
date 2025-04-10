import os
from PyPDF2 import PdfReader
from docx import Document

def extract_text(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == '.txt':
        return extract_txt(file_path)
    elif ext == '.pdf':
        return extract_pdf(file_path)
    elif ext == '.docx':
        return extract_docx(file_path)
    return ""

def extract_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        return f"[ERROR] Could not read TXT file: {e}"

def extract_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        if reader.is_encrypted:
            try:
                reader.decrypt("")  # Try empty password first
            except:
                return "[ERROR] PDF is password-protected and could not be read."
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
        return text or "[INFO] No text found in PDF."
    except Exception as e:
        return f"[ERROR] Could not extract PDF: {e}"

def extract_docx(file_path):
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        return f"[ERROR] Could not extract DOCX: {e}"
