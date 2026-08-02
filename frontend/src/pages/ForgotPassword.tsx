import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Terminal } from 'lucide-react'
import { forgotPassword } from '../api/auth'

export default function ForgotPassword() {
  const [email, setEmail] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [resetToken, setResetToken] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const data = await forgotPassword(email)
      setResetToken(data.reset_token)
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Something went wrong')
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
          <h1 className="text-xl font-semibold mb-1 text-ink">Reset your password</h1>
          <p className="text-sm text-muted mb-6">Enter your email and we'll generate a reset link.</p>

          {!resetToken ? (
            <form onSubmit={handleSubmit}>
              {error && <p className="text-danger text-sm mb-4">{error}</p>}
              <label className="block text-sm font-medium text-ink mb-1">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full border border-line rounded px-3 py-2 mb-6 focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary"
              />
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-primary hover:bg-primary-dark text-white font-medium py-2.5 rounded transition disabled:opacity-50"
              >
                {loading ? 'Generating...' : 'Send reset link'}
              </button>
            </form>
          ) : (
            <div>
              <div className="bg-accent/10 border border-accent/30 rounded p-4 mb-4">
                <p className="text-sm text-ink font-medium mb-1">Dev mode notice</p>
                <p className="text-xs text-muted">
                  Email delivery isn't configured, so your reset link is shown here directly instead of being emailed.
                </p>
              </div>
              <Link
                to={'/reset-password?token=' + resetToken}
                className="block text-center w-full bg-primary hover:bg-primary-dark text-white font-medium py-2.5 rounded transition"
              >
                Continue to reset password
              </Link>
            </div>
          )}

          <p className="text-sm text-muted mt-5 text-center">
            <Link to="/login" className="text-primary font-medium hover:underline">Back to login</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
