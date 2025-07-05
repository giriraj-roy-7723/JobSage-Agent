import os
from dotenv import load_dotenv
from typing import Dict
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "models/gemini-1.5-flash"
'''
   
'''
def generate_cover_letter(parsed_resume: Dict, job_description: str) -> str:
    prompt = f"""
    Write a personalized cover letter for the following job description based on the candidate's resume.

    Candidate Info:
    Email: {parsed_resume.get("email")}
    Phone: {parsed_resume.get("phone")}
    Skills: {', '.join(parsed_resume.get("skills", []))}

     Raw Resume Text:
    {parsed_resume.get("raw_text", "")}
    Job Description:
    {job_description}

    The tone should be professional, enthusiastic, and job-specific.
    """

    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    return response.text
