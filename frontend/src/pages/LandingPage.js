// src/pages/LandingPage.js
import React from 'react';
import './LandingPage.css';
import { useNavigate } from 'react-router-dom';

function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="hero-section">
      <div className="hero-overlay">
        <h1 className="main-heading">LAND YOUR DREAM JOB FASTER</h1>
        <p className="sub-heading">
         An AI-powered career agent that parses your resume, intelligently scrapes job listings from multiple platforms, and delivers the most relevant jobs just for you — all in one place!
        </p>
        <button className="hero-button" onClick={() => navigate('/')}>Explore Jobs →</button>
      </div>

      <div className="feature-section">
        <div className="feature-block">
          <h3>💼 Smart Job Scraping</h3>
          <p>Get real-time job postings from Internshala, Glassdoor, and Jobright.</p>
        </div>
        <div className="feature-block">
          <h3>🧠 AI Career Matching</h3>
          <p>Powered by LangGraph and Sentence Transformers, we personalize job recommendations for you.</p>
        </div>
        <div className="feature-block">
          <h3>⚡ Seamless Backend</h3>
          <p>FastAPI + MongoDB for instant decision-making and resume syncing.</p>
        </div>
      </div>
    </div>
  );
}

export default LandingPage;
