import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Terminal } from 'lucide-react'
import { loginUser } from '../api/auth'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const data = await loginUser({ email, password })
      login(data.access_token)
      navigate('/dashboard')
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-paper px-4">
      <div className="w-full max-w-sm">
        <div className="flex items-center gap-2 justify-center mb-6">
          <Terminal className="text-primary" size={22} />
          <span className="font-mono-brand font-bold text-xl text-ink">AutoDev<span className="text-accent">.AI</span></span>
        </div>
        <form onSubmit={handleSubmit} className="bg-panel border border-line p-8 rounded-lg shadow-sm">
          <h1 className="text-xl font-semibold mb-1 text-ink">Welcome back</h1>
          <p className="text-sm text-muted mb-6">Log in to manage your AI-generated projects</p>
          {error && <p className="text-danger text-sm mb-4">{error}</p>}
          <label className="block text-sm font-medium text-ink mb-1">Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full border border-line rounded px-3 py-2 mb-4 focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary"
          />
          <div className="flex items-center justify-between mb-1">
            <label className="block text-sm font-medium text-ink">Password</label>
            <Link to="/forgot-password" className="text-xs text-primary hover:underline">Forgot password?</Link>
          </div>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full border border-line rounded px-3 py-2 mb-6 focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary"
          />
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-primary hover:bg-primary-dark text-white font-medium py-2.5 rounded transition disabled:opacity-50"
          >
            {loading ? 'Logging in...' : 'Log in'}
          </button>
          <p className="text-sm text-muted mt-5 text-center">
            No account? <Link to="/register" className="text-primary font-medium hover:underline">Register</Link>
          </p>
        </form>
      </div>
    </div>
  )
}
