import React, { useEffect, useState } from 'react';
import './Home.css';

function Home() {
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
    <div className="home-wrapper">
      <h1 className="home-heading">💼 All Jobs</h1>

      {loading ? (
        <div className="loader">⏳ Loading jobs...</div>
      ) : jobs.length === 0 ? (
        <p className="no-jobs">No jobs available at the moment.</p>
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
                View Posting ↗
              </a>
              <p className="timestamp">
                Scraped at:{' '}
                <strong>
                  {new Date(job.scraped_at).toLocaleString('en-IN', {
                    timeZone: 'Asia/Kolkata',
                  })}
                </strong>
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Home;
