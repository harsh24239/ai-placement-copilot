import { useState } from 'react'
import { Menu, X } from 'lucide-react'
import './App.css'
import { AuthProvider, useAuth } from './context/AuthContext'
import Sidebar from './components/Sidebar'
import Auth from './pages/Auth'
import ResumeAnalysis from './pages/ResumeAnalysis'
import DsaCoach from './pages/DsaCoach'
import MockInterview from './pages/MockInterview'

function Dashboard() {
  const [activePage, setActivePage] = useState('resume')
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { credits, logout } = useAuth()

  const handleNavigate = (page) => {
    setActivePage(page)
    setSidebarOpen(false)
  }

  return (
    <div className="app-shell">
      {sidebarOpen && <div className="sidebar-overlay" onClick={() => setSidebarOpen(false)} />}

      <Sidebar
        activePage={activePage}
        onNavigate={handleNavigate}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      <main className="main-content">
        <div className="top-bar">
          <button className="menu-toggle" onClick={() => setSidebarOpen(true)}>
            <Menu size={20} />
          </button>
          <div className="top-bar-right">
            <span className="credits-pill">⚡ {credits} credits</span>
            <button className="logout-btn" onClick={logout}>Log out</button>
          </div>
        </div>
        <div className="page-inner">
          {activePage === 'resume' && <ResumeAnalysis />}
          {activePage === 'dsa' && <DsaCoach />}
          {activePage === 'interview' && <MockInterview />}
        </div>
      </main>
    </div>
  )
}

function AppShell() {
  const { token } = useAuth()
  return token ? <Dashboard /> : <Auth />
}

function App() {
  return (
    <AuthProvider>
      <AppShell />
    </AuthProvider>
  )
}

export default App
