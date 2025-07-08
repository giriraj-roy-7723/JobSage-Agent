from langgraph.graph import StateGraph, END
from typing import Annotated, Dict, List, Any
from database.mongo_utils import get_latest_resume, get_all_jobs
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import os ,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

State = Dict[str, Any]
NodeOutput = Annotated[State, "node output"]
def load_resume(state: State) -> NodeOutput:
    resume = get_latest_resume()
    if not resume:
        raise ValueError("No resume found in DB")
    state["resume"] = resume
    return state

def load_jobs(state: State) -> NodeOutput:
    jobs = get_all_jobs()
    state["jobs"] = jobs
    return state

from google.generativeai import GenerativeModel
import os
from dotenv import load_dotenv
load_dotenv()


from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

model = SentenceTransformer("all-MiniLM-L6-v2")
gemini=GenerativeModel("models/gemini-1.5-flash")
def score_jobs(state: State) -> NodeOutput:
    resume = state["resume"]
    resume_skills = resume.get("skills", [])
    raw_text = resume.get("raw_text", "")
    jobs = state["jobs"]
    resume_input = " ".join(resume_skills) + " " + raw_text[:1500]
    resume_embedding = model.encode(resume_input)
    scored = []
    for job in jobs:
        title = job.get("title", "")
        job_embedding = model.encode(title)
        score = cosine_similarity([resume_embedding], [job_embedding])[0][0]

        scored.append({
            "title": title,
            "link": job.get("link", ""),
            "source": job.get("source", "Unknown"),
            "score": float(round(score, 3))  #casting to float cause json cant parse float32 kind of dtypes
            
        })
    top_20 = sorted(scored, key=lambda x: -x["score"])[:20]

    state["scored_jobs"] = top_20
    return state


def package_results(state: State) -> NodeOutput:
    top_n = 20
    top_jobs = state["scored_jobs"][:top_n]
    state["recommended_jobs"] = top_jobs
    
    return state




graph = StateGraph(State)


graph.add_node("load_resume", load_resume)
graph.add_node("load_jobs", load_jobs)
graph.add_node("score_jobs", score_jobs)
graph.add_node("package_results", package_results)
graph.set_entry_point("load_resume")
graph.add_edge("load_resume", "load_jobs")
graph.add_edge("load_jobs", "score_jobs")
graph.add_edge("score_jobs", "package_results")
graph.add_edge("package_results", END)


job_graph = graph.compile()

def run_job_matching_agent_langgraph():
    result = job_graph.invoke({})
    return {
        "status": "success",
        "resume_id": str(result['resume'].get('_id')),
        "recommended_jobs": result["recommended_jobs"]
    }
