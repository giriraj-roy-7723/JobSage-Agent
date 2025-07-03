import re
import docx2txt
from PyPDF2 import PdfReader
from typing import Dict

def extract_text_from_pdf(pdf_bytes) -> str:
    reader = PdfReader(pdf_bytes)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(docx_bytes) -> str:
    with open("temp.docx", "wb") as f:
        f.write(docx_bytes)
    return docx2txt.process("temp.docx")

def extract_basic_info(text: str) -> Dict:
    email = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    phone = re.findall(r"\+?\d[\d \-\(\)]{8,}\d", text)

    # Sample keyword-based skill detection (customize later)
    skills_keywords = ['python', 'java', 'sql', 'ml', 'nlp', 'react', 'node', 'c++', 'mongodb']
    words = text.lower().split()
    skills = list(set(word for word in words if word in skills_keywords))

    return {
        "email": email[0] if email else "",
        "phone": phone[0] if phone else "",
        "skills": skills,
    }

def parse_resume(file: bytes, filename: str) -> Dict:
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file)
    elif filename.endswith(".docx"):
        text = extract_text_from_docx(file)
    else:
        raise ValueError("Unsupported file format")

    info = extract_basic_info(text)
    info["raw_text"] = text
    return info
