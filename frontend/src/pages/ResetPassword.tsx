import { useState } from 'react'
import { useNavigate, useSearchParams, Link } from 'react-router-dom'
import { Terminal } from 'lucide-react'
import { resetPassword } from '../api/auth'

export default function ResetPassword() {
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token') || ''
  const [newPassword, setNewPassword] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await resetPassword(token, newPassword)
      setSuccess(true)
      setTimeout(() => navigate('/login'), 2000)
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Reset failed')
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
        <div className="bg-panel border border-line p-8 rounded-lg shadow-sm">
          <h1 className="text-xl font-semibold mb-1 text-ink">Set a new password</h1>
          {success ? (
            <p className="text-sm text-primary mt-4">Password reset. Redirecting to login...</p>
          ) : (
            <form onSubmit={handleSubmit} className="mt-4">
              {error && <p className="text-danger text-sm mb-4">{error}</p>}
              <label className="block text-sm font-medium text-ink mb-1">New password</label>
              <input
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                required
                className="w-full border border-line rounded px-3 py-2 mb-6 focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary"
              />
              <button
                type="submit"
                disabled={loading || !token}
                className="w-full bg-primary hover:bg-primary-dark text-white font-medium py-2.5 rounded transition disabled:opacity-50"
              >
                {loading ? 'Resetting...' : 'Reset password'}
              </button>
              {!token && <p className="text-danger text-xs mt-3">No reset token found in the link.</p>}
            </form>
          )}
          <p className="text-sm text-muted mt-5 text-center">
            <Link to="/login" className="text-primary font-medium hover:underline">Back to login</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
