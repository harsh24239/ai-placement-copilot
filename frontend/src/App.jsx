import { useState } from 'react'
import './App.css'

function App() {
  const [status, setStatus] = useState(null)
  const [loading, setLoading] = useState(false)

  const checkBackend = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://127.0.0.1:8000/health')
      const data = await response.json()
      setStatus(data)
    } catch (error) {
      setStatus({ status: 'error', message: error.message })
    }
    setLoading(false)
  }

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>AI Placement Copilot</h1>
      <button onClick={checkBackend} disabled={loading}>
        {loading ? 'Checking...' : 'Check Backend'}
      </button>

      {status && (
        <pre style={{ marginTop: '1rem' }}>
          {JSON.stringify(status, null, 2)}
        </pre>
      )}
    </div>
  )
}

export default App