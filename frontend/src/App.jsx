import { useState } from 'react'
import './App.css'

function App() {
  const [resumeFile, setResumeFile] = useState(null)
  const [jdFile, setJdFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleSubmit = async () => {
    if (!resumeFile || !jdFile) {
      setError('Please select both a resume and a job description PDF.')
      return
    }
    setError(null)
    setLoading(true)
    setResult(null)

    const formData = new FormData()
    formData.append('resume_file', resumeFile)
    formData.append('jd_file', jdFile)

    try {
      const response = await fetch('http://127.0.0.1:8000/workflow/placement', {
        method: 'POST',
        body: formData
      })
      if (!response.ok) throw new Error('Server returned an error')
      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    }
    setLoading(false)
  }

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif', maxWidth: '700px', margin: '0 auto' }}>
      <h1>AI Placement Copilot</h1>

      <div style={{ marginBottom: '1rem' }}>
        <label>Resume (PDF): </label>
        <input type="file" accept=".pdf" onChange={(e) => setResumeFile(e.target.files[0])} />
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <label>Job Description (PDF): </label>
        <input type="file" accept=".pdf" onChange={(e) => setJdFile(e.target.files[0])} />
      </div>

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? 'Analyzing... (this can take up to a minute)' : 'Analyze'}
      </button>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {result && (
        <div style={{ marginTop: '2rem' }}>
          <h2>ATS Score: {result.resume_analysis.ats_score}/100</h2>

          <h3>Matching Skills</h3>
          <ul>
            {result.skill_gap.matching_skills.map((skill, i) => <li key={i}>{skill}</li>)}
          </ul>

          <h3>Missing Skills</h3>
          <ul>
            {result.skill_gap.missing_skills.map((skill, i) => <li key={i}>{skill}</li>)}
          </ul>

          <h3>Fit Summary</h3>
          <p>{result.skill_gap.fit_summary}</p>
        </div>
      )}
    </div>
  )
}

export default App