import { useState } from 'react'

export default function DsaCoach() {
  const [topic, setTopic] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleSubmit = async () => {
    if (!topic.trim()) {
      setError('Enter a topic you want to practice, e.g. "dynamic programming".')
      return
    }
    setError(null)
    setLoading(true)
    setResult(null)

    try {
      const response = await fetch('http://127.0.0.1:8000/dsa/coach', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ weak_topic: topic })
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
        <div className="page-eyebrow">Step 2 of 3</div>
        <h1 className="page-title">DSA Coach</h1>
        <p className="page-subtitle">
          Tell us a topic you're weak in. We'll recommend problems and a short strategy to approach them.
        </p>
      </div>

      <div className="card">
        <div className="upload-row">
          <input
            className="chat-input"
            placeholder="e.g. dynamic programming, graphs, arrays..."
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
          />
          <div>
            <button className="btn-primary" onClick={handleSubmit} disabled={loading}>
              {loading ? 'Thinking...' : 'Get Recommendations'}
            </button>
            {error && <div className="error-text">{error}</div>}
          </div>
        </div>
      </div>

      {loading && (
        <div className="card">
          <div className="loading-block">
            <div className="loading-spinner" />
            <div className="loading-text">Finding the right problems for you...</div>
          </div>
        </div>
      )}

      {result && !loading && (
        <>
          <div className="card">
            <div className="section-label">Recommended Problems</div>
            <div className="chip-group">
              {result.problems_recommended.map((p, i) => (
                <span key={i} className="chip chip-success">
                  #{p.id} {p.title} — {p.difficulty}
                </span>
              ))}
            </div>
          </div>

          <div className="card">
            <div className="section-label">Coaching Advice</div>
            <p className="fit-summary-text" style={{ whiteSpace: 'pre-wrap' }}>
              {result.coaching_advice}
            </p>
          </div>
        </>
      )}
    </div>
  )
}
