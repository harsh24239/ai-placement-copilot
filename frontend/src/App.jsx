import { useState } from 'react'
import './App.css'
import Sidebar from './components/Sidebar'
import ResumeAnalysis from './pages/ResumeAnalysis'
import DsaCoach from './pages/DsaCoach'
import MockInterview from './pages/MockInterview'

function App() {
  const [activePage, setActivePage] = useState('resume')

  return (
    <div className="app-shell">
      <Sidebar activePage={activePage} onNavigate={setActivePage} />
      <main className="main-content">
        {activePage === 'resume' && <ResumeAnalysis />}
        {activePage === 'dsa' && <DsaCoach />}
        {activePage === 'interview' && <MockInterview />}
      </main>
    </div>
  )
}

export default App
