Folder Structure ->

jobsage-agent/
├── backend/
│   ├── agents/
│   │   ├── resume\_parser.py
│   │   ├── job\_scraper.py
│   │   ├── cover\_letter\_gen.py
│   │   └── result\_packager.py
│   ├── langgraph/
│   │   └── job\_agent\_graph.py
│   ├── database/
│   │   └── mongo\_utils.py
│   ├── api/
│   │   └── main.py              # FastAPI backend
│   ├── scripts/
│   │   └── realtime\_loop.py
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