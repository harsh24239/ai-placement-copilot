import { useState } from 'react'
import { useAuth } from '../context/AuthContext'

export default function Auth() {
  const [mode, setMode] = useState('login')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()

  const handleSubmit = async () => {
    setError(null)
    setLoading(true)
    try {
      const response = await fetch(`http://127.0.0.1:8000/auth/${mode}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || 'Something went wrong')
      login(data.access_token, data.credits_remaining, email)
    } catch (err) {
      setError(err.message)
    }
    setLoading(false)
  }

  return (
    <div className="auth-shell">
      <div className="auth-card">
        <div className="sidebar-orb" style={{ margin: '0 auto 18px' }} />
        <h1 className="page-title" style={{ textAlign: 'center' }}>
          {mode === 'login' ? 'Welcome back' : 'Create your account'}
        </h1>
        <p className="page-subtitle" style={{ textAlign: 'center', margin: '0 auto 24px' }}>
          {mode === 'login' ? 'Log in to continue your prep.' : 'Start with 20 free credits.'}
        </p>

        <input
          className="chat-input"
          style={{ marginBottom: '12px' }}
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          className="chat-input"
          style={{ marginBottom: '18px' }}
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
        />

        <button className="btn-primary" style={{ width: '100%' }} onClick={handleSubmit} disabled={loading}>
          {loading ? 'Please wait...' : mode === 'login' ? 'Log In' : 'Sign Up'}
        </button>

        {error && <div className="error-text" style={{ textAlign: 'center' }}>{error}</div>}

        <p className="auth-switch">
          {mode === 'login' ? "Don't have an account? " : 'Already have an account? '}
          <span onClick={() => setMode(mode === 'login' ? 'signup' : 'login')}>
            {mode === 'login' ? 'Sign up' : 'Log in'}
          </span>
        </p>
      </div>
    </div>
  )
}
