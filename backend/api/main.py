from fastapi import FastAPI, UploadFile, File,Form
from fastapi.middleware.cors import CORSMiddleware

from agents.resume_parser import parse_resume
from database.mongo_utils import save_parsed_resume

app = FastAPI()

#cors error is the error for calling one domain from other which might not have permission for that domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  #React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def hi():
    return ({"message":"hello i am job sage!"})
@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    contents = await file.read()
    parsed_data = parse_resume(file=contents, filename=file.filename)
    resume_id = save_parsed_resume(parsed_data)
    parsed_data["_id"] = str(resume_id)  #convert the object id
    return {
        "status": "success",
        "resume_id": resume_id,
        "parsed": parsed_data
    }
from agents.cover_letter_gen import generate_cover_letter
@app.post("/generate-cover-letter")
async def generate_cover_letter_endpoint(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    contents = await file.read()
    parsed_data = parse_resume(file=contents, filename=file.filename)
    resume_id = save_parsed_resume(parsed_data)
    parsed_data["_id"] = str(resume_id)

    cover_letter = generate_cover_letter(parsed_data, job_description)

    return {
        "status": "success",
        "resume_id": parsed_data["_id"],
        "cover_letter": cover_letter
    }


from agents.job_scraper import scrape_internshala_jobs
from fastapi.responses import JSONResponse
from database.mongo_utils import delete_all_jobs
import subprocess , sys

@app.get("/scrape/jobs")
async def scrape_jobs1():
    delete_all_jobs()
   
    try:
        subprocess.run([sys.executable, "agents/job_scraper.py"], check=True)
        return {"status": "success", "message": "Scraping started"}
        # await scrape_internshala_jobs()
        # return JSONResponse(content={"status": "success", "message": "Internshala jobs scraped and stored!"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})





from database.mongo_utils import get_all_jobs
from fastapi.responses import JSONResponse

@app.get("/jobs")
async def fetch_jobs():
    try:
        jobs = get_all_jobs()
        return {"status": "success", "jobs": jobs}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


#running the job matching agent
from langgraph.job_agent_graph import run_job_matching_agent_langgraph

@app.get("/personalized-jobs")
def get_personalized_jobs():
    return run_job_matching_agent_langgraph()


#creating a loop for the scraper to run every 10 hrs on its own


import asyncio
from agents.job_scraper import scrape_internshala_jobs, scrape_jobright_jobs, scrape_glassdoor_jobs

# @app.on_event("startup")
# async def schedule_periodic_scraping():
#     async def loop_scraper():
#         while True:
#             try:
#                 print("Running scheduled job scraping...")
#                 await scrape_glassdoor_jobs()
#                 await scrape_jobright_jobs()
#                 await scrape_internshala_jobs()
#                     #await scrape_jobright_jobs()
#                 print("Scraping completed!")
#             except Exception as e:
#                 print(f"Scraping failed: {e}")
#             await asyncio.sleep(5)  #  Sleep 10 hours

#     asyncio.create_task(loop_scraper())
