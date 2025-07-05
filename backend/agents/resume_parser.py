import re
import docx2txt
from PyPDF2 import PdfReader
from typing import Dict

import io
def extract_text_from_pdf(pdf_bytes) -> str:
    pdf_stream=io.BytesIO(pdf_bytes)#pdf bytes is a raw bytes . we are converting it toa file like stream 
    #the only difference between the two is the former doesnot contain a pinter and the latter contains a pointer hence the functions like seek() will work on it

    reader = PdfReader(pdf_stream)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(docx_bytes) -> str:
    with open("temp.docx", "wb") as f:
        f.write(docx_bytes)
    return docx2txt.process("temp.docx")

def extract_basic_info(text: str) -> dict:
    clean_text = re.sub(r'\s+', ' ', text)
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w{2,}', clean_text)
    if not email_match:
        partial_email = re.search(r'[\w\.-]+@', clean_text)
        email = partial_email.group() + "gmail.com" if partial_email else None
    else:
        email = email_match.group()
    #email = re.search(r'[\w\.-]+@[\w\.-]+\.\w{2,}', clean_text)
    phone = re.search(r'(\+91)?[ -]?\(?\d{10}\)?', clean_text)
    skill_keywords = [
        "Python", "C", "C++", "Java", "JavaScript", "Node.js", "Express.js",
        "MongoDB", "React", "HTML", "CSS", "Langchain", "TensorFlow", "PyTorch",
        "Keras", "NumPy", "Pandas", "Matplotlib", "Scikit-Learn"
    ]
    
    found_skills = [skill for skill in skill_keywords if skill.lower() in clean_text.lower()]

    return {
        "email": email if email else None,
        "phone": phone.group().strip() if phone else None,
        "skills": found_skills
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
