const NAV_ITEMS = [
  { id: 'resume', label: 'Resume Analysis' },
  { id: 'dsa', label: 'DSA Coach' },
  { id: 'interview', label: 'Mock Interview' },
]

export default function Sidebar({ activePage, onNavigate }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="sidebar-orb" />
        <div className="sidebar-title">AI Placement<br />Copilot</div>
      </div>
      <nav className="sidebar-nav">
        {NAV_ITEMS.map((item) => (
          <button
            key={item.id}
            className={`nav-item ${activePage === item.id ? 'active' : ''}`}
            onClick={() => onNavigate(item.id)}
          >
            {item.label}
          </button>
        ))}
      </nav>
    </aside>
  )
}
