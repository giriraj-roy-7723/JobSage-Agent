// src/components/Navbar.js
import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  const { pathname } = useLocation();
  const navigate = useNavigate();

  return (
    <nav className="navbar">
      <div className="navbar-logo" onClick={() => navigate('/landing')}>
        <span className="logo-text">Job Sage Agent</span>
      </div>
      <div className="navbar-links">
        <Link to="/" className={pathname === '/' ? 'active' : ''}>Home</Link>
        <Link to="/personalized" className={pathname === '/personalized' ? 'active' : ''}>Jobs Personalized</Link>
        <Link to="/resume" className={pathname === '/resume' ? 'active' : ''}>Resume Upload</Link>
      </div>
    </nav>
  );
}

export default Navbar;
