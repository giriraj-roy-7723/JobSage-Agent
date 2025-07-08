// src/components/Navbar.js
import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const [scraping, setScraping] = useState(false);

  const triggerScrape = async () => {
    try {
      setScraping(true);
      navigate('/scrape');
      await fetch('http://127.0.0.1:8000/scrape/jobs');
    } catch (err) {
      alert('❌ Failed to trigger scraping.');
    } finally {
      setScraping(false);
    }
  };

  return (
    <nav className="navbar">
      <div className="navbar-left" onClick={() => navigate('/landing')}>
        <span className="navbar-logo"> Job Sage Agent</span>
      </div>

      <div className="navbar-right">
        <button
          className={`navbar-link scrape ${pathname === '/scrape' ? 'active' : ''}`}
          onClick={triggerScrape}
          disabled={scraping}
        >
          {scraping ? '⏳ Scraping...' : ' Trigger Scraping'}
        </button>

        <div className="separator" />

        <Link to="/" className={`navbar-link ${pathname === '/' ? 'active' : ''}`}>
           Job Basket
        </Link>

        <div className="separator" />
        <Link to="/resume" className={`navbar-link ${pathname === '/resume' ? 'active' : ''}`}>
           Resume Upload
        </Link>
        <Link to="/personalized" className={`navbar-link ${pathname === '/personalized' ? 'active' : ''}`}>
           Personalized Jobs
        </Link>

        <div className="separator" />

        
      </div>
    </nav>
  );
}

export default Navbar;
