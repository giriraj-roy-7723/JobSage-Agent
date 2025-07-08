import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import PersonalizedJobs from './pages/PersonalizedJobs';
import ResumeUpload from './pages/ResumeUpload';
import './App.css';
import LandingPage from './pages/LandingPage';


import ScrapeJob from './pages/ScrapeJobs';




function App() {
  return (
    <Router>
      <div className="app-container">
        <Navbar />
        <div className="page-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/personalized" element={<PersonalizedJobs />} />
            <Route path="/resume" element={<ResumeUpload />} />
            <Route path="/landing" element={<LandingPage />} />
            <Route path="/scrape" element={<ScrapeJob />} />

          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
