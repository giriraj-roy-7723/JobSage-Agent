from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "jobsage_db")
COLLECTION_NAME = os.getenv("RESUME_COLLECTION", "resumes")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
resume_collection = db[COLLECTION_NAME]

def save_parsed_resume(data: dict) -> str:
    """
    Stores parsed resume data into MongoDB.
    Returns the inserted document ID.
    """
    result = resume_collection.insert_one(data)
    return str(result.inserted_id)

def get_all_resumes():
    """
    Returns all stored resumes as a list.
    """
    return list(resume_collection.find())
