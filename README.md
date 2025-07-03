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