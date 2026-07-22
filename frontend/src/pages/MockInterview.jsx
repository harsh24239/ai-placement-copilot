import { useState } from 'react'

export default function MockInterview() {
  const [topic, setTopic] = useState('')
  const [sessionId, setSessionId] = useState(null)
  const [messages, setMessages] = useState([])
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)
  const [feedback, setFeedback] = useState(null)

  const startInterview = async () => {
    if (!topic.trim()) return
    setLoading(true)
    const response = await fetch('http://127.0.0.1:8000/interview/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic })
    })
    const data = await response.json()
    setSessionId(data.session_id)
    setMessages([{ role: 'assistant', content: data.message }])
    setLoading(false)
  }

  const sendAnswer = async () => {
    if (!answer.trim()) return
    const newMessages = [...messages, { role: 'user', content: answer }]
    setMessages(newMessages)
    setAnswer('')
    setLoading(true)

    const response = await fetch('http://127.0.0.1:8000/interview/continue', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId, answer })
    })
    const data = await response.json()
    setMessages([...newMessages, { role: 'assistant', content: data.message }])
    setLoading(false)
  }

  const getFeedback = async () => {
    setLoading(true)
    const response = await fetch(`http://127.0.0.1:8000/interview/feedback/${sessionId}`)
    const data = await response.json()
    setFeedback(data)
    setLoading(false)
  }

  return (
    <div>
      <div className="page-header">
        <div className="page-eyebrow">Step 3 of 3</div>
        <h1 className="page-title">Mock Interview</h1>
        <p className="page-subtitle">
          Practice a live technical interview. Answer each question — we'll follow up like a real interviewer.
        </p>
      </div>

      {!sessionId && (
        <div className="card">
          <div className="upload-row">
            <input
              className="chat-input"
              placeholder="Topic, e.g. arrays and hashmaps"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
            />
            <div>
              <button className="btn-primary" onClick={startInterview} disabled={loading}>
                {loading ? 'Starting...' : 'Start Interview'}
              </button>
            </div>
          </div>
        </div>
      )}

      {sessionId && (
        <div className="card">
          <div className="chat-window">
            {messages.map((m, i) => (
              <div key={i} className={`chat-bubble ${m.role}`}>{m.content}</div>
            ))}
            {loading && <div className="loading-text">Thinking...</div>}
          </div>

          <div className="chat-input-row">
            <input
              className="chat-input"
              placeholder="Type your answer..."
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendAnswer()}
            />
            <button className="btn-primary" onClick={sendAnswer} disabled={loading}>Send</button>
          </div>

          <div style={{ marginTop: '14px' }}>
            <button className="btn-primary" onClick={getFeedback} disabled={loading || messages.length < 2}>
              Get Feedback
            </button>
          </div>
        </div>
      )}

      {feedback && (
        <div className="card">
          <div className="section-label">Performance Feedback</div>
          <div className="score-bars">
            {[
              ['Confidence', feedback.confidence_score],
              ['Technical Accuracy', feedback.technical_accuracy_score],
              ['Communication', feedback.communication_score],
            ].map(([label, val]) => (
              <div className="score-bar-row" key={label}>
                <span className="score-bar-label">{label}</span>
                <div className="score-bar-track">
                  <div className="score-bar-fill" style={{ width: `${val * 10}%` }} />
                </div>
                <span className="score-bar-num">{val}/10</span>
              </div>
            ))}
          </div>
          <p className="fit-summary-text" style={{ marginTop: '18px' }}>{feedback.overall_feedback}</p>
        </div>
      )}
    </div>
  )
}
