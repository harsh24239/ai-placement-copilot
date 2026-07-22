import { useState, useEffect } from 'react'
import ScoreRing from '../components/ScoreRing'

const LOADING_MESSAGES = [
  'Reading your resume...',
  'Reading the job description...',
  'Comparing skills...',
  'Writing your fit summary...',
]

export default function ResumeAnalysis() {
  const [resumeFile, setResumeFile] = useState(null)
  const [jdFile, setJdFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [loadingStep, setLoadingStep] = useState(0)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!loading) return
    const interval = setInterval(() => {
      setLoadingStep((s) => (s + 1) % LOADING_MESSAGES.length)
    }, 3000)
    return () => clearInterval(interval)
  }, [loading])

  const handleSubmit = async () => {
    if (!resumeFile || !jdFile) {
      setError('Please select both a resume and a job description PDF.')
      return
    }
    setError(null)
    setLoading(true)
    setLoadingStep(0)
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
    <div>
      <div className="page-header">
        <div className="page-eyebrow">Step 1 of 3</div>
        <h1 className="page-title">Resume Analysis</h1>
        <p className="page-subtitle">
          Upload your resume and a job description. We'll score your ATS match and show exactly what's missing.
        </p>
      </div>

      <div className="card">
        <div className="upload-row">
          <label className="file-drop">
            <span className="file-drop-label">Resume (PDF)</span>
            <span className="file-drop-name">{resumeFile ? resumeFile.name : 'Choose file'}</span>
            <input type="file" accept=".pdf" onChange={(e) => setResumeFile(e.target.files[0])} />
          </label>

          <label className="file-drop">
            <span className="file-drop-label">Job Description (PDF)</span>
            <span className="file-drop-name">{jdFile ? jdFile.name : 'Choose file'}</span>
            <input type="file" accept=".pdf" onChange={(e) => setJdFile(e.target.files[0])} />
          </label>

          <div>
            <button className="btn-primary" onClick={handleSubmit} disabled={loading}>
              {loading ? 'Analyzing...' : 'Analyze'}
            </button>
            {error && <div className="error-text">{error}</div>}
          </div>
        </div>
      </div>

      {loading && (
        <div className="card">
          <div className="loading-block">
            <div className="loading-spinner" />
            <div className="loading-text">{LOADING_MESSAGES[loadingStep]}</div>
          </div>
        </div>
      )}

      {result && !loading && (
        <>
          <div className="card">
            <div className="score-section">
              <ScoreRing score={result.resume_analysis.ats_score} />
              <div>
                <p className="score-meta-title">ATS Compatibility Score</p>
                <p className="score-meta-desc">
                  Based on how well your resume's listed skills align with this role's requirements.
                </p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="section-label">Matching Skills</div>
            <div className="chip-group">
              {result.skill_gap.matching_skills.map((skill, i) => (
                <span key={i} className="chip chip-success">{skill}</span>
              ))}
            </div>
          </div>

          <div className="card">
            <div className="section-label">Missing Skills</div>
            <div className="chip-group">
              {result.skill_gap.missing_skills.map((skill, i) => (
                <span key={i} className="chip chip-danger">{skill}</span>
              ))}
            </div>
          </div>

          <div className="card">
            <div className="section-label">Fit Summary</div>
            <p className="fit-summary-text">{result.skill_gap.fit_summary}</p>
          </div>
        </>
      )}
    </div>
  )
}
