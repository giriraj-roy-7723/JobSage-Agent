// src/App.js
import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/jobs')
      .then(res => res.json())
      .then(data => {
        setJobs(data.jobs);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to fetch jobs:', err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="app-container">
      <div className="content-wrapper">
        <h1 className="main-heading">Internshala Job Listings</h1>

        {loading ? (
          <div className="loader">Loading jobs...</div>
        ) : (
          <div className="job-list">
            {jobs.length === 0 ? (
              <p className="no-jobs">No jobs available.</p>
            ) : (
              jobs.map((job, index) => (
                <div key={index} className="job-card">
                  <a
                    href={job.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="job-link"
                  >
                    {job.link}
                  </a>
                  <p className="timestamp">
                    Scraped at: <strong>{new Date(job.scraped_at).toLocaleString()}</strong>
                  </p>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
