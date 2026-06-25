import { Routes, Route, Link, useLocation } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Reports from './pages/Reports'

export default function App() {
  const location = useLocation()

  return (
    <div className="min-h-screen bg-navy">
      <nav className="border-b border-gray-800 bg-surface/80 backdrop-blur sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2 text-textPrimary font-bold text-lg">
            <span className="text-2xl">🛡️</span>
            <span>PhishGuard</span>
          </Link>
          <div className="flex gap-4">
            <Link
              to="/"
              className={`text-sm font-medium transition ${
                location.pathname === '/' ? 'text-info' : 'text-textSecondary hover:text-textPrimary'
              }`}
            >
              Dashboard
            </Link>
            <Link
              to="/reports"
              className={`text-sm font-medium transition ${
                location.pathname === '/reports' ? 'text-info' : 'text-textSecondary hover:text-textPrimary'
              }`}
            >
              Reports
            </Link>
          </div>
        </div>
      </nav>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/reports" element={<Reports />} />
      </Routes>
    </div>
  )
}
