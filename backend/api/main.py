from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from agents.resume_parser import parse_resume
from database.mongo_utils import save_parsed_resume

app = FastAPI()

# Allow frontend (React) to call backend API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    contents = await file.read()

    # Parse resume content
    parsed_data = parse_resume(file=contents, filename=file.filename)

    # Store parsed data in MongoDB
    resume_id = save_parsed_resume(parsed_data)

    return {
        "status": "success",
        "resume_id": resume_id,
        "parsed": parsed_data
    }
