from langgraph.graph import StateGraph, END
from typing import Annotated, Dict, List, Any
from database.mongo_utils import get_latest_resume, get_all_jobs
from agents.cover_letter_gen import generate_cover_letter
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
gemini = GenerativeModel("models/gemini-1.5-flash-latest") 

def score_jobs(state: State) -> NodeOutput:
    resume = state["resume"]
    resume_skills = resume.get("skills", [])
    jobs = state["jobs"]

    scored = []
    for job in jobs:
        job_title = job.get("title", "")
        prompt = f"""
        You are a career advisor AI. A candidate has the following skills: {', '.join(resume_skills)}.
        The job title is "{job_title}". 
        Does this job align well with the candidate's skills?

        Return a JSON in the format:
        {{
          "match": true/false,
          "confidence": score between 0 and 1
        }}
        """

        try:
            response = gemini.generate_content(prompt)
            result = response.text.strip()
            import json
            data = json.loads(result)

            if data.get("match", False):
                scored.append({
                    "title": job_title,
                    "link": job.get("link", ""),
                    "score": round(data.get("confidence", 0), 3)
                })

        except Exception as e:
            print(f"Error scoring job: {job_title} — {e}")
            continue

    state["scored_jobs"] = scored
    return state


def package_results(state: State) -> NodeOutput:
    top_n = 5
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
