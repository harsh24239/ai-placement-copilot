import { FileText, Code2, MessagesSquare, X } from 'lucide-react'
import { useAuth } from '../context/AuthContext'

const NAV_ITEMS = [
  { id: 'resume', label: 'Resume Analysis', icon: FileText },
  { id: 'dsa', label: 'DSA Coach', icon: Code2 },
  { id: 'interview', label: 'Mock Interview', icon: MessagesSquare },
]

export default function Sidebar({ activePage, onNavigate, isOpen, onClose }) {
  const { email } = useAuth()
  const initial = email ? email[0].toUpperCase() : '?'

  return (
    <aside className={`sidebar ${isOpen ? 'sidebar-open' : ''}`}>
      <div>
        <div className="sidebar-brand">
          <div className="sidebar-brand-left">
            <div className="sidebar-orb" />
            <div className="sidebar-title">AI Placement<br />Copilot</div>
          </div>
          <button className="sidebar-close" onClick={onClose}>
            <X size={18} />
          </button>
        </div>
        <nav className="sidebar-nav">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon
            return (
              <button
                key={item.id}
                className={`nav-item ${activePage === item.id ? 'active' : ''}`}
                onClick={() => onNavigate(item.id)}
              >
                <Icon size={17} strokeWidth={2} />
                <span className="nav-item-label">{item.label}</span>
              </button>
            )
          })}
        </nav>
      </div>

      <div className="sidebar-footer">
        <div className="sidebar-avatar">{initial}</div>
        <span className="sidebar-email">{email}</span>
      </div>
    </aside>
  )
}
