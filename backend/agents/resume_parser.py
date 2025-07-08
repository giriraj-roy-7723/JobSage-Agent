import re
import docx2txt
from PyPDF2 import PdfReader
from typing import Dict
import io

def extract_text_from_pdf(pdf_bytes) -> str:
    pdf_stream = io.BytesIO(pdf_bytes)
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

    phone = re.search(r'(\+91)?[ -]?\(?\d{10}\)?', clean_text)
    skill_keywords = [
    "Python", "C", "C++", "Java", "JavaScript", "TypeScript","Rust", "Ruby", "Swift", "PHP", "SQL", "Shell",
    "HTML", "CSS", "SASS", "Tailwind", "Bootstrap", "React", "Next.js", "Vue", "Angular", "Redux", "Framer Motion",
    "Node.js", "Express.js", "Flask", "Django", "Spring", "FastAPI", "GraphQL", "REST", "gRPC",
    "MongoDB", "MySQL", "PostgreSQL", "SQLite", "Firebase", "Redis", "Elasticsearch",
    "Docker", "Kubernetes", "Git", "GitHub", "CI/CD", "Jenkins", "Linux", "Bash", "AWS", "GCP", "Azure", 
    "TensorFlow", "PyTorch", "Keras", "Scikit-Learn", "XGBoost", "LightGBM", "OpenCV", "Transformers", "spaCy",
    "Langchain", "LlamaIndex", "HuggingFace", "Pinecone", "ChromaDB", "BERT", "LLM", "Fine-tuning",
    "NumPy", "Pandas", "Matplotlib", "Seaborn", "Plotly", "SQL", "Tableau", "Power BI", "Excel",
    "NLTK", "spaCy", "BART","BERT", "T5", "TextBlob", "Summarization", "NER", "RAG", "Embedding",
    "Agile", "Scrum", "Figma", "UI/UX", "Postman", "Firebase", "Notion", "Jira", "Trello","ReactNative","Swift","Kotlin"
]

    
    found_skills = [skill for skill in skill_keywords if skill.lower() in clean_text.lower()]

    return {
        "email": email if email else None,
        "phone": phone.group().strip() if phone else None,
        "skills": found_skills
    }

def clean_resume_text(text: str) -> str: #do using chatgpt later
    # Fix broken words like 'A N N' → 'ANN'
    text = re.sub(r'\b(?:\w\s+){1,6}\w\b', lambda x: x.group().replace(" ", ""), text)
    # Replace multiple newlines or spaces with single space
    text = re.sub(r'\s+', ' ', text)
    # Remove bullets and stray symbols
    text = text.replace("❖", "").replace("|", "")
    # Remove spacing before punctuation
    text = re.sub(r'\s+([.,:;!?])', r'\1', text)
    return text.strip()

def parse_resume(file: bytes, filename: str) -> Dict:
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file)
    elif filename.endswith(".docx"):
        text = extract_text_from_docx(file)
    else:
        raise ValueError("Unsupported file format")

    info = extract_basic_info(text)
    info["raw_text"] = clean_resume_text(text)
    return info
