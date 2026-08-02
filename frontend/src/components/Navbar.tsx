import { Link, useNavigate } from 'react-router-dom'
import { LogOut, User } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import PipelineStrip from './PipelineStrip'

export default function Navbar() {
  const { logout, isAuthenticated } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="bg-ink text-white px-6 py-4 flex items-center justify-between border-b border-black/20">
      <Link to="/dashboard" className="flex items-center gap-3">
        <span className="font-mono-brand font-bold text-lg tracking-tight">AutoDev<span className="text-accent">.AI</span></span>
        <PipelineStrip size="mini" />
      </Link>
      {isAuthenticated && (
        <div className="flex items-center gap-2">
          <Link
            to="/profile"
            className="flex items-center gap-1.5 text-sm text-white/70 hover:text-white px-3 py-2 rounded transition"
          >
            <User size={16} />
            Profile
          </Link>
          <button
            onClick={handleLogout}
            className="flex items-center gap-1.5 bg-white/10 hover:bg-white/20 px-3 py-2 rounded text-sm transition"
          >
            <LogOut size={16} />
            Logout
          </button>
        </div>
      )}
    </nav>
  )
}
