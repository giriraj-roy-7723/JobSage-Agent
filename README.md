# 🧠 Job Sage Agent

**Job Sage Agent** is an intelligent, full-stack AI-powered job assistant that:
- Parses resumes 🧾
- Scrapes real-time job listings from **Internshala**, **Glassdoor**, and **Jobright** 🌐
- Matches resumes to jobs using LLMs (Gemini + LangGraph) 🔍
- Generates personalized cover letters ✍️
- Presents everything in a modern, responsive React UI 💼

---

## 🚀 Features

- ✅ **Resume Parsing**  
  Upload a PDF resume — the system extracts email, phone, skills, and raw text.

- 🌐 **Job Scraping (Every 10 Hours)**  
  Automatically scrapes latest jobs from:
  - Internshala
  - Glassdoor
  - Jobright

- 🤖 **AI Matching **  
  Uses Sentence Transformers + LangGraph agents to:
  - Match your resume to relevant jobs
  - Generate cover letters based on job description + your resume - which is not done yet

- 💡 **Frontend Dashboard (React)**  
  - View all scraped jobs
  - View personalized matches
  - Upload resume
  - Trigger scraping manually  
  *(Beautiful, animated, mobile-friendly UI with Glassmorphism)*

- ☁️ **MongoDB Integration**  
  Stores resumes and job data with timestamps.

---


Folder Structure ->

jobsage-agent/
├── backend/
│   ├── agents/
│   │   ├── resume_parser.py
│   │   ├── job_scraper.py
│   │   ├── cover_letter_gen.py
│   │   └── result_packager.py
│   ├── langgraph/
│   │   └── job_agent_graph.py
│   ├── database/
│   │   └── mongo_utils.py
│   ├── api/
│   │   └── main.py              # FastAPI backend
│   ├── scripts/
│   │   └── realtime_loop.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ResumeUploader.jsx
│   │   │   ├── JobCard.jsx
│   │   │   └── CoverLetterModal.jsx
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   └── Home.jsx
│   │   └── App.jsx
│   └── package.json
│
├── .env
└── README.md

Setup -

To start the server-
go to backend , run -> uvicorn api.main:app --reload

To start the frontend-
go to frontend and do npm start 

And of course you should have your own environment setup

Any kind of contributions PR requests will be appreciated feel free to contribute!! :)


