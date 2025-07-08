// src/pages/ScrapeJob.js
import React from 'react';
import './ScrapeJobs.css';

function ScrapeJob() {
  return (
    <div className="scrape-job-wrapper">
      <h1 className="scrape-title">🌊 Surfing through the job waves...</h1>
      <p className="scrape-description">
        Our agent is currently surfing through <strong>Internshala</strong>, <strong>Glassdoor</strong>,
        and <strong>Jobright</strong> , diving deep into job listings and pulling out the best matches just for you!
      </p>
      <p className="scrape-note">
        Sit back, relax, and let Job Sage Agent do the job hunt for you.
      </p>
    </div>
  );
}

export default ScrapeJob;
