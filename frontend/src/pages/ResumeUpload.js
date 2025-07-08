import React, { useState } from 'react';
import './ResumeUpload.css';

function ResumeUpload() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setStatus('');
  };

  const handleUpload = async () => {
    if (!file) {
      setStatus('⚠️ Please select a resume file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file); // MUST match FastAPI param

    try {
      const res = await fetch('http://127.0.0.1:8000/upload-resume/', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        const errText = await res.text();
        throw new Error(errText);
      }

      const data = await res.json();
      console.log(data);
      setStatus(`✅ Resume uploaded!\n\nSkills extracted: ${data.parsed.skills.join(', ')}`);
    } catch (err) {
      console.error(err);
      setStatus(`❌ Upload failed: ${err.message}`);
    }
  };

  return (
    <div className="resume-upload-wrapper">
      <div className="resume-upload-box">
        <h1 className="resume-heading">📄 Upload Your Resume</h1>
        <p className="resume-subheading">
          Let our AI analyze your resume to generate job matches and custom cover letters.
        </p>

        <div className="upload-controls">
          <input
            className="file-input"
            type="file"
            accept=".pdf,.doc,.docx"
            onChange={handleFileChange}
          />
          <button className="upload-btn" onClick={handleUpload}>
            Upload
          </button>
        </div>

        {status && <p className="upload-status">{status}</p>}
      </div>
    </div>
  );
}

export default ResumeUpload;
