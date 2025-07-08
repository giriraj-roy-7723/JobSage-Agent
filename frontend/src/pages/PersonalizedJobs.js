import React, { useEffect, useState } from 'react';
import './PersonalizedJobs.css';

function PersonalizedJobs() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [status, setStatus] = useState('');

  useEffect(() => {
    fetch('http://127.0.0.1:8000/personalized-jobs')
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          setJobs(data.recommended_jobs);
          setStatus('');
        } else {
          setStatus(data.message || 'No matches found.');
        }
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching personalized jobs:', err);
        setStatus('❌ Failed to fetch personalized jobs.');
        setLoading(false);
      });
  }, []);

  return (
    <div className="personalized-wrapper">
      <h1 className="personalized-heading">🧠 Personalized Jobs</h1>

      {loading ? (
        <p className="status-message">Loading personalized jobs...</p>
      ) : status ? (
        <p className="status-message">{status}</p>
      ) : (
        <div className="job-grid">
          {jobs.map((job, index) => (
            <div key={index} className="job-card">
              <h3 className="job-title">{job.title || 'Untitled Job'}</h3>
              <a
                href={job.link}
                target="_blank"
                rel="noreferrer"
                className="job-link"
              >
                View Job ↗
              </a>
              <p className="match-score">
                Match Score: <strong>{job.score}</strong>
              </p>

              {job.cover_letter && (
                <details className="cover-letter">
                  <summary>📄 Cover Letter</summary>
                  <p>{job.cover_letter}</p>
                </details>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default PersonalizedJobs;
